import json


class DictToObject:
    def __init__(self, data):
        for key, value in data.items():
            if isinstance(value, dict):
                setattr(self, key, DictToObject(value))
            elif isinstance(value, list):
                setattr(self, key, [DictToObject(item) if isinstance(item, dict) else item for item in value])
            else:
                setattr(self, key, value)

    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, value):
        setattr(self, key, value)


class DictToObjectEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, DictToObject):
            # 将 DictToObject 实例转换为字典
            result = {}
            for attr in dir(obj):
                if not attr.startswith("__"):
                    result[attr] = getattr(obj, attr)
            return result
        return super().default(obj)

def json_to_object(json_content):
    if isinstance(json_content, dict):
        json_content = json.dumps(json_content)
    try:
        data = json.loads(json_content)
        return DictToObject(data)
    except json.JSONDecodeError as e:
        print(f"转换为 JSON 时出错: {e}")
        return None


def object_to_json(obj):
    try:
        return json.dumps(obj, cls=DictToObjectEncoder)
    except TypeError as e:
        print(f"转换为 JSON 时出错: {e}")
        return None
