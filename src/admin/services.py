from io import BytesIO

import pandas as pd
from fastapi import UploadFile

from src.core.database import get_session
from src.models.meal import MealModel


async def get_df_from_file(file: UploadFile):
    content = await file.read()

    if file.filename.endswith(".csv"):
        df = pd.read_csv(BytesIO(content))
    elif file.filename.endswith(".xlsx"):
        df = pd.read_excel(BytesIO(content))
    else:
        return None

    return df


async def create_meal_objects_from_df(df):
    meal_objects = [
        MealModel(
            image_url=str(row["image_url"]),
            name=row["name"],
            category_id=int(row["category_id"]),
            description=row["description"],
            unit_price=float(row["unit_price"])
        ) for _, row in df.iterrows()
    ]

    async for session in get_session():
        session.add_all(meal_objects)
        await session.commit()
