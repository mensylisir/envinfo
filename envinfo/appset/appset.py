import requests
import urllib3
from envinfo.backend.template import TemplateState

from envinfo.response.http_response import HttpResponse
from envinfo.config.config import wrapped_config
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_applicationsets(token, endpoints):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}',
    }
    url = f"https://{endpoints}/apis/argoproj.io/v1alpha1/namespaces/argocd-system/applicationsets"
    try:
        with requests.get(url, headers=headers, verify=False) as response:
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

def get_applicationsets_by_template(template_name, token, endpoints):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}',
    }
    url = f"https://{endpoints}/apis/argoproj.io/v1alpha1/namespaces/argocd-system/applicationsets?labelSelector=app.kubernetes.io/from-template%3D{template_name}"
    try:
        with requests.get(url, headers=headers, verify=False) as response:
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

def create_applicationset(data, token, endpoints):
    url = f"https://{endpoints}/apis/argoproj.io/v1alpha1/namespaces/argocd-system/applicationsets"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}',
    }
    if isinstance(data, str):
        import json
        data = json.loads(data)
    try:
        with requests.post(url, json=data, headers=headers, verify=False, timeout=10) as response:
            response.raise_for_status()
            return HttpResponse(
                code=200,
                status="success",
                data=response.json(),
                message=""
            )
    except requests.exceptions.RequestException as e:
        print(str(e))
        return HttpResponse(
            code=500,
            status="fail",
            message=str(e)
        )