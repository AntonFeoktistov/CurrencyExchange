import json


class View:

    @staticmethod
    def get_index_json():
        return json.dumps({"message": "Main Page"}, ensure_ascii=False, indent=4)

    @staticmethod
    def get_error_json(message: str):
        return json.dumps({"message": message}, ensure_ascii=False, indent=4)

    @staticmethod
    def get_json_from_list(data: list):
        return json.dumps(data, ensure_ascii=False, indent=4)

    @staticmethod
    def get_json_from_dict(data: dict):
        return json.dumps(data, ensure_ascii=False, indent=4)
