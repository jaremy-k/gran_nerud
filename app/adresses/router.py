from fastapi import APIRouter, Depends

from app.adresses.dao import AdressesDAO
from app.adresses.shemas import SAdresses
from app.users.dependencies import get_current_admin_user

router = APIRouter(
    prefix="/adresses",
    tags=["Адреса"]
)


@router.get("/{id}")
async def get_adress(id: str, current_user=Depends(get_current_admin_user)) -> SAdresses:
    result = await AdressesDAO.find_one_or_none(id=id)
    return result


@router.get("")
async def get_adresses(data: SAdresses = Depends(), current_user=Depends(get_current_admin_user)) -> list[
    SAdresses]:
    result = await AdressesDAO.find_all(**data.model_dump(exclude_none=True))
    return result
