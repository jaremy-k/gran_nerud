from fastapi import APIRouter, Depends

from app.deals.dao import DealsDAO
from app.deals.shemas import SDeals
from app.users.dependencies import get_current_admin_user

router = APIRouter(
    prefix="/deals",
    tags=["Сделки"]
)


@router.get("/{id}")
async def get_deal(id: str, current_user=Depends(get_current_admin_user)) -> SDeals:
    result = await DealsDAO.find_one_or_none(id=id)
    return result


@router.get("")
async def get_deals(data: SDeals = Depends(), current_user=Depends(get_current_admin_user)) -> list[
    SDeals]:
    result = await DealsDAO.find_all(**data.model_dump(exclude_none=True))
    return result
