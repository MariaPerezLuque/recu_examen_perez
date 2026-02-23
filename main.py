from fastapi import FastAPI, Depends
from sqlmodel import SQLModel, create_engine, Session, update
from models.product import Product, ProductRequest, ProductResponse
from dotenv import load_dotenv

import os
app = FastAPI()
load_dotenv()

DATABASE_URL=os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SQLModel.metadata.create_all(engine)

def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()

#Crear un endpoint per afegir un registre nou.
@app.post("/product/", response_model=dict)
def afegir_product(product: ProductRequest, db: Session = Depends(get_db)):
    product = Product.model_validate(product)
    db.add(product)
    db.commit()
    return {"msg":"producte afegit amb èxit"}

#Crear un endpoint per modificar un camp de registre.
# Cal buscar el registre pel segon camp de la vostra taula creada.
@app.patch("/product/{id}", response_model=dict)
def patch_product(id, name, db:Session=Depends(get_db)):
    stmt = update(Product).where(Product.id==id).values(Product.name, name)
    db.exec(stmt).first()
    return{"msg":"producte acualitzat amb èxit"}

#Crear un endpoint per llegir un registre segons un camp.
@app.get("/product/{id}", response_model=ProductResponse)
def get_product_by_id(id, db:Session=Depends(get_db)):
    product= db.get(Product, id)
    product_response= ProductResponse.model_validate(product)
    return product_response
