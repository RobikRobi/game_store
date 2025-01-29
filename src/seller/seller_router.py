from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from .seller_shema import CreateProduct, CreateSellerProfile

from src.db import get_session
from src.app_auth.auth_models import User

from src.get_current_user import get_current_user,get_current_confirm_seller
from src.seller.seller_models import SellerProfile,SellerProduct
from src.products.products_models import Product,SubCategory
from src.types.ProductType import ProductType

app = APIRouter(prefix="/seller", tags=["seller"])

@app.get("/products/", response_model=list[ProductType])
async def get_our_products(session:AsyncSession = Depends(get_session)):
    
    products = await session.scalars(select(Product).options(selectinload(Product.subCategory).selectinload(SubCategory.category)))
    return products.all()

@app.get("/profiles")
async def get_profiles(session:AsyncSession = Depends(get_session)):
    profiles = await session.scalars(select((SellerProfile)).options(selectinload(SellerProfile.products).selectinload(SellerProduct.reviews)))
    return profiles.all()

@app.get("/profiles/{id}")
async def get_profile(id:int, session:AsyncSession = Depends(get_session)):
    profile = await session.scalar(select(SellerProfile).where(SellerProfile.id == id).options(selectinload(SellerProfile.products)))
    return profile


@app.post("/profile/current/create")
async def create_profile(data:CreateSellerProfile,user:User = Depends(get_current_user), session:AsyncSession = Depends(get_session)):
    if user.profile:
        raise HTTPException(status_code=426, detail={
            "token":"You already have a profile",
            "status":426
        })
    newProfile = SellerProfile(shop_name=data.shop_name,number=data.number,user=user)
    
    session.add(newProfile)
    await session.commit()
    
    
    await session.refresh(newProfile)
    
    return newProfile

@app.get("/profile/current")
async def get_current_profile(user:User = Depends(get_current_user), session:AsyncSession = Depends(get_session)):
    return user.profile

@app.get("/profile/current/products")
async def get_products(user = Depends(get_current_confirm_seller), session:AsyncSession = Depends(get_session)):
    products = await session.scalars(select(SellerProduct).where(SellerProduct.sellerProfile == user.profile).options(selectinload(SellerProduct.product)))
    return products.all()

# CRUD seller products

@app.post("/profile/current/products/create")
async def create_product(data:CreateProduct, user:User = Depends(get_current_confirm_seller), session:AsyncSession = Depends(get_session)):
    newProduct = SellerProduct(description=data.description,price=data.price,currency=data.currency,sellerProfile=user.profile, product_id= data.product_id)
    session.add(newProduct)
    await session.commit()
    await session.refresh(newProduct)
    
    return newProduct
    
@app.delete("/profile/current/products/delete/{id}")
async def delete_product(id:int, user:User = Depends(get_current_confirm_seller), session:AsyncSession = Depends(get_session)):
    product = await session.scalar(select(SellerProduct).where(SellerProduct.id == id).options(selectinload(SellerProduct.sellerProfile)))
    if product.sellerProfile != user.profile:
        raise HTTPException(status_code=403, detail={    
            "token":"You are not the seller of this product",
            "status":403
        })
    await session.delete(product)
    await session.commit()
    return True