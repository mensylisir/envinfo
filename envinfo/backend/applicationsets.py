import json

import reflex as rx
from .models import ApplicationSets
from envinfo.backend.applications import ApplicationsState
from envinfo.template.manager import template_manager
from envinfo.utils.json import json_to_object
from envinfo.utils.json import object_to_json
from envinfo.appset.appset import create_applicationset
from envinfo.appset.appset import get_applicationsets
from envinfo.appset.appset import get_applicationsets_by_template
from .models import Template
class ApplicationSetsState(rx.State):
    applicationsets: list[ApplicationSets] = []

    @rx.var
    def get_cluster_name(self) -> str:
        return self.router.page.params.get("cluster_name", "")

    @rx.var
    def get_template_name(self) -> str:
        return self.router.page.params.get("template_name", "")

    def create_applicationset(self,form_data: dict):
        data = template_manager._cache[form_data["Template"]]
        result = json_to_object(json.dumps(data))
        self.get_template_name = result.metadata.name
        result.metadata.name = form_data["Name"]
        result.spec.template.spec.destination.namespace = form_data["Namespace"]
        result.spec.template.metadata.labels["app.kubernetes.io/created-by"] = form_data["Name"]
        for generator in result.spec.generators:
            for element in generator.list.elements:
                element.name = form_data["Namespace"] + "-" + element.name
        json_data = object_to_json(result)
        create_applicationset(self.get_cluster_name, json_data)
        # yield rx.redirect(f"/applications/{form_data['Name']}")
        yield rx.redirect(f"/clusters/{self.get_cluster_name}/templates/{self.get_template_name}/applicationsets/{form_data['Name']}/applications")
        # yield ApplicationsState.list_applications_by_appset(form_data["Name"])
        yield ApplicationsState.list_applications_by_appset()

    def list_applicationsets(self):
        result = get_applicationsets(self.get_cluster_name)
        data = json_to_object(result.data)
        self.applicationsets = []
        for item in data.items:
            applicationset = ApplicationSets()
            applicationset.name = item.metadata.name
            applicationset.alias_name = item.metadata.annotations["app.kubernetes.io/alias_name"]
            applicationset.description = item.metadata.annotations["app.kubernetes.io/description"]
            applicationset.action = "查看"
            self.applicationsets += [applicationset]


    def list_applicationsets_by_template(self):
        result = get_applicationsets_by_template(self.get_cluster_name, self.get_template_name)
        data = json_to_object(result.data)
        self.applicationsets = []
        for item in data.items:
            applicationset = ApplicationSets()
            applicationset.name = item.metadata.name
            applicationset.alias_name = item.metadata.annotations["app.kubernetes.io/alias_name"]
            applicationset.description = item.metadata.annotations["app.kubernetes.io/description"]
            applicationset.action = "查看"
            self.applicationsets += [applicationset]

