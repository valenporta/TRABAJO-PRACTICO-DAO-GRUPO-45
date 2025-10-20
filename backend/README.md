# Backend Turnos Médicos (FastAPI + SQLAlchemy)

## Ejecutar
```bash
cd backend
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## CORS
Configura FRONTEND_ORIGIN en `.env` si tu front corre en otro puerto.

## Nota sobre especialidad en el Turno
Para el reporte “Cantidad de turnos por especialidad” es conveniente guardar la especialidad elegida al momento de reservar.
Si tu base **no** tiene la columna, puedes agregarla con:
```sql
ALTER TABLE turnos ADD COLUMN especialidad_id INTEGER REFERENCES especialidades(id);
```
El backend trata `especialidad_id` como opcional. Si no se envía, aparecerá como “Sin especialidad” en reportes.
