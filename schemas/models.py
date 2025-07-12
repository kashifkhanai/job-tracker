
from pydantic import BaseModel, EmailStr, Field, field_validator,model_validator
from typing import Annotated, Optional
from enum import Enum
from datetime import datetime
from pydantic import ConfigDict
import re

######################## Auth Models ####################################################################

class UserRole(str, Enum):
    JOB_SEEKER = "job_seeker"
    EMPLOYER = "employer"
    ADMIN = 'admin'
    
    
# --- Regex for password ---
PASSWORD_REGEX = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*(),.?\":{}|<>]).{8,}$"

# --- User Register Schema ---   
class User(BaseModel):
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
    role: UserRole = Field(..., description="User role: 'job_seeker' or 'employer'", examples=["job_seeker", "employer"])
    is_admin: Optional[bool] = False
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
    
class UserRegisterResponse(BaseModel):
    message: str
    user_id: str
    
    
# --- User Login Schema ---
class UserLogin(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    password: str

    @model_validator(mode="after")
    def check_email_or_username(self) -> 'UserLogin':
        if not self.email and not self.username:
            raise ValueError("Either email or username must be provided")
        return self
    
    
################## Admin models ####################################################################################

class AddAdminResponse(BaseModel):
    message: str
    admin_id: str
 

class GetUser(BaseModel):
    model_config = ConfigDict(
        extra="allow"
    )
    firstname: str
    lastname: str
    username: str
    phone: str
    role: str
    email: EmailStr

class DeleteUserResponse(BaseModel):
    message: str


################## Token ################################################################
class TokenData(BaseModel):
    email: str
    exp: datetime | None = None

class Token(BaseModel):
    access_token: str
    token_type: str
    

class JobTitle(str, Enum):
    DEVELOPER = "Developer"
    DESIGNER = "Designer"
    MANAGER = "Manager"
    DATA_SCIENTIST = "Data Scientist"
    QA_ENGINEER = "QA Engineer"

class JobLocation(str, Enum):
    REMOTE = "Remote"
    ONSITE = "Onsite"
    HYBRID = "Hybrid"
    
################### Job Models ######################################################################

class JobPostModel(BaseModel):
    title: JobTitle = Field(..., description="Select the job title", examples=["Developer"])
    location: JobLocation = Field(..., description="Select the job location", examples=["Remote"])
    description: Optional[str] = Field(None, description="Job description")
    company_name: Optional[str] = Field(None, description="Company name")
    salary: Optional[str] = Field(None, description="Salary range")
    posted_at: datetime = Field(default_factory=datetime.now, description="Date posted")
    
    
class JobPostResponse(BaseModel):
    message: str
    job_id: str
    
class JobResponseModel(BaseModel):
    title: JobTitle
    location: JobLocation
    description: Optional[str] = None
    company_name: Optional[str] = None
    salary: Optional[str] = None
    posted_at: datetime
    employer_id: str
    employer_name: str
    employer_email: EmailStr