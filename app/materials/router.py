from fastapi import APIRouter, Depends

from app.materials.dao import MaterialsDAO
from app.materials.shemas import SMaterials
from app.users.dependencies import get_current_admin_user

router = APIRouter(
    prefix="/materials",
    tags=["Нерудные материалы"]
)


@router.get("/{id}")
async def get_material(id: str, current_user=Depends(get_current_admin_user)) -> SMaterials:
    result = await MaterialsDAO.find_one_or_none(id=id)
    return result


@router.get("")
async def get_materials(data: SMaterials = Depends(), current_user=Depends(get_current_admin_user)) -> list[
    SMaterials]:
    result = await MaterialsDAO.find_all(**data.model_dump(exclude_none=True))
    return result
