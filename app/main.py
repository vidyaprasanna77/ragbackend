import logging
from fastapi import FastAPI
from app.routes import auth_routes, rag_routes

# Configure logging
logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="RAG Backend Service",
    description="Backend service integrating Keycloak and external AI tools.",
    version="1.0.0"
)

# Include API routers
app.include_router(auth_routes.router)
app.include_router(rag_routes.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the RAG Backend Service!"}
