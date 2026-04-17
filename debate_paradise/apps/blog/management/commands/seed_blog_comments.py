from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = "Seed test blog comments into `blog_comments` table"

    def handle(self, *args, **options):
        rows = [
            (
                1,
                1,
                None,
                "教授，按照你的理论，我不睡觉三年了，为什么我现在的黑眼圈已经可以用来扫码支付了？",
                125,
                "2026-04-09 08:30:00",
            ),
            (
                1,
                2,
                None,
                "胡说！梦里的奶茶是不长胖的，现实里的奶茶一口下去就是三斤肉！所以我选择永眠。",
                86,
                "2026-04-09 10:15:00",
            ),
            (
                1,
                4,
                1,
                "那是因为你没有正确安装“遮瑕”补丁。",
                34,
                "2026-04-09 11:00:00",
            ),
            (
                2,
                5,
                None,
                "我的扫地机器人最近开始故意绕开我的拖鞋，它是不是不爱我了？",
                56,
                "2026-04-10 09:00:00",
            ),
            (
                3,
                3,
                None,
                "今天下午试了一下，结果老板从我背后飘过，量子态坍缩为“被扣绩效”。",
                78,
                "2026-04-11 16:20:00",
            ),
        ]

        sql = (
            "INSERT INTO blog_comments "
            "(post_id,user_id,parent_id,content,upvotes,created_at) "
            "VALUES (%s,%s,%s,%s,%s,%s)"
        )

        with connection.cursor() as cursor:
            cursor.executemany(sql, rows)
            cursor.execute("SELECT COUNT(*) FROM blog_comments")
            comments_count = cursor.fetchone()[0]

        self.stdout.write(f"inserted={len(rows)} blog_comments_count={comments_count}")

