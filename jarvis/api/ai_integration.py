from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from jarvis.modules.ai.ollama_manager import OllamaManager
from jarvis.api.logger import logger
import os
from fastapi.security import APIKeyHeader
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
api_key_header = APIKeyHeader(name="X-API-Key")

class QueryInput(BaseModel):
    query: str
    user_id: str

async def verify_api_key(api_key: str = Depends(api_key_header)) -> str:
    if api_key != os.getenv("API_KEY"):
        raise HTTPException(status_code=401, detail="Invalid API key")
    return api_key

@app.post("/query")
async def handle_query(query_input: QueryInput, api_key: str = Depends(verify_api_key)) -> dict:
    model_manager = OllamaManager()
    try:
        responses = await model_manager.query_all(query_input.query)
        best_response = model_manager.select_best_response(responses, query_input.query)
        return {
            "model": best_response["model"],
            "response": best_response["response"],
            "system_result": "No system command executed"
        }
    except Exception as e:
        logger.error(f"Query error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))