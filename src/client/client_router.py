from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from client_shema import CreateReview
from src.db import get_session
from src.app_auth.auth_models import User

from src.get_current_user import get_current_user,get_current_id
from src.products.products_models import Product,SubCategory,Category
from src.seller.seller_models import SellerProfile,SellerProduct, Review
from src.app_auth.auth_models import ClientBacket
from src.types.ProductType import ProductType

app = APIRouter(prefix="/client", tags=["client"])

@app.get("/products", response_model=list[ProductType])
async def get_products(session:AsyncSession = Depends(get_session)):
    products = await session.scalars(select(SellerProduct).options(selectinload(SellerProduct.product), selectinload(SellerProduct.sellerProfile)))
    return products.all()
    
@app.post("products/reviews/create")
async def create_review(data:CreateReview, user:User = Depends(get_current_user), session:AsyncSession = Depends(get_session)):
    review = Review(text=data.text,is_positive=data.is_positive,seller_product_id=data.seller_product_id, user_id=user.id)
    session.add(review)
    await session.commit()
    await session.refresh(review)
    return review

@app.get("products/reviews")
async def get_reviews(user_id:int = Depends(get_current_id), session:AsyncSession = Depends(get_session)):
    user = await session.scalar(select(User).options(selectinload(User.reviews)).where(User.id == user_id))
    if not user:
        
            raise HTTPException(status_code=426, detail={
                "token":"Your token is not valid",
                "status":426
            })

    return user.reviews


@app.delete("products/reviews/delete/{id}")
async def delete_review(id:int, user:User = Depends(get_current_user), session:AsyncSession = Depends(get_session)):
    review = await session.scalar(select(Review).where(Review.id == id, Review.user_id == user.id))
    if not review:
        
            raise HTTPException(status_code=426, detail={
                "details":"This review is not exists",
                "status":426
            })
    await session.delete(review)
    await session.commit()
    return True


@app.get("/backet")
async def get_backet(user:User = Depends(get_current_user), session:AsyncSession = Depends(get_session)):
    total_price = await session.scalar(select(func.sum(ClientBacket.counts*SellerProduct.price))
                                              .join(SellerProduct)
                                              .where(ClientBacket.user_id == user.id))
    
    backet = await session.execute(select(ClientBacket, (ClientBacket.counts*SellerProduct.price).label("all_price"))
                                .join(SellerProduct)
                                .options(selectinload(ClientBacket.product))
                                .where(ClientBacket.user_id == user.id)) 
    data={
        "user":user,
        "total_price":total_price,
        "backet":[{"all_price":res[1],"backet":res[0] } for res in backet.all()] 
    }
   
    return data


@app.put("/backet/add/{id}")
async def update_backet(id:int, user:User = Depends(get_current_user), session:AsyncSession = Depends(get_session)):
    product = await session.scalar(select(SellerProduct).where(SellerProduct.id == id))
    backet_product = await session.scalar(select(ClientBacket).where(ClientBacket.product_id == id, ClientBacket.user_id == user.id))
    if not product:
        
            raise HTTPException(status_code=426, detail={
                "details":"This product is not exists",
                "status":426
            })
    if backet_product:
        backet_product.counts+=1
    else:
        user.backet.append(product)
    await session.commit()
    return True


@app.delete("/backet/delete/{id}")
async def delete_backet(id:int, user:User = Depends(get_current_user), session:AsyncSession = Depends(get_session)):
    product = await session.scalar(select(SellerProduct).where(SellerProduct.id == id))
    if not product:
        
            raise HTTPException(status_code=426, detail={
                "details":"This product is not exists",
                "status":426
            })
    if product in user.backet:
        user.backet.remove(product)

        await session.commit()
        return True
    return False