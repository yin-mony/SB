import json
import secrets
from datetime import timedelta

from django.db import connection
from django.db.models import Count, Sum
from django.db.models.functions import TruncDate
from django.utils import timezone
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView

from apps.core.models import ActivityLog, Badge, UserBadge
from apps.core.responses import fail, ok
from apps.debate.models import DebatePost, Topic
from apps.blog.models import BlogPost

from .models import Follow, User


_BADGE_ICON_IDS = [
    "badge-crown",
    "badge-lightning",
    "badge-quill",
    "badge-shield",
    "badge-rocket",
    "badge-star",
    "badge-brain",
    "badge-scroll",
    "badge-medal",
    "badge-flame",
    "badge-compass",
    "badge-heart",
]


def _normalize_badge_icon_id(icon, condition_json, badge_id: int):
    if isinstance(icon, str) and icon in _BADGE_ICON_IDS:
        return icon

    cond = condition_json
    if isinstance(cond, str):
        try:
            cond = json.loads(cond)
        except Exception:
            cond = {}

    if isinstance(cond, dict) and cond:
        keys = list(cond.keys())
        if len(keys) == 1:
            k = keys[0]
            m = {
                "topics_created": "badge-scroll",
                "debate_posts": "badge-lightning",
                "blog_posts": "badge-quill",
                "followers": "badge-heart",
                "following": "badge-compass",
                "likes_total": "badge-star",
                "hot_topics": "badge-rocket",
                "late_night_posts": "badge-flame",
            }
            if k in m:
                return m[k]
        return "badge-medal"

    try:
        i = int(badge_id or 0)
    except Exception:
        i = 0
    return _BADGE_ICON_IDS[i % len(_BADGE_ICON_IDS)]


def _user_public_dict(user: User):
    return {
        "id": user.id,
        "username": user.username,
        "avatar_url": user.avatar_url,
        "bio": user.bio,
        "role": user.role,
        "created_at": user.created_at,
    }


def _build_user_metrics(user_id: int):
    topics_qs = Topic.objects.filter(creator_id=user_id)
    debate_qs = DebatePost.objects.filter(user_id=user_id)
    # 与 UserContentView、博客列表展示口径一致：仅已发布文章
    blog_qs = BlogPost.objects.filter(author_id=user_id, is_published=True)
    # 获赞：已发布博客的 like_count + 用户观点的 upvotes（与内容区展示字段一致）
    blog_likes = blog_qs.aggregate(x=Sum("like_count")).get("x") or 0
    debate_likes = debate_qs.aggregate(x=Sum("upvotes")).get("x") or 0
    likes_total = int(blog_likes or 0) + int(debate_likes or 0)
    return {
        "topics_created": topics_qs.count(),
        "debate_posts": debate_qs.count(),
        "blog_posts": blog_qs.count(),
        "followers": Follow.objects.filter(followee_id=user_id).count(),
        "following": Follow.objects.filter(follower_id=user_id).count(),
        "likes_total": likes_total,
        "hot_topics": topics_qs.filter(hot_score__gte=80).count(),
        "late_night_posts": debate_qs.filter(created_at__hour__in=[0, 1, 2, 3]).count()
        + blog_qs.filter(created_at__hour__in=[0, 1, 2, 3]).count(),
    }


def _sync_user_badges(user_id: int):
    metrics = _build_user_metrics(user_id)
    now = timezone.now()
    badge_ids = set(UserBadge.objects.filter(user_id=user_id).values_list("badge_id", flat=True))
    all_badges = Badge.objects.all().only("id", "condition_json")
    for b in all_badges:
        cond = b.condition_json
        if isinstance(cond, str):
            try:
                cond = json.loads(cond)
            except Exception:
                cond = {}
        if not isinstance(cond, dict) or not cond:
            continue
        ok_all = True
        for k, v in cond.items():
            need = int(v or 0)
            cur = int(metrics.get(k) or 0)
            if cur < need:
                ok_all = False
                break
        if not ok_all or b.id in badge_ids:
            continue
        UserBadge.objects.create(user_id=user_id, badge_id=b.id, awarded_at=now)
        badge_ids.add(b.id)
    return metrics


class UserDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, user_id: int):
        user = User.objects.filter(id=user_id).first()
        if not user:
            return fail(msg="用户不存在", code=404)
        return ok(data=_user_public_dict(user))


class UserStatsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, user_id: int):
        user = User.objects.filter(id=user_id).first()
        if not user:
            return fail(msg="用户不存在", code=404)
        return ok(data=_build_user_metrics(user_id))


class UserActivityView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, user_id: int):
        try:
            limit = int(request.query_params.get("limit") or 50)
        except Exception:
            limit = 50
        limit = max(1, min(limit, 50))

        before_id = request.query_params.get("before_id")
        try:
            before_id = int(before_id) if before_id not in (None, "", "0") else None
        except Exception:
            before_id = None

        qs = ActivityLog.objects.filter(user_id=user_id)
        if before_id:
            qs = qs.filter(id__lt=before_id)
        qs = qs.order_by("-id").values("id", "action_type", "target_type", "target_id", "data", "created_at")

        rows = list(qs[: limit + 1])
        has_more = len(rows) > limit
        items = rows[:limit]
        next_before_id = items[-1]["id"] if items else None
        return ok(data={"items": items, "has_more": has_more, "next_before_id": next_before_id})


class UserBadgesView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, user_id: int):
        _sync_user_badges(user_id)
        badge_ids = list(UserBadge.objects.filter(user_id=user_id).values_list("badge_id", flat=True))
        badges = list(Badge.objects.filter(id__in=badge_ids).values("id", "name", "description", "icon", "condition_json"))
        for b in badges:
            b["icon_id"] = _normalize_badge_icon_id(b.get("icon"), b.get("condition_json"), b.get("id"))
            b.pop("icon", None)
        return ok(data={"items": badges})


class UserHeatmapView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, user_id: int):
        end = timezone.now().date()
        start = end - timedelta(days=364)
        qs = (
            ActivityLog.objects.filter(user_id=user_id, created_at__date__gte=start, created_at__date__lte=end)
            .annotate(d=TruncDate("created_at"))
            .values("d")
            .annotate(c=Count("id"))
        )
        m = {row["d"].isoformat(): int(row["c"]) for row in qs}
        days = []
        cur = start
        while cur <= end:
            iso = cur.isoformat()
            days.append({"date": iso, "count": m.get(iso, 0)})
            cur += timedelta(days=1)
        return ok(data={"start_date": start.isoformat(), "end_date": end.isoformat(), "days": days})


class UserFollowView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id: int):
        follower_id = request.user.id
        followee_id = user_id
        if follower_id == followee_id:
            return fail(msg="不能关注自己", code=400)
        if not User.objects.filter(id=followee_id).exists():
            return fail(msg="用户不存在", code=404)
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO follows (follower_id,followee_id,created_at) VALUES (%s,%s,NOW()) "
                "ON DUPLICATE KEY UPDATE created_at=created_at",
                [follower_id, followee_id],
            )
        return ok(data={})

    def delete(self, request, user_id: int):
        follower_id = request.user.id
        followee_id = user_id
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM follows WHERE follower_id=%s AND followee_id=%s", [follower_id, followee_id])
        return ok(data={})


class UserFollowersView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, user_id: int):
        follower_ids = list(Follow.objects.filter(followee_id=user_id).order_by("-created_at").values_list("follower_id", flat=True)[:50])
        users = list(User.objects.filter(id__in=follower_ids).values("id", "username", "avatar_url", "bio"))
        users.sort(key=lambda u: follower_ids.index(u["id"]) if u["id"] in follower_ids else 10**9)
        return ok(data={"items": users})


class UserFollowingView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, user_id: int):
        followee_ids = list(Follow.objects.filter(follower_id=user_id).order_by("-created_at").values_list("followee_id", flat=True)[:50])
        users = list(User.objects.filter(id__in=followee_ids).values("id", "username", "avatar_url", "bio"))
        users.sort(key=lambda u: followee_ids.index(u["id"]) if u["id"] in followee_ids else 10**9)
        return ok(data={"items": users})


class UserContentView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id: int):
        if request.user.id != user_id:
            return fail(msg="无权限访问", code=403)

        try:
            limit = int(request.query_params.get("limit") or 10)
        except Exception:
            limit = 10
        limit = max(1, min(limit, 30))

        topics = (
            Topic.objects.filter(creator_id=user_id)
            .order_by("-created_at")
            .values("id", "title", "category", "hot_score", "view_count", "comment_count", "created_at")[:limit]
        )
        blog_posts = (
            BlogPost.objects.filter(author_id=user_id, is_published=True)
            .order_by("-created_at")
            .values("id", "title", "slug", "category", "view_count", "comment_count", "like_count", "created_at")[:limit]
        )
        debate_posts = (
            DebatePost.objects.select_related("topic")
            .filter(user_id=user_id)
            .order_by("-created_at")
            .only("id", "topic_id", "side", "content", "upvotes", "created_at", "topic__id", "topic__title")[:limit]
        )
        debate_items = []
        for p in debate_posts:
            debate_items.append(
                {
                    "id": p.id,
                    "topic_id": p.topic_id,
                    "topic_title": getattr(p.topic, "title", ""),
                    "side": p.side,
                    "content": (p.content or "")[:200],
                    "upvotes": p.upvotes,
                    "created_at": p.created_at,
                }
            )

        return ok(data={"topics": list(topics), "blog_posts": list(blog_posts), "debate_posts": debate_items})


_QUICK_REPLY_AUTO_LINES = [
    "你说得对，但这恰恰证明了我更对。",
    "逻辑上你赢了，现实里我不服。",
    "我不是抬杠，我是在做严谨的情绪表达。",
    "建议把你的论点放进冰箱，冷静一下再拿出来。",
    "你这个观点很新颖，建议下次别用了。",
]


class QuickReplyView(APIView):
    """个人中心「快速回喷」：写入活动流水，供时间线展示。"""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        auto = bool(request.data.get("auto"))
        text = (request.data.get("text") or "").strip()
        u = request.user
        auto_on = bool(getattr(u, "auto_debate_mode", False))

        if auto_on and auto:
            text = secrets.choice(_QUICK_REPLY_AUTO_LINES)
        elif text:
            pass
        else:
            return fail(msg="参数错误", code=400, data={"text": ["先写点什么，或开启自动抬杠模式后再试"]})

        if len(text) > 500:
            return fail(msg="参数错误", code=400, data={"text": ["内容过长（最多 500 字）"]})

        ActivityLog.objects.create(
            user_id=u.id,
            action_type="quick_reply",
            target_type=None,
            target_id=None,
            data={"text": text},
            created_at=timezone.now(),
        )
        return ok(data={"text": text})

