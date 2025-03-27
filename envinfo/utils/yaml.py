import yaml


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

class DictToObjectYamlDumper(yaml.Dumper):
    def represent_data(self, data):
        if isinstance(data, DictToObject):
            result = {}
            for attr in dir(data):
                if not attr.startswith("__"):
                    result[attr] = getattr(data, attr)
            return self.represent_dict(result)
        return super().represent_data(data)

def yaml_to_object(yaml_content):
    try:
        data = yaml.safe_load(yaml_content)
        return DictToObject(data)
    except yaml.YAMLError as e:
        print(f"解析 YAML 时出错: {e}")
        return None

def object_to_yaml(obj):
    try:
        return yaml.dump(obj, Dumper=DictToObjectYamlDumper)
    except yaml.YAMLError as e:
        print(f"转换为 YAML 时出错: {e}")
        return None
