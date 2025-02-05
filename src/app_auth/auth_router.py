from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.app_auth.auth_models import User
from src.app_auth.auth_shema import RegisterUser, ShowUser, LoginUser, UpdateUser
from fastapi import HTTPException
from src.db import get_session
from src.app_auth.auth_utilits import create_access_token, encode_password, check_password
from src.get_current_user import get_current_user

app = APIRouter(prefix="/users", tags=["Users"])

@app.get("/me", response_model=ShowUser)
async def me(me = Depends(get_current_user)):
     return me

@app.post("/login")
async def login_user(data:LoginUser,session:AsyncSession = Depends(get_session)):

    user = await session.scalar(select(User).where(User.email == data.email))

    if user:
        if await check_password(password=data.password, old_password=user.password):
                user_token = await create_access_token(user_id=user.id)
                return {"token":user_token}

    raise HTTPException(status_code=401, detail={
                "details":"user is not exists",
                "status":401
        })

@app.post("/register")
async def register_user(data:RegisterUser ,session:AsyncSession = Depends(get_session)):
    
    isUserEx = await session.scalar(select(User).where(User.email == data.email))
    
    if isUserEx:
        raise HTTPException(status_code=411, detail={
        "status":411,
        "data":"user is exists"
        })
        
    data_dict = data.model_dump()
        
    data_dict["password"] = await encode_password(password=data.password)
    
    user = User(**data_dict)
    session.add(user) 
    await session.flush()

    user_id = user.id
        
    await session.commit()
        
    user_token = await create_access_token(user_id=user_id)
    data_dict["token"] = user_token  
        
    return data_dict

@app.put("/update", response_model=ShowUser)
async def update_user(data:UpdateUser,me:User = Depends(get_current_user) ,session:AsyncSession = Depends(get_session)):
    
    await session.refresh(me)
    if data.email:
        me.email = data.email
    if data.name:
        me.name = data.name
    if data.surname:
        me.surname = data.surname    


    await session.commit()
    await session.refresh(me)

    return me