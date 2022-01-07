from fastapi import APIRouter

from app.api.v1.admin import router as admin_router

api_admin_router = APIRouter(prefix='/admin')
api_admin_router.include_router(admin_router, tags=["后端管理接口"])
