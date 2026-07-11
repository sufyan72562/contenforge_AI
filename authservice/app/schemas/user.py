from pydantic import BaseModel, EmailStr, Field

# -------- REQUEST --------
class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=72)

# -------- RESPONSE --------
class UserResponse(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str