from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from controller.auth_controller import router as auth_router
from controller.producto_controller import router as producto_router
from db.database import crear_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    crear_db()
    yield


app = FastAPI(
    title="Tienda Online",
    description="Backend modular con FastAPI, SQLModel y JWT",
    version="1.0.0",
    lifespan=lifespan
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router)
app.include_router(producto_router)


@app.get("/")
def inicio():
    return {
        "mensaje": "API de tienda funcionando"
    }