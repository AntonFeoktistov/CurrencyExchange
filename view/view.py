import json


class View:
    def get_index_json(self):
        return json.dumps({"message": "Main Page"}, ensure_ascii=False, indent=4)

    def get_error_json(self, message: str):
        return json.dumps({"message": message}, ensure_ascii=False, indent=4)

    def get_json_from_list(self, data: list):
        return json.dumps(data, ensure_ascii=False, indent=4)

    def get_json_from_dict(self, data: dict):
        return json.dumps(data, ensure_ascii=False, indent=4)
