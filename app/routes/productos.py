from fastapi import APIRouter, HTTPException
from app.models import Producto

router = APIRouter()

# "Base de datos" en memoria
productos = {}
siguiente_id = 1

@router.get("/productos")
def obtener_productos():
    return list(productos.values())

@router.get("/productos/{id}")
def obtener_producto(id: int):
    if id not in productos:
        raise HTTPException(404, "No existe")
    return productos[id]

@router.post("/productos")
def crear_producto(producto: Producto):
    global siguiente_id
    nuevo = {**producto.dict(), "id": siguiente_id}
    productos[siguiente_id] = nuevo
    siguiente_id += 1
    return nuevo

@router.put("/productos/{id}")
def actualizar_producto(id: int, producto: Producto):
    if id not in productos:
        raise HTTPException(404, "No existe")
    productos[id] = {**producto.dict(), "id": id}
    return productos[id]

@router.delete("/productos/{id}")
def eliminar_producto(id: int):
    if id not in productos:
        raise HTTPException(404, "No existe")
    del productos[id]
    return {"ok": True}