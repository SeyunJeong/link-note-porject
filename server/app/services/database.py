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
            self._client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
        return self._client

    async def save_link(
        self,
        url: str,
        title: str,
        thumbnail: Optional[str],
        summary: str,
        tags: list[str],
        category: str,
    ) -> dict:
        data = {
            'id': str(uuid.uuid4()),
            'url': url,
            'title': title,
            'thumbnail': thumbnail,
            'summary': summary,
            'tags': tags,
            'category': category,
            'created_at': datetime.utcnow().isoformat(),
        }

        result = self.client.table('links').insert(data).execute()
        return result.data[0] if result.data else data

    async def get_links(self, limit: int = 50, offset: int = 0) -> list[dict]:
        result = self.client.table('links').select('*').order('created_at', desc=True).range(offset, offset + limit - 1).execute()
        return result.data

    async def get_link_by_id(self, link_id: str) -> Optional[dict]:
        result = self.client.table('links').select('*').eq('id', link_id).execute()
        return result.data[0] if result.data else None

    async def get_links_count(self) -> int:
        result = self.client.table('links').select('id', count='exact').execute()
        return result.count or 0

    async def delete_link(self, link_id: str) -> bool:
        result = self.client.table('links').delete().eq('id', link_id).execute()
        return len(result.data) > 0


db_service = DatabaseService()
