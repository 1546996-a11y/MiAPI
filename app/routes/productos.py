from fastapi import APIRouter, HTTPException
from app.models import Producto
from app.database import get_db_connection

router = APIRouter()

@router.get("/productos")
def obtener_productos():
    connection = get_db_connection()
    if not connection:
        raise HTTPException(500, "Database connection failed")
    
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.callproc('sp_listarproductos')
        
        productos = []
        for result in cursor.stored_results():
            productos = result.fetchall()
        
        return productos
    except Exception as e:
        raise HTTPException(500, f"Database error: {str(e)}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

@router.get("/productos/{id}")
def obtener_producto(id: int):
    connection = get_db_connection()
    if not connection:
        raise HTTPException(500, "Database connection failed")
    
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.callproc('sp_busidproductos', [id])
        
        producto = None
        for result in cursor.stored_results():
            producto = result.fetchone()
        
        if not producto:
            raise HTTPException(404, "Producto no existe")
        
        return producto
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, f"Database error: {str(e)}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

@router.post("/productos")
def crear_producto(producto: Producto):
    connection = get_db_connection()
    if not connection:
        raise HTTPException(500, "Database connection failed")
    
    try:
        cursor = connection.cursor()
        cursor.callproc('sp_ingproductos', [
            producto.nombre,
            producto.precio,
            producto.id_uni,
            producto.id_marca,
            producto.id_cat,
            producto.stock,
            producto.estado
        ])
        connection.commit()
        
        return {"message": "Producto creado exitosamente"}
    except Exception as e:
        connection.rollback()
        raise HTTPException(500, f"Database error: {str(e)}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

@router.put("/productos/{id}")
def actualizar_producto(id: int, producto: Producto):
    connection = get_db_connection()
    if not connection:
        raise HTTPException(500, "Database connection failed")
    
    try:
        cursor = connection.cursor()
        cursor.callproc('sp_modproductos', [
            id,
            producto.nombre,
            producto.precio,
            producto.id_uni,
            producto.id_marca,
            producto.id_cat,
            producto.stock,
            producto.estado
        ])
        connection.commit()
        
        return {"message": "Producto actualizado exitosamente"}
    except Exception as e:
        connection.rollback()
        raise HTTPException(500, f"Database error: {str(e)}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

@router.delete("/productos/{id}")
def eliminar_producto(id: int):
    connection = get_db_connection()
    if not connection:
        raise HTTPException(500, "Database connection failed")
    
    try:
        cursor = connection.cursor()
        cursor.callproc('sp_eliproductos', [id])
        connection.commit()
        
        return {"message": "Producto eliminado exitosamente"}
    except Exception as e:
        connection.rollback()
        raise HTTPException(500, f"Database error: {str(e)}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
