from fastapi import APIRouter, Depends

from app.users.dependencies import get_current_admin_user
from app.vehicles.dao import VehiclesDAO
from app.vehicles.shemas import SVehicles

router = APIRouter(
    prefix="/vehicles",
    tags=["Машины транспортных компаний"]
)


@router.get("/{id}")
async def get_vehicle(id: str, current_user=Depends(get_current_admin_user)) -> SVehicles:
    result = await VehiclesDAO.find_one_or_none(id=id)
    return result


@router.get("")
async def get_vehicles(data: SVehicles = Depends(), current_user=Depends(get_current_admin_user)) -> list[
    SVehicles]:
    result = await VehiclesDAO.find_all(**data.model_dump(exclude_none=True))
    return result
