import json
import os

import reflex as rx

from .models import Template
from sales.template.manager import template_manager
from sales.utils.json import json_to_object

class TemplateState(rx.State):
    """The app state."""

    current_template: Template = Template()
    templates: list[Template] = []
    def load_entries(self):
        self.get_templates()

    def get_template(self, tp: Template):
        self.current_template = tp

    def get_templates(self):
        self.templates= []
        for key, value in template_manager._cache.items():
            result = json_to_object(json.dumps(value))
            template = Template()
            template.name = result.metadata.labels["app.kubernetes.io/from-template"]
            template.description = result.metadata.annotations["app.kubernetes.io/description"]
            template.alias_name = result.metadata.annotations["app.kubernetes.io/alias_name"]
            template.action = "create"
            self.templates += [template]