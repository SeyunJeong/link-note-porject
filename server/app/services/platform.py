"""URL 도메인 기반 매체(media_type) 감지 모듈"""

from urllib.parse import urlparse

# 도메인 → media_type 매핑
DOMAIN_PATTERNS: dict[str, list[str]] = {
    "youtube": ["youtube.com", "youtu.be", "youtube-nocookie.com"],
    "instagram": ["instagram.com", "instagr.am"],
    "threads": ["threads.net"],
    "x": ["x.com", "twitter.com"],
    "tiktok": ["tiktok.com"],
}

VALID_MEDIA_TYPES = ["youtube", "instagram", "threads", "x", "tiktok", "web"]


def detect_media_type(url: str) -> str:
    """URL에서 도메인을 추출하여 media_type을 반환한다.

    Returns:
        youtube | instagram | threads | x | tiktok | web
    """
    try:
        hostname = urlparse(url).hostname or ""
        hostname = hostname.lower().removeprefix("www.")

        for media_type, domains in DOMAIN_PATTERNS.items():
            for domain in domains:
                if hostname == domain or hostname.endswith(f".{domain}"):
                    return media_type

        return "web"
    except Exception:
        return "web"
