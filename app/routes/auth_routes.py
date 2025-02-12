from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.utils import keycloak_client

router = APIRouter()

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/login")
def login(login_request: LoginRequest):
    """
    Login endpoint that authenticates the user with Keycloak.
    """
    try:
        tokens = keycloak_client.login_user(login_request.username, login_request.password)
        return tokens
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
