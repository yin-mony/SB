from django.db import connection
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.core.responses import fail, ok
from apps.blog.models import BlogPost
from apps.debate.models import DebatePost, Topic
from apps.notifications.models import Notification


class HealthView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({"code": 200, "msg": "success", "data": {"service": "debate_paradise"}})


class FavoritesView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        target_type = (request.data.get("target_type") or "").strip()
        try:
            target_id = int(request.data.get("target_id") or 0)
        except Exception:
            target_id = 0

        if target_type not in {"topic", "blog_post", "debate_post"}:
            return fail(msg="target_type 无效", code=400)
        if target_id <= 0:
            return fail(msg="target_id 无效", code=400)

        if target_type == "topic" and not Topic.objects.filter(id=target_id).exists():
            return fail(msg="收藏失败", code=400, data={"target_id": ["话题不存在"]})
        if target_type == "blog_post" and not BlogPost.objects.filter(id=target_id, is_published=True).exists():
            return fail(msg="收藏失败", code=400, data={"target_id": ["文章不存在或已下架"]})
        if target_type == "debate_post" and not DebatePost.objects.filter(id=target_id).exists():
            return fail(msg="收藏失败", code=400, data={"target_id": ["观点不存在"]})

        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO favorites (user_id,target_type,target_id,created_at)
                VALUES (%s,%s,%s,NOW())
                ON DUPLICATE KEY UPDATE id=id
                """,
                [request.user.id, target_type, target_id],
            )
            cursor.execute(
                "SELECT id,created_at FROM favorites WHERE user_id=%s AND target_type=%s AND target_id=%s LIMIT 1",
                [request.user.id, target_type, target_id],
            )
            row = cursor.fetchone()

        return ok(data={"id": row[0] if row else None, "target_type": target_type, "target_id": target_id})

    def get(self, request):
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

        with connection.cursor() as cursor:
            if before_id:
                cursor.execute(
                    "SELECT id,target_type,target_id,created_at FROM favorites WHERE user_id=%s AND id < %s ORDER BY id DESC LIMIT %s",
                    [request.user.id, before_id, limit + 1],
                )
            else:
                cursor.execute(
                    "SELECT id,target_type,target_id,created_at FROM favorites WHERE user_id=%s ORDER BY id DESC LIMIT %s",
                    [request.user.id, limit + 1],
                )
            rows = cursor.fetchall()

        has_more = len(rows) > limit
        rows = rows[:limit]

        items = []
        topic_ids = [r[2] for r in rows if r[1] == "topic"]
        blog_ids = [r[2] for r in rows if r[1] == "blog_post"]
        debate_ids = [r[2] for r in rows if r[1] == "debate_post"]

        topic_map = {t.id: t for t in Topic.objects.filter(id__in=topic_ids)}
        blog_map = {p.id: p for p in BlogPost.objects.filter(id__in=blog_ids)}
        debate_map = {p.id: p for p in DebatePost.objects.filter(id__in=debate_ids)}

        for fav_id, target_type, target_id, created_at in rows:
            target = None
            if target_type == "topic" and target_id in topic_map:
                t = topic_map[target_id]
                target = {"id": t.id, "title": t.title, "category": t.category}
            elif target_type == "blog_post" and target_id in blog_map:
                p = blog_map[target_id]
                target = {"id": p.id, "title": p.title, "slug": p.slug, "category": p.category}
            elif target_type == "debate_post" and target_id in debate_map:
                p = debate_map[target_id]
                target = {"id": p.id, "topic_id": p.topic_id, "side": p.side, "content": p.content[:120]}
            items.append(
                {
                    "id": fav_id,
                    "target_type": target_type,
                    "target_id": target_id,
                    "created_at": created_at,
                    "target": target,
                }
            )
        next_before_id = items[-1]["id"] if items else None
        return ok(data={"items": items, "has_more": has_more, "next_before_id": next_before_id})

    def delete(self, request):
        target_type = (request.query_params.get("target_type") or "").strip()
        try:
            target_id = int(request.query_params.get("target_id") or 0)
        except Exception:
            target_id = 0

        if target_type not in {"topic", "blog_post", "debate_post"}:
            return fail(msg="target_type 无效", code=400)
        if target_id <= 0:
            return fail(msg="target_id 无效", code=400)

        with connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM favorites WHERE user_id=%s AND target_type=%s AND target_id=%s",
                [request.user.id, target_type, target_id],
            )
        return ok(data={})


class FavoritesStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        target_type = (request.query_params.get("target_type") or "").strip()
        try:
            target_id = int(request.query_params.get("target_id") or 0)
        except Exception:
            target_id = 0

        if target_type not in {"topic", "blog_post", "debate_post"}:
            return fail(msg="target_type 无效", code=400)
        if target_id <= 0:
            return fail(msg="target_id 无效", code=400)

        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT id FROM favorites WHERE user_id=%s AND target_type=%s AND target_id=%s LIMIT 1",
                [request.user.id, target_type, target_id],
            )
            row = cursor.fetchone()
        return ok(data={"is_favorited": bool(row), "favorite_id": row[0] if row else None})


class NotificationsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
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

        qs = Notification.objects.filter(recipient_id=request.user.id)
        if before_id:
            qs = qs.filter(id__lt=before_id)
        qs = qs.order_by("-id")
        rows = list(qs.values("id", "type", "data", "is_read", "created_at")[: limit + 1])
        has_more = len(rows) > limit
        items = rows[:limit]
        next_before_id = items[-1]["id"] if items else None
        return ok(data={"items": items, "has_more": has_more, "next_before_id": next_before_id})


class NotificationReadView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, notification_id: int):
        exists = Notification.objects.filter(id=notification_id, recipient_id=request.user.id).exists()
        if not exists:
            return fail(msg="通知不存在", code=404)
        Notification.objects.filter(id=notification_id, recipient_id=request.user.id).update(is_read=True)
        return ok(data={})


class NotificationsReadAllView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        Notification.objects.filter(recipient_id=request.user.id, is_read=False).update(is_read=True)
        return ok(data={})
