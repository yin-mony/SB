from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = "Seed test notifications into `notifications` table"

    def handle(self, *args, **options):
        rows = [
            (
                1,
                "comment_reply",
                '{"actor": "逻辑黑洞·小美", "content": "回复了你的观点", "target": "如果记忆可以被数字备份..."}',
                False,
            ),
            (
                2,
                "vote",
                '{"actor": "杠精之王·阿强", "content": "赞了你的观点", "target": "想得美！没有了肉体..."}',
                False,
            ),
            (4, "follow", '{"actor": "杠精一号", "content": "关注了你"}', True),
            (3, "system", '{"content": "恭喜！你的话题登上热榜前三！"}', False),
        ]

        sql = (
            "INSERT INTO notifications (recipient_id,type,data,is_read,created_at) "
            "VALUES (%s,%s,%s,%s,NOW())"
        )

        with connection.cursor() as cursor:
            cursor.executemany(sql, rows)
            cursor.execute("SELECT COUNT(*) FROM notifications")
            notifications_count = cursor.fetchone()[0]

        self.stdout.write(f"inserted={len(rows)} notifications_count={notifications_count}")

