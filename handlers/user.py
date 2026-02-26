from typing import Annotated

from fastapi import APIRouter, Depends

from dependecy import get_user_service
from schema import UserLoginSchema, UserCreateSchema
from service import UserService

router = APIRouter(prefix="/user", tags=["user"])


@router.post("", response_model=UserLoginSchema)
async def create_user(username: str, password: str, user_service: Annotated[UserService, Depends(get_user_service)]):
    return user_service.create_user(username=username, password=password)