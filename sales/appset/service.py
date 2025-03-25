import aiohttp
from sales.response.http_response import HttpResponse
from sales.utils.relation import get_relation_info
from sales.utils.json import json_to_object

headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6InZBWUppaENWVWVRcWN0Ykw5ZHhBSGktRE5ndnFTNk5UZ0xiLWtlWFM5eVUifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJ0YWljaHUtYWRtaW4iLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoidGFpY2h1LWFkbWluIiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQudWlkIjoiODVmYWNmMGUtMTg4MC00NDc5LTkwNWQtNzQyNTEyZjQ0MjM1Iiwic3ViIjoic3lzdGVtOnNlcnZpY2VhY2NvdW50Omt1YmUtc3lzdGVtOnRhaWNodS1hZG1pbiJ9.AycjOnhp2_7DweD6tqmD5PkWzs1Gl0_1af1uBdbcFnWcb6bP5BYaaqScntGQ4GXmfuXzJe2xkH2nVDUJDhNv8dEvcliHoAidRYY69A4OqopN75HZZp_nqoK_jXyRfFbs9AdrCkjJ3mL6NPkh_3sastGFas6-vpNZq1TPGqc8OJmKYDPCqwBahAWywp40nqOA7tcfDOKervGEZEWlMIncFGPM0H8Nv1DbywEEERE9eDw1zLfPBJ4aStgimGRRO0cC8mHU0mvt5ogZnhvkQvw9wgz6w5EgqmEujAMZGoWIWklG0lge8f0Xz3U0wgjIxkISzl38XHvDtAJQEWULogJVfA"
}

class AccessUrl:
    def __init__(self):
        self.name = None
        self.ip = None
        self.port = None

    def default(self):
        self.name = "-"
        self.ip = "-"
        self.port = "-"

    def __str__(self):
        name_str = self.name if self.name else "None"
        ip_str = self.ip if self.ip else "None"
        port_str = self.port if self.port else "None"
        return f"AccessUrl(name={name_str}, ip={ip_str}, port={port_str})"


async def get_service_url(namespace: str, instance_name: str):
    info = get_relation_info(instance_name)
    print(info)
    if info["service"].startswith("-"):
        service_name = f'{namespace}{info["service"]}'
    else:
        service_name = info["service"]
    url = f"https://172.30.1.12:6443/api/v1/namespaces/{namespace}/services/{service_name}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, ssl=False) as response:
                response.raise_for_status()
                json_data = await response.json()
                response = json_to_object(json_data)
                acessUrls = []
                for res in response.spec.ports:
                    accessUrl = AccessUrl()
                    if hasattr(res, 'name') and res.name != None:
                        accessUrl.name = res.name
                    else:
                        accessUrl.name = "-"
                    accessUrl.ip = response.spec.clusterIP
                    accessUrl.port = res.port
                    print(accessUrl)
                    acessUrls.append(accessUrl)
                print([str(url) for url in acessUrls])
                return HttpResponse(
                    code=200,
                    status="success",
                    data=acessUrls,
                    message=""
                )
    except aiohttp.ClientError as e:
        print("请求出错：", e)
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