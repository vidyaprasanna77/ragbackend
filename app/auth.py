from fastapi import HTTPException, Depends, Header
from app.utils import keycloak_client

def get_token_from_header(authorization: str = Header(...)):
    """
    Extract the token from the Authorization header.
    Expect header format: "Bearer <token>"
    """
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Invalid authentication scheme.")
        return token
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid authorization header.")

def get_current_user(token: str = Depends(get_token_from_header)):
    """
    Validate the provided token using Keycloak and return user info.
    """
    token_info = keycloak_client.validate_token(token)
    if token_info is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token.")
    return token_info
