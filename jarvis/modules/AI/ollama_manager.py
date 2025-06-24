import asyncio
from typing import Dict, List
import ollama
from jarvis.api.logger import logger

class OllamaManager:
    def __init__(self) -> None:
        self.models: List[str] = ["mistral", "phi3", "llama3.1"]
        self.model_strengths: Dict[str, str] = {
            "mistral": "quick_response",
            "phi3": "resource_efficient",
            "llama3.1": "complex_reasoning"
        }

    async def query_model(self, model: str, query: str) -> Dict[str, str | None]:
        try:
            response = await asyncio.to_thread(
                ollama.chat,
                model=model,
                messages=[{"role": "user", "content": query}],
                host="http://127.0.0.1:11435"
            )
            return {"model": model, "response": response["message"]["content"], "error": None}
        except Exception as e:
            logger.error(f"Error querying {model}: {str(e)}")
            return {"model": model, "response": None, "error": str(e)}

    async def query_all(self, query: str) -> List[Dict[str, str | None]]:
        tasks = [self.query_model(model, query) for model in self.models]
        return await asyncio.gather(*tasks)

    def select_best_response(self, responses: List[Dict[str, str | None]], query: str) -> Dict[str, str | None]:
        if len(query.split()) > 20 or "reason" in query.lower():
            target_model = "llama3.1"
        elif len(query.split()) < 5:
            target_model = "phi3"
        else:
            target_model = "mistral"
        for response in responses:
            if response["model"] == target_model and response["response"]:
                return response
        for response in responses:
            if response["response"]:
                return response
        raise ValueError("All model queries failed")