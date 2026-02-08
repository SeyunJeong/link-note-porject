from typing import Optional


class LinkNoteException(Exception):
    """LinkNote 애플리케이션 기본 예외"""
    def __init__(
        self,
        message: str,
        status_code: int = 400,
        error_type: Optional[str] = None
    ):
        self.message = message
        self.status_code = status_code
        self.error_type = error_type or self.__class__.__name__
        super().__init__(self.message)


class YouTubeExtractionError(LinkNoteException):
    """YouTube 메타데이터 추출 실패"""
    def __init__(self, message: str, error_type: str = "youtube_error"):
        super().__init__(message, status_code=400, error_type=error_type)


class AIProcessingError(LinkNoteException):
    """AI 처리 실패"""
    def __init__(self, message: str, error_type: str = "ai_error"):
        super().__init__(message, status_code=500, error_type=error_type)


class DatabaseError(LinkNoteException):
    """데이터베이스 작업 실패"""
    def __init__(self, message: str, error_type: str = "database_error"):
        super().__init__(message, status_code=500, error_type=error_type)


class ValidationError(LinkNoteException):
    """입력 검증 실패"""
    def __init__(self, message: str, error_type: str = "validation_error"):
        super().__init__(message, status_code=400, error_type=error_type)


class NotFoundError(LinkNoteException):
    """리소스를 찾을 수 없음"""
    def __init__(self, message: str, error_type: str = "not_found"):
        super().__init__(message, status_code=404, error_type=error_type)


class DuplicateError(LinkNoteException):
    """중복 리소스"""
    def __init__(self, message: str, existing_id: Optional[str] = None):
        super().__init__(message, status_code=409, error_type="duplicate")
        self.existing_id = existing_id


class AuthenticationError(LinkNoteException):
    """인증 실패"""
    def __init__(self, message: str = "인증이 필요합니다.", error_type: str = "authentication_error"):
        super().__init__(message, status_code=401, error_type=error_type)
