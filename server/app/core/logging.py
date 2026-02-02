import logging
import sys
from typing import Optional


def setup_logging(level: str = "INFO") -> logging.Logger:
    """애플리케이션 로깅 설정"""
    log_level = getattr(logging, level.upper(), logging.INFO)

    # 기본 포맷 설정
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # 스트림 핸들러 (콘솔 출력)
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)

    # 루트 로거 설정
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # 기존 핸들러 제거 (중복 방지)
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    root_logger.addHandler(stream_handler)

    # 애플리케이션 로거 반환
    return logging.getLogger("linknote")


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """모듈별 로거 반환"""
    if name:
        return logging.getLogger(f"linknote.{name}")
    return logging.getLogger("linknote")


# 기본 로거 초기화
logger = setup_logging()
