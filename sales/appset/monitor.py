from sales.utils.relation import get_relation_info
def get_monitor(namespace: str, instance_name: str):
    info = get_relation_info(instance_name)
    if info["monitor"] != "":
        return info["monitor"].format(namespace)