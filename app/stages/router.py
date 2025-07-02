from fastapi import APIRouter, Depends

from app.stages.dao import StagesDAO
from app.stages.shemas import SStages
from app.users.dependencies import get_current_admin_user

router = APIRouter(
    prefix="/stages",
    tags=["Этапы сделки"]
)


@router.get("/{id}")
async def get_stage(id: str, current_user=Depends(get_current_admin_user)) -> SStages:
    result = await StagesDAO.find_one_or_none(id=id)
    return result


@router.get("")
async def get_stages(data: SStages = Depends(), current_user=Depends(get_current_admin_user)) -> list[
    SStages]:
    result = await StagesDAO.find_all(**data.model_dump(exclude_none=True))
    return result
