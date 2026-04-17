from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = "Seed test favorites into `favorites` table"

    def handle(self, *args, **options):
        rows = [
            (1, "topic", 2),
            (1, "blog_post", 1),
            (2, "topic", 1),
            (2, "blog_post", 2),
            (3, "topic", 3),
            (4, "debate_post", 1),
            (5, "blog_post", 3),
        ]

        sql = (
            "INSERT INTO favorites (user_id,target_type,target_id,created_at) "
            "VALUES (%s,%s,%s,NOW()) "
            "ON DUPLICATE KEY UPDATE created_at=created_at"
        )

        with connection.cursor() as cursor:
            cursor.executemany(sql, rows)
            cursor.execute("SELECT COUNT(*) FROM favorites")
            favorites_count = cursor.fetchone()[0]

        self.stdout.write(f"inserted_or_ignored={len(rows)} favorites_count={favorites_count}")

