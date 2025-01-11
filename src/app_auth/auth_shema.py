from pydantic import BaseModel, EmailStr, Field

# схема для регистрации пользователя
class UserRegister(BaseModel):
    email: EmailStr = Field(..., description="e-mail")
    password: str = Field(..., min_length=5, max_length=50, description="Password, from 5 to 50 characters")
    name: str = Field(..., min_length=3, max_length=50, description="Name, from 3 to 50 characters")