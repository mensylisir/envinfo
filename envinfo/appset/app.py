import requests
import urllib3

from envinfo.response.http_response import HttpResponse
from envinfo.backend.models import ApplicationSets
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from envinfo.config.config import wrapped_config
def get_applications(token, endpoints):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}',
    }
    url = f"https://{endpoints}/apis/argoproj.io/v1alpha1/namespaces/argocd-system/applications"
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

def get_application_by_appname(app_name, token, endpoints):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}',
    }
    url = f"https://{endpoints}/apis/argoproj.io/v1alpha1/namespaces/argocd-system/applications/{app_name}"
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

def get_applications_by_appset(appset_name, token, endpoints):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}',
    }
    url = f"https://{endpoints}/apis/argoproj.io/v1alpha1/namespaces/argocd-system/applications?labelSelector=app.kubernetes.io/created-by%3D{appset_name}"
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