from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = "Seed test blog posts into `blog_posts` table"

    def handle(self, *args, **options):
        rows = [
            (
                4,
                "为什么“不睡觉”是2026年人类进化的终极方案？",
                "why-no-sleep-2026",
                "https://images.unsplash.com/photo-1518020382113-a7e8fc38eac9?w=600",
                "# 逻辑一：睡眠只是下载补丁\n\n根据我邻居王大爷的理论，人类其实是高级生物模拟器。所谓的睡眠，不过是系统在连接云端服务器进行漏洞修复和补丁下载。\n\n> “我不是在熬夜，我是在拒绝系统的强制更新。”\n\n# 逻辑二：梦境是广告位\n\n你以为梦见发财是真的？不，那是宇宙服务商植入的强制广告。总之，2026年的人类，应该学会用光合作用替代睡眠。",
                "科学家（我邻居王大爷）指出，睡眠只是大脑在下载补丁。只要我不连接服务器，我就可以永久在线！",
                "逻辑体操",
                '["熬夜", "进化", "伪科学"]',
                5600,
                1200,
                89,
                True,
                "2026-04-08 22:00:00",
            ),
            (
                2,
                "如何跟你的智能扫地机器人建立长达十年的恋爱关系？",
                "love-with-robot-vacuum",
                "https://images.unsplash.com/photo-1550745165-9bc0b252726f?w=600",
                "它懂我的寂寞，它也懂我地板上的头发。每天下班回家，看到它勤勤恳恳地撞墙，我就觉得人间值得。\n\n## 第一步：取个名字\n叫它“小石头”或“薛定谔”，取决于你想让它觉得自己是宠物还是哲学家。\n\n## 第二步：理解避障雷达\n每一次它绕开你的脚，都不是偶然，那是刻意的温柔。",
                "本文深度剖析跨越物种的电子爱恋，教你如何读懂避障雷达的每一次闪烁。",
                "赛博生活",
                '["AI", "情感", "机器人"]',
                3400,
                856,
                42,
                True,
                "2026-04-09 16:45:00",
            ),
            (
                3,
                "解析“摸鱼”的量子力学态：只要我不看老板，我就在工作",
                "quantum-fish-touching",
                "https://images.unsplash.com/photo-1614728263952-84ea256f9679?w=600",
                "薛定谔的打工人：在老板推开门的那一刻，我的量子态发生坍缩。本文教你如何维持高频次的“不确定性”摸鱼。\n\n## 核心理论\n当你处于“屏幕最小化+Excel表格打开”的叠加态时，你就是不可观测的。",
                "摸鱼是一种微观粒子的自然运动，不应被宏观规则束缚。",
                "职场歪理",
                '["摸鱼", "量子力学", "职场"]',
                2100,
                520,
                28,
                True,
                "2026-04-11 14:30:00",
            ),
        ]

        sql = (
            "INSERT INTO blog_posts "
            "(author_id,title,slug,cover_image,content,excerpt,category,tags,view_count,like_count,comment_count,is_published,created_at) "
            "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "
            "ON DUPLICATE KEY UPDATE "
            "author_id=VALUES(author_id), "
            "title=VALUES(title), "
            "cover_image=VALUES(cover_image), "
            "content=VALUES(content), "
            "excerpt=VALUES(excerpt), "
            "category=VALUES(category), "
            "tags=VALUES(tags), "
            "view_count=VALUES(view_count), "
            "like_count=VALUES(like_count), "
            "comment_count=VALUES(comment_count), "
            "is_published=VALUES(is_published), "
            "created_at=VALUES(created_at)"
        )

        with connection.cursor() as cursor:
            cursor.executemany(sql, rows)
            cursor.execute("SELECT COUNT(*) FROM blog_posts")
            posts_count = cursor.fetchone()[0]

        self.stdout.write(f"inserted_or_updated={len(rows)} blog_posts_count={posts_count}")

