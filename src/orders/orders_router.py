from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy import func, select
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from src.get_current_user import get_current_user
from src.db import get_session
from src.app_auth.auth_models import User
from src.app_auth.auth_models import ClientBacket
from src.orders.orders_models import Orders, OrdersSellerProduct
from src.seller.seller_models import SellerProduct
from types.OrderStatusEnum import OrderStatus

app = APIRouter(prefix="/orders", tags=["orders"])




@app.post("/orders/create")
async def create_order(user:User = Depends(get_current_user), session:AsyncSession = Depends(get_session)):
    
    backet = await session.scalars(select(ClientBacket).options(selectinload(ClientBacket.product)).where(ClientBacket.user_id == user.id))
    
    if not backet:
        raise HTTPException(status_code=426, detail={
            "details":"You have not products",
            "status":426
        })
    price = await session.scalar(select(func.sum(ClientBacket.counts*SellerProduct.price))
                                              .join(SellerProduct)
                                              .where(ClientBacket.user_id == user.id))
    
    order = Orders(user_id=user.id,price = price, orderStatus=OrderStatus.CREATED)
    session.add(order)
    await session.flush()
        
    for product in backet.all():
        print(order.id)
        new_product_order = OrdersSellerProduct(seller_product_id=product.product_id,order_id=order.id,counts=product.counts)
        session.add(new_product_order)
        
    await session.delete(backet)
    await session.commit()
        
    return {"status":200}
        

@app.get("/orders")
async def get_orders(user:User = Depends(get_current_user), session:AsyncSession = Depends(get_session)):
    orders = await session.scalars(select(Orders).where(Orders.user_id == user.id))
    return orders.all()


@app.get("/orders/{order_id}")
async def get_order(order_id:int, user:User = Depends(get_current_user), session:AsyncSession = Depends(get_session)):
    order = await session.scalar(select(Orders).where(Orders.id == order_id, Orders.user_id == user.id))
    if not order:
        raise HTTPException(status_code=426, detail={
            "details":"This order is not exists",
            "status":426
        })
    orders_products = await session.scalars(select(OrdersSellerProduct).options(selectinload(OrdersSellerProduct.seller_product)).where(OrdersSellerProduct.order_id == id))
    
    data = {
        "price":order.price,
        "product":[
            {
            "count":product.counts,
            "product":product.seller_product
            } for product in orders_products
        ]
    }
    
    return data