from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = "Seed test topics into `topics` table"

    def handle(self, *args, **options):
        rows = [
            (
                1,
                "如果记忆可以被数字备份，那么“死亡”是不是只是个Bug？",
                "想象一下你把记忆传到了云端，你的肉体领了便当。你现在的云端版本还在给前任发微信，这算不算你还活着？",
                "哲学脑洞",
                "深蹲逻辑",
                "永生派大星",
                "别删我档",
                "open",
                12500,
                842,
                98.5,
                "2026-04-10 08:00:00",
            ),
            (
                2,
                "AI到底会先抢走我们的工作，还是先抢走我们的寂寞？",
                "打工人担心饭碗，单身狗期待陪伴。AI的第一志愿到底是什么？",
                "科技拆解",
                "快嘴乱斗",
                "觉醒的打工人",
                "赛博情感大师",
                "open",
                9800,
                621,
                85.2,
                "2026-04-12 11:30:00",
            ),
            (
                4,
                "咸豆腐脑是否应该被定为非法？",
                "一场跨越南北的终极对决。美味即正义 vs 逻辑至上。",
                "社恐日常",
                "复读机模式",
                "咸党万岁",
                "甜党无敌",
                "open",
                6700,
                305,
                72.8,
                "2026-04-14 19:15:00",
            ),
            (
                5,
                "猫咪到底是主子还是室友？",
                "当你深夜被踩脸时，法律上它算不算故意伤害？",
                "哲学脑洞",
                "快嘴乱斗",
                "主子派",
                "室友派",
                "open",
                4300,
                188,
                65.0,
                "2026-04-15 13:20:00",
            ),
            (
                1,
                "摸鱼算不算一种被动收入？",
                "如果带薪拉屎是福利，那带薪发呆就是理财。",
                "社恐日常",
                "快嘴乱斗",
                "经济学大师",
                "资本家走狗",
                "open",
                5100,
                210,
                70.5,
                "2026-04-13 15:00:00",
            ),
        ]

        sql = (
            "INSERT INTO topics "
            "(creator_id,title,description,category,format,side_a_name,side_b_name,status,view_count,comment_count,hot_score,created_at) "
            "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        )

        with connection.cursor() as cursor:
            cursor.executemany(sql, rows)
            cursor.execute("SELECT COUNT(*) FROM topics")
            topics_count = cursor.fetchone()[0]

        self.stdout.write(f"inserted={len(rows)} topics_count={topics_count}")

