from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    use_in_migrations = False

    def create_user(self, username, email=None, password=None, **extra_fields):
        if not username:
            raise ValueError("username is required")
        if not email:
            raise ValueError("email is required")
        user = self.model(username=username, email=email, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("role", User.Role.ADMIN)
        user = self.create_user(username=username, email=email, password=password, **extra_fields)
        return user


class User(AbstractBaseUser):
    class Role(models.TextChoices):
        USER = "user"
        MODERATOR = "moderator"
        ADMIN = "admin"

    id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=255, db_column="password_hash")
    avatar_url = models.CharField(max_length=500, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    auto_debate_mode = models.BooleanField(default=False)
    hide_win_rate = models.BooleanField(default=False)
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.USER)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(null=True, blank=True, db_column="last_login_at")

    objects = UserManager()

    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["email"]

    class Meta:
        managed = False
        db_table = "users"

    @property
    def is_staff(self):
        return self.role in {self.Role.MODERATOR, self.Role.ADMIN}

    @property
    def is_superuser(self):
        return self.role == self.Role.ADMIN

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    def __str__(self):
        return self.username


class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.DO_NOTHING, db_column="follower_id", related_name="following_rel")
    followee = models.ForeignKey(User, on_delete=models.DO_NOTHING, db_column="followee_id", related_name="follower_rel")
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "follows"
        unique_together = (("follower", "followee"),)
