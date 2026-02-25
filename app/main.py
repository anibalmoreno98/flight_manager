from fastapi import FastAPI
from app.database import create_db_and_tables
from app.routers import mision, piloto, telemetria, usuario, vuelo, aeronave

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(usuario.router)
app.include_router(piloto.router)
app.include_router(aeronave.router)
app.include_router(mision.router)
app.include_router(vuelo.router)
app.include_router(telemetria.router)

@app.get("/")
def root():
    return {"message": "API de gestor de vuelos funcionando."}
