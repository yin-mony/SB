from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = "Ensure users.id is AUTO_INCREMENT (MySQL only)."

    def handle(self, *args, **options):
        self.stdout.write("检查 users.id AUTO_INCREMENT ...")
        if connection.vendor != "mysql":
            self.stderr.write(self.style.ERROR("当前不是 MySQL 连接，无法修改 users 表。"))
            self.stderr.write(self.style.WARNING(f"connection.vendor={connection.vendor}"))
            return

        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT COLUMN_TYPE, IS_NULLABLE, COLUMN_KEY, EXTRA
                FROM information_schema.COLUMNS
                WHERE TABLE_SCHEMA=DATABASE()
                  AND TABLE_NAME='users'
                  AND COLUMN_NAME='id'
                """.strip()
            )
            row = cursor.fetchone()

            if not row:
                self.stderr.write(self.style.ERROR("未找到 users.id 字段，请确认当前连接的数据库是否正确。"))
                return

            column_type, is_nullable, column_key, extra = row
            extra = extra or ""
            if "auto_increment" in extra.lower():
                self.stdout.write(self.style.SUCCESS("users.id 已是 AUTO_INCREMENT，无需修改。"))
                return

            cursor.execute(
                """
                SELECT COUNT(*) FROM information_schema.KEY_COLUMN_USAGE
                WHERE TABLE_SCHEMA=DATABASE()
                  AND TABLE_NAME='users'
                  AND CONSTRAINT_NAME='PRIMARY'
                  AND COLUMN_NAME='id'
                """.strip()
            )
            has_pk = bool(cursor.fetchone()[0])

            cursor.execute("SELECT COUNT(*) - COUNT(DISTINCT id) FROM users")
            dup_count = int(cursor.fetchone()[0] or 0)
            cursor.execute("SELECT COUNT(*) FROM users WHERE id IS NULL")
            null_count = int(cursor.fetchone()[0] or 0)

            if dup_count > 0 or null_count > 0:
                self.stderr.write(self.style.ERROR("users.id 存在重复或 NULL，无法安全设置为 AUTO_INCREMENT。"))
                self.stderr.write(self.style.WARNING(f"duplicate_ids={dup_count}, null_ids={null_count}"))
                return

            if not has_pk:
                cursor.execute("ALTER TABLE users ADD PRIMARY KEY (id)")
                self.stdout.write(self.style.SUCCESS("已为 users.id 补齐 PRIMARY KEY。"))

            cursor.execute(f"ALTER TABLE users MODIFY COLUMN id {column_type} NOT NULL AUTO_INCREMENT")
            cursor.execute("SELECT IFNULL(MAX(id),0)+1 FROM users")
            next_id = int(cursor.fetchone()[0] or 1)
            cursor.execute(f"ALTER TABLE users AUTO_INCREMENT = {next_id}")

        self.stdout.write(self.style.SUCCESS(f"已设置 users.id 为 AUTO_INCREMENT（next={next_id}）。"))

