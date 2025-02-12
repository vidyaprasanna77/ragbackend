
# RAG Backend Service: Keycloak & Hugging Face Integration

## Overview

This project is an end-to-end backend service that integrates Keycloak for authentication and implements a Retrieval-Augmented Generation (RAG) pipeline using FastAPI. The service includes endpoints for user login, retrieval of relevant data, and text generation via the Hugging Face Inference API. It is fully containerized using Docker and Docker Compose.

## Features

- **Keycloak Integration:** Secure authentication with token management.
- **RAG Pipeline:** 
  - **/predict:** Simulates a retrieval step by returning relevant data based on a query.
  - **/generate:** Calls the Hugging Face Inference API (using, for example, the EleutherAI/gpt-neo-125M model) to generate text in a streaming fashion.
- **Dockerized Setup:** Both Keycloak and the backend service are containerized.
- **Swagger Documentation:** Interactive API documentation is available at `/docs`.
- **Testing:** Includes unit and integration tests using pytest.

## Architecture and Code Structure

The project is organized as follows:

```
rag-backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # Application entry point
│   ├── config.py            # Configuration for Keycloak, Hugging Face, etc.
│   ├── auth.py              # Authentication dependencies for token extraction and validation
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth_routes.py   # /login endpoint for Keycloak authentication
│   │   └── rag_routes.py    # /predict and /generate endpoints for the RAG pipeline
│   └── utils/
│       ├── __init__.py
│       ├── keycloak_client.py  # Helper functions for interacting with Keycloak
│       └── hf_client.py        # Helper functions for calling Hugging Face Inference API
├── tests/                      # Unit and integration tests (using pytest)
│   ├── test_auth.py
│   └── test_rag.py
├── Dockerfile                  # Dockerfile for the backend service
├── docker-compose.yml          # Docker Compose file to run Keycloak and the backend
├── requirements.txt            # Python package dependencies
└── README.md                   # This file
```

## Environment Setup

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [Python 3.9+](https://www.python.org/downloads/)
- (Optional) [Git](https://git-scm.com/)

### Keycloak Setup

1. **Create a Project Directory**  
   ```bash
   mkdir rag-backend
   cd rag-backend
   ```

2. **Docker Compose Configuration for Keycloak**  
   Create a `docker-compose.yml` file with the following content (Keycloak service snippet):
   ```yaml
   version: '3.8'
   services:
     keycloak:
       image: quay.io/keycloak/keycloak:latest
       environment:
         KEYCLOAK_ADMIN: admin
         KEYCLOAK_ADMIN_PASSWORD: admin
       ports:
         - "8080:8080"
       command: start-dev
   ```

3. **Start Keycloak**  
   Run:
   ```bash
   docker-compose up keycloak
   ```
   Keycloak will be available at [http://localhost:8080](http://localhost:8080).

4. **Configure Keycloak**  
   - Log into the admin console with username `admin` and password `admin`.
   - Create a new realm (e.g., `myrealm`).
   - Under **Clients**, create a new client (e.g., `backend-client`) with:
     - **Access Type:** `confidential` (to enable client secret usage).
     - **Login Settings:** Set the Root URL to `http://localhost:8000`, Valid Redirect URLs to `http://localhost:8000/*`, and Web Origins to `http://localhost:8000`.
   - Copy the client secret and update your environment variables accordingly.
   - Create a test user (e.g., `testuser`) with a permanent password.

### Backend Setup

1. **Clone the Repository**  
   ```bash
   git clone <repository_url>
   cd rag-backend
   ```

2. **Configure Environment Variables**  
   Create a `.env` file in the project root with content similar to:
   ```
   KEYCLOAK_SERVER_URL=http://localhost:8080
   KEYCLOAK_REALM=myrealm
   KEYCLOAK_CLIENT_ID=backend-client
   KEYCLOAK_CLIENT_SECRET=<your-keycloak-client-secret>
   HUGGINGFACE_API_URL=<model chosen , I chose gpt2>
   HUGGINGFACE_API_TOKEN=hf_your_valid_token_here
   DEBUG=True
   ```

3. **Setup Python Virtual Environment and Install Dependencies**  
   ```bash
   python3 -m venv venv
   source venv/bin/activate  
   pip install -r requirements.txt
   ```

4. **Dockerize the Backend**  
   A `Dockerfile` is provided to containerize the backend service. To build and run the full stack (Keycloak and the backend), use:
   ```bash
   docker-compose up --build
   ```

## API Endpoints

### /login (POST)

- **Description:**  
  Authenticates a user with Keycloak and returns access and refresh tokens.
- **Request Body:**
  ```json
  {
    "username": "testuser",
    "password": "testpassword"
  }
  ```
- **Response:**  
  JSON object containing tokens:
  ```json
  {
    "access_token": "...",
    "refresh_token": "...",
    ...
  }
  ```

### /predict (POST)

- **Description:**  
  Simulates a retrieval task by accepting a query and returning relevant data.
- **Request Body:**
  ```json
  {
    "query": "What is FastAPI?"
  }
  ```
- **Response:**  
  ```json
  {
    "relevant_data": "Relevant data for query: What is FastAPI?"
  }
  ```

### /generate (POST)

- **Description:**  
  Accepts data from `/predict` along with additional input, then calls the Hugging Face Inference API to generate text. The response is streamed back to the client.
- **Request Body:**
  ```json
  {
    "relevant_data": "Relevant data for query: What is FastAPI?",
    "additional_input": "More context here"
  }
  ```
- **Response:**  
  Streams generated text (chunked response).

### Swagger Documentation

Access the interactive API documentation at:  
[http://localhost:8000/docs](http://localhost:8000/docs)

## Testing

- **Run Tests:**  
  Use pytest to run unit and integration tests:
  ```bash
  pytest
  ```

## Error Handling and Logging

- Robust error handling is implemented for:
  - Authentication failures
  - Token refresh errors
  - API call errors (including handling 401 responses)
- Logging captures key events (e.g., successful logins, token validation, external API errors).

## Docker and Deployment

- **Dockerfile:**  
  The Dockerfile sets up the FastAPI backend.
- **docker-compose.yml:**  
  The Docker Compose file runs both the Keycloak and backend services.  
  To start the entire stack:
  ```bash
  docker-compose up --build
  ```

## Future Enhancements

- **Automatic Token Refresh:**  
  Implement automatic token refresh on receiving a 401 Unauthorized response.
- **Enhanced Retrieval:**  
  Replace the static retrieval in `/predict` with a more advanced retrieval system.
- **Production Readiness:**  
  Optimize for scalability, performance, and enhanced error monitoring.

## License

[Specify your license here – e.g., MIT License]

## Contact

For any questions or issues, please contact srividyaprasannakumar@gmail.com.

---

*Prepared by srividya on 12/2/2025*
```

---

## How to Use

1. **Commit the Code:**  
   Initialize your Git repository, add the files, and commit:
   ```bash
   git init
   git add .
   git commit -m "Initial commit: RAG Backend Service with Keycloak and Hugging Face Integration"
   ```

2. **Push to Your Remote Repository:**  
   (Replace `<remote_url>` with your repository URL)
   ```bash
   git remote add origin <remote_url>
   git push -u origin master
   ```

