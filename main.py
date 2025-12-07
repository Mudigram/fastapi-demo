from fastapi import Depends, FastAPI
from models import Product
from database import session, engine
import database_models 
from sqlalchemy.orm import Session

app = FastAPI()


database_models.Base.metadata.create_all(bind=engine) #This Line creates the table for you in PostGress


@app.get("/")
def greet():
    return "Welcome Mudi"


products = [
    Product(id=1, name="Phone", description="Budget Phone", price= 299.9, quantity=20),
            Product(id=2, name="CellPhone", description="Budget Phone", price= 89999.9, quantity=200),
            Product(id=3, name="Phone", description="Budget Phone", price= 899.9, quantity=200),
            Product(id=4, name="Cell", description="Budget Phone", price= 20.0, quantity=200)
            ]

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

def init_db():
    db = session()
    count = db.query(database_models.Product).count()

    if count == 0:
        for product in products:
            db.add(database_models.Product(**product.model_dump()))
        db.commit()

init_db()

@app.get("/products")
def get_all_products(db: Session = Depends(get_db)):

    db_products = db.query(database_models.Product).all()
    return db_products

@app.get("/product/{id}")
def get_all_products_by_id(id: int, db: Session = Depends(get_db)):
    db_products = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_products: 
        return  db_products
    return "product not found"

@app.post("/product")
def add_product(product: Product, db: Session = Depends(get_db)):
    db.add(database_models.Product(**product.model_dump()))
    db.commit()
    return product

@app.put("/product")
def update_product(id: int, product: Product, db: Session = Depends(get_db)):
    db_products = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_products:
        db_products.name = product.name
        db_products.description = product.description
        db_products.price = product.price
        db_products.quantity = product.quantity
        db.commit()
        return "Product Updated"
    else:
        return "product not found"

@app.delete("/product")
def delete_product(id: int,  db: Session = Depends(get_db)):
    db_products = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_products:
        db.delete(db_products)
        db.commit()  
        return "product deleted "
    else:
        return "product not found"
