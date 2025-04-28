import aiohttp
import urllib3

from envinfo.response.http_response import HttpResponse
from envinfo.utils.relation import get_relation_info
from envinfo.utils.json import json_to_object
from envinfo.config.config import wrapped_config
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class AccessUrl:
    def __init__(self):
        self.name = None
        self.ip = None
        self.port = None
        self.type = None
        self.external_port = None

    def default(self):
        self.name = "-"
        self.ip = "-"
        self.port = "-"
        self.type = "-"
        self.external_port = "-"

    def __str__(self):
        name_str = self.name if self.name else "None"
        ip_str = self.ip if self.ip else "None"
        port_str = self.port if self.port else "None"
        type_str = self.type if self.type else "None"
        ext_port_str = self.external_port if self.external_port else "None"
        return f"AccessUrl(name={name_str}, ip={ip_str}, port={port_str})," f"type={type_str}, external_port={ext_port_str})"


async def get_service_url(namespace: str, instance_name: str, token: str, endpoints: str):
    info = get_relation_info(instance_name)
    if info["service"].startswith("-"):
        service_name = f'{namespace}{info["service"]}'
    else:
        service_name = info["service"]

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}',
    }
    url = f"https://{endpoints}/api/v1/namespaces/{namespace}/services/{service_name}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, ssl=False) as response:
                response.raise_for_status()
                json_data = await response.json()
                response = json_to_object(json_data)
                acessUrls = []
                for res in response.spec.ports:
                    accessUrl = AccessUrl()
                    accessUrl.type = response.spec.type
                    if accessUrl.type == "NodePort" or accessUrl.type == "LoadBalancer":
                        accessUrl.external_port = res.nodePort
                    if hasattr(res, 'name') and res.name != None:
                        accessUrl.name = res.name
                    else:
                        accessUrl.name = "-"
                    accessUrl.ip = response.spec.clusterIP
                    accessUrl.port = res.port
                    acessUrls.append(accessUrl)
                return HttpResponse(
                    code=200,
                    status="success",
                    data=acessUrls,
                    message=""
                )
    except aiohttp.ClientError as e:
        return HttpResponse(
            code=500,
            status="fail",
            data=[default()],
            message=str(e)
        )


def default():
    accessUrl = AccessUrl()
    accessUrl.name = "-"
    accessUrl.ip = "-"
    accessUrl.port = "-"
    return accessUrl