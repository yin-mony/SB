from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = "Seed test user badges into `user_badges` table"

    def handle(self, *args, **options):
        rows = [
            (1, 1),
            (1, 2),
            (2, 1),
            (3, 2),
            (4, 4),
            (4, 5),
        ]

        sql = (
            "INSERT INTO user_badges (user_id,badge_id,awarded_at) "
            "VALUES (%s,%s,NOW()) "
            "ON DUPLICATE KEY UPDATE awarded_at=awarded_at"
        )

        with connection.cursor() as cursor:
            cursor.executemany(sql, rows)
            cursor.execute("SELECT COUNT(*) FROM user_badges")
            user_badges_count = cursor.fetchone()[0]

        self.stdout.write(f"inserted_or_ignored={len(rows)} user_badges_count={user_badges_count}")

