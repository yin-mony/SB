import base64
import secrets
from string import ascii_uppercase, digits

from django.conf import settings
from django.core.cache import cache


def _ttl() -> int:
    return int(getattr(settings, "CAPTCHA_TTL_SECONDS", 300))


def _code_len() -> int:
    return int(getattr(settings, "CAPTCHA_CODE_LENGTH", 4))


def _captcha_key(captcha_id: str) -> str:
    return f"captcha:{captcha_id}"


def generate_code() -> str:
    alphabet = digits + ascii_uppercase
    n = max(4, min(_code_len(), 8))
    return "".join(secrets.choice(alphabet) for _ in range(n))


def _svg(code: str) -> str:
    # 轻量 SVG：不依赖 Pillow，前端直接 <img :src> 即可
    w, h = 140, 44
    jitter = [secrets.randbelow(9) - 4 for _ in range(len(code))]
    xs = [18 + i * 28 for i in range(len(code))]
    ys = [30 + j for j in jitter]
    lines = []
    for _ in range(6):
        x1, y1 = secrets.randbelow(w), secrets.randbelow(h)
        x2, y2 = secrets.randbelow(w), secrets.randbelow(h)
        sw = 1 + secrets.randbelow(2)
        opacity = 0.15 + secrets.randbelow(30) / 100
        lines.append(
            f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
            f'stroke="black" stroke-width="{sw}" opacity="{opacity:.2f}" />'
        )
    chars = []
    for i, ch in enumerate(code):
        rot = secrets.randbelow(31) - 15
        chars.append(
            f'<text x="{xs[i]}" y="{ys[i]}" font-size="26" font-weight="900" '
            f'font-family="Arial, sans-serif" transform="rotate({rot} {xs[i]} {ys[i]})">{ch}</text>'
        )
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
        f'<rect x="0" y="0" width="{w}" height="{h}" rx="12" ry="12" fill="#fff" stroke="#000" stroke-width="4"/>'
        f'{"".join(lines)}'
        f'{"".join(chars)}'
        "</svg>"
    )


def issue_captcha() -> dict:
    captcha_id = secrets.token_urlsafe(16)
    code = generate_code()
    cache.set(_captcha_key(captcha_id), code, timeout=_ttl())
    svg = _svg(code)
    b64 = base64.b64encode(svg.encode("utf-8")).decode("ascii")
    return {"captcha_id": captcha_id, "image": f"data:image/svg+xml;base64,{b64}"}


def verify_captcha(captcha_id: str, user_input: str) -> bool:
    if not captcha_id:
        return False
    expected = cache.get(_captcha_key(captcha_id))
    if not expected:
        return False
    inp = (user_input or "").strip().upper()
    exp = str(expected).strip().upper()
    return secrets.compare_digest(inp, exp)


def consume_captcha(captcha_id: str) -> None:
    if captcha_id:
        cache.delete(_captcha_key(captcha_id))

