from fastapi import FastAPI
from jarvis.api import surveillance, ai_integration
import uvicorn
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Jarvis API",
    description="Gateway to communicate with Jarvis and entry point for the UI.",
    version="1.0.0"
)
app.include_router(surveillance.router)
app.include_router(ai_integration.app, prefix="/ai")

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8443,
        ssl_keyfile="C:/Users/XxUse/source/repos/cranky/key.pem",
        ssl_certfile="C:/Users/XxUse/source/repos/cranky/cert.pem"
    )