from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = "Seed test follows into `follows` table"

    def handle(self, *args, **options):
        rows = [
            (1, 2),
            (1, 4),
            (2, 1),
            (2, 3),
            (3, 1),
            (3, 2),
            (3, 4),
            (4, 1),
            (4, 2),
            (5, 1),
            (5, 4),
        ]

        sql = (
            "INSERT INTO follows (follower_id,followee_id,created_at) "
            "VALUES (%s,%s,NOW()) "
            "ON DUPLICATE KEY UPDATE created_at=created_at"
        )

        with connection.cursor() as cursor:
            cursor.executemany(sql, rows)
            cursor.execute("SELECT COUNT(*) FROM follows")
            follows_count = cursor.fetchone()[0]

        self.stdout.write(f"inserted_or_ignored={len(rows)} follows_count={follows_count}")

