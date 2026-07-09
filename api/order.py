from fastapi import APIRouter, status, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session

from crud.order import order, orders, order_update, order_create, order_delete
from schemas.orders import OrderSchema, OrderCreateSchema, OrderSchemaPatch, OrderSchemaid
from database import get_db

router = APIRouter(
    tags=['order']
)


@router.get('/orders', response_model=List[OrderSchemaid])
def get_order(db: Session = Depends(get_db)):
    data = orders(db=db)
    if data is not None:
        return data
    raise HTTPException(404, "Baza bo'm-bo'sh")


@router.get('/order/{order_id}', response_model=List[OrderSchemaid])
def get_item(order_id: int, db: Session = Depends(get_db)):
    data = order(order_id=order_id, db=db)
    if data is not None:
        return data
    raise HTTPException(404, "Buyurtma mavjud emas!")


@router.post('/order/')
def create_item(order: OrderCreateSchema, db: Session = Depends(get_db)):
    order_create(status=order.status, customer_id=order.customer_id, db=db)   
    return {"message": "Yaratildi !", "status":status.HTTP_201_CREATED}


@router.put('/order/{order_id}')
def put_item(order_id: int, order: OrderSchema, db: Session = Depends(get_db)):
    order_update(
        order_id=order_id,
        status=order.status,
        customer_id=order.customer_id,
        db=db
    )
    return {"message":"Yangilandi!", "status":status.HTTP_200_OK}


@router.patch('/order/{order_id}')
def put_item(order_id: int, order: OrderSchemaPatch, db: Session = Depends(get_db)):
    order_update(
        order_id=order_id,
        status=order.status,
        customer_id=order.customer_id,
        db=db
    )
    return {"message":"Yangilandi!", "status":status.HTTP_200_OK}


@router.delete('/order/{order_id}')
def patch_item(order_id: int, db: Session = Depends(get_db)):
    if order(order_id):
        order_delete(order_id, db=db)
        return {"message":"O'chirildi!", "status":status.HTTP_204_NO_CONTENT}
    raise HTTPException(404, "Kiritilgan buyurtma topilmadi!")