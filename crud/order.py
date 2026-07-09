from sqlalchemy.orm import Session

from models import Order



def orders(db: Session):
    return db.query(Order).all()


def order(order_id: int, db: Session):
    return db.query(Order).filter(Order.id == order_id).first()


def order_create(customer_id: int, db: Session):
    new_order = Order(
        customer_id=customer_id
    )
    db.add(new_order)
    db.commit()


def order_update(order_id: int, status: str, customer_id: int, db: Session):
    upd_order = db.query(Order).filter(Order.id == order_id).first()
    if upd_order:
        upd_order.status = status
        upd_order.customer_id = customer_id
        db.commit()
        db.refresh(upd_order)


def order_delete(order_id: int, db: Session):
    order_item = db.query(Order).filter(Order.id == order_id).first()
    if order_item:
        db.delete(order_item)
        db.commit()