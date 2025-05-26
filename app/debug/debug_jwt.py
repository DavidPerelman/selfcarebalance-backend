import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from datetime import datetime, timedelta, timezone
from jose import jwt
from app.core.config import settings

user_id = "68321e44ef44f720f3085ad4"

expire = datetime.now(timezone.utc) + timedelta(minutes=60)
to_encode = {"sub": user_id, "exp": expire}

token = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

print("JWT Token:")
print(token)
