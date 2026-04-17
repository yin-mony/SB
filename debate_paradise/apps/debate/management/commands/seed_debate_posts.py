from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = "Seed test debate posts into `debate_posts` table"

    def handle(self, *args, **options):
        rows = [
            (
                1,
                1,
                1,
                None,
                "A",
                "人类不就是一堆数据的集合吗？如果我的情感、记忆和骚话都能被完整保存，那我就是换了个碳基以外的壳子而已！死亡只是硬件报废，软件还在运行啊！",
                156,
                "2026-04-10 08:30:00",
            ),
            (
                2,
                1,
                2,
                None,
                "B",
                "想得美！没有了肉体，你连辣条的味道都尝不到，那叫哪门子活着？云端那个只是你的动态表情包集合体，它不是你，它只是你的“电子遗照”！",
                142,
                "2026-04-10 09:15:00",
            ),
            (
                3,
                1,
                4,
                1,
                "A",
                "支持！我甚至觉得现在的我已经是第37代备份了，之前36个都在水群时阵亡了。",
                45,
                "2026-04-10 10:00:00",
            ),
            (
                4,
                1,
                5,
                2,
                "B",
                "你说的对，但电子遗照也是遗照啊！至少清明节还能云端上香。",
                38,
                "2026-04-10 10:30:00",
            ),
            (
                5,
                2,
                3,
                None,
                "A",
                "AI已经在抢我饭碗了！上周我写的周报被GPT优化后，老板说“这才像人话”。",
                89,
                "2026-04-12 12:00:00",
            ),
            (
                6,
                2,
                2,
                None,
                "B",
                "AI先抢寂寞！我现在和Siri聊天的频率比和人类都高，她还会讲冷笑话。",
                76,
                "2026-04-12 13:20:00",
            ),
            (
                7,
                3,
                4,
                None,
                "A",
                "咸豆腐脑是早餐的灵魂！甜的那是零食！非法必须非法！",
                102,
                "2026-04-14 20:00:00",
            ),
            (
                8,
                3,
                1,
                None,
                "B",
                "甜豆腐脑是舌尖上的江南！咸的是对豆花的亵渎！",
                98,
                "2026-04-14 21:10:00",
            ),
        ]

        sql = (
            "INSERT INTO debate_posts "
            "(id,topic_id,user_id,parent_id,side,content,upvotes,created_at) "
            "VALUES (%s,%s,%s,%s,%s,%s,%s,%s) "
            "ON DUPLICATE KEY UPDATE "
            "topic_id=VALUES(topic_id), "
            "user_id=VALUES(user_id), "
            "parent_id=VALUES(parent_id), "
            "side=VALUES(side), "
            "content=VALUES(content), "
            "upvotes=VALUES(upvotes), "
            "created_at=VALUES(created_at)"
        )

        with connection.cursor() as cursor:
            cursor.executemany(sql, rows)
            cursor.execute("SELECT COUNT(*) FROM debate_posts")
            posts_count = cursor.fetchone()[0]

        self.stdout.write(f"inserted_or_updated={len(rows)} debate_posts_count={posts_count}")

