from fastapi import APIRouter, Depends, HTTPException
from bson import ObjectId
from utils.db_getter import get_db
from motor.motor_asyncio import AsyncIOMotorDatabase
from core.admincheck import admin_required
from schemas.models import User, GetUser,AddAdminResponse
from utils.utils import hash_password

router = APIRouter(prefix="/admin")

# Get all users (except passwords)
@router.get("/users", response_model=list[GetUser])
async def get_all_users(
    db: AsyncIOMotorDatabase = Depends(get_db),
    admin = Depends(admin_required)):
    users = await db["users"].find({}, {"password": 0}).to_list()
    # Convert ObjectId to string for each user
    for user in users:
        if "_id" in user:
            user["_id"] = str(user["_id"])
    return users

# Delete a user by ID
@router.delete("/user/{user_id}")
async def delete_user(
    user_id: str,
    db: AsyncIOMotorDatabase = Depends(get_db),
    admin = Depends(admin_required)):
    result = await db["users"].delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}

#  Add new admin
@router.post("/add-admin" ,response_model=AddAdminResponse)
async def add_admin(
    payload: User,
    db: AsyncIOMotorDatabase = Depends(get_db),
    admin = Depends(admin_required)):
    existing = await db.get_collection("users").find_one({"email": payload.email})
    if existing:
        raise HTTPException(status_code=400, detail="Admin already exists")

    hashed_pwd = hash_password(payload.password)

    new_admin = {
        "firstname": payload.firstname,
        "lastname": payload.lastname,
        "username": payload.username,
        "phone": payload.phone,
        "role":"admin",
        "email": payload.email,
        "password": hashed_pwd,
        "is_admin": True
    }

    result = await db["users"].insert_one(new_admin)
    return {"message": "Admin created", "admin_id": str(result.inserted_id)}
