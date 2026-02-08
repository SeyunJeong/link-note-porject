from supabase import create_client, Client
from app.core.config import settings
from typing import Optional
import uuid
from datetime import datetime


class DatabaseService:
    def __init__(self):
        self._client: Optional[Client] = None

    @property
    def client(self) -> Client:
        if self._client is None:
            # service key가 있으면 사용 (RLS 우회), 없으면 anon key 사용
            key = settings.SUPABASE_SERVICE_KEY or settings.SUPABASE_KEY
            self._client = create_client(settings.SUPABASE_URL, key)
        return self._client

    async def save_link(
        self,
        url: str,
        title: str,
        thumbnail: Optional[str],
        summary: str,
        tags: list[str],
        category: str,
        user_id: str,
    ) -> dict:
        data = {
            'id': str(uuid.uuid4()),
            'url': url,
            'title': title,
            'thumbnail': thumbnail,
            'summary': summary,
            'tags': tags,
            'category': category,
            'user_id': user_id,
            'created_at': datetime.utcnow().isoformat(),
        }

        result = self.client.table('links').insert(data).execute()
        return result.data[0] if result.data else data

    async def get_links(self, user_id: str, limit: int = 50, offset: int = 0) -> list[dict]:
        result = (
            self.client.table('links')
            .select('*')
            .eq('user_id', user_id)
            .order('created_at', desc=True)
            .range(offset, offset + limit - 1)
            .execute()
        )
        return result.data

    async def get_link_by_id(self, link_id: str, user_id: str) -> Optional[dict]:
        result = (
            self.client.table('links')
            .select('*')
            .eq('id', link_id)
            .eq('user_id', user_id)
            .execute()
        )
        return result.data[0] if result.data else None

    async def get_link_by_url(self, url: str, user_id: str) -> Optional[dict]:
        """URL로 링크 조회 (사용자별 중복 체크용)"""
        result = (
            self.client.table('links')
            .select('*')
            .eq('url', url)
            .eq('user_id', user_id)
            .execute()
        )
        return result.data[0] if result.data else None

    async def get_links_count(self, user_id: str) -> int:
        result = (
            self.client.table('links')
            .select('id', count='exact')
            .eq('user_id', user_id)
            .execute()
        )
        return result.count or 0

    async def delete_link(self, link_id: str, user_id: str) -> bool:
        result = (
            self.client.table('links')
            .delete()
            .eq('id', link_id)
            .eq('user_id', user_id)
            .execute()
        )
        return len(result.data) > 0


db_service = DatabaseService()
