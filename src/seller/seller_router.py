import os
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from src.seller.seller_shema import CreateProduct, CreateSellerProfile

from src.db import get_session
from src.models.UserModel import User

from src.get_current_user import get_current_user,get_current_confirm_seller
from models.seller_models.SellerProductModel import SellerProfile,SellerProduct
from models.product_models.ProductsModel import Product,SubCategory
from src.type.ProductType import ProductType
from src.constants import UPLOAD_FOLDER

app = APIRouter(prefix="/seller", tags=["seller"])

@app.get("/products/", response_model=list[ProductType])
async def get_our_products(session:AsyncSession = Depends(get_session)):
    
    products = await session.scalars(select(Product).options(selectinload(Product.subCategory).selectinload(SubCategory.category)))
    return products.all()

@app.get("/profiles")
async def get_profiles(session:AsyncSession = Depends(get_session)):
    profiles = await session.scalars(select((SellerProfile)).options(selectinload(SellerProfile.products).selectinload(SellerProduct.reviews)))
    return profiles.all()

@app.get("/profiles/{profile_id}")
async def get_profile(profile_id:int, session:AsyncSession = Depends(get_session)):
    profile = await session.scalar(select(SellerProfile).where(SellerProfile.id == profile_id).options(selectinload(SellerProfile.products)))
    return profile



@app.post("/profile/current/create")
async def create_profile(data: CreateSellerProfile, user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    if user.profile:
        raise HTTPException(status_code=400, detail={
            "message": "You already have a profile",
            "status": 400
        })
    
    try:
        new_profile = SellerProfile(
            shop_name=data.shop_name.strip(),
            number=data.number.strip(),
            user=user
        )
        
        session.add(new_profile)
        await session.commit()
        await session.refresh(new_profile)
        
        return new_profile
        
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail={
            "message": "Failed to create profile",
            "status": 500
        })


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
    newProduct = SellerProduct(**data.model_dump())
    session.add(newProduct)
    await session.commit()
    await session.refresh(newProduct)
    
    return newProduct
    

@app.post("/profile/current/products/create/image")
async def create_product_image(product_id:int,file: UploadFile = File(...), user:User = Depends(get_current_confirm_seller), session:AsyncSession = Depends(get_session)):
    product = await session.scalar(select(SellerProduct).where(SellerProduct.id == product_id).options(selectinload(SellerProduct.sellerProfile)))
    if product.sellerProfile != user.profile:
        raise HTTPException(status_code=403, detail={    
            "details":"You are not the seller of this product",
            "status":403
        })
    file_location = f"{UPLOAD_FOLDER}/{product.id}.png"
    with open(file_location, "wb") as f:
        f.write(await file.read())
    product.img = str(file_location)
    await session.commit()
    await session.refresh(product)
    return product

@app.get("/profile/current/products/image/{product_id}")
async def get_product_image(product_id:int, session:AsyncSession = Depends(get_session)):
    product = await session.scalar(select(SellerProduct).where(SellerProduct.id == product_id))
    if not product:
        raise HTTPException(status_code=404, detail={    
            "details":"Product image not found",
            "status":404
        })
    if not product.img:
        raise HTTPException(status_code=404, detail={    
            "details":"Product image not found",
            "status":404
        })
    file_location = str(product.img)
        
    if not os.path.exists(file_location):
        raise HTTPException(status_code=404, detail={    
            "details":"Product image not found",
            "status":404
        })
    return FileResponse(file_location)


@app.delete("/profile/current/products/delete/{product_id}")
async def delete_product(product_id:int, user:User = Depends(get_current_confirm_seller), session:AsyncSession = Depends(get_session)):
    product = await session.scalar(select(SellerProduct).where(SellerProduct.id == product_id).options(selectinload(SellerProduct.sellerProfile)))
    if product.sellerProfile != user.profile:
        raise HTTPException(status_code=403, detail={    
            "token":"You are not the seller of this product",
            "status":403
        })
    await session.delete(product)
    await session.commit()
    return True