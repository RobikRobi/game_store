from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.db import engine,Base
from src.app_auth.auth_router import app as auth_app
from src.seller.seller_router import app as seller_app

from src.admin_panel.admin_router import app as admin_app

from src.products.products_models import Product, Category, SubCategory
from src.seller.seller_models import SellerProfile, SellerProduct


app = FastAPI()

# routers
app.include_router(auth_app)
app.include_router(seller_app)

# ADMIN PANEL

app.include_router(admin_app)


# CORS

origins = [
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type",
                   "Set-Cookie",
                   "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                   "Authorization"],
)

@app.get("/init")
async def create_db():
    async with engine.begin() as conn:
        try:
            await conn.run_sync(Base.metadata.drop_all)
        except:
            pass
        await  conn.run_sync(Base.metadata.create_all)
    return({"msg":"db creat! =)"})