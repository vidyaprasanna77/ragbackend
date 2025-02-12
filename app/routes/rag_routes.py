from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from app.auth import get_current_user
from app.utils import hf_client

router = APIRouter()

class PredictRequest(BaseModel):
    query: str

@router.post("/predict")
def predict(predict_request: PredictRequest, user=Depends(get_current_user)):
    """
    Predict endpoint simulating a retrieval task.
    In a real implementation, this would perform a search/retrieval operation.
    """
    relevant_data = f"Relevant data for query: {predict_request.query}"
    return {"relevant_data": relevant_data}

class GenerateRequest(BaseModel):
    relevant_data: str
    additional_input: str = ""

@router.post("/generate")
async def generate(generate_request: GenerateRequest, user=Depends(get_current_user)):
    """
    Generate endpoint that calls the Hugging Face Inference API and streams the result.
    """
    # Build the payload to send to the Hugging Face Inference API
    input_text = f"{generate_request.relevant_data}\n{generate_request.additional_input}"
    payload = {"inputs": input_text}

    async def stream_generator():
        try:
            async for chunk in hf_client.call_inference_api(payload):
                yield chunk
        except Exception as e:
            yield f"\nError during generation: {str(e)}"

    return StreamingResponse(stream_generator(), media_type="text/plain")
