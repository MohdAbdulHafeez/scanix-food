from fastapi import APIRouter

from .service import (
    digital_twin_service
)

router = APIRouter(

    prefix="/digital-twin",

    tags=[
        "System 6 - Human Body Digital Twin"
    ]
)


@router.post(
    "/analyze"
)
async def analyze_digital_twin(

    payload: dict

):

    return (

        digital_twin_service
        .analyze(
            payload
        )

    )