import uuid

from fastapi import APIRouter, HTTPException
from app.models.link import LinkCreate, LinkResponse, LinkListResponse
from app.services.youtube import youtube_service
from app.services.ai import ai_service
from app.services.database import db_service
from app.core.exceptions import YouTubeExtractionError
from app.core.logging import get_logger

logger = get_logger("api.links")

router = APIRouter(prefix="/links", tags=["links"])


@router.post("/save", response_model=LinkResponse)
async def save_link(link: LinkCreate):
    url = link.url.strip()

    if not youtube_service.is_youtube_url(url):
        raise HTTPException(status_code=400, detail="현재는 유튜브 링크만 지원합니다.")

    # 1. URL 정규화
    normalized_url = youtube_service.normalize_youtube_url(url)

    # 2. 중복 체크
    existing = await db_service.get_link_by_url(normalized_url)
    if existing:
        raise HTTPException(
            status_code=409,
            detail="이미 저장된 링크입니다.",
            headers={"X-Existing-Link-Id": existing['id']}
        )

    try:
        metadata = youtube_service.extract_metadata(normalized_url)
    except YouTubeExtractionError as e:
        raise HTTPException(status_code=400, detail=e.message)

    if not metadata:
        raise HTTPException(status_code=400, detail="링크 정보를 가져올 수 없습니다.")

    title = metadata['title']
    description = metadata['description']

    summary = await ai_service.generate_summary(title, description)
    tags = await ai_service.generate_tags(title, description)
    category = await ai_service.categorize(title, description)

    saved_link = await db_service.save_link(
        url=normalized_url,
        title=title,
        thumbnail=metadata['thumbnail'],
        summary=summary,
        tags=tags,
        category=category,
    )

    return LinkResponse(**saved_link)


@router.get("/", response_model=LinkListResponse)
async def get_links(limit: int = 50, offset: int = 0):
    links = await db_service.get_links(limit=limit, offset=offset)
    total = await db_service.get_links_count()

    return LinkListResponse(
        links=[LinkResponse(**link) for link in links],
        total=total,
    )


@router.get("/{link_id}", response_model=LinkResponse)
async def get_link(link_id: str):
    link = await db_service.get_link_by_id(link_id)
    if not link:
        raise HTTPException(status_code=404, detail="링크를 찾을 수 없습니다.")

    return LinkResponse(**link)


@router.delete("/{link_id}")
async def delete_link(link_id: str):
    # 0. UUID 형식 검증
    try:
        uuid.UUID(link_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="유효하지 않은 링크 ID 형식입니다.")

    # 1. 링크 존재 확인
    link = await db_service.get_link_by_id(link_id)
    if not link:
        raise HTTPException(status_code=404, detail="링크를 찾을 수 없습니다.")

    # 2. 삭제 실행
    success = await db_service.delete_link(link_id)
    if not success:
        raise HTTPException(status_code=500, detail="삭제에 실패했습니다.")

    logger.info(f"링크 삭제 완료: {link_id}")
    return {"message": "삭제되었습니다.", "id": link_id}
