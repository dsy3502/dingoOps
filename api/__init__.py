# 路由接口功能
import os

from fastapi import APIRouter

from api import assets, bigscreens

# 启动时创建excel的临时存放目录
excel_temp_dir = "/home/dingoops/temp_excel/"
if not os.path.exists(excel_temp_dir):
    os.makedirs(excel_temp_dir)

api_router = APIRouter()
api_router.include_router(assets.router, tags=["Assets"])
api_router.include_router(bigscreens.router, tags=["BigScreens"])