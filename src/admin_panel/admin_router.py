from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


from ..db import get_session
from ..app_auth.auth_models import User
from ..seller.seller_models import SellerProfile
from ..products.products_models import Product,SubCategory,Category
from ..get_current_user import get_current_user


app = APIRouter(prefix="/admin", tags=["admin"])

@app.post("/confirm/all")
async def confirm_all( session:AsyncSession = Depends(get_session)):
    
    profiles = await session.scalars(select(SellerProfile).where(SellerProfile.is_confirmed == False))
    for profile in profiles:
        profile.is_confirmed = True
    await session.commit()
    return True

@app.post("/category")
async def create_category(name:str, session:AsyncSession = Depends(get_session)):
    newCategory = Category(name=name)
    
    session.add(newCategory)
    await session.commit()
    return newCategory

@app.post("/Subcategory")
async def create_category(name:str,category_id:int, session:AsyncSession = Depends(get_session)):
    newCategory = SubCategory(name=name, category_id=category_id)
    
    session.add(newCategory)
    await session.commit()
    return newCategory

@app.post("/product/create")
async def create_product(name:str, description:str, subCategory_id:int, session:AsyncSession = Depends(get_session)):
    newProduct = Product(name=name, description=description, subCategory_id=subCategory_id)
    
    session.add(newProduct)
    await session.commit()
    return newProduct