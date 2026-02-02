from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.api.links import router as links_router
from app.core.logging import setup_logging, get_logger
from app.core.exceptions import LinkNoteException, DuplicateError

# 로깅 초기화
setup_logging()
logger = get_logger("main")

app = FastAPI(
    title="LinkNote API",
    description="링크 저장 및 요약 API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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


# 요청 로깅 미들웨어
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url.path}")
    response = await call_next(request)
    logger.info(f"Response: {request.method} {request.url.path} - {response.status_code}")
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
