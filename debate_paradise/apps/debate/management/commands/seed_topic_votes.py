from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = "Seed test topic votes into `topic_votes` table"

    def handle(self, *args, **options):
        rows = []

        rows += [(1, 1, "A"), (1, 2, "B"), (1, 3, "A"), (1, 4, "A"), (1, 5, "B")]
        rows += [(2, 1, "B"), (2, 2, "A"), (2, 3, "A"), (2, 4, "B"), (2, 5, "A")]
        rows += [(3, 1, "A"), (3, 2, "A"), (3, 3, "B"), (3, 4, "B"), (3, 5, "A")]
        rows += [(4, 1, "B"), (4, 2, "A"), (4, 3, "B"), (4, 4, "A"), (4, 5, "B")]
        rows += [(5, 1, "A"), (5, 2, "A"), (5, 3, "B"), (5, 4, "A"), (5, 5, "B")]

        sql = "INSERT INTO topic_votes (topic_id,user_id,side,created_at) VALUES (%s,%s,%s,NOW())"

        with connection.cursor() as cursor:
            cursor.executemany(sql, rows)
            cursor.execute("SELECT COUNT(*) FROM topic_votes")
            votes_count = cursor.fetchone()[0]

        self.stdout.write(f"inserted={len(rows)} topic_votes_count={votes_count}")

