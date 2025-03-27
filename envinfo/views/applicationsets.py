import reflex as rx
from envinfo.views.navbar import navbar
from ..components.header_cell import header_cell
from ..backend.models import ApplicationSets
from ..backend.applicationsets import ApplicationSetsState
from ..backend.applications import ApplicationsState


@rx.page(route='/clusters/[cluster_name]/templates/[template_name]/applicationsets', on_load=ApplicationSetsState.list_applicationsets_by_template)
def appset_index() -> rx.Component:
    return rx.vstack(
        navbar("环境管理->实例管理"),
        rx.flex(
            rx.box(main_table(), width=["100%", "100%", "100%", "100%"]),
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



@rx.event
def _show_applicationsets(appset: ApplicationSets):
    return rx.table.row(
        rx.table.row_header_cell(appset.name),
        rx.table.cell(appset.description),
        rx.table.cell(
            rx.dialog.root(
                rx.dialog.trigger(
                    rx.link(
                        rx.button(
                            rx.icon("briefcase", size=18),
                            rx.text(appset.action),
                            color_scheme="blue",
                            # on_click=ApplicationsState.list_applications_by_appset(appset.name)
                            on_click=ApplicationsState.list_applications_by_appset()
                        ),
                        # href=f"/applications/{appset.name}",
                        href=f"/clusters/{ApplicationSetsState.get_cluster_name}/templates/{ApplicationsState.get_template_name}/applicationsets/{appset.name}/applications"
                    ),
                ),
            ),
        ),
        style={"_hover": {"bg": rx.color("accent", 2)}},
        align="center",
    )


def main_table():
    return rx.fragment(
        rx.table.root(
            rx.table.header(
                rx.table.row(
                    header_cell("实例名称", "square-user-round"),
                    header_cell("描述", "briefcase"),
                    header_cell("查看", "cog"),
                ),
            ),
            rx.table.body(rx.foreach(ApplicationSetsState.applicationsets, _show_applicationsets)),
            variant="surface",
            size="3",
            width="100%",
        ),
    )