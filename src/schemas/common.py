from pydantic import BaseModel, Field


class PaginationParams(BaseModel):
    page: int = Field(1, ge=1, description="Page number (starts from 1)")
    per_page: int = Field(
        10, ge=1, le=50, description="Number of items per page"
    )


class PaginatedBaseResponse(BaseModel):
    total: int
    page: int
    total_pages: int
