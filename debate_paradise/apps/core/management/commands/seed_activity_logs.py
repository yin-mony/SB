from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = "Seed test activity logs into `activity_logs` table"

    def handle(self, *args, **options):
        rows = [
            (1, "create_topic", "topic", 1, '{"title": "如果记忆可以被数字备份..."}', "2026-04-10 08:00:00"),
            (1, "post_debate", "debate_post", 1, '{"content": "人类不就是一堆数据的集合吗？"}', "2026-04-10 08:30:00"),
            (2, "post_debate", "debate_post", 2, '{"content": "想得美！没有了肉体..."}', "2026-04-10 09:15:00"),
            (4, "publish_blog", "blog_post", 1, '{"title": "为什么“不睡觉”是2026年人类进化的终极方案？"}', "2026-04-08 22:00:00"),
            (2, "publish_blog", "blog_post", 2, '{"title": "如何跟你的智能扫地机器人建立长达十年的恋爱关系？"}', "2026-04-09 16:45:00"),
            (3, "follow", "user", 2, '{"followee": "逻辑黑洞·小美"}', "2026-04-12 09:00:00"),
            (5, "create_topic", "topic", 4, '{"title": "猫咪到底是主子还是室友？"}', "2026-04-15 13:20:00"),
        ]

        sql = (
            "INSERT INTO activity_logs "
            "(user_id,action_type,target_type,target_id,data,created_at) "
            "VALUES (%s,%s,%s,%s,%s,%s)"
        )

        with connection.cursor() as cursor:
            cursor.executemany(sql, rows)
            cursor.execute("SELECT COUNT(*) FROM activity_logs")
            logs_count = cursor.fetchone()[0]

        self.stdout.write(f"inserted={len(rows)} activity_logs_count={logs_count}")

