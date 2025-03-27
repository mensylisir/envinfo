import reflex as rx
from envinfo.views.navbar import navbar
from envinfo.components.header_cell import header_cell
from envinfo.backend.pods import PodsState
from envinfo.backend.models import Pods


@rx.page(route='/clusters/[cluster_name]/templates/[template_name]/applicationsets/[appset_name]/applications/[namespace]/[app_name]', on_load=PodsState.list_pods_by_app)
def pod_index() -> rx.Component:
    return rx.vstack(
        navbar("环境管理->Pod 管理"),
        rx.flex(
            rx.box(main_table(), width=["100%", "100%", "100%", "100%"]),
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


def _show_pods(pod: Pods):
    return rx.table.row(
        rx.table.row_header_cell(pod.name),
        rx.table.cell(pod.status),
        rx.table.cell(pod.namespace),
        style={"_hover": {"bg": rx.color("accent", 2)}},
        align="center",
    )


def main_table():
    return rx.fragment(
        rx.table.root(
            rx.table.header(
                rx.table.row(
                    header_cell("Pod 名称", "square-user-round"),
                    header_cell("状态", "briefcase"),
                    header_cell("命名空间", "briefcase"),
                ),
            ),
            rx.table.body(rx.foreach(PodsState.pods, _show_pods)),
            variant="surface",
            size="3",
            width="100%",
        ),
    )