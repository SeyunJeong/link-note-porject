"""메타데이터 추출기 기본 클래스 및 데이터 모델"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ContentMetadata:
    """플랫폼 무관 콘텐츠 메타데이터"""
    title: str = ""
    description: str = ""
    thumbnail: Optional[str] = None
    platform: str = "web"
    duration: Optional[int] = None
    author: Optional[str] = None
    view_count: Optional[int] = None


class MetadataExtractor(ABC):
    """메타데이터 추출기 인터페이스"""

    @abstractmethod
    def can_handle(self, url: str) -> bool:
        """이 추출기가 해당 URL을 처리할 수 있는지 반환"""
        ...

    @abstractmethod
    def extract(self, url: str) -> ContentMetadata:
        """URL에서 메타데이터를 추출하여 반환"""
        ...
