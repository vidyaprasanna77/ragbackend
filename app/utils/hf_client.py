import logging
import httpx
from app.config import HUGGINGFACE_API_URL, HUGGINGFACE_API_TOKEN

logger = logging.getLogger(__name__)

async def call_inference_api(payload: dict):
    headers = {}
    if HUGGINGFACE_API_TOKEN:
        headers["Authorization"] = f"Bearer {HUGGINGFACE_API_TOKEN}"
    
    async with httpx.AsyncClient(timeout=None) as client:
        try:
            # Use the stream() method for streaming responses.
            async with client.stream("POST", HUGGINGFACE_API_URL, json=payload, headers=headers) as response:
                response.raise_for_status()
                async for chunk in response.aiter_text():
                    yield chunk
        except httpx.HTTPError as e:
            logger.error("Error calling Hugging Face Inference API: %s", str(e))
            raise e

