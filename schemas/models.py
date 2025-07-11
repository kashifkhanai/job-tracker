from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Annotated, Optional
from enum import Enum
import re

# --- Enums ---
class JobStatus(str, Enum):
    applied = "applied"
    interviewing = "interviewing"
    offered = "offered"
    rejected = "rejected"

class JobType(str, Enum):
    developer = "developer"
    designer = "designer"
    manager = "manager"
    data_analyst = "data_analyst"
    qa_engineer = "qa_engineer"

# --- Regex for password ---
PASSWORD_REGEX = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*(),.?\":{}|<>]).{8,}$"

# --- User Register Schema ---
class UserRegister(BaseModel):
    firstname: Annotated[str, Field(..., description="First name is required")]
    lastname: Optional[str] = Field(default=None, description="Last name is optional")
    username: Annotated[
        str,
        Field(..., min_length=3, max_length=20, pattern=r"^[a-zA-Z0-9_]+$", description="Only letters, numbers, underscores")
    ]
    phone: Annotated[
        Optional[str],
        Field(default=None, min_length=10, max_length=16, pattern=r"^\+?\d{10,15}$", description="Valid phone number")
    ]
    jobtitle: JobType
    email: EmailStr
    password: str

    # Custom validator for password
    @field_validator('password')
    @classmethod
    def validate_password(cls, value: str) -> str:
        if not re.match(PASSWORD_REGEX, value):
            raise ValueError(
                "Password must be at least 8 characters long, include uppercase, "
                "lowercase, number, and special character."
            )
        return value

# --- User Login Schema ---
class UserLogin(BaseModel):
    username: str
    email: EmailStr
    password: str
