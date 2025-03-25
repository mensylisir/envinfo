from sales.utils.relation import get_relation_info
from sales.response.http_response import HttpResponse
import aiohttp
import base64
from sales.utils.json import json_to_object

headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6InZBWUppaENWVWVRcWN0Ykw5ZHhBSGktRE5ndnFTNk5UZ0xiLWtlWFM5eVUifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJ0YWljaHUtYWRtaW4iLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoidGFpY2h1LWFkbWluIiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQudWlkIjoiODVmYWNmMGUtMTg4MC00NDc5LTkwNWQtNzQyNTEyZjQ0MjM1Iiwic3ViIjoic3lzdGVtOnNlcnZpY2VhY2NvdW50Omt1YmUtc3lzdGVtOnRhaWNodS1hZG1pbiJ9.AycjOnhp2_7DweD6tqmD5PkWzs1Gl0_1af1uBdbcFnWcb6bP5BYaaqScntGQ4GXmfuXzJe2xkH2nVDUJDhNv8dEvcliHoAidRYY69A4OqopN75HZZp_nqoK_jXyRfFbs9AdrCkjJ3mL6NPkh_3sastGFas6-vpNZq1TPGqc8OJmKYDPCqwBahAWywp40nqOA7tcfDOKervGEZEWlMIncFGPM0H8Nv1DbywEEERE9eDw1zLfPBJ4aStgimGRRO0cC8mHU0mvt5ogZnhvkQvw9wgz6w5EgqmEujAMZGoWIWklG0lge8f0Xz3U0wgjIxkISzl38XHvDtAJQEWULogJVfA"
}

class UserInfo:
    user: str
    password: str

    def default(self):
        self.user = "-"
        self.password = "-"

async def get_secret(namespace: str, instance_name: str):
    info = get_relation_info(instance_name)
    print(info)
    userInfo = UserInfo()
    if info["secret"] == "":
        userInfo.user = info["user"]
        userInfo.password = info["password"]
        return HttpResponse(
            code=200,
            status="success",
            data=userInfo,
            message=""
        )
    elif info["secret"].startswith("-"):
        secret_name = f'{namespace}{info["secret"]}'
    else:
        secret_name = info["secret"]  # 修正为字符串
    url = f"https://172.30.1.12:6443/api/v1/namespaces/{namespace}/secrets/{secret_name}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, ssl=False) as response:
                response.raise_for_status()
                json_data = await response.json()
                response = json_to_object(json_data)
                userInfo.user = info["user"]
                password_key = info["secret-password"]
                try:
                    encoded_password = response.data[password_key]
                    decoded_password = base64.b64decode(encoded_password).decode('utf-8')
                    userInfo.password = decoded_password
                except (KeyError, TypeError):
                    print(f"无法获取 {password_key} 信息")
                    return HttpResponse(
                        code=500,
                        status="fail",
                        message=f"无法获取 {password_key} 信息"
                    )
                return HttpResponse(
                    code=200,
                    status="success",
                    data=userInfo,
                    message=""
                )
    except aiohttp.ClientError as e:
        print("请求出错：", e)
        return HttpResponse(
            code=500,
            status="fail",
            data=userInfo.default(),
            message=str(e)
        )