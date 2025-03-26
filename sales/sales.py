import reflex as rx

from .backend.template import TemplateState
from .backend.applicationsets import ApplicationSetsState
from .backend.applications import ApplicationsState
from .backend.pods import PodsState
from .views.navbar import navbar
from .views.template import main_table
from .views.applicationsets import appset_index
from .views.applications import app_index
from .views.pods import pod_index
from .views.template import template_index




app = rx.App(
    theme=rx.theme(
        appearance="light", has_background=True, radius="large", accent_color="blue"
    ),
)
# app.add_page(
#     template_index,
#     route="/clusters/[cluster_name]/templates",
#     on_load=TemplateState.load_entries,
#     title="Template Pages",
#     description="Template Pages",
# )

# app.add_page(
#     appset_index,
#     route="/applicationsets",
#     on_load=ApplicationSetsState.list_applicationsets,
#     title="Appset Pages",
#     description="Appset Pages",
# )
#
# app.add_page(
#     app_index,
#     route="/applications",
#     on_load=ApplicationsState.list_applications,
#     title="App Pages",
#     description="App Pages",
# )
#
# app.add_page(
#     pod_index,
#     route="/pods",
#     on_load=PodsState.list_pods,
#     title="Pod Pages",
#     description="Pod Pages",
# )