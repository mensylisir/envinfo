import urllib3

from envinfo.utils.relation import get_relation_info
from envinfo.response.http_response import HttpResponse
import aiohttp
import base64
from envinfo.utils.json import json_to_object
from envinfo.config.config import wrapped_config
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class UserInfo:
    user: str
    password: str

    def default(self):
        self.user = "-"
        self.password = "-"

async def get_secret(namespace: str, instance_name: str, token: str, endpoints: str):
    info = get_relation_info(instance_name)
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
        secret_name = info["secret"]

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}',
    }
    url = f"https://{endpoints}/api/v1/namespaces/{namespace}/secrets/{secret_name}"
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
        return HttpResponse(
            code=500,
            status="fail",
            data=userInfo.default(),
            message=str(e)
        )