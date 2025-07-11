from fastapi import Depends, HTTPException, status
from core.authenticator import verify_jwt_token
from utils.db_getter import get_db
from motor.motor_asyncio import AsyncIOMotorDatabase

async def admin_required(
    token_data = Depends(verify_jwt_token),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    admin = await db["admins"].find_one({"email": token_data.email})
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to perform this action"
        )
    return admin
