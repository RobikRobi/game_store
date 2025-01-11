from fastapi import APIRouter
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase
from .config import config

app = APIRouter(prefix="/db")

DATABASE_URL = f"postgresql+asyncpg://{config.user}:{config.password}@{config.host}/{config.database}"

engine = create_async_engine(DATABASE_URL, echo=True)

async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_session():
    async with  async_session() as session:
        yield session
        await session.commit()

class Base(AsyncAttrs, DeclarativeBase):
    pass

@app.get("/")
async def create_db():
    async with engine.begin() as conn:
        try:
            await conn.run_sync(Base.metadata.drop_all)
        except:
            pass
        await  conn.run_sync(Base.metadata.create_all)
    return({"msg":"db creat! =)"})