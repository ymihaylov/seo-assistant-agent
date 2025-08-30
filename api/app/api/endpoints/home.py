from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.core.auth import verify_jwt

router = APIRouter(
    tags=["home"],
)


class HelloResponse(BaseModel):
    message: str


@router.get("/", response_model=HelloResponse)
async def read_root():

    return HelloResponse(
        message="There's nothing for you to do here, you should go! 🥔"
    )


@router.get("/me")
def me(claims=Depends(verify_jwt)):
    return claims
