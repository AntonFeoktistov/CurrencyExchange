import json


# переименовать в FrontMixin и добавить сюда методы из базового для фронта
class JSONMixin:
    """Миксин для отправки JSON ответов"""

    def send_json(self, data, status: int):
        """Отправляет JSON с указанным статусом."""
        # Используем handler если он есть, иначе self
        handler = getattr(self, "handler", self)

        handler.send_response(status)
        handler.send_header("Content-Type", "application/json; charset=utf-8")
        handler.end_headers()

        # Преобразуем в JSON если нужно
        if not isinstance(data, str):
            data = json.dumps(data, ensure_ascii=False)

        handler.wfile.write(data.encode("utf-8"))
