from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse

from src.admin.services import get_df_from_file, create_meal_objects_from_df
from src.core.utils.s3 import upload_file_to_s3

admin_router = APIRouter(
    prefix="/admin", tags=["Admin"], include_in_schema=False
)


@admin_router.post("/upload-meal-image")
async def upload_meal_image(file: UploadFile = File(...)):
    try:
        s3_url = upload_file_to_s3(file.file, file.filename)
        return JSONResponse({
            "status": 0,
            "msg": "success",
            "data": {"value": s3_url}
        })
    except Exception as e:
        return JSONResponse({
            "status": 0,
            "msg": "success",
            "data": {"value": str(e)}
        })


@admin_router.post("/meal-import")
async def import_meals(file: UploadFile = File(...)):
    df = await get_df_from_file(file)

    if not df:
        return JSONResponse({
            "status": 0,
            "msg": "success",
            "data": {"value": "Invalid file format"}
        })

    await create_meal_objects_from_df(df)

    return JSONResponse({
        "status": 0,
        "msg": "success",
        "data": {"value": f"{file.filename}"}
    })
