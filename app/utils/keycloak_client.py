import logging
import requests
from app.config import KEYCLOAK_SERVER_URL, KEYCLOAK_REALM, KEYCLOAK_CLIENT_ID, KEYCLOAK_CLIENT_SECRET

logger = logging.getLogger(__name__)

def login_user(username: str, password: str):
    """Authenticate a user with Keycloak using the password grant."""
    token_url = f"{KEYCLOAK_SERVER_URL}/realms/{KEYCLOAK_REALM}/protocol/openid-connect/token"
    payload = {
        "client_id": KEYCLOAK_CLIENT_ID,
        "username": username,
        "password": password,
        "grant_type": "password"
    }
    if KEYCLOAK_CLIENT_SECRET:
        payload["client_secret"] = KEYCLOAK_CLIENT_SECRET

    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(token_url, data=payload, headers=headers)
    
    if response.status_code == 200:
        logger.info("User %s authenticated successfully.", username)
        return response.json()
    else:
        logger.error("Failed to authenticate user %s. Response: %s", username, response.text)
        response.raise_for_status()

def refresh_access_token(refresh_token: str):
    """Refresh the access token using the refresh token."""
    token_url = f"{KEYCLOAK_SERVER_URL}/realms/{KEYCLOAK_REALM}/protocol/openid-connect/token"
    payload = {
        "client_id": KEYCLOAK_CLIENT_ID,
        "grant_type": "refresh_token",
        "refresh_token": refresh_token
    }
    if KEYCLOAK_CLIENT_SECRET:
        payload["client_secret"] = KEYCLOAK_CLIENT_SECRET

    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(token_url, data=payload, headers=headers)
    
    if response.status_code == 200:
        logger.info("Access token refreshed successfully.")
        return response.json()
    else:
        logger.error("Failed to refresh access token. Response: %s", response.text)
        response.raise_for_status()

def validate_token(access_token: str):
    """Validate the access token by calling Keycloak's introspection endpoint."""
    introspect_url = f"{KEYCLOAK_SERVER_URL}/realms/{KEYCLOAK_REALM}/protocol/openid-connect/token/introspect"
    payload = {
        "token": access_token,
        "client_id": KEYCLOAK_CLIENT_ID
    }
    if KEYCLOAK_CLIENT_SECRET:
        payload["client_secret"] = KEYCLOAK_CLIENT_SECRET

    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(introspect_url, data=payload, headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        if result.get("active"):
            return result
        else:
            logger.warning("Access token is not active.")
            return None
    else:
        logger.error("Failed to validate token. Response: %s", response.text)
        response.raise_for_status()
