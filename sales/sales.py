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


def index() -> rx.Component:
    return rx.vstack(
        navbar("环境管理->模板管理"),
        rx.flex(
            rx.box(main_table(), width=["100%", "100%", "100%", "100%"]),
            # email_gen_ui(),
            spacing="6",
            width="100%",
            flex_direction=["column", "column", "column", "row"],
        ),
        height="100vh",
        bg=rx.color("accent", 1),
        width="100%",
        spacing="6",
        padding_x=["1.5em", "1.5em", "3em"],
        padding_y=["1em", "1em", "2em"],
    )


app = rx.App(
    theme=rx.theme(
        appearance="light", has_background=True, radius="large", accent_color="blue"
    ),
)
app.add_page(
    index,
    on_load=TemplateState.load_entries,
    title="Template Pages",
    description="Template Pages",
)

app.add_page(
    appset_index,
    route="/applicationsets",
    on_load=ApplicationSetsState.list_applicationsets,
    title="Appset Pages",
    description="Appset Pages",
)

app.add_page(
    app_index,
    route="/applications",
    on_load=ApplicationsState.list_applications,
    title="App Pages",
    description="App Pages",
)

app.add_page(
    pod_index,
    route="/pods",
    on_load=PodsState.list_pods,
    title="Pod Pages",
    description="Pod Pages",
)