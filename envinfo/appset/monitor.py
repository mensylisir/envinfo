from envinfo.utils.relation import get_relation_info
from envinfo.config.config import wrapped_config
def get_monitor(granafa_url: str, namespace: str, instance_name: str):
    info = get_relation_info(instance_name)
    if info["monitor"] != "":
        endpoint = granafa_url
        return info["monitor"].format(endpoint, namespace)
    return info["monitor"]