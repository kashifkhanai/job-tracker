from fastapi import APIRouter ,HTTPException,status,Depends
from schemas.models import UserRegister,UserLogin
from utils.db_getter import get_db
from utils.utils import hash_password
from motor.motor_asyncio import AsyncIOMotorDatabase

router = APIRouter(prefix="/auth")

@router.post("/register")
async def register_user(payload: UserRegister, db:AsyncIOMotorDatabase=Depends(get_db)):
    
    # 🔍 Check if user exists by email or username
    existing_user = await db["users"].find_one({"$or": [{"email": payload.email},{"username": payload.username}]})
    if existing_user:
        if existing_user.get("email") == payload.email:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Email already registered")
        if existing_user.get("username") == payload.username:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Username already exists. Please choose a different one."
            )

    # ✅ Register new user
    hash_pwd=hash_password(payload.password)
    new_user={
        "firstname": payload.firstname,
        "lastname" :payload.lastname,
        "username":payload.username,
        "phone": payload.phone,
        "jobtitle":payload.jobtitle,
        "email":payload.email,
        "password":hash_pwd
    }
    result = await db["users"].insert_one(new_user)
    return {"message": "User registered successfully", "user_id": str(result.inserted_id)}

