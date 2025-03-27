import reflex as rx
from envinfo.appset.pods import get_pods
from envinfo.appset.pods import get_pod_logs
from envinfo.appset.app import get_application_by_appname
from envinfo.utils.json import json_to_object
from .models import Pods
from envinfo.backend.applications import ApplicationsState


class PodsState(rx.State):
    pods: list[Pods] = []

    @rx.var
    def get_cluster_name(self) -> str:
        return self.router.page.params.get("cluster_name", "")

    @rx.var
    def get_template_name(self) -> str:
        return self.router.page.params.get("template_name", "")

    @rx.var
    def get_appset_name(self) -> str:
        return self.router.page.params.get("appset_name", "")

    @rx.var
    def get_app_name(self) -> str:
        return self.router.page.params.get("app_name", "")

    @rx.var
    def get_namespace(self) -> str:
        return self.router.page.params.get("namespace", "")

    def list_pods(self):
        result = get_pods(self.get_cluster_name, self.get_namespace)
        data = json_to_object(result.data)
        self.pods = []
        for item in data.items:
            pod = Pods()
            pod.name = item.metadata.name
            pod.status = item.status.phase
            pod.namespace = item.metadata.namespace
            self.pods += [pod]

    def list_pods_by_app(self):
        result = get_pods(self.get_cluster_name, self.get_namespace)
        data = json_to_object(result.data)
        self.pods = []
        for item in data.items:
            if item.metadata.name.startswith(self.get_app_name):
                pod = Pods()
                pod.name = item.metadata.name
                pod.status = item.status.phase
                pod.namespace = item.metadata.namespace
                pod.parent = self.get_app_name
                self.pods += [pod]