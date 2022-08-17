from pydantic import BaseModel,EmailStr
from typing import Optional

class UserRegisterRequest(BaseModel):
    username:str
    email:Optional[EmailStr]
    password:str
    
class LoginRequest(BaseModel):
    username:str
    password:str