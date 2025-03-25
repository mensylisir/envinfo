import json

import reflex as rx
from .models import ApplicationSets
from sales.template.manager import template_manager
from sales.utils.json import json_to_object
from sales.utils.json import object_to_json
from sales.appset.appset import create_applicationset
from sales.appset.appset import get_applicationsets
from sales.appset.appset import get_applicationsets_by_template
from .models import Template
class ApplicationSetsState(rx.State):
    applicationsets: list[ApplicationSets] = []
    def create_applicationset(self,form_data: dict):
        print(form_data)
        data = template_manager._cache[form_data["Template"]]
        result = json_to_object(json.dumps(data))
        result.metadata.name = form_data["Name"]
        result.spec.template.spec.destination.namespace = form_data["Namespace"]
        result.spec.template.metadata.labels["app.kubernetes.io/created-by"] = form_data["Namespace"]
        for generator in result.spec.generators:
            for element in generator.list.elements:
                element.name = form_data["Namespace"] + "-" + element.name
        json_data = object_to_json(result)
        # print(json_data)
        create_applicationset(json_data)

    def list_applicationsets(self):
        result = get_applicationsets()
        data = json_to_object(result.data)
        print('#################################################################')
        self.applicationsets = []
        for item in data.items:
            applicationset = ApplicationSets()
            applicationset.name = item.metadata.name
            applicationset.description = item.metadata.annotations["app.kubernetes.io/description"]
            applicationset.action = "view"
            self.applicationsets += [applicationset]
        print(self.applicationsets)


    def list_applicationsets_by_template(self, template: Template):
        result = get_applicationsets_by_template(template.name)
        data = json_to_object(result.data)
        print('#################################################################')
        self.applicationsets = []
        for item in data.items:
            applicationset = ApplicationSets()
            applicationset.name = item.metadata.name
            applicationset.description = item.metadata.annotations["app.kubernetes.io/description"]
            applicationset.action = "view"
            self.applicationsets += [applicationset]
        print(self.applicationsets)

