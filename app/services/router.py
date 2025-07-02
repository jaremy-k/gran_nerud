from fastapi import APIRouter, Depends

from app.services.dao import ServicesDAO
from app.services.shemas import SServices
from app.users.dependencies import get_current_admin_user

router = APIRouter(
    prefix="/services",
    tags=["Оказываемые услуги"]
)


@router.get("/{id}")
async def get_service(id: str, current_user=Depends(get_current_admin_user)) -> SServices:
    result = await ServicesDAO.find_one_or_none(id=id)
    return result


@router.get("")
async def get_services(data: SServices = Depends(), current_user=Depends(get_current_admin_user)) -> list[
    SServices]:
    result = await ServicesDAO.find_all(**data.model_dump(exclude_none=True))
    return result
