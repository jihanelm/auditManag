from fastapi import APIRouter, Depends
from app.core.security import verify_token, has_role

router = APIRouter()

@router.get("/me")
def get_user(user_info: dict = Depends(verify_token)):
    return {"message": f"Bienvenue {user_info['preferred_username']}", "roles": user_info.get("realm_access", {}).get("roles", [])}

@router.get("/admin")
def admin_access(user_info: dict = Depends(has_role("admin"))):
    return {"message": f"Accès Admin autorisé, bienvenue {user_info['preferred_username']}"}
