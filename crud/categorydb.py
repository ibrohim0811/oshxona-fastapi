from sqlalchemy.orm import Session
from models import Category



def categories(db: Session):
    return db.query(Category).all()


def category_detail(id, db: Session):
    data = db.query(Category).filter(Category.id == id).first()
    return data


def category_create(category_name: str, db: Session):
    category = Category(
        name=category_name
    )
    db.add(category)
    db.commit()
    db.refresh(category)


def category_update(id: int, category_name: str, db: Session):
    category = db.query(Category).filter(Category.id == id).first()
    if category:
        category.name = category_name
        db.commit()
        db.refresh(category)
    return category


def category_delete(id: int, db: Session):
    category = db.query(Category).filter(Category.id == id).first()
    if category:
        db.delete(category)
        db.commit()
    return category


