from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.responses import JSONResponse

from app.api.v1.endpoints.audit import (router as audit_router)
from app.api.v1.endpoints.plan import (router as plan_router)
from app.api.v1.endpoints.affect import (router as affect_router)
from app.api.v1.endpoints.admin import (router as admin_router)
from app.api.v1.endpoints.dashboard import (router as dashboard_router)
#from app.api.v1.endpoints.flux import (router as flux_router)
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import Base, engine
from app.api.v1.endpoints import auth


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(audit_router, prefix="/audits", tags=["Audits"])
app.include_router(plan_router, prefix="/plan", tags=["Plan"])
app.include_router(affect_router, prefix="/affect", tags=["Affect"])
app.include_router(admin_router, prefix="/admin", tags=["Admin"])
app.include_router(dashboard_router, prefix="/dash", tags=["Dashboard"])
#app.include_router(flux_router, prefix="/flux", tags=["Flux"])

#app.include_router(auth_router, prefix="/auth", tags=["auth"])

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
app.mount("/affectations_pdfs", StaticFiles(directory="affectations_pdfs"), name="affectations")

@app.get("/")
def root():
    return {"message": "Bienvenue sur l'APP de gestion des audits"}
