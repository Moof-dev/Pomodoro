from fastapi import FastAPI
from app.routers import all_routers
from app.exception import BaseAppException
from app.exception_handler import common_exception_handler

app = FastAPI()

app.add_exception_handler(BaseAppException, common_exception_handler)
app.include_router(all_routers)


