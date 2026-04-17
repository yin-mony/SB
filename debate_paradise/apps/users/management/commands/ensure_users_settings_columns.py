from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = "Ensure users settings columns exist (auto_debate_mode, hide_win_rate). MySQL only."

    def handle(self, *args, **options):
        if connection.vendor != "mysql":
            self.stderr.write(self.style.ERROR("当前不是 MySQL 连接，无法修改 users 表。"))
            self.stderr.write(self.style.WARNING(f"connection.vendor={connection.vendor}"))
            return

        want = {
            "auto_debate_mode": "TINYINT(1) NOT NULL DEFAULT 0",
            "hide_win_rate": "TINYINT(1) NOT NULL DEFAULT 0",
        }

        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT COLUMN_NAME
                FROM information_schema.COLUMNS
                WHERE TABLE_SCHEMA=DATABASE() AND TABLE_NAME='users'
                """.strip()
            )
            existing = {r[0] for r in cursor.fetchall()}

            missing = [name for name in want.keys() if name not in existing]
            if not missing:
                self.stdout.write(self.style.SUCCESS("users 设置字段已存在，无需修改。"))
                return

            parts = [f"ADD COLUMN {name} {want[name]}" for name in missing]
            sql = f"ALTER TABLE users {', '.join(parts)}"
            cursor.execute(sql)

        self.stdout.write(self.style.SUCCESS(f"已添加 users 设置字段: {', '.join(missing)}"))

