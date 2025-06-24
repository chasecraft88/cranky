import requests
from jarvis.modules.logger import logger

def listen() -> str:
    # Existing voice recognition code
    query = "recognized voice input"  # Placeholder
    try:
        response = requests.post(
            "http://localhost:8000/ai/query",
            json={"query": query, "user_id": "XxUse"}
        )
        response.raise_for_status()
        data = response.json()
        return data["response"]  # Return model response for speaker
    except Exception as e:
        logger.error(f"AI query error: {str(e)}")
        return "Sorry, I couldn't process that request."