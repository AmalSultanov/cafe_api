from fastapi_amis_admin import admin
from fastapi_amis_admin.amis.components import (
    InputImage, Action, Form, InputFile, Dialog
)
from src.admin import site
from src.core.utils.type_converters import url_to_str
from src.models.meal import MealModel


@site.register_admin
class MealModelAdmin(admin.ModelAdmin):
    page_schema = "MealModel"
    model = MealModel

    async def get_create_form(self, request, bulk: bool = False, **kwargs):
        form = await super().get_create_form(request, bulk=bulk, **kwargs)
        form.body = [
            InputImage(
                name="image_url",
                label="meal_image",
                receiver="post:/admin/upload-meal-image",
                accept="image/*",
                maxSize=5 * 1024 * 1024,
                required=True
            )
        ] + form.body
        return form

    async def get_update_form(self, request, **kwargs):
        form = await super().get_update_form(request, **kwargs)
        form.body = [
            InputImage(
                name="image_url",
                label="Meal Image",
                receiver="post:/admin/upload-meal-image",
                accept="image/*",
                maxSize=5 * 1024 * 1024,
            )
        ] + form.body
        return form

    async def on_create_pre(self, request, obj, **kwargs):
        data = obj.model_dump(exclude_unset=True)
        if "image_url" in data and data["image_url"]:
            data["image_url"] = url_to_str(data["image_url"])
        return data

    async def on_update_pre(self, request, obj, item_id, **kwargs):
        data = obj.model_dump(exclude_unset=True)
        if "image_url" in data and data["image_url"]:
            data["image_url"] = url_to_str(data["image_url"])
        return data

    async def get_list_table(self, request):
        table = await super().get_list_table(request)
        import_button = Action(
            label="Import Meals",
            level="primary",
            actionType="dialog",
            dialog=Dialog(
                title="Upload CSV/Excel File",
                body=Form(
                    api=None,
                    body=[
                        InputFile(
                            name="file",
                            label="CSV/Excel File",
                            accept=".csv,.xlsx",
                            required=True,
                            receiver="/admin/meal-import"
                        )
                    ]
                )
            )
        )
        table.headerToolbar.append(import_button)

        return table
