import os
from dotenv import load_dotenv

load_dotenv()

# Keycloak configuration
KEYCLOAK_SERVER_URL = os.getenv("KEYCLOAK_SERVER_URL", "http://localhost:8080")
KEYCLOAK_REALM = os.getenv("KEYCLOAK_REALM", "myrealm")
KEYCLOAK_CLIENT_ID = os.getenv("KEYCLOAK_CLIENT_ID", "backend-client")
KEYCLOAK_CLIENT_SECRET = os.getenv("KEYCLOAK_CLIENT_SECRET", "DPHmDvTx5FFw8HJPEsKQ0bOLpBs1GfP6")

# Hugging Face configuration (if applicable)
HUGGINGFACE_API_URL = os.getenv("HUGGINGFACE_API_URL",  "https://api-inference.huggingface.co/models/gpt2")
HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN", "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")

DEBUG = os.getenv("DEBUG", "True") == "True"
