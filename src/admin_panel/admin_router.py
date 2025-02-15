from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


from src.db import get_session
from src.models.SellerModel import SellerProfile
from src.models.ProductsModel import Product,SubCategory,Category


app = APIRouter(prefix="/admin", tags=["admin"])

@app.post("/confirm/all")
async def confirm_all( session:AsyncSession = Depends(get_session)):
    
    profiles = await session.scalars(select(SellerProfile).where(SellerProfile.is_confirmed == False))
    for profile in profiles:
        profile.is_confirmed = True
    await session.commit()
    return {"status":"200"}

@app.post("/category")
async def create_category(name:str, session:AsyncSession = Depends(get_session)):
    newCategory = Category(name=name)
    
    session.add(newCategory)
    await session.commit()
    await session.refresh(newCategory)
    return newCategory

@app.post("/Subcategory")
async def create_subcategory(name:str,category_id:int, session:AsyncSession = Depends(get_session)):
    newCategory = SubCategory(name=name, category_id=category_id)
    
    session.add(newCategory)
    await session.commit()
    await session.refresh(newCategory)
    return newCategory

@app.post("/product/create")
async def create_product(name:str, description:str, subCategory_id:int, session:AsyncSession = Depends(get_session)):
    newProduct = Product(name=name, description=description, subCategory_id=subCategory_id)
    
    session.add(newProduct)
    await session.commit()
    await session.refresh(newProduct)
    return newProduct