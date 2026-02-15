"""OpenGraph 메타태그 기반 메타데이터 추출기 (Threads, 일반 웹, fallback)"""

import httpx
from bs4 import BeautifulSoup
from app.core.logging import get_logger
from .base import ContentMetadata, MetadataExtractor

logger = get_logger("metadata.opengraph")


class OpenGraphExtractor(MetadataExtractor):
    """OpenGraph 메타태그를 파싱하는 범용 추출기"""

    def __init__(self):
        self.timeout = 15.0
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; LinkNoteBot/1.0)',
            'Accept': 'text/html,application/xhtml+xml',
            'Accept-Language': 'ko-KR,ko;q=0.9,en;q=0.8',
        }

    def can_handle(self, url: str) -> bool:
        # 모든 URL을 처리할 수 있는 fallback 추출기
        return True

    def extract(self, url: str) -> ContentMetadata:
        logger.info(f"OpenGraph extracting: {url[:80]}")

        try:
            with httpx.Client(timeout=self.timeout, follow_redirects=True) as client:
                response = client.get(url, headers=self.headers)
                response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            return self._parse_og_tags(soup, url)

        except Exception as e:
            logger.warning(f"OpenGraph extraction failed: {url[:60]} - {e}")
            # 실패해도 URL 기반 기본 메타데이터 반환
            return ContentMetadata(title=url, platform="web")

    def _parse_og_tags(self, soup: BeautifulSoup, url: str) -> ContentMetadata:
        def get_og(prop: str) -> str:
            tag = soup.find('meta', property=f'og:{prop}')
            if tag and tag.get('content'):
                return tag['content'].strip()
            return ""

        title = get_og('title') or self._get_title(soup) or url
        description = get_og('description') or self._get_description(soup)
        thumbnail = get_og('image') or None
        site_name = get_og('site_name')
        author = site_name or None

        return ContentMetadata(
            title=title,
            description=description,
            thumbnail=thumbnail,
            platform="web",
            author=author,
        )

    def _get_title(self, soup: BeautifulSoup) -> str:
        title_tag = soup.find('title')
        return title_tag.get_text(strip=True) if title_tag else ""

    def _get_description(self, soup: BeautifulSoup) -> str:
        meta = soup.find('meta', attrs={'name': 'description'})
        if meta and meta.get('content'):
            return meta['content'].strip()
        return ""
