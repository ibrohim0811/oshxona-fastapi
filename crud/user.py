from sqlalchemy.orm import Session

from models import Customer


def customers(db: Session):
    customers_data = db.query(Customer).all()
    return customers_data


def customer(id: int, db: Session):
    customer_id = db.query(Customer).filter(Customer.id == id).first()
    if customer_id:
        return customer_id
    

def customer_create(first_name: str, last_name: str, email: str, db: Session):
    new_customer = Customer(
        first_name=first_name,
        last_name=last_name,
        email=email
    )
    db.add(new_customer)
    db.commit()


def customer_update(customer_id: int, first_name: str, last_name: str, email: str, db: Session):
    customer_check = db.query(Customer).filter(Customer.id == customer_id).first()
    if customer_check:
        customer_check.first_name = first_name
        customer_check.last_name = last_name
        customer_check.email = email
        db.commit()
        db.refresh(customer_check)

    return customer_check


def customer_delete(customer_id, db: Session):
    customer_check = db.query(Customer).filter(Customer.id == customer_id).first()
    if customer_check:
        db.delete(customer_check)
        db.commit()