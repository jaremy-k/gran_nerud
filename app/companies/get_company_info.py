from datetime import datetime
from typing import Dict, Any


def parse_company_data(json_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Парсит JSON ответ и преобразует в унифицированный формат
    """
    result = {
        "name": "",
        "abbreviatedName": "",
        "inn": 0,
        "contacts": [],
        "type": "",
        "deleted_at": None,
        "is_deleted": False
    }

    if not json_data.get("items"):
        return result

    item = json_data["items"][0]

    # Определяем тип организации (ИП или ЮЛ)
    if "ИП" in item:
        company_data = item["ИП"]
        result["type"] = "Индивидуальный предприниматель"
        result = _parse_individual_entrepreneur(company_data, result)
    elif "ЮЛ" in item:
        company_data = item["ЮЛ"]
        result["type"] = "Юридическое лицо"
        result = _parse_legal_entity(company_data, result)

    return result


def _parse_individual_entrepreneur(ip_data: Dict[str, Any], result: Dict[str, Any]) -> Dict[str, Any]:
    """Парсит данные индивидуального предпринимателя"""
    # Основные поля
    result["name"] = ip_data.get("ФИОПолн", "")
    result["abbreviatedName"] = ip_data.get("ФИОПолн", "")

    # ИНН
    inn_str = ip_data.get("ИННФЛ", "")
    try:
        result["inn"] = int(inn_str) if inn_str else 0
    except (ValueError, TypeError):
        result["inn"] = 0

    # Контакты
    contacts = []

    # Email
    email = ip_data.get("E-mail") or ip_data.get("Контакты", {}).get("e-mail", [""])[0]
    if email:
        contacts.append({"email": email.lower()})

    # Адрес
    address = ip_data.get("Адрес", {}).get("АдресПолн")
    if address:
        contacts.append({"address": address})

    result["contacts"] = contacts

    # Статус (для определения is_deleted)
    status = ip_data.get("Статус", "")
    if status and "прекращ" in status.lower() or "не действ" in status.lower():
        result["is_deleted"] = True
        result["deleted_at"] = datetime.now().isoformat()

    return result


def _parse_legal_entity(ul_data: Dict[str, Any], result: Dict[str, Any]) -> Dict[str, Any]:
    """Парсит данные юридического лица"""
    # Основные поля
    result["name"] = ul_data.get("НаимПолнЮЛ", "")
    result["abbreviatedName"] = ul_data.get("НаимСокрЮЛ", "")

    # ИНН
    inn_str = ul_data.get("ИНН", "")
    try:
        result["inn"] = int(inn_str) if inn_str else 0
    except (ValueError, TypeError):
        result["inn"] = 0

    # Контакты
    contacts = []

    # Адрес
    address = ul_data.get("Адрес", {}).get("АдресПолн")
    if address:
        contacts.append({"address": address})

    # Руководитель (может быть контактным лицом)
    director = ul_data.get("Руководитель", {})
    if director.get("ФИОПолн"):
        contacts.append({"director": director["ФИОПолн"]})

    result["contacts"] = contacts

    # Статус (для определения is_deleted)
    status = ul_data.get("Статус", "")
    if status and any(word in status.lower() for word in ["прекращ", "ликвидир", "не действ", "исключен"]):
        result["is_deleted"] = True
        result["deleted_at"] = datetime.now().isoformat()

    return result
