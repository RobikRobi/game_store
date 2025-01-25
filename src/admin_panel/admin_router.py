from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


from src.db import get_session
from src.seller.seller_models import SellerProfile
from src.products.products_models import Product,SubCategory,Category


app = APIRouter(prefix="/admin", tags=["admin"])

@app.post("/confirm/all")
async def confirm_all( session:AsyncSession = Depends(get_session)):
    
    profiles = await session.scalars(select(SellerProfile).where(not SellerProfile.is_confirmed))
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
async def create_subcategory(name:str,category_id:int, session:AsyncSession = Depends(get_session)):
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