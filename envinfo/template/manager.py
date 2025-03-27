import os
from typing import Optional, Dict, Any
import yaml


class Manager:
    _instance = None
    _cache: Dict[str, Dict[str, Any]] = {}
    _template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_templates()
        return cls._instance

    def _load_templates(self):
        for filename in os.listdir(self._template_dir):
            if filename.endswith(".yaml"):
                name = filename[:-5]  # 去除.yaml 后缀
                file_path = os.path.join(self._template_dir, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = yaml.safe_load(f)
                        self._cache[name] = data
                except Exception as e:
                    print(f"加载模板 {filename} 失败: {str(e)}")

    def get_template(self, name: str) -> Optional[Dict[str, Any]]:
        return self._cache.get(name)


# 创建 Manager 实例
template_manager = Manager()


# 示例：获取指定 YAML 文件的内容
def get_yaml_content(yaml_name: str):
    return template_manager.get_template(yaml_name)
