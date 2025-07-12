

from fastapi import Depends, HTTPException, status
from core.authenticator import verify_jwt_token
from utils.db_getter import get_db
from motor.motor_asyncio import AsyncIOMotorDatabase

def require_role(expected_role: str):
    async def role_checker(
        token_data = Depends(verify_jwt_token),
        db: AsyncIOMotorDatabase = Depends(get_db)
    ):
        user = await db["users"].find_one({"email": token_data.email})
        if not user or user.get("role") != expected_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Only {expected_role}s are allowed to access this route"
            )
        return user

    return role_checker

