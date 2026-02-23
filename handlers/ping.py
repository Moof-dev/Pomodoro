from fastapi import APIRouter
from settings import Setting

router = APIRouter(prefix="/ping", tags=["ping"])

@router.get("/db")
async def ping_db():
    settings = Setting()

    return {"massage": f"OK {settings.GOOGLE_TOKEN_ID}"}

@router.get("/app")
async def ping_app():
    return {"massage": "OK"}