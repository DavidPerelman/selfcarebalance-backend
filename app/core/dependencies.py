from app.core.security import verify_token
from app.models.user import User

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()


from app.core.security import verify_token
from app.models.user import User

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> User:
    raw_token = credentials.credentials

    token = raw_token.replace("Bearer ", "").strip()

    user_id = verify_token(token)

    user = await User.get(user_id)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")

    return user
