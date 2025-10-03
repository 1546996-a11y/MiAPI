from pydantic import BaseModel

class Producto(BaseModel):
    nombre: str
    precio: float
    stock: int
    id_cat: int
    id_marca: int
    id_uni: int
    estado: str = "A"
