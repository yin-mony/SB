import json
import os
import re
import secrets
from typing import Optional
from uuid import uuid4

from django.conf import settings
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import transaction
from django.db.models import F
from django.utils.text import get_valid_filename, slugify
from django.utils import timezone
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView

from apps.blog.models import BlogComment, BlogPost
from apps.core.responses import fail, ok

ALLOWED_BLOG_CATEGORIES = frozenset({"逻辑体操", "赛博生活", "职场歪理"})

# 封面上传接口写入的文件名：uuid32hex + 白名单扩展名（与 BlogCoverUploadView 一致）
_COVER_FILENAME_RE = re.compile(r"^[a-f0-9]{32}\.(?:png|jpg|jpeg|webp|gif)$", re.IGNORECASE)


def _validate_own_blog_cover_url(cover_image: str, user_id: int) -> bool:
    """仅允许当前用户目录下、本站上传生成的封面路径，禁止任意外链或畸形 URL。"""
    if not cover_image:
        return True
    prefix = f"/uploads/blog_covers/user_{user_id}/"
    if ".." in cover_image or not cover_image.startswith(prefix):
        return False
    rest = cover_image[len(prefix) :]
    if "/" in rest:
        return False
    return bool(_COVER_FILENAME_RE.match(rest))


def _normalize_tags(raw):
    if raw is None:
        return []
    if isinstance(raw, list):
        out = [str(x).strip()[:30] for x in raw if str(x).strip()]
    elif isinstance(raw, str):
        out = [t.strip()[:30] for t in raw.replace("，", ",").split(",") if t.strip()]
    else:
        out = []
    seen = set()
    uniq = []
    for t in out:
        if t.lower() in seen:
            continue
        seen.add(t.lower())
        uniq.append(t)
        if len(uniq) >= 20:
            break
    return uniq


def _serialize_tags_field(tags):
    if isinstance(tags, str):
        try:
            return json.loads(tags)
        except Exception:
            return []
    return tags or []


def _post_to_item(p):
    tags = _serialize_tags_field(p.tags)
    return {
        "id": p.id,
        "author": {
            "id": p.author_id,
            "username": getattr(p.author, "username", ""),
            "avatar_url": getattr(p.author, "avatar_url", None),
            "bio": getattr(p.author, "bio", None),
        },
        "title": p.title,
        "slug": p.slug,
        "cover_image": p.cover_image,
        "excerpt": p.excerpt,
        "category": p.category,
        "tags": tags,
        "view_count": p.view_count,
        "like_count": p.like_count,
        "comment_count": p.comment_count,
        "created_at": p.created_at,
        "is_published": bool(getattr(p, "is_published", True)),
    }


def _post_to_detail_item(p):
    item = _post_to_item(p)
    item["content"] = p.content
    return item


def _make_unique_slug(title: str, user_id: int) -> str:
    base = slugify((title or "")[:120]) or "post"
    base = base[:120].strip("-") or "post"
    for _ in range(8):
        tail = secrets.token_hex(3)
        candidate = f"{base}-{user_id}-{tail}"[:200]
        if not BlogPost.objects.filter(slug=candidate).exists():
            return candidate
    return f"{base}-{user_id}-{secrets.token_hex(8)}"[:200]


def _excerpt_from_content(content: str, excerpt: Optional[str]) -> str:
    ex = (excerpt or "").strip()
    if ex:
        return ex[:500]
    plain = re.sub(r"\s+", " ", (content or "").replace("#", "")).strip()
    return plain[:500] if plain else "（暂无摘要）"


class BlogPostsView(APIView):
    permission_classes = [AllowAny]

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated()]
        return [AllowAny()]

    def get(self, request):
        try:
            limit = int(request.query_params.get("limit") or 20)
        except Exception:
            limit = 20
        limit = max(1, min(limit, 50))

        try:
            offset = int(request.query_params.get("offset") or 0)
        except Exception:
            offset = 0
        offset = max(0, min(offset, 5000))

        category = (request.query_params.get("category") or "").strip()
        sort = (request.query_params.get("sort") or "new").strip()

        qs = BlogPost.objects.select_related("author").filter(is_published=True)
        if category:
            qs = qs.filter(category=category)
        if sort == "hot":
            qs = qs.order_by("-view_count", "-like_count", "-id")
        else:
            qs = qs.order_by("-created_at", "-id")

        qs = qs.only(
            "id",
            "author_id",
            "title",
            "slug",
            "cover_image",
            "excerpt",
            "category",
            "tags",
            "view_count",
            "like_count",
            "comment_count",
            "created_at",
            "is_published",
            "author__id",
            "author__username",
            "author__avatar_url",
            "author__bio",
        )

        window = list(qs[offset : offset + limit + 1])
        has_more = len(window) > limit
        window = window[:limit]
        items = [_post_to_item(p) for p in window]

        return ok(data={"items": items, "has_more": has_more, "next_offset": offset + limit if has_more else None})

    def post(self, request):
        title = (request.data.get("title") or "").strip()
        content = (request.data.get("content") or "").strip()
        if not title:
            return fail(msg="参数错误", code=400, data={"title": ["标题不能为空"]})
        if len(title) > 200:
            return fail(msg="参数错误", code=400, data={"title": ["标题过长"]})
        if not content:
            return fail(msg="参数错误", code=400, data={"content": ["内容不能为空"]})
        if len(content) > 50000:
            return fail(msg="参数错误", code=400, data={"content": ["内容过长"]})

        category = (request.data.get("category") or "逻辑体操").strip()
        if category not in ALLOWED_BLOG_CATEGORIES:
            return fail(msg="参数错误", code=400, data={"category": ["分类无效"]})

        tags_list = _normalize_tags(request.data.get("tags"))
        cover_image = (request.data.get("cover_image") or "").strip() or None
        if cover_image and len(cover_image) > 500:
            return fail(msg="参数错误", code=400, data={"cover_image": ["封面链接过长"]})
        if cover_image and not _validate_own_blog_cover_url(cover_image, request.user.id):
            return fail(
                msg="参数错误",
                code=400,
                data={"cover_image": ["请使用本站上传的封面或留空"]},
            )

        excerpt = _excerpt_from_content(content, request.data.get("excerpt"))
        slug = _make_unique_slug(title, request.user.id)
        now = timezone.now()

        post = BlogPost(
            author_id=request.user.id,
            title=title[:200],
            slug=slug,
            cover_image=cover_image,
            content=content,
            excerpt=excerpt[:500],
            category=category,
            tags=tags_list or None,
            view_count=0,
            like_count=0,
            comment_count=0,
            is_published=True,
            created_at=now,
            updated_at=now,
        )
        post.save()

        p = (
            BlogPost.objects.select_related("author")
            .filter(id=post.id)
            .only(
                "id",
                "author_id",
                "title",
                "slug",
                "cover_image",
                "content",
                "excerpt",
                "category",
                "tags",
                "view_count",
                "like_count",
                "comment_count",
                "created_at",
                "author__id",
                "author__username",
                "author__avatar_url",
                "author__bio",
            )
            .first()
        )
        return ok(data={"item": _post_to_detail_item(p)})


class BlogPostDetailView(APIView):
    permission_classes = [AllowAny]

    def get_permissions(self):
        if self.request.method in ("PATCH", "DELETE"):
            return [IsAuthenticated()]
        return [AllowAny()]

    _post_detail_only = (
        "id",
        "author_id",
        "title",
        "slug",
        "cover_image",
        "content",
        "excerpt",
        "category",
        "tags",
        "view_count",
        "like_count",
        "comment_count",
        "created_at",
        "is_published",
        "author__id",
        "author__username",
        "author__avatar_url",
        "author__bio",
    )

    def get(self, request, post_id: int):
        p = (
            BlogPost.objects.select_related("author")
            .filter(id=post_id)
            .only(*self._post_detail_only)
            .first()
        )
        if not p:
            return ok(data={"item": None})
        if not p.is_published:
            if not (getattr(request.user, "is_authenticated", False) and request.user.id == p.author_id):
                return ok(data={"item": None})
            item = _post_to_detail_item(p)
            item["view_count"] = int(p.view_count or 0)
            return ok(data={"item": item})

        item = _post_to_detail_item(p)
        item["view_count"] = (p.view_count or 0) + 1
        BlogPost.objects.filter(id=post_id).update(view_count=F("view_count") + 1)

        return ok(data={"item": item})

    def patch(self, request, post_id: int):
        p = BlogPost.objects.filter(id=post_id).first()
        if not p or p.author_id != request.user.id:
            return fail(msg="文章不存在或无权限", code=404)

        now = timezone.now()
        if "title" in request.data:
            t = (request.data.get("title") or "").strip()
            if not t:
                return fail(msg="参数错误", code=400, data={"title": ["标题不能为空"]})
            if len(t) > 200:
                return fail(msg="参数错误", code=400, data={"title": ["标题过长"]})
            p.title = t[:200]

        if "content" in request.data:
            content = (request.data.get("content") or "").strip()
            if not content:
                return fail(msg="参数错误", code=400, data={"content": ["内容不能为空"]})
            if len(content) > 50000:
                return fail(msg="参数错误", code=400, data={"content": ["内容过长"]})
            p.content = content
            p.excerpt = _excerpt_from_content(content, request.data.get("excerpt"))[:500]
        elif "excerpt" in request.data:
            ex = (request.data.get("excerpt") or "").strip()
            p.excerpt = ex[:500] if ex else _excerpt_from_content(p.content or "", None)[:500]

        if "category" in request.data:
            category = (request.data.get("category") or "").strip() or "逻辑体操"
            if category not in ALLOWED_BLOG_CATEGORIES:
                return fail(msg="参数错误", code=400, data={"category": ["分类无效"]})
            p.category = category

        if "tags" in request.data:
            p.tags = _normalize_tags(request.data.get("tags")) or None

        if "cover_image" in request.data:
            cover_image = (request.data.get("cover_image") or "").strip() or None
            if cover_image and len(cover_image) > 500:
                return fail(msg="参数错误", code=400, data={"cover_image": ["封面链接过长"]})
            if cover_image and not _validate_own_blog_cover_url(cover_image, request.user.id):
                return fail(
                    msg="参数错误",
                    code=400,
                    data={"cover_image": ["请使用本站上传的封面或留空"]},
                )
            p.cover_image = cover_image

        if request.data.get("is_published") is True:
            p.is_published = True

        p.updated_at = now
        p.save()
        p2 = (
            BlogPost.objects.select_related("author")
            .filter(id=p.id)
            .only(
                "id",
                "author_id",
                "title",
                "slug",
                "cover_image",
                "content",
                "excerpt",
                "category",
                "tags",
                "view_count",
                "like_count",
                "comment_count",
                "created_at",
                "is_published",
                "author__id",
                "author__username",
                "author__avatar_url",
                "author__bio",
            )
            .first()
        )
        return ok(data={"item": _post_to_detail_item(p2)})

    def delete(self, request, post_id: int):
        p = BlogPost.objects.filter(id=post_id).only("id", "author_id", "is_published").first()
        if not p or p.author_id != request.user.id:
            return fail(msg="文章不存在或无权限", code=404)
        if not p.is_published:
            return ok(data={"unpublished": True})
        BlogPost.objects.filter(id=post_id).update(is_published=False, updated_at=timezone.now())
        return ok(data={"unpublished": True})


class BlogPostRelatedView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, post_id: int):
        p = BlogPost.objects.filter(id=post_id, is_published=True).only("id", "category").first()
        if not p:
            return ok(data={"items": []})

        qs = (
            BlogPost.objects.select_related("author")
            .filter(is_published=True, category=p.category)
            .exclude(id=post_id)
            .order_by("-view_count", "-like_count", "-id")[:6]
            .only(
                "id",
                "author_id",
                "title",
                "slug",
                "cover_image",
                "excerpt",
                "category",
                "tags",
                "view_count",
                "like_count",
                "comment_count",
                "created_at",
                "author__id",
                "author__username",
                "author__avatar_url",
                "author__bio",
            )
        )
        items = [_post_to_item(x) for x in qs]
        return ok(data={"items": items})


class BlogPostCommentsView(APIView):
    permission_classes = [AllowAny]

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated()]
        return [AllowAny()]

    def get(self, request, post_id: int):
        p = BlogPost.objects.filter(id=post_id).only("id", "is_published", "author_id").first()
        if not p:
            return fail(msg="文章不存在", code=404)
        if not p.is_published and (
            not getattr(request.user, "is_authenticated", False) or request.user.id != p.author_id
        ):
            return fail(msg="文章不存在", code=404)

        try:
            limit = int(request.query_params.get("limit") or 30)
        except Exception:
            limit = 30
        limit = max(1, min(limit, 100))

        try:
            offset = int(request.query_params.get("offset") or 0)
        except Exception:
            offset = 0
        offset = max(0, min(offset, 50_000))

        qs = BlogComment.objects.select_related("user").filter(post_id=post_id).order_by("created_at")
        window = list(qs[offset : offset + limit + 1])
        has_more = len(window) > limit
        chunk = window[:limit]

        items = []
        for c in chunk:
            items.append(
                {
                    "id": c.id,
                    "post_id": c.post_id,
                    "user": {
                        "id": c.user_id,
                        "username": getattr(c.user, "username", ""),
                        "avatar_url": getattr(c.user, "avatar_url", None),
                        "bio": getattr(c.user, "bio", None),
                    },
                    "parent_id": c.parent_id,
                    "content": c.content,
                    "upvotes": c.upvotes,
                    "created_at": c.created_at,
                }
            )
        return ok(data={"items": items, "has_more": has_more, "next_offset": offset + limit if has_more else None})

    def post(self, request, post_id: int):
        p = BlogPost.objects.filter(id=post_id).only("id", "is_published").first()
        if not p:
            return fail(msg="文章不存在", code=404)
        if not p.is_published:
            return fail(msg="文章已下架", code=400)

        content = (request.data.get("content") or "").strip()
        parent_id = request.data.get("parent_id")

        if not content:
            return fail(msg="参数错误", code=400, data={"content": ["内容不能为空"]})
        if len(content) > 2000:
            return fail(msg="参数错误", code=400, data={"content": ["内容过长（最多 2000 字）"]})

        parent = None
        if parent_id not in (None, "", 0, "0"):
            try:
                parent_id = int(parent_id)
            except Exception:
                return fail(msg="参数错误", code=400, data={"parent_id": ["parent_id 无效"]})
            parent = BlogComment.objects.filter(id=parent_id, post_id=post_id).only("id").first()
            if not parent:
                return fail(msg="参数错误", code=400, data={"parent_id": ["父评论不存在"]})

        c = BlogComment(
            post_id=post_id,
            user_id=request.user.id,
            parent_id=parent.id if parent else None,
            content=content,
            upvotes=0,
            created_at=timezone.now(),
        )
        c.save()
        BlogPost.objects.filter(id=post_id).update(comment_count=F("comment_count") + 1)

        return ok(
            data={
                "item": {
                    "id": c.id,
                    "post_id": post_id,
                    "user": {
                        "id": request.user.id,
                        "username": getattr(request.user, "username", ""),
                        "avatar_url": getattr(request.user, "avatar_url", None),
                        "bio": getattr(request.user, "bio", None),
                    },
                    "parent_id": c.parent_id,
                    "content": content,
                    "upvotes": 0,
                    "created_at": c.created_at,
                }
            }
        )


def _delete_blog_comment_subtree(comment_id: int) -> int:
    """后序删除子树，返回删除条数。"""
    deleted = 0
    for cid in list(BlogComment.objects.filter(parent_id=comment_id).values_list("id", flat=True)):
        deleted += _delete_blog_comment_subtree(cid)
    deleted += BlogComment.objects.filter(id=comment_id).delete()[0]
    return deleted


class BlogCommentDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, post_id: int, comment_id: int):
        post = BlogPost.objects.filter(id=post_id).only("id", "author_id", "comment_count").first()
        if not post:
            return fail(msg="文章不存在", code=404)
        c = BlogComment.objects.filter(id=comment_id, post_id=post_id).first()
        if not c:
            return fail(msg="评论不存在", code=404)

        uid = request.user.id
        is_author = c.user_id == uid
        is_post_owner = post.author_id == uid

        if not is_author and not is_post_owner:
            return fail(msg="无权限", code=403)

        if not is_post_owner and BlogComment.objects.filter(parent_id=comment_id).exists():
            return fail(msg="请先删除回复后再删本条", code=400)

        with transaction.atomic():
            if is_post_owner:
                n = _delete_blog_comment_subtree(comment_id)
            else:
                BlogComment.objects.filter(id=comment_id).delete()
                n = 1
            new_cc = max(0, int(post.comment_count or 0) - n)
            BlogPost.objects.filter(id=post_id).update(comment_count=new_cc)

        return ok(data={"deleted": n})


class BlogCoverUploadView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        f = request.FILES.get("file")
        if not f:
            return fail(msg="参数错误", code=400, data={"file": ["缺少文件"]})

        content_type = (getattr(f, "content_type", "") or "").lower()
        if content_type not in {"image/png", "image/jpeg", "image/jpg", "image/webp", "image/gif"}:
            return fail(msg="文件类型不支持", code=400, data={"file": ["仅支持 png/jpg/webp/gif"]})

        if f.size and f.size > 3 * 1024 * 1024:
            return fail(msg="文件过大", code=400, data={"file": ["最大 3MB"]})

        ext = os.path.splitext(f.name or "")[1].lower()
        if ext not in {".png", ".jpg", ".jpeg", ".webp", ".gif"}:
            ext = ".png"

        filename = get_valid_filename(f"{uuid4().hex}{ext}")
        project_root = os.path.dirname(str(settings.BASE_DIR))
        frontend_public_dir = os.path.join(project_root, "frontend", "public")
        rel_dir = os.path.join("uploads", "blog_covers", f"user_{request.user.id}")
        abs_dir = os.path.join(frontend_public_dir, rel_dir)
        os.makedirs(abs_dir, exist_ok=True)
        abs_path = os.path.join(abs_dir, filename)

        with open(abs_path, "wb") as dst:
            for chunk in f.chunks():
                dst.write(chunk)

        cover_url = f"/{rel_dir.replace(os.sep, '/')}/{filename}"
        return ok(data={"cover_image": cover_url})


class BlogNewsletterSubscribeView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = (request.data.get("email") or "").strip().lower()
        if not email:
            return fail(msg="参数错误", code=400, data={"email": ["邮箱不能为空"]})
        try:
            validate_email(email)
        except ValidationError:
            return fail(msg="邮箱格式不对", code=400, data={"email": ["邮箱格式不对"]})

        key = f"blog_nl:{email}"
        already = cache.get(key) is not None
        cache.set(key, 1, timeout=60 * 60 * 24 * 365 * 5)
        return ok(data={"subscribed": True, "already": already})
