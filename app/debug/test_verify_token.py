import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from app.core.security import verify_token

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2ODMyMWU0NGVmNDRmNzIwZjMwODVhZDQiLCJleHAiOjE3NDgxMjQzNTV9.bA7P5zN-M0O123zfURlAWuDLvX7fOseNzIpm7AqDKI4"

try:
    user_id = verify_token(token)
    print("✅ Token OK, user_id =", user_id)
except Exception as e:
    print("❌ Token error:", e)
