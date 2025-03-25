import requests
from sales.response.http_response import HttpResponse

headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6InZBWUppaENWVWVRcWN0Ykw5ZHhBSGktRE5ndnFTNk5UZ0xiLWtlWFM5eVUifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJ0YWljaHUtYWRtaW4iLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoidGFpY2h1LWFkbWluIiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQudWlkIjoiODVmYWNmMGUtMTg4MC00NDc5LTkwNWQtNzQyNTEyZjQ0MjM1Iiwic3ViIjoic3lzdGVtOnNlcnZpY2VhY2NvdW50Omt1YmUtc3lzdGVtOnRhaWNodS1hZG1pbiJ9.AycjOnhp2_7DweD6tqmD5PkWzs1Gl0_1af1uBdbcFnWcb6bP5BYaaqScntGQ4GXmfuXzJe2xkH2nVDUJDhNv8dEvcliHoAidRYY69A4OqopN75HZZp_nqoK_jXyRfFbs9AdrCkjJ3mL6NPkh_3sastGFas6-vpNZq1TPGqc8OJmKYDPCqwBahAWywp40nqOA7tcfDOKervGEZEWlMIncFGPM0H8Nv1DbywEEERE9eDw1zLfPBJ4aStgimGRRO0cC8mHU0mvt5ogZnhvkQvw9wgz6w5EgqmEujAMZGoWIWklG0lge8f0Xz3U0wgjIxkISzl38XHvDtAJQEWULogJVfA"
}
def get_applicationsets():
    url = "https://172.30.1.12:6443/apis/argoproj.io/v1alpha1/namespaces/argocd-system/applicationsets"
    try:
        with requests.get(url, headers=headers, verify=False) as response:
            response.raise_for_status()
            # print("请求成功，响应内容：", response.json())
            return HttpResponse(
                code=200,
                status="success",
                data=response.json(),
                message=""
            )
    except requests.exceptions.RequestException as e:
            print("请求出错：", e)
            return HttpResponse(
                code=500,
                status="fail",
                message=str(e)
            )

def get_applicationsets_by_template(template_name):
    url = f"https://172.30.1.12:6443/apis/argoproj.io/v1alpha1/namespaces/argocd-system/applicationsets?labelSelector=app.kubernetes.io/from-template%3D{template_name}"
    print(url)
    try:
        with requests.get(url, headers=headers, verify=False) as response:
            response.raise_for_status()
            # print("请求成功，响应内容：", response.json())
            return HttpResponse(
                code=200,
                status="success",
                data=response.json(),
                message=""
            )
    except requests.exceptions.RequestException as e:
            print("请求出错：", e)
            return HttpResponse(
                code=500,
                status="fail",
                message=str(e)
            )

def create_applicationset(data):
    url = "https://172.30.1.12:6443/apis/argoproj.io/v1alpha1/namespaces/argocd-system/applicationsets"
    # 如果 data 是字符串，先将其转换为字典
    if isinstance(data, str):
        import json
        data = json.loads(data)
    try:
        # 每次请求都关闭连接
        with requests.post(url, json=data, headers=headers, verify=False, timeout=10) as response:
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