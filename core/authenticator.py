from typing import Annotated
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt.exceptions import InvalidTokenError
from settings import JWTSettings
from schemas.models import TokenData

JWT_Settings = JWTSettings()

oauth2_scheme = HTTPBearer(scheme_name="JWT")

async def verify_jwt_token(token: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)])->TokenData:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(jwt=token.credentials, key=JWT_Settings.SECRET_KEY, algorithms=[JWT_Settings.ALGORITHM])
        print(payload)
        token_data = payload.get("email")
        if token_data is None:
            print("TOken NOne Error")
            raise credentials_exception
        return TokenData(email=payload.get("email"), exp=payload.get("exp"))
    except InvalidTokenError:
        print("TOken invalid Error")
        raise credentials_exception