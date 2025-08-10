from typing import Optional

import requests
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from starlette import status

from app.companies.dao import CompaniesDAO
from app.companies.shemas import SCompanies, SCompaniesAdd
from app.config import settings
from app.logger import logger
from app.users.dependencies import get_current_admin_user

router = APIRouter(
    prefix="/companies",
    tags=["Компании партнеры"]
)


@router.get("/{id}", response_model=SCompanies, summary="Получить компанию по ID")
async def get_company_by_id(id: str) -> SCompanies:
    result = await CompaniesDAO.find_one_or_none(_id=ObjectId(id))
    return result


@router.get("", response_model=list[SCompanies], summary="Получить список компаний")
async def get_companies(data: SCompanies = Depends()) -> list[
    SCompanies]:
    result = await CompaniesDAO.find_all(**data.model_dump(exclude_none=True))
    return result


@router.get("/get_company_info/{inn}", summary="Получить компанию по ИНН или ОГРН")
async def get_company_info(inn: int):
    try:
        params = {'req': inn,
                  'key': settings.API_FNS_KEY}
        result = requests.get(url=settings.API_FNS_URL, params=params)
        logger.info(f"Company info: {result.text}")
        return result.json()
    except Exception as e:
        logger.error(f"Ошибка при получении данных о компании: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при получении данных о компании"
        )


@router.post(
    "",
    response_model=SCompanies,
    summary="Добавить Объект",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {"description": "Объект успешно создан"},
        status.HTTP_409_CONFLICT: {"description": "Объект с таким именем уже существует"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Ошибка сервера"}
    }
)
async def add_company(data: SCompaniesAdd):
    """
    Добавление новой компании.

    Проверяет уникальность инн компании перед добавлением.
    """
    try:
        # Проверка уникальности без учёта регистра и с обрезкой пробелов
        if not await CompaniesDAO.is_unique(
                field_name="inn",
                value=data.inn,
                case_sensitive=False,
                trim_spaces=True
        ):
            raise HTTPException(
                status_code=409,
                detail="Компания с таким инн уже существует"
            )

        # Создание
        company_data = data.model_dump(exclude_none=True)
        result = await CompaniesDAO.add(document=company_data)

        if not result:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Не удалось создать компанию"
            )

        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка при создании материала: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Произошла ошибка при создании материала"
        )


@router.patch(
    "/{id}",
    response_model=SCompanies,
    summary="Обновить материал по ID",
    responses={
        200: {"description": "Материал успешно обновлен"},
        400: {"description": "Невалидные данные или имя уже существует"},
        404: {"description": "Материал не найден"},
        500: {"description": "Внутренняя ошибка сервера"}
    }
)
async def update_material(
        id: str,
        data: SCompaniesAdd,
        background_tasks: BackgroundTasks
):
    """
    Обновляет материал с проверкой уникальности имени.

    Проверяет:
    - Что материал с указанным ID существует
    - Что новое имя (если передано) не занято другими материалами
    - Обрезает пробелы в имени
    - Не учитывает регистр при проверке уникальности
    """
    try:
        # Проверяем существование
        existing_material = await CompaniesDAO.find_one_or_none(_id=ObjectId(id))

        if not existing_material:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Материал не найден"
            )

        update_data = data.model_dump(exclude_none=True)

        if "inn" in update_data:
            # Проверка на уникальность
            if not await CompaniesDAO.is_unique(
                    field_name="inn",
                    value=data.inn,
                    exclude_id=id,
                    case_sensitive=False,
                    trim_spaces=True
            ):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Материал с таким именем уже существует"
                )

        # Фоновое логирование изменения
        background_tasks.add_task(
            logger.info,
            "Material updated: id=%s, changes=%s",  # Сообщение
            id,  # Первый аргумент
            list(update_data.keys()),  # Второй аргумент
            extra={
                'material_id': id,
                'changes': list(update_data.keys()),
                'action': 'material_update'
            }
        )

        # Выполняем обновление
        result = await CompaniesDAO.update_by_id(
            object_id=id,
            update_data=update_data
        )

        if not result:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Не удалось обновить материал"
            )

        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка обновления материала: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Внутренняя ошибка сервера"
        )


@router.delete(
    "/{id}",
    response_model=Optional[SCompanies],
    summary="Безопасное удаление материала",
    responses={
        status.HTTP_200_OK: {
            "description": "Материал успешно удален",
            "model": SCompanies
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Материал не найден"
        },
        status.HTTP_409_CONFLICT: {
            "description": "Материал имеет связанные зависимости"
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Внутренняя ошибка сервера"
        }
    }
)
async def safe_delete_material(
        id: str,
        background_tasks: BackgroundTasks,
        check_dependencies: bool = True
):
    """
    Безопасное удаление материала с проверками:

    - Проверяет существование материала
    - Проверяет связанные зависимости (если check_dependencies=True)
    - Софт-удаление (помечает как удаленный)
    - Логирование действия

    Параметры:
    - id: ID материала
    - check_dependencies: Проверять ли связанные объекты (по умолчанию True)
    """
    try:
        # Проверяем существование материала
        material = await CompaniesDAO.find_one_or_none(_id=ObjectId(id))
        if not material:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Материал не найден"
            )

        # Проверка зависимостей (если требуется)
        if check_dependencies:
            has_dependencies = await check_material_dependencies(id)
            if has_dependencies:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Невозможно удалить материал - имеются связанные объекты"
                )

        # Софт-удаление (помечаем как удаленный)
        result = await CompaniesDAO.soft_delete(id)

        if not result:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Не удалось удалить материал"
            )

        # Логирование в фоне
        background_tasks.add_task(
            logger.info,
            "Material safely deleted: id=%s", id,
            extra={
                'material_id': id,
                'action': 'safe_delete',
                'deleted_by': 'system',  # Можно добавить auth пользователя
                'dependencies_checked': check_dependencies
            }
        )

        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "Safe delete failed: %s", str(e),
            extra={
                'material_id': id,
                'error': str(e),
                'stack_trace': True
            }
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Внутренняя ошибка сервера при удалении"
        )


async def check_material_dependencies(adress_id: str) -> bool:
    """
    Проверяет наличие зависимых объектов у материала

    Возвращает:
    - True если есть зависимости
    - False если зависимостей нет
    """
    # Пример проверки в других коллекциях
    from app.deals.dao import DealsDAO

    # Проверяем, используется ли материал в продуктах
    deals_using_company = await DealsDAO.count(
        {"customerId": ObjectId(adress_id)}
    )

    # Можно добавить другие проверки (заказы, документы и т.д.)

    return deals_using_company > 0
