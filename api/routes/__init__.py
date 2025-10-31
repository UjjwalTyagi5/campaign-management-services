from fastapi import APIRouter
from api.routes import health,campaigns,customers

router = APIRouter()

@router.get('/')
async def hello_world():
    return {"msg": "Hello World"}

router.include_router(health.router,
                       prefix="/health",tags=["Health"])

router.include_router(campaigns.router,
                       prefix="/campaigns", 
                       tags=["Campaigns"])

router.include_router(customers.router,
                       prefix="/customers", 
                       tags=["Customers"])