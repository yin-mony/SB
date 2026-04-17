from django.conf import settings
from django.db import models


class Badge(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(null=True, blank=True)
    icon = models.CharField(max_length=50, default="🏅")
    condition_json = models.JSONField()
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "badges"


class UserBadge(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, db_column="user_id")
    badge = models.ForeignKey(Badge, on_delete=models.DO_NOTHING, db_column="badge_id")
    awarded_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "user_badges"
        unique_together = (("user", "badge"),)


class Favorite(models.Model):
    class TargetType(models.TextChoices):
        TOPIC = "topic"
        BLOG_POST = "blog_post"
        DEBATE_POST = "debate_post"

    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, db_column="user_id")
    target_type = models.CharField(max_length=20, choices=TargetType.choices)
    target_id = models.BigIntegerField()
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "favorites"
        unique_together = (("user", "target_type", "target_id"),)

class ActivityLog(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, db_column="user_id")
    action_type = models.CharField(max_length=30)
    target_type = models.CharField(max_length=20, null=True, blank=True)
    target_id = models.BigIntegerField(null=True, blank=True)
    data = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "activity_logs"
