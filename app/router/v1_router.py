from fastapi import APIRouter
from app.api.v1.video import router as video_router


# from app.api.v1.sys_api import router as sys_api_router
# from app.api.v1.administrator import router as admin_create_router
# from app.api.v1.recapi import router as rec_router

api_v1_router = APIRouter(prefix='/v1')
api_v1_router.include_router(video_router, tags=["获取复数个或单个video信息的接口"])
# api_v1_router.include_router(sys_api_router, tags=["服务API管理"])
# api_v1_router.include_router(admin_create_router, tags=["系统管理员管理"])
# api_v1_router.include_router(rec_router, tags=["推荐系统API管理"])
