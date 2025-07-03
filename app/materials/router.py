from bson import ObjectId
from fastapi import APIRouter, Depends

from app.materials.dao import MaterialsDAO
from app.materials.shemas import SMaterials
from app.users.dependencies import get_current_admin_user

router = APIRouter(
    prefix="/materials",
    tags=["Нерудные материалы"],
    dependencies=[Depends(get_current_admin_user)]
)


@router.get("/{id}", response_model=SMaterials, summary="Получить материал по ID")
async def get_material(id: str) -> SMaterials:
    result = await MaterialsDAO.find_one_or_none(_id=ObjectId(id))
    return result


@router.get("", response_model=list[SMaterials], summary="Получить список материалов")
async def get_materials(data: SMaterials = Depends()) -> list[
    SMaterials]:
    result = await MaterialsDAO.find_all(**data.model_dump(exclude_none=True))
    return result
