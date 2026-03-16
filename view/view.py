import json


class View:

    def get_error_json(self, message: str):
        return json.dumps({"message": message}, ensure_ascii=False, indent=4)

    def get_json(self, data: list | dict):
        return json.dumps(data, ensure_ascii=False, indent=4)
