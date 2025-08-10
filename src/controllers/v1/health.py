from fastapi import APIRouter

from src.core.logging import logger

router = APIRouter(prefix="/health", tags=["Health"])


@router.get(
    "",
    description="Health check endpoint to verify application status",
    response_description="Application health status"
)
async def health_check():
    logger.info("API request: Health check")
    return {"status": "healthy"}
