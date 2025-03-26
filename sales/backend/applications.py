import reflex as rx

import asyncio
from sales.appset.app import get_applications
from sales.appset.app import get_applications_by_appset
from sales.appset.service import get_service_url
from sales.appset.secret import get_secret
from sales.appset.monitor import get_monitor
from sales.utils.json import json_to_object
from .models import Applications
from .models import ApplicationSets
import pyperclip


class ApplicationsState(rx.State):
    app: Applications | None = None
    # appset_name: str = ""
    applications: list[Applications] = []

    @rx.event
    def copy_to_clipboard(self, text):
        pyperclip.copy(text)
        return rx.window_alert("已复制到剪贴板")
    @rx.event
    def toggle_password(self, app: Applications):
        for index, app_in_state in enumerate(self.applications):
            if app_in_state.name == app.name:
                self.applications[index].show_password = not self.applications[index].show_password
                break

    def list_applications(self):
        result = get_applications()
        data = json_to_object(result.data)
        self.applications = []
        for item in data.items:
            application = Applications()
            application.name = item.metadata.name
            application.namespace = item.spec.destination.namespace
            application.description = ""
            application.action = "view"
            self.applications += [application]

    async def list_applications_by_appset(self, appset):
        result = get_applications_by_appset(appset)
        data = json_to_object(result.data)
        self.applications = []
        tasks = []
        for item in data.items:
            application = Applications()
            application.name = item.metadata.name
            application.namespace = item.spec.destination.namespace
            application.description = ""
            application.action = "view"
            namespace = item.spec.destination.namespace
            name = application.name
            application.monitor = get_monitor(namespace, name)
            service_task = get_service_url(namespace, name)
            secret_task = get_secret(namespace, name)
            tasks.append((application, service_task, secret_task))

        for application, service_task, secret_task in tasks:
            response, user = await asyncio.gather(service_task, secret_task)
            application.address = ""
            if response.data is not None:
                for res in response.data:
                    if hasattr(res, 'name') and res.name != "-":
                        application.address += "{}->{}".format(res.name, "{}:{}\n".format(res.ip, res.port))
                    elif res.ip != "-" and res.port != "-":
                        application.address += "{}:{}\n".format(res.ip, res.port)
                    else:
                        application.address = "-"
                self.applications.append(application)
            if user.data is not None:
                application.username = user.data.user
                application.password = user.data.password

