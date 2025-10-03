from fastapi import FastAPI
from app.routes import productos

app = FastAPI()

app.include_router(productos.router)