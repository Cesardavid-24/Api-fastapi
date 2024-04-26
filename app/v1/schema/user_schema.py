from pydantic import BaseModel
from pydantic import Field
from pydantic import EmailStr

class UserBase(BaseModel):
    email: EmailStr = Field(..., examples="cesar@gmail.com")
    username : str = Field(..., min_length=4, max_length=20, examples="MyUsername")

class User(UserBase):
    id: int = Field(..., examples="5")

class UserRegister(UserBase):
    password: str = Field(..., min_length=8, max_length=64, examples="strongpass123")