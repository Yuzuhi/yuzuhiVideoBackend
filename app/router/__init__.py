from fastapi import APIRouter

from app.router.v1_router import api_v1_router

api_router = APIRouter(prefix='/api')
api_router.include_router(api_v1_router)
