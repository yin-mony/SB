import secrets

from django.contrib.auth.hashers import check_password
from django.db.models import Q
from rest_framework import serializers

from .captcha import consume_captcha, verify_captcha
from .models import User


def _check_raw_or_django_password(raw_password: str, stored_hash: str) -> bool:
    if stored_hash and stored_hash.startswith("$2"):
        try:
            import bcrypt
        except Exception:
            return False
        return bcrypt.checkpw(raw_password.encode("utf-8"), stored_hash.encode("utf-8"))
    return check_password(raw_password, stored_hash)


def _synthetic_email() -> str:
    """数据库 email 唯一且非空：占位邮箱，用户无需知晓。"""
    return f"u{secrets.token_hex(12)}@user.debate.local"


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(min_length=6, write_only=True)
    captcha_id = serializers.CharField()
    captcha = serializers.CharField(max_length=10)

    def validate_username(self, value):
        v = value.strip()
        if User.objects.filter(username__iexact=v).exists():
            raise serializers.ValidationError("用户名已存在")
        return v

    def validate(self, attrs):
        captcha_id = str(attrs.get("captcha_id") or "").strip()
        captcha = str(attrs.get("captcha") or "").strip()
        if not verify_captcha(captcha_id, captcha):
            raise serializers.ValidationError({"captcha": "验证码无效或已过期，请刷新后重试"})
        return attrs

    def create(self, validated_data):
        username = validated_data["username"].strip()
        captcha_id = str(validated_data.get("captcha_id") or "").strip()
        email = _synthetic_email()
        while User.objects.filter(email=email).exists():
            email = _synthetic_email()
        user = User(username=username, email=email, role=User.Role.USER, is_active=True)
        user.set_password(validated_data["password"])
        user.save()
        consume_captcha(captcha_id)
        return user


class LoginSerializer(serializers.Serializer):
    account = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        account = attrs["account"].strip()
        password = attrs["password"]
        al = account.lower()
        user = User.objects.filter(Q(username__iexact=account) | Q(email=al)).first()
        if not user:
            raise serializers.ValidationError({"account": "账号或密码错误"})
        if not user.is_active:
            raise serializers.ValidationError({"account": "账号已被禁用"})
        if not _check_raw_or_django_password(password, user.password):
            raise serializers.ValidationError({"account": "账号或密码错误"})
        attrs["user"] = user
        return attrs


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "avatar_url",
            "bio",
            "auto_debate_mode",
            "hide_win_rate",
            "role",
            "is_active",
            "created_at",
            "last_login",
        )
        read_only_fields = ("id", "role", "is_active", "created_at", "last_login")


class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email", "avatar_url", "bio", "auto_debate_mode", "hide_win_rate")

    def validate_username(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("用户名不能为空")
        qs = User.objects.filter(username__iexact=value).exclude(id=self.instance.id)
        if qs.exists():
            raise serializers.ValidationError("用户名已存在")
        return value

    def validate_email(self, value):
        value = value.strip().lower()
        qs = User.objects.filter(email=value).exclude(id=self.instance.id)
        if qs.exists():
            raise serializers.ValidationError("邮箱已存在")
        return value


class PasswordResetConfirmSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=50)
    captcha_id = serializers.CharField()
    captcha = serializers.CharField(max_length=10)
    new_password = serializers.CharField(min_length=6, write_only=True)

    def validate_username(self, value):
        return value.strip()

    def validate(self, attrs):
        captcha_id = str(attrs.get("captcha_id") or "").strip()
        captcha = str(attrs.get("captcha") or "").strip()
        if not verify_captcha(captcha_id, captcha):
            raise serializers.ValidationError({"captcha": "验证码无效或已过期"})
        return attrs
