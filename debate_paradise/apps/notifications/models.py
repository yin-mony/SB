from django.conf import settings
from django.db import models


class Notification(models.Model):
    id = models.BigAutoField(primary_key=True)
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, db_column="recipient_id")
    type = models.CharField(max_length=30)
    data = models.JSONField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "notifications"

