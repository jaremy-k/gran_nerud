from fastapi import APIRouter, Depends

from app.companies.dao import CompaniesDAO
from app.companies.shemas import SCompanies
from app.users.dependencies import get_current_admin_user

router = APIRouter(
    prefix="/companies",
    tags=["Компании партнеры"]
)


@router.get("/{id}")
async def get_company(id: str, current_user=Depends(get_current_admin_user)) -> SCompanies:
    result = await CompaniesDAO.find_one_or_none(id=id)
    return result


@router.get("")
async def get_companies(data: SCompanies = Depends(), current_user=Depends(get_current_admin_user)) -> list[
    SCompanies]:
    result = await CompaniesDAO.find_all(**data.model_dump(exclude_none=True))
    return result
