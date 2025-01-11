from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .auth_models import User
from .auth_shema import UserRegister
from fastapi import HTTPException
from ..db import get_session
from .auth_utilits import creat_access_token, encode_password, check_password
from ..get_current_user import get_current_user

app = APIRouter(prefix="/users", tags=["Users"])


@app.post("/register")
async def create_user(user: UserRegister, session: AsyncSession = Depends(get_session)):
    h_password = await encode_password(user.password)
    db_user = User(name=user.name, email=user.email, password=h_password)
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user

@app.get("/users")
async def get_users(session: AsyncSession = Depends(get_session), skip: int = 0, limit: int = 10):
    result = await session.execute(select(User).offset(skip).limit(limit))
    return result.scalars().all()

@app.get("/{id}")
async def get_user_by_id(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User).filter(User.id == id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

