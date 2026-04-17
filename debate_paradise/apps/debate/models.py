from django.conf import settings
from django.db import models


class Topic(models.Model):
    class Status(models.TextChoices):
        OPEN = "open"
        CLOSED = "closed"
        ARCHIVED = "archived"

    id = models.BigAutoField(primary_key=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, db_column="creator_id")
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    category = models.CharField(max_length=50)
    format = models.CharField(max_length=30, default="快嘴乱斗")
    side_a_name = models.CharField(max_length=50, default="正方")
    side_b_name = models.CharField(max_length=50, default="反方")
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.OPEN)
    view_count = models.PositiveIntegerField(default=0)
    comment_count = models.PositiveIntegerField(default=0)
    hot_score = models.FloatField(default=0)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "topics"


class TopicVote(models.Model):
    class Side(models.TextChoices):
        A = "A"
        B = "B"

    id = models.BigAutoField(primary_key=True)
    topic = models.ForeignKey(Topic, on_delete=models.DO_NOTHING, db_column="topic_id")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, db_column="user_id")
    side = models.CharField(max_length=1, choices=Side.choices)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "topic_votes"
        unique_together = (("topic", "user"),)


class DebatePost(models.Model):
    class Side(models.TextChoices):
        A = "A"
        B = "B"

    id = models.BigAutoField(primary_key=True)
    topic = models.ForeignKey(Topic, on_delete=models.DO_NOTHING, db_column="topic_id")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, db_column="user_id")
    parent = models.ForeignKey("self", on_delete=models.DO_NOTHING, db_column="parent_id", null=True, blank=True)
    side = models.CharField(max_length=1, choices=Side.choices)
    content = models.TextField()
    evidence_url = models.CharField(max_length=500, null=True, blank=True)
    upvotes = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "debate_posts"

