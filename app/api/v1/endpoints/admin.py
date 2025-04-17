from fastapi import Body, Depends, HTTPException, APIRouter
from sqlalchemy import text, inspect
from sqlalchemy.orm import Session
from log_config import setup_logger

from app.core.database import get_db

logger = setup_logger()

router = APIRouter()
@router.post("/plan/add-column")
def add_plan_column(
    column_name: str = Body(..., embed=True),
    column_type: str = Body("VARCHAR(255)", embed=True),
    db: Session = Depends(get_db)
):
    # Restrict access to authenticated admins only
    # current_user = Depends(get_current_user)
    # if not current_user.is_admin:
    #     raise HTTPException(status_code=403, detail="Unauthorized")

    if not column_name.isidentifier():
        logger.error("Nom de colonne invalide.")
        raise HTTPException(status_code=400)

    try:
        sql = text(f"ALTER TABLE plans ADD COLUMN `{column_name}` {column_type};")
        db.execute(sql)
        db.commit()
        logger.info("Colonne ajoutee avec succes")
        return {"message": f"Colonne '{column_name}' ajoutée avec succès."}
    except Exception as e:
        db.rollback()
        error_message = str(e.orig) if hasattr(e, 'orig') else str(e)
        logger.error(f"Erreur lors de l'ajout de la colonne' : {error_message}")
        raise HTTPException(status_code=500, detail="Erreur lors de l'ajout de la colonne")

@router.get("/plan/columns")
def get_plan_columns(db: Session = Depends(get_db)):
    inspector = inspect(db.bind)
    columns = inspector.get_columns('plans')
    return [{"name": col['name'], "type": str(col['type'])} for col in columns]
