from fastapi import APIRouter ,HTTPException,status,Depends
from schemas.models import UserRegister,UserLogin,Token,TokenData
from utils.db_getter import get_db
from utils.utils import hash_password,verify_password
from motor.motor_asyncio import AsyncIOMotorDatabase
from datetime import datetime,timezone,timedelta
from settings import JWTSettings
import jwt

jwt_settings=JWTSettings()



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

    # Register new user
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

@router.post("/login",response_model=Token)
async def login_user(payload: UserLogin, db: AsyncIOMotorDatabase = Depends(get_db)):
    if not payload.password:
        raise HTTPException(status_code=400, detail="Password is required")

    query = {}
    if payload.email:
        query["email"] = payload.email
    elif payload.username:
        query["username"] = payload.username
    else:
        raise HTTPException(status_code=400, detail="Email or username is required")

    user = await db["users"].find_one(query)
    if not user or not verify_password(payload.password, user["password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    # Create JWT Token
    expire = datetime.now(timezone.utc) + timedelta(minutes=jwt_settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload_data = {
        "email": user["email"],
        "exp": expire,
        "user_id": str(user["_id"])
    }
    token = jwt.encode(payload=payload_data, key=jwt_settings.SECRET_KEY, algorithm=jwt_settings.ALGORITHM)
    return Token(access_token=token, token_type="bearer")