from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from sqlalchemy.orm import Session

from crud.user import (
customer, customers, 
customer_update, customer_create, 
customer_delete
)
from schemas.customer import CustomerSchema, CustomerSchemaPatch, CustomerChemaid
from database import get_db

router = APIRouter(
    tags=['customer']
)

@router.get('/customers/', response_model=List[CustomerChemaid])
def get_customers(db: Session = Depends(get_db)):
    data = customers(db=db)

    return data


@router.get('/customer/{customer_id}')
def get_customer(customer_id: int,  db: Session = Depends(get_db)):
    data = customer(customer_id=customer_id, db=db)
    if data:
        return data
    raise HTTPException(404, "Bunday User mavjud emas")


@router.post('/customer/')
def create_customer(user: CustomerSchema, db: Session = Depends(get_db)):
    customer_create(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        db=db
    )
    return {"message":"User Yaratildi!", "status":status.HTTP_201_CREATED}


@router.put('/customer/{customer_id}')
def put_customer(customer_id: int, customerschema: CustomerSchema, db: Session = Depends(get_db)):
    if customer(customer_id):
        customer_update(
            customer_id=customer_id,
            first_name=customerschema.first_name,
            last_name=customerschema.last_name,
            email=customerschema.email,
            db=db
        )   
        return {"message":"Yangilandi!", "status":status.HTTP_200_OK}
    raise HTTPException(404, "Bunday User mavjud emas")


@router.patch('/customer/{customer_id}')
def patch_customer(customer_id: int, customerschema: CustomerSchemaPatch, db: Session = Depends(get_db)):
    if customer(customer_id):
        customer_update(
            customer_id=customer_id,
            first_name=customerschema.first_name,
            last_name=customerschema.last_name,
            email=customerschema.email,
            db=db
        )   
        return {"message":"Yangilandi!", "status":status.HTTP_200_OK}
    raise HTTPException(404, "Bunday User mavjud emas")


@router.delete('/customer/{customer_id}')
def delete_user(customer_id: int, db: Session = Depends(get_db)):
    if customer(customer_id):
        customer_delete(customer_id, db=db)
        return {"message":f"{customer_id} li User Chopildi !!!", "status": status.HTTP_204_NO_CONTENT}
    raise HTTPException(404, "Bunday User mavjud emas")
