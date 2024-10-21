from typing import Annotated
from fastapi import APIRouter, Depends
from app.dependency import get_user_service
from app.users.auth.schema import UserLoginSchema
from app.users.user_profile.schema import UserBaseSchema
from app.users.user_profile.service import UserService

router = APIRouter(prefix="/user", tags=["user"])


@router.post("/", response_model=UserLoginSchema)
async def create_user(body: UserBaseSchema, user_service: Annotated[UserService, Depends(get_user_service)]):
    return await user_service.create_user(body)
