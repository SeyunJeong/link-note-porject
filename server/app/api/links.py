import uuid

from typing import Optional
from fastapi import APIRouter, HTTPException, Depends, Query, Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from app.models.link import LinkCreate, LinkResponse, LinkListResponse
from app.services.youtube import youtube_service
from app.services.ai import ai_service
from app.services.database import db_service
from app.services.platform import detect_media_type
from app.services.metadata import MetadataExtractorFactory
from app.core.auth import get_current_user
from app.core.logging import get_logger

limiter = Limiter(key_func=get_remote_address)

logger = get_logger("api.links")

router = APIRouter(prefix="/links", tags=["links"])

metadata_factory = MetadataExtractorFactory()


@router.post("/save", response_model=LinkResponse)
@limiter.limit("30/minute")
async def save_link(request: Request, link: LinkCreate, user_id: str = Depends(get_current_user)):
    url = link.url.strip()

    # 1. 매체 타입 감지
    media_type = detect_media_type(url)

    # 2. URL 정규화 (YouTube만 정규화 적용)
    normalized_url = url
    if media_type == "youtube" and youtube_service.is_youtube_url(url):
        normalized_url = youtube_service.normalize_youtube_url(url)

    # 3. 중복 체크 (사용자별)
    existing = await db_service.get_link_by_url(normalized_url, user_id)
    if existing:
        raise HTTPException(
            status_code=409,
            detail="이미 저장된 링크입니다.",
            headers={"X-Existing-Link-Id": existing['id']}
        )

    # 4. 메타데이터 추출 (팩토리 패턴)
    try:
        metadata = metadata_factory.extract(normalized_url)
        title = metadata.title or normalized_url
        description = metadata.description or ""
        thumbnail = metadata.thumbnail
    except Exception as e:
        logger.warning(f"메타데이터 추출 실패, URL을 제목으로 사용: {e}")
        title = normalized_url
        description = ""
        thumbnail = None

    # 5. AI 요약/태그/카테고리
    summary = await ai_service.generate_summary(title, description)
    tags = await ai_service.generate_tags(title, description)
    category = await ai_service.categorize(title, description)

    # 6. 저장
    saved_link = await db_service.save_link(
        url=normalized_url,
        title=title,
        thumbnail=thumbnail,
        summary=summary,
        tags=tags,
        category=category,
        user_id=user_id,
        media_type=media_type,
    )

    return LinkResponse(**saved_link)


@router.get("/", response_model=LinkListResponse)
@limiter.limit("60/minute")
async def get_links(
    request: Request,
    limit: int = 50,
    offset: int = 0,
    media_type: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    user_id: str = Depends(get_current_user),
):
    links = await db_service.get_links(
        user_id, limit=limit, offset=offset,
        media_type=media_type, category=category,
    )
    total = await db_service.get_links_count(user_id, media_type=media_type, category=category)

    return LinkListResponse(
        links=[LinkResponse(**link) for link in links],
        total=total,
    )


@router.get("/{link_id}", response_model=LinkResponse)
@limiter.limit("60/minute")
async def get_link(request: Request, link_id: str, user_id: str = Depends(get_current_user)):
    link = await db_service.get_link_by_id(link_id, user_id)
    if not link:
        raise HTTPException(status_code=404, detail="링크를 찾을 수 없습니다.")

    return LinkResponse(**link)


@router.delete("/{link_id}")
@limiter.limit("30/minute")
async def delete_link(request: Request, link_id: str, user_id: str = Depends(get_current_user)):
    # 0. UUID 형식 검증
    try:
        uuid.UUID(link_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="유효하지 않은 링크 ID 형식입니다.")

    # 1. 링크 존재 확인 (사용자 소유 확인 포함)
    link = await db_service.get_link_by_id(link_id, user_id)
    if not link:
        raise HTTPException(status_code=404, detail="링크를 찾을 수 없습니다.")

    # 2. 삭제 실행
    success = await db_service.delete_link(link_id, user_id)
    if not success:
        raise HTTPException(status_code=500, detail="삭제에 실패했습니다.")

    logger.info(f"링크 삭제 완료: {link_id} (user: {user_id})")
    return {"message": "삭제되었습니다.", "id": link_id}
