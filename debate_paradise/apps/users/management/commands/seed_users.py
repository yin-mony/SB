from django.core.management.base import BaseCommand
from django.db import connection

import bcrypt


class Command(BaseCommand):
    help = "Seed test users into `users` table"

    def handle(self, *args, **options):
        password_hash = bcrypt.hashpw(b"123456", bcrypt.gensalt(rounds=12)).decode("utf-8")
        rows = [
            (
                "杠精之王·阿强",
                "aqiang@debate.paradise",
                password_hash,
                "https://api.dicebear.com/7.x/avataaars/svg?seed=Aqiang",
                "键盘上的每一个键位都有灵魂——直到漏电为止。",
                "user",
                "2026-03-01 10:00:00",
            ),
            (
                "逻辑黑洞·小美",
                "xiaomei@debate.paradise",
                password_hash,
                "https://api.dicebear.com/7.x/avataaars/svg?seed=Xiaomei",
                "你以为你赢了，其实你只是进入了我的下一个死循环。",
                "user",
                "2026-03-05 14:20:00",
            ),
            (
                "熬夜冠军·大壮",
                "dazhuang@debate.paradise",
                password_hash,
                "https://api.dicebear.com/7.x/avataaars/svg?seed=Dazhuang",
                "服务器不睡我不睡，我是秃头小宝贝。",
                "admin",
                "2026-02-20 03:15:00",
            ),
            (
                "陈教授(假)",
                "professor.chen@debate.paradise",
                password_hash,
                "https://api.dicebear.com/7.x/avataaars/svg?seed=ProfessorChen",
                "资深瞎话学者，睡眠守门人。",
                "user",
                "2026-03-10 09:30:00",
            ),
            (
                "杠精一号",
                "gangjing1@debate.paradise",
                password_hash,
                "https://api.dicebear.com/7.x/avataaars/svg?seed=Gangjing1",
                "不杠不舒服斯基。",
                "user",
                "2026-04-01 16:45:00",
            ),
        ]

        sql = (
            "INSERT INTO users (username,email,password_hash,avatar_url,bio,role,created_at) "
            "VALUES (%s,%s,%s,%s,%s,%s,%s) "
            "ON DUPLICATE KEY UPDATE "
            "email=VALUES(email), "
            "password_hash=VALUES(password_hash), "
            "avatar_url=VALUES(avatar_url), "
            "bio=VALUES(bio), "
            "role=VALUES(role), "
            "created_at=VALUES(created_at)"
        )

        with connection.cursor() as cursor:
            cursor.executemany(sql, rows)
            cursor.execute("SELECT COUNT(*) FROM users")
            users_count = cursor.fetchone()[0]

        self.stdout.write(f"inserted_or_updated={len(rows)} users_count={users_count}")

