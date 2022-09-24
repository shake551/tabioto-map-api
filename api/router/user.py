from fastapi import APIRouter

import api.schema.user as user_schema

router = APIRouter()


@router.post("/user", response_model=user_schema.UserResponse)
async def login(body: user_schema.UserRequest):
    return user_schema.UserResponse(
        id=1,
        name=body.name
    )
