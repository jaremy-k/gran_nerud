all_fields_config = {
    "baseFields": [
        {"name": "serviceId", "label": "Услуга", "type": "select", "options": "services", "required": True},
        {"name": "stageId", "label": "Этап сделки", "type": "select", "options": "stages", "required": True},
        {"name": "customerId", "label": "Заказчик", "type": "company", "required": True},
        {"name": "providerId", "label": "Поставщик", "type": "company", "required": True},
    ],
    "serviceSpecificFields": {
        "1": [  # продажа сырья
            {"name": "quantity", "label": "Количество (тонн)", "type": "number", "step": "1", "min": "1", "required": True},
            {"name": "amountPerUnit", "label": "Цена за тонну (₽)", "type": "number", "step": "0.01", "min": "0", "required": True},
            {"name": "materialId", "label": "Материал", "type": "select", "options": "materials", "required": True},
        ],
        "2": [  # утилизация
            {"name": "quantity", "label": "Объем (тонн)", "type": "number", "step": "1", "min": "1", "required": True},
            {"name": "amountPerUnit", "label": "Цена за утилизацию (₽)", "type": "number", "step": "0.01", "min": "0", "required": True},
            {"name": "materialId", "label": "Вид отходов", "type": "select", "options": "materials", "required": True},
        ],
        "3": [  # доставка
            {"name": "quantity", "label": "Расстояние (км)", "type": "number", "step": "1", "min": "1", "required": True},
            {"name": "amountPerUnit", "label": "Цена за км (₽)", "type": "number", "step": "0.01", "min": "0", "required": True},
        ],
    },
    "additionalFields": [
        {"name": "description", "label": "Описание сделки", "type": "textarea"},
        {"name": "date", "label": "Дата сделки", "type": "date", "required": True},
        {"name": "organizationId", "label": "Организация", "type": "select", "options": "organizations", "required": True},
        {"name": "comment", "label": "Комментарий", "type": "textarea"},
    ]
}