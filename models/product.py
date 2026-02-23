from sqlmodel import SQLModel, Field

class Product(SQLModel, Table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    descripcio: str
    preu: float

class ProductRequest(SQLModel):
    name: str
    descripcio: str
    preu: float

class ProductResponse(SQLModel):
    name: str
    descripcio: str
    preu: float