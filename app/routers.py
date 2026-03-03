from fastapi import APIRouter
from app.users.user_profile.handlers import router as user_router
from app.users.auth.handlers import router as auth_router
from app.tasks.handlers import router as task_router

all_routers = APIRouter()

# Подключаем их. Здесь же можно удобно добавить префиксы или теги
all_routers.include_router(user_router)
all_routers.include_router(auth_router)
all_routers.include_router(task_router)
