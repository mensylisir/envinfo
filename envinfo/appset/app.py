import requests
import urllib3

from envinfo.response.http_response import HttpResponse
from envinfo.backend.models import ApplicationSets
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from envinfo.config.config import wrapped_config
def get_applications(cluster_name):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {wrapped_config[cluster_name].kubernetes.headers["Authorization"]}',
    }
    url = f"https://{wrapped_config[cluster_name].kubernetes.ip}:{wrapped_config[cluster_name].kubernetes.port}/apis/argoproj.io/v1alpha1/namespaces/argocd-system/applications"
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

def get_application_by_appname(cluster_name, app_name):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {wrapped_config[cluster_name].kubernetes.headers["Authorization"]}',
    }
    url = f"https://{wrapped_config[cluster_name].kubernetes.ip}:{wrapped_config[cluster_name].kubernetes.port}/apis/argoproj.io/v1alpha1/namespaces/argocd-system/applications/{app_name}"
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

def get_applications_by_appset(cluster_name, appset_name):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {wrapped_config[cluster_name].kubernetes.headers["Authorization"]}',
    }
    url = f"https://{wrapped_config[cluster_name].kubernetes.ip}:{wrapped_config[cluster_name].kubernetes.port}/apis/argoproj.io/v1alpha1/namespaces/argocd-system/applications?labelSelector=app.kubernetes.io/created-by%3D{appset_name}"
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