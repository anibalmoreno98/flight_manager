from fastapi import FastAPI
from app.database import create_db_and_tables
from app.routers import auth, mision, piloto, telemetria, usuario, vuelo, aeronave

app = FastAPI()

app.include_router(usuario.router)
app.include_router(piloto.router)
app.include_router(aeronave.router)
app.include_router(mision.router)
app.include_router(vuelo.router)
app.include_router(telemetria.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "API de gestor de vuelos funcionando."}
