import pandas as pd
from fastapi import APIRouter, UploadFile, File, HTTPException

router = APIRouter()


@router.post("/upload")
async def upload_plan(file: UploadFile = File(...)):
    try:
        # Lire le fichier Excel
        df = pd.read_excel(file.file)

        # Retourner toutes les données sous forme de dictionnaire
        return {"columns": df.columns.tolist(), "data": df.to_dict(orient="records")}

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erreur lors du traitement du fichier : {str(e)}")
