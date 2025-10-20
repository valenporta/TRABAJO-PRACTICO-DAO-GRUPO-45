from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.config import FRONTEND_ORIGIN
from .routers import pacientes, medicos, especialidades, agenda, turnos, historial, recetas, reportes

app = FastAPI(title="Turnos Médicos API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(pacientes.router)
app.include_router(medicos.router)
app.include_router(especialidades.router)
app.include_router(agenda.router)
app.include_router(turnos.router)
app.include_router(historial.router)
app.include_router(recetas.router)
app.include_router(reportes.router)

@app.get("/")
def root():
    return {"ok": True, "service": "turnos"}
