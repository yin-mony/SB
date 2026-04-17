import os

from .base import *

DEBUG = False

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = os.environ.get("DJANGO_SECURE_SSL_REDIRECT") == "1"
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# 无 HTTPS 的临时部署（如仅内网 IP）：设 DJANGO_INSECURE_COOKIES=1，避免浏览器拒收 Secure Cookie
if os.environ.get("DJANGO_INSECURE_COOKIES") == "1":
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False

# 容器或挂载卷中的 SQLite 路径（持久化数据库文件）
_sqlite_path = os.environ.get("DJANGO_SQLITE_PATH", "").strip()
if _sqlite_path and not USE_MYSQL:
    DATABASES["default"]["NAME"] = _sqlite_path

# 前后端不同域时，逗号分隔源站，例如 https://app.example.com,https://www.example.com
_cors = os.environ.get("DJANGO_CORS_ALLOWED_ORIGINS", "").strip()
if _cors:
    CORS_ALLOWED_ORIGINS = [o.strip() for o in _cors.split(",") if o.strip()]
