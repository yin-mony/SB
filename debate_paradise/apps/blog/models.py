from django.conf import settings
from django.db import models


class BlogPost(models.Model):
    id = models.BigAutoField(primary_key=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, db_column="author_id")
    title = models.CharField(max_length=200)
    slug = models.CharField(max_length=200, unique=True)
    cover_image = models.CharField(max_length=500, null=True, blank=True)
    content = models.TextField()
    excerpt = models.CharField(max_length=500, null=True, blank=True)
    category = models.CharField(max_length=50, default="逻辑体操")
    tags = models.JSONField(null=True, blank=True)
    view_count = models.PositiveIntegerField(default=0)
    like_count = models.PositiveIntegerField(default=0)
    comment_count = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "blog_posts"


class BlogComment(models.Model):
    id = models.BigAutoField(primary_key=True)
    post = models.ForeignKey(BlogPost, on_delete=models.DO_NOTHING, db_column="post_id")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, db_column="user_id")
    parent = models.ForeignKey("self", on_delete=models.DO_NOTHING, db_column="parent_id", null=True, blank=True)
    content = models.TextField()
    upvotes = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "blog_comments"

