from sales.utils.relation import get_relation_info
from sales.config.config import wrapped_config
def get_monitor(cluster_name: str, namespace: str, instance_name: str):
    info = get_relation_info(instance_name)
    if info["monitor"] != "":
        endpoint = f"{wrapped_config[cluster_name].monitor.ip}:{wrapped_config[cluster_name].monitor.port}"
        return info["monitor"].format(endpoint, namespace)
    return info["monitor"]