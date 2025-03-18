from fastapi import FastAPI
from app.api.v1.endpoints.audit import (router as audit_router)
from app.api.v1.endpoints.plan import (router as plan_router)
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(audit_router, prefix="/audits", tags=["Audits"])
app.include_router(plan_router, prefix="/plan", tags=["Plan"])


@app.get("/")
def root():
    return {"message": "Bienvenue sur l'API de gestion des audits"}


