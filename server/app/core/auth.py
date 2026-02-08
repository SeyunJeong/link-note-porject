import jwt
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.config import settings
from app.core.exceptions import AuthenticationError

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> str:
    """JWT 토큰에서 user_id를 추출하는 FastAPI Dependency"""
    token = credentials.credentials
    try:
        payload = jwt.decode(
            token,
            settings.SUPABASE_JWT_SECRET,
            algorithms=["HS256"],
            audience="authenticated",
        )
        user_id = payload.get("sub")
        if not user_id:
            raise AuthenticationError("토큰에 사용자 정보가 없습니다.")
        return user_id
    except jwt.ExpiredSignatureError:
        raise AuthenticationError("토큰이 만료되었습니다.")
    except jwt.InvalidTokenError:
        raise AuthenticationError("유효하지 않은 토큰입니다.")
