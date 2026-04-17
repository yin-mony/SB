from django.db import transaction
from django.db.models import Count, F, Q
from django.utils import timezone
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView

from apps.core.responses import fail, ok
from apps.debate.models import DebatePost, Topic, TopicVote


class TopicCategoriesView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        status = (request.query_params.get("status") or "").strip()
        qs = Topic.objects.all()
        if status:
            qs = qs.filter(status=status)

        rows = qs.values("category").annotate(count=Count("id")).order_by("-count", "category")
        items = []
        total = 0
        for r in rows:
            c = int(r.get("count") or 0)
            total += c
            items.append({"category": r.get("category") or "", "count": c})
        return ok(data={"items": items, "total": total})


class TopicsView(APIView):
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
            page = int(request.query_params.get("page") or 1)
        except Exception:
            page = 1
        page = max(1, min(page, 1000000))

        q = (request.query_params.get("q") or "").strip()
        category = (request.query_params.get("category") or "").strip()
        status = (request.query_params.get("status") or "").strip()
        fmt = (request.query_params.get("format") or "").strip()
        sort = (request.query_params.get("sort") or "hot").strip()

        base_qs = Topic.objects.select_related("creator")
        if q:
            base_qs = base_qs.filter(Q(title__icontains=q) | Q(description__icontains=q))
        if category:
            base_qs = base_qs.filter(category=category)
        if status:
            base_qs = base_qs.filter(status=status)
        if fmt:
            base_qs = base_qs.filter(format=fmt)

        if sort == "new":
            base_qs = base_qs.order_by("-created_at", "-id")
        else:
            base_qs = base_qs.order_by("-hot_score", "-created_at", "-id")

        offset = (page - 1) * limit
        qs = (
            base_qs.only(
                "id",
                "creator_id",
                "title",
                "description",
                "category",
                "format",
                "side_a_name",
                "side_b_name",
                "status",
                "view_count",
                "comment_count",
                "hot_score",
                "created_at",
                "creator__id",
                "creator__username",
                "creator__avatar_url",
                "creator__bio",
            )[offset : offset + limit + 1]
        )
        qs = list(qs)
        has_more = len(qs) > limit
        if has_more:
            qs = qs[:limit]

        topic_ids = [t.id for t in qs]
        vote_rows = (
            TopicVote.objects.filter(topic_id__in=topic_ids)
            .values("topic_id", "side")
            .annotate(c=Count("id"))
        )
        vote_map = {}
        for r in vote_rows:
            vote_map.setdefault(r["topic_id"], {"A": 0, "B": 0})[r["side"]] = r["c"]

        items = []
        for t in qs:
            votes = vote_map.get(t.id, {"A": 0, "B": 0})
            items.append(
                {
                    "id": t.id,
                    "creator": {
                        "id": t.creator_id,
                        "username": getattr(t.creator, "username", ""),
                        "avatar_url": getattr(t.creator, "avatar_url", None),
                        "bio": getattr(t.creator, "bio", None),
                    },
                    "title": t.title,
                    "description": t.description,
                    "category": t.category,
                    "format": t.format,
                    "side_a_name": t.side_a_name,
                    "side_b_name": t.side_b_name,
                    "status": t.status,
                    "view_count": t.view_count,
                    "comment_count": t.comment_count,
                    "hot_score": t.hot_score,
                    "created_at": t.created_at,
                    "votes": votes,
                }
            )

        return ok(data={"items": items, "page": page, "limit": limit, "has_more": has_more})

    def post(self, request):
        title = (request.data.get("title") or "").strip()
        description = (request.data.get("description") or "").strip()
        category = (request.data.get("category") or "").strip() or "综合"
        fmt = (request.data.get("format") or "").strip() or "快嘴乱斗"
        side_a_name = (request.data.get("side_a_name") or "").strip()
        side_b_name = (request.data.get("side_b_name") or "").strip()

        errors = {}
        if not title:
            errors["title"] = ["标题不能为空"]
        elif len(title) > 200:
            errors["title"] = ["标题过长（最多 200 字）"]
        if description and len(description) > 2000:
            errors["description"] = ["描述过长（最多 2000 字）"]
        if not side_a_name:
            errors["side_a_name"] = ["正方立场不能为空"]
        elif len(side_a_name) > 50:
            errors["side_a_name"] = ["正方立场过长（最多 50 字）"]
        if not side_b_name:
            errors["side_b_name"] = ["反方立场不能为空"]
        elif len(side_b_name) > 50:
            errors["side_b_name"] = ["反方立场过长（最多 50 字）"]
        if category and len(category) > 50:
            errors["category"] = ["分类过长（最多 50 字）"]
        if fmt and len(fmt) > 30:
            errors["format"] = ["赛制过长（最多 30 字）"]

        if errors:
            return fail(msg="参数错误", code=400, data=errors)

        now = timezone.now()
        t = Topic(
            creator_id=request.user.id,
            title=title,
            description=description or None,
            category=category,
            format=fmt,
            side_a_name=side_a_name,
            side_b_name=side_b_name,
            status=Topic.Status.OPEN,
            view_count=0,
            comment_count=0,
            hot_score=0,
            created_at=now,
            updated_at=now,
        )
        t.save()

        return ok(
            data={
                "item": {
                    "id": t.id,
                    "creator": {
                        "id": request.user.id,
                        "username": getattr(request.user, "username", ""),
                        "avatar_url": getattr(request.user, "avatar_url", None),
                        "bio": getattr(request.user, "bio", None),
                    },
                    "title": t.title,
                    "description": t.description,
                    "category": t.category,
                    "format": t.format,
                    "side_a_name": t.side_a_name,
                    "side_b_name": t.side_b_name,
                    "status": t.status,
                    "view_count": t.view_count,
                    "comment_count": t.comment_count,
                    "hot_score": t.hot_score,
                    "created_at": t.created_at,
                    "votes": {"A": 0, "B": 0},
                }
            }
        )


class TopicDetailView(APIView):
    permission_classes = [AllowAny]

    def get_permissions(self):
        if self.request.method == "PATCH":
            return [IsAuthenticated()]
        return [AllowAny()]

    def get(self, request, topic_id: int):
        t = (
            Topic.objects.select_related("creator")
            .only(
                "id",
                "creator_id",
                "title",
                "description",
                "category",
                "format",
                "side_a_name",
                "side_b_name",
                "status",
                "view_count",
                "comment_count",
                "hot_score",
                "created_at",
                "creator__id",
                "creator__username",
                "creator__avatar_url",
                "creator__bio",
            )
            .filter(id=topic_id)
            .first()
        )
        if not t:
            return ok(data={"item": None})

        Topic.objects.filter(id=topic_id).update(view_count=F("view_count") + 1)
        try:
            t.view_count = int(t.view_count or 0) + 1
        except Exception:
            pass

        vote_rows = (
            TopicVote.objects.filter(topic_id=topic_id)
            .values("side")
            .annotate(c=Count("id"))
        )
        votes = {"A": 0, "B": 0}
        for r in vote_rows:
            votes[r["side"]] = r["c"]

        my_vote = None
        if getattr(request.user, "is_authenticated", False):
            my_vote = TopicVote.objects.filter(topic_id=topic_id, user_id=request.user.id).values_list("side", flat=True).first()

        return ok(
            data={
                "item": {
                    "id": t.id,
                    "creator": {
                        "id": t.creator_id,
                        "username": getattr(t.creator, "username", ""),
                        "avatar_url": getattr(t.creator, "avatar_url", None),
                        "bio": getattr(t.creator, "bio", None),
                    },
                    "title": t.title,
                    "description": t.description,
                    "category": t.category,
                    "format": t.format,
                    "side_a_name": t.side_a_name,
                    "side_b_name": t.side_b_name,
                    "status": t.status,
                    "view_count": t.view_count,
                    "comment_count": t.comment_count,
                    "hot_score": t.hot_score,
                    "created_at": t.created_at,
                    "votes": votes,
                    "my_vote": my_vote,
                }
            }
        )

    def patch(self, request, topic_id: int):
        t = Topic.objects.filter(id=topic_id).first()
        if not t:
            return fail(msg="话题不存在", code=404)
        if t.creator_id != request.user.id:
            return fail(msg="无权限", code=403)
        if t.status == Topic.Status.ARCHIVED:
            return fail(msg="话题已归档，无法修改", code=400)

        allowed = {"status", "title", "description", "category", "format", "side_a_name", "side_b_name"}
        if not any(k in request.data for k in allowed):
            return fail(msg="参数错误", code=400, data={"detail": ["无有效更新字段"]})

        present = {k for k in allowed if k in request.data}
        if t.status == Topic.Status.CLOSED and present != {"status"}:
            return fail(msg="话题已关闭，仅可修改 status（重开为 open 或归档为 archived）", code=400)

        if "status" in request.data:
            ns = (request.data.get("status") or "").strip().lower()
            if ns not in {Topic.Status.OPEN, Topic.Status.CLOSED, Topic.Status.ARCHIVED}:
                return fail(msg="参数错误", code=400, data={"status": ["状态无效"]})
            cur = t.status
            ok_transition = False
            if ns == cur:
                ok_transition = True
            elif cur == Topic.Status.OPEN and ns in (Topic.Status.CLOSED, Topic.Status.ARCHIVED):
                ok_transition = True
            elif cur == Topic.Status.CLOSED and ns in (Topic.Status.OPEN, Topic.Status.ARCHIVED):
                ok_transition = True
            if not ok_transition:
                return fail(msg="不允许的状态变更", code=400, data={"status": ["当前状态不可切换为目标状态"]})
            t.status = ns

        if "title" in request.data:
            title = (request.data.get("title") or "").strip()
            if not title:
                return fail(msg="参数错误", code=400, data={"title": ["标题不能为空"]})
            if len(title) > 200:
                return fail(msg="参数错误", code=400, data={"title": ["标题过长（最多 200 字）"]})
            t.title = title

        if "description" in request.data:
            description = (request.data.get("description") or "").strip()
            if description and len(description) > 2000:
                return fail(msg="参数错误", code=400, data={"description": ["描述过长（最多 2000 字）"]})
            t.description = description or None

        if "category" in request.data:
            category = (request.data.get("category") or "").strip() or "综合"
            if len(category) > 50:
                return fail(msg="参数错误", code=400, data={"category": ["分类过长"]})
            t.category = category

        if "format" in request.data:
            fmt = (request.data.get("format") or "").strip() or "快嘴乱斗"
            if len(fmt) > 30:
                return fail(msg="参数错误", code=400, data={"format": ["赛制过长"]})
            t.format = fmt

        if "side_a_name" in request.data:
            side_a_name = (request.data.get("side_a_name") or "").strip()
            if not side_a_name:
                return fail(msg="参数错误", code=400, data={"side_a_name": ["正方立场不能为空"]})
            if len(side_a_name) > 50:
                return fail(msg="参数错误", code=400, data={"side_a_name": ["正方立场过长"]})
            t.side_a_name = side_a_name

        if "side_b_name" in request.data:
            side_b_name = (request.data.get("side_b_name") or "").strip()
            if not side_b_name:
                return fail(msg="参数错误", code=400, data={"side_b_name": ["反方立场不能为空"]})
            if len(side_b_name) > 50:
                return fail(msg="参数错误", code=400, data={"side_b_name": ["反方立场过长"]})
            t.side_b_name = side_b_name

        t.updated_at = timezone.now()
        t.save()

        t2 = (
            Topic.objects.select_related("creator")
            .filter(id=topic_id)
            .only(
                "id",
                "creator_id",
                "title",
                "description",
                "category",
                "format",
                "side_a_name",
                "side_b_name",
                "status",
                "view_count",
                "comment_count",
                "hot_score",
                "created_at",
                "creator__id",
                "creator__username",
                "creator__avatar_url",
                "creator__bio",
            )
            .first()
        )
        vote_rows = TopicVote.objects.filter(topic_id=topic_id).values("side").annotate(c=Count("id"))
        votes = {"A": 0, "B": 0}
        for r in vote_rows:
            votes[r["side"]] = r["c"]
        my_vote = None
        if getattr(request.user, "is_authenticated", False):
            my_vote = TopicVote.objects.filter(topic_id=topic_id, user_id=request.user.id).values_list("side", flat=True).first()

        return ok(
            data={
                "item": {
                    "id": t2.id,
                    "creator": {
                        "id": t2.creator_id,
                        "username": getattr(t2.creator, "username", ""),
                        "avatar_url": getattr(t2.creator, "avatar_url", None),
                        "bio": getattr(t2.creator, "bio", None),
                    },
                    "title": t2.title,
                    "description": t2.description,
                    "category": t2.category,
                    "format": t2.format,
                    "side_a_name": t2.side_a_name,
                    "side_b_name": t2.side_b_name,
                    "status": t2.status,
                    "view_count": t2.view_count,
                    "comment_count": t2.comment_count,
                    "hot_score": t2.hot_score,
                    "created_at": t2.created_at,
                    "votes": votes,
                    "my_vote": my_vote,
                }
            }
        )


class TopicVoteView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, topic_id: int):
        if not Topic.objects.filter(id=topic_id).only("id").exists():
            return fail(msg="话题不存在", code=404)
        side = TopicVote.objects.filter(topic_id=topic_id, user_id=request.user.id).values_list("side", flat=True).first()
        return ok(data={"side": side})

    def post(self, request, topic_id: int):
        t = Topic.objects.filter(id=topic_id).only("id", "status").first()
        if not t:
            return fail(msg="话题不存在", code=404)
        if t.status != Topic.Status.OPEN:
            return fail(msg="话题已关闭", code=400)

        side = (request.data.get("side") or "").strip().upper()
        if side not in {"A", "B"}:
            return fail(msg="参数错误", code=400, data={"side": ["side 必须是 A 或 B"]})

        exists = TopicVote.objects.filter(topic_id=topic_id, user_id=request.user.id).only("id").exists()
        if exists:
            return fail(msg="你已投过票啦", code=400)

        TopicVote.objects.create(topic_id=topic_id, user_id=request.user.id, side=side, created_at=timezone.now())
        return ok(data={"side": side})


class TopicPostsView(APIView):
    permission_classes = [AllowAny]

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated()]
        return [AllowAny()]

    def get(self, request, topic_id: int):
        try:
            limit = int(request.query_params.get("limit") or 200)
        except Exception:
            limit = 200
        limit = max(1, min(limit, 500))

        qs = (
            DebatePost.objects.select_related("user")
            .filter(topic_id=topic_id)
            .order_by("created_at")
            .only(
                "id",
                "topic_id",
                "user_id",
                "parent_id",
                "side",
                "content",
                "evidence_url",
                "upvotes",
                "created_at",
                "user__id",
                "user__username",
                "user__avatar_url",
                "user__bio",
            )[:limit]
        )
        items = []
        for p in qs:
            items.append(
                {
                    "id": p.id,
                    "topic_id": p.topic_id,
                    "user": {
                        "id": p.user_id,
                        "username": getattr(p.user, "username", ""),
                        "avatar_url": getattr(p.user, "avatar_url", None),
                        "bio": getattr(p.user, "bio", None),
                    },
                    "parent_id": p.parent_id,
                    "side": p.side,
                    "content": p.content,
                    "evidence_url": p.evidence_url,
                    "upvotes": p.upvotes,
                    "created_at": p.created_at,
                }
            )
        return ok(data={"items": items})

    def post(self, request, topic_id: int):
        t = Topic.objects.filter(id=topic_id).only("id", "status").first()
        if not t:
            return fail(msg="话题不存在", code=404)
        if t.status != Topic.Status.OPEN:
            return fail(msg="话题已关闭", code=400)

        side = (request.data.get("side") or "").strip().upper()
        content = (request.data.get("content") or "").strip()
        evidence_url = (request.data.get("evidence_url") or "").strip() or None
        parent_id = request.data.get("parent_id")

        if side not in {"A", "B"}:
            return fail(msg="参数错误", code=400, data={"side": ["side 必须是 A 或 B"]})
        if not content:
            return fail(msg="参数错误", code=400, data={"content": ["内容不能为空"]})
        if len(content) > 2000:
            return fail(msg="参数错误", code=400, data={"content": ["内容过长（最多 2000 字）"]})

        if evidence_url:
            if len(evidence_url) > 500:
                return fail(msg="参数错误", code=400, data={"evidence_url": ["链接过长（最多 500 字符）"]})
            low = evidence_url.lower()
            if low.startswith(("javascript:", "data:", "vbscript:")):
                return fail(msg="参数错误", code=400, data={"evidence_url": ["链接格式不支持"]})

        parent = None
        if parent_id not in (None, "", 0, "0"):
            try:
                parent_id = int(parent_id)
            except Exception:
                return fail(msg="参数错误", code=400, data={"parent_id": ["parent_id 无效"]})
            parent = DebatePost.objects.filter(id=parent_id, topic_id=topic_id).only("id").first()
            if not parent:
                return fail(msg="参数错误", code=400, data={"parent_id": ["父观点不存在"]})

        p = DebatePost(
            topic_id=topic_id,
            user_id=request.user.id,
            parent_id=parent.id if parent else None,
            side=side,
            content=content,
            evidence_url=evidence_url,
            upvotes=0,
            created_at=timezone.now(),
        )
        p.save()
        Topic.objects.filter(id=topic_id).update(comment_count=F("comment_count") + 1)

        return ok(
            data={
                "item": {
                    "id": p.id,
                    "topic_id": topic_id,
                    "user": {
                        "id": request.user.id,
                        "username": getattr(request.user, "username", ""),
                        "avatar_url": getattr(request.user, "avatar_url", None),
                        "bio": getattr(request.user, "bio", None),
                    },
                    "parent_id": p.parent_id,
                    "side": side,
                    "content": content,
                    "evidence_url": evidence_url,
                    "upvotes": 0,
                    "created_at": p.created_at,
                }
            }
        )


class DebatePostDetailView(APIView):
    permission_classes = [AllowAny]

    def get_permissions(self):
        if self.request.method in ("PATCH", "DELETE"):
            return [IsAuthenticated()]
        return [AllowAny()]

    def patch(self, request, topic_id: int, post_id: int):
        t = Topic.objects.filter(id=topic_id).only("id", "status").first()
        if not t or t.status != Topic.Status.OPEN:
            return fail(msg="话题已关闭或不存在", code=400)
        p = DebatePost.objects.filter(id=post_id, topic_id=topic_id).first()
        if not p or p.user_id != request.user.id:
            return fail(msg="观点不存在或无权限", code=404)

        updated = False
        if "content" in request.data:
            content = (request.data.get("content") or "").strip()
            if not content:
                return fail(msg="参数错误", code=400, data={"content": ["内容不能为空"]})
            if len(content) > 2000:
                return fail(msg="参数错误", code=400, data={"content": ["内容过长（最多 2000 字）"]})
            p.content = content
            updated = True

        if "evidence_url" in request.data:
            evidence_url = (request.data.get("evidence_url") or "").strip() or None
            if evidence_url:
                if len(evidence_url) > 500:
                    return fail(msg="参数错误", code=400, data={"evidence_url": ["链接过长（最多 500 字符）"]})
                low = evidence_url.lower()
                if low.startswith(("javascript:", "data:", "vbscript:")):
                    return fail(msg="参数错误", code=400, data={"evidence_url": ["链接格式不支持"]})
            p.evidence_url = evidence_url
            updated = True

        if not updated:
            return fail(msg="参数错误", code=400, data={"content": ["请提供要修改的 content 或 evidence_url"]})

        p.save()
        p2 = (
            DebatePost.objects.select_related("user")
            .filter(id=p.id)
            .only(
                "id",
                "topic_id",
                "user_id",
                "parent_id",
                "side",
                "content",
                "evidence_url",
                "upvotes",
                "created_at",
                "user__id",
                "user__username",
                "user__avatar_url",
                "user__bio",
            )
            .first()
        )
        return ok(
            data={
                "item": {
                    "id": p2.id,
                    "topic_id": p2.topic_id,
                    "user": {
                        "id": p2.user_id,
                        "username": getattr(p2.user, "username", ""),
                        "avatar_url": getattr(p2.user, "avatar_url", None),
                        "bio": getattr(p2.user, "bio", None),
                    },
                    "parent_id": p2.parent_id,
                    "side": p2.side,
                    "content": p2.content,
                    "evidence_url": p2.evidence_url,
                    "upvotes": p2.upvotes,
                    "created_at": p2.created_at,
                }
            }
        )

    def delete(self, request, topic_id: int, post_id: int):
        t = Topic.objects.filter(id=topic_id).only("id", "status").first()
        if not t or t.status != Topic.Status.OPEN:
            return fail(msg="话题已关闭或不存在", code=400)
        p = DebatePost.objects.filter(id=post_id, topic_id=topic_id).first()
        if not p or p.user_id != request.user.id:
            return fail(msg="观点不存在或无权限", code=404)
        if DebatePost.objects.filter(parent_id=post_id).exists():
            return fail(msg="请先删除回复后再删本条", code=400)

        with transaction.atomic():
            p.delete()
            cur = Topic.objects.filter(id=topic_id).values_list("comment_count", flat=True).first()
            new_cc = max(0, int(cur or 0) - 1)
            Topic.objects.filter(id=topic_id).update(comment_count=new_cc)

        return ok(data={})

