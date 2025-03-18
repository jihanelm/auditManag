from fastapi import Depends, HTTPException, Security
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
import requests
from app.core.config import settings

ALGORITHM = "RS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=settings.KEYCLOAK_TOKEN_URL)

def get_public_keys():
    response = requests.get(settings.KEYCLOAK_CERTS_URL)
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Impossible de récupérer les clés Keycloak")
    return response.json()["keys"]


def verify_token(token: str = Security(oauth2_scheme)):
    public_keys = get_public_keys()
    try:
        payload = jwt.decode(token, public_keys[0], algorithms=[ALGORITHM], options={"verify_aud": False})
        return payload
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Token invalide")


def has_role(required_role: str):
    def role_checker(user_info: dict = Depends(verify_token)):
        roles = user_info.get("realm_access", {}).get("roles", [])
        if required_role not in roles:
            raise HTTPException(status_code=403, detail="Accès interdit")
        return user_info
    return role_checker
