import requests
import urllib3

from envinfo.response.http_response import HttpResponse
from envinfo.config.config import wrapped_config
import os
from envinfo.utils.json import object_to_json
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_pods(namespace, token, endpoints):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}',
    }
    url = f"https://{endpoints}/api/v1/namespaces/{namespace}/pods"
    try:
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        return HttpResponse(
            code=200,
            status="success",
            data=response.json(),
            message=""
        )
    except requests.exceptions.RequestException as e:
        return HttpResponse(
            code=500,
            status="fail",
            message=str(e)
        )

def get_pod_logs(cluster_name, namespace, pod_name, token, endpoints):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}',
    }
    url = f"https://{endpoints}/api/v1/namespaces/{namespace}/pods/{pod_name}/log"
    try:
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        return HttpResponse(
            code=200,
            status="success",
            data=response.text,
            message=""
        )
    except requests.exceptions.RequestException as e:
        return HttpResponse(
            code=500,
            data="",
            status="fail",
            message=str(e)
        )