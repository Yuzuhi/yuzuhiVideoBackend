import asyncio

from fastapi import APIRouter, Depends
from core.training import training_bg
from schemas.response import response_code

router = APIRouter()


@router.post("/train/")
async def rec_train(q: str = Depends(training_bg)):
    return response_code.response_200(data=q)

