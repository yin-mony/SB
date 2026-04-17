import logging
import os
from uuid import uuid4

from django.conf import settings
from django.db import IntegrityError
from django.utils.text import get_valid_filename
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from apps.core.responses import fail, ok

from .captcha import issue_captcha, consume_captcha
from .serializers import (
    LoginSerializer,
    PasswordResetConfirmSerializer,
    ProfileSerializer,
    ProfileUpdateSerializer,
    RegisterSerializer,
)
from .models import User

logger = logging.getLogger(__name__)


class CaptchaView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # purpose 仅用于前端区分文案；后端不做差异化存储
        _ = (request.data.get("purpose") or "").strip()
        return ok(data=issue_captcha())


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return fail(msg="参数错误", data=serializer.errors, code=400)
        try:
            user = serializer.save()
        except IntegrityError:
            return fail(msg="用户名已存在", code=400, data={"username": ["用户名已存在"]})
        token = RefreshToken.for_user(user)
        return ok(
            data={
                "user": ProfileSerializer(user).data,
                "token": {"access": str(token.access_token), "refresh": str(token)},
            }
        )


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return fail(msg="登录失败", data=serializer.errors, code=400)
        user = serializer.validated_data["user"]
        token = RefreshToken.for_user(user)
        return ok(
            data={
                "user": ProfileSerializer(user).data,
                "token": {"access": str(token.access_token), "refresh": str(token)},
            }
        )


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        return ok(data={})


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return ok(data=ProfileSerializer(request.user).data)

    def patch(self, request):
        serializer = ProfileUpdateSerializer(instance=request.user, data=request.data, partial=True)
        if not serializer.is_valid():
            return fail(msg="参数错误", data=serializer.errors, code=400)
        serializer.save()
        return ok(data=ProfileSerializer(request.user).data)


class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if not serializer.is_valid():
            return fail(msg="参数错误", data=serializer.errors, code=400)

        username = serializer.validated_data["username"]
        new_password = serializer.validated_data["new_password"]
        captcha_id = serializer.validated_data.get("captcha_id") or ""
        user = User.objects.filter(username__iexact=username).first()
        if not user or not user.is_active:
            consume_captcha(captcha_id)
            return fail(
                msg="该用户名不存在或账号已停用",
                code=400,
                data={"username": ["请确认用户名是否正确"]},
            )

        user.set_password(new_password)
        user.save(update_fields=["password"])
        consume_captcha(captcha_id)
        return ok(data={})


class AvatarUploadView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        f = request.FILES.get("file")
        if not f:
            return fail(msg="参数错误", code=400, data={"file": ["缺少文件"]})

        content_type = (getattr(f, "content_type", "") or "").lower()
        if content_type not in {"image/png", "image/jpeg", "image/jpg", "image/webp", "image/gif"}:
            return fail(msg="文件类型不支持", code=400, data={"file": ["仅支持 png/jpg/webp/gif"]})

        if f.size and f.size > 2 * 1024 * 1024:
            return fail(msg="文件过大", code=400, data={"file": ["最大 2MB"]})

        ext = os.path.splitext(f.name or "")[1].lower()
        if ext not in {".png", ".jpg", ".jpeg", ".webp", ".gif"}:
            ext = ".png"

        filename = get_valid_filename(f"{uuid4().hex}{ext}")
        project_root = os.path.dirname(str(settings.BASE_DIR))
        frontend_public_dir = os.path.join(project_root, "frontend", "public")
        rel_dir = os.path.join("uploads", "avatars", f"user_{request.user.id}")
        abs_dir = os.path.join(frontend_public_dir, rel_dir)
        os.makedirs(abs_dir, exist_ok=True)
        abs_path = os.path.join(abs_dir, filename)

        with open(abs_path, "wb") as dst:
            for chunk in f.chunks():
                dst.write(chunk)

        avatar_url = f"/{rel_dir.replace(os.sep,'/')}/{filename}"
        request.user.avatar_url = avatar_url
        request.user.save(update_fields=["avatar_url"])

        return ok(data={"avatar_url": avatar_url})

