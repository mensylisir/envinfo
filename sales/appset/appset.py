import requests
import urllib3
from sales.backend.template import TemplateState

from sales.response.http_response import HttpResponse
from sales.config.config import wrapped_config
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_applicationsets(cluster_name):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {wrapped_config[cluster_name].kubernetes.headers["Authorization"]}',
    }
    url = f"https://{wrapped_config[cluster_name].kubernetes.ip}:{wrapped_config[cluster_name].kubernetes.port}/apis/argoproj.io/v1alpha1/namespaces/argocd-system/applicationsets"
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

def get_applicationsets_by_template(cluster_name, template_name):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {wrapped_config[cluster_name].kubernetes.headers["Authorization"]}',
    }
    url = f"https://{wrapped_config[cluster_name].kubernetes.ip}:{wrapped_config[cluster_name].kubernetes.port}/apis/argoproj.io/v1alpha1/namespaces/argocd-system/applicationsets?labelSelector=app.kubernetes.io/from-template%3D{template_name}"
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

def create_applicationset(cluster_name, data):
    url = f"https://{wrapped_config[cluster_name].kubernetes.ip}:{wrapped_config[cluster_name].kubernetes.port}/apis/argoproj.io/v1alpha1/namespaces/argocd-system/applicationsets"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {wrapped_config[cluster_name].kubernetes.headers["Authorization"]}',
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