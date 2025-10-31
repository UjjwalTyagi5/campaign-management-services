from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()
async def health_check():
    "Api for health of api pod"
    return JSONResponse(status_code=200,content={"status":"ok"})