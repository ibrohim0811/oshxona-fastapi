from fastapi import APIRouter, status, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session

from schemas.category import CategorySchema, CategoryCreateSchema, CategoryPatchSchema, CategoryPutSchema
from crud.categorydb import (
categories, category_detail, 
category_create, category_delete, 
category_update
)
from database import get_db

router = APIRouter(
    tags=["category"]
)


@router.get("/categories", response_model=List[CategorySchema])
def get_categories(db: Session = Depends(get_db)):
    db_data = categories(db)
    return db_data


@router.get("/category/{category_id}", response_model=List[CategorySchema])
def get_category_id(category_id: int, db: Session = Depends(get_db)):
    data = category_detail(category_id, db)
    if data:
        return data
    raise HTTPException(404, "Bunday kategoriya mavjud emas!")


@router.post("/category")
def create_category(category: CategoryCreateSchema, db: Session = Depends(get_db)):
    try:
        category_create(category_name=category.name, db=db)
        return {"message": "Kategoriya qo'shildi!", "status":status.HTTP_201_CREATED}
    except Exception as e:
        print(e)
        return {"message":"Serverda xatolik!", "status":status.HTTP_500_INTERNAL_SERVER_ERROR}
    

@router.put('/category/{category_id}')
def update_category_put(category_id: int, category: CategoryPutSchema, db: Session = Depends(get_db)):
    if category_detail(category_id, db=db):
        category_update(category_id, category.name)
        return {"message":"Yangilandi", "status": status.HTTP_200_OK}
    raise HTTPException(404, "Kiritilgan Kategoriya topilmadi!")


@router.patch('/category/{category_id}')
def update_category_patcht(category_id: int, category: CategoryPatchSchema, db: Session = Depends(get_db)):
    if category_detail(category_id, db=db):
        category_update(category_id, category.name)
        return {"message":"Yangilandi", "status": status.HTTP_200_OK}
    raise HTTPException(404, "Kiritilgan Kategoriya topilmadi!")


@router.delete('/category/{category_id}')
def delete_category(category_id: int, db: Session = Depends(get_db)):
    if category_detail(category_id, db=db):
        category_delete(category_id)
        return {"message":f"{category_id} id raqamli Kategoriya O'chirildi !", "status": status.HTTP_204_NO_CONTENT}
    raise HTTPException(404, "Kiritilgan Kategoriya topilmadi!")