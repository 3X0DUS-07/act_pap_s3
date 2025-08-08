from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI()

class Producto(BaseModel):
    nombre: str
    precio: float
    categoria: str
    stock: int

class ProductoParcial(BaseModel):
    nombre: Optional[str] = None
    precio: Optional[float] = None
    categoria: Optional[str] = None
    stock: Optional[int] = None

productos = [
    {"id": 1, "nombre": "Croquetas para perro", "precio": 20.5, "categoria": "alimento", "stock": 10},
    {"id": 2, "nombre": "Pelota de goma", "precio": 5.99, "categoria": "juguetes", "stock": 25},
    {"id": 3, "nombre": "Collar ajustable", "precio": 12.0, "categoria": "accesorios", "stock": 15},
]

def buscar_producto(producto_id: int):
    for producto in productos:
        if producto["id"] == producto_id:
            return producto
    return None

@app.get("/productos/", response_model=List[dict])
def listar_productos(
    categoria: Optional[str] = Query(None),
    nombre: Optional[str] = Query(None)
):
    resultado = productos

    if categoria:
        resultado = [p for p in resultado if p["categoria"].lower() == categoria.lower()]

    if nombre:
        resultado = [p for p in resultado if nombre.lower() in p["nombre"].lower()]

    return resultado

@app.get("/productos/{producto_id}")
def obtener_producto(producto_id: int):
    producto = buscar_producto(producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto

@app.post("/productos/", status_code=201)
def crear_producto(producto: Producto):
    nuevo_id = max(p["id"] for p in productos) + 1 if productos else 1
    nuevo_producto = producto.dict()
    nuevo_producto["id"] = nuevo_id
    productos.append(nuevo_producto)
    return nuevo_producto

@app.put("/productos/{producto_id}")
def actualizar_producto(producto_id: int, producto_actualizado: Producto):
    producto = buscar_producto(producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    producto.update(producto_actualizado.dict())
    return producto

@app.patch("/productos/{producto_id}")
def actualizar_parcial_producto(producto_id: int, producto_parcial: ProductoParcial):
    producto = buscar_producto(producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    for campo, valor in producto_parcial.dict(exclude_unset=True).items():
        producto[campo] = valor
    return producto

@app.delete("/productos/{producto_id}", status_code=204)
def eliminar_producto(producto_id: int):
    producto = buscar_producto(producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    productos.remove(producto)
