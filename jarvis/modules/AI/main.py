from fastapi import FastAPI
from jarvis.api import surveillance, ai_integration

app = FastAPI()
app.include_router(surveillance.router)
app.include_router(ai_integration.app, prefix="/ai")