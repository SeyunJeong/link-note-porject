import os
import time

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from app.api.links import router as links_router
from app.core.logging import setup_logging, get_logger
from app.core.exceptions import LinkNoteException, DuplicateError, AuthenticationError

# 로깅 초기화
setup_logging()
logger = get_logger("main")

# Rate limiter 설정
limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="LinkNote API",
    description="링크 저장 및 요약 API",
    version="1.0.0",
)

# Rate limiter를 app state에 등록
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS 설정
# Production에서는 환경변수 ALLOWED_ORIGINS에 허용할 도메인을 콤마로 구분하여 설정
# 예: ALLOWED_ORIGINS=https://linknote.app,https://www.linknote.app
# 미설정 시 ["*"]로 동작 (개발 호환성 유지)
allowed_origins = os.environ.get("ALLOWED_ORIGINS", "*").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 인증 예외 핸들러
@app.exception_handler(AuthenticationError)
async def authentication_exception_handler(request: Request, exc: AuthenticationError):
    return JSONResponse(
        status_code=401,
        content={
            "detail": exc.message,
            "type": exc.error_type
        },
        headers={"WWW-Authenticate": "Bearer"}
    )


# 전역 예외 핸들러
@app.exception_handler(LinkNoteException)
async def linknote_exception_handler(request: Request, exc: LinkNoteException):
    logger.error(f"LinkNoteException: {exc.error_type} - {exc.message}")
    response_content = {
        "detail": exc.message,
        "type": exc.error_type
    }

    # DuplicateError인 경우 기존 ID 포함
    if isinstance(exc, DuplicateError) and exc.existing_id:
        response_content["existing_id"] = exc.existing_id

    return JSONResponse(
        status_code=exc.status_code,
        content=response_content
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.exception(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "detail": "서버 내부 오류가 발생했습니다.",
            "type": "internal_error"
        }
    )


# 요청 로깅 미들웨어 (timestamp, method, path, status_code, response_time)
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration_ms = (time.time() - start_time) * 1000
    logger.info(
        f"{request.method} {request.url.path} "
        f"status={response.status_code} "
        f"duration={duration_ms:.1f}ms"
    )
    return response


app.include_router(links_router, prefix="/api")


@app.get("/")
async def root():
    return {"message": "LinkNote API is running"}


@app.get("/health")
async def health():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    logger.info("Starting LinkNote API server...")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
