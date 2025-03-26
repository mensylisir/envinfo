import reflex as rx
from sales.appset.pods import get_pods
from sales.appset.pods import get_pod_logs
from sales.utils.json import json_to_object
from .models import Pods


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

    def list_pods(self, namesppace, app_name):
        result = get_pods(self.get_cluster_name, namesppace)
        data = json_to_object(result.data)
        self.pods = []
        for item in data.items:
            pod = Pods()
            pod.name = item.metadata.name
            pod.status = item.status.phase
            pod.namespace = item.metadata.namespace
            self.pods += [pod]

    def list_pods_by_app(self, namesppace, app_name):
        result = get_pods(self.get_cluster_name, namesppace)
        data = json_to_object(result.data)
        self.pods = []
        for item in data.items:
            if item.metadata.name.startswith(app_name):
                pod = Pods()
                pod.name = item.metadata.name
                pod.status = item.status.phase
                pod.namespace = item.metadata.namespace
                pod.parent = app_name
                self.pods += [pod]
