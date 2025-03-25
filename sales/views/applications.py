import reflex as rx
from sales.views.navbar import navbar
from ..components.header_cell import header_cell
from ..backend.applications import ApplicationsState
from ..backend.models import Applications


@rx.page(route='/applications/[appset_name]')
def app_index() -> rx.Component:
    return rx.vstack(
        navbar("环境管理->中间件管理"),
        rx.flex(
            rx.box(main_table(), width=["100%", "100%", "100%", "100%"]),
            # email_gen_ui(),
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

def _show_applications(app: Applications):

    return rx.table.row(
        rx.table.row_header_cell(app.name),
        # rx.table.cell(app.namespace),
        rx.table.cell(
            rx.text(app.address, style={"whiteSpace": "pre-wrap"})
        ),
        rx.table.cell(app.username),
        # rx.table.cell(
        #     rx.input(
        #         type="text",
        #         value=app.password,
        #         disabled=False,
        #     )
        # ),
        rx.table.cell(
            rx.hstack(
                rx.cond(
                    ~app.show_password,  # 使用位运算符取反
                    rx.input(
                        type="password",
                        value=app.password,
                        disabled=True,
                    ),
                    rx.input(
                        type="text",
                        value=app.password,
                        disabled=True,
                    )
                ),
                rx.button(
                    rx.cond(
                        ~app.show_password,  # 使用位运算符取反
                        rx.icon("eye"),
                        rx.icon("eye-off")
                    ),
                    on_click=lambda: ApplicationsState.toggle_password(app),
                    color_scheme="blue",
                    style={
                        "border": "none",
                        "padding": "0.2em",
                        "background": "none",
                        "width": "2em",
                        "height": "2em",
                        "color": "#0090ff",
                    },
                ),
                rx.button(
                    rx.icon("copy"),
                    on_click=lambda: ApplicationsState.copy_to_clipboard(app.password),
                    style={
                        "border": "none",
                        "padding": "0.2em",
                        "background": "none",
                        "width": "2em",
                        "height": "2em",
                        "color": "#0090ff",
                    },
                ),
                style={
                    "border": "0px solid #ccc",
                    "border_radius": "4px",
                    "align_items": "center",
                    "padding": "0.2em",
                    "width": "auto",
                }
            )
        ),
        rx.table.cell(
            rx.dialog.root(
                rx.dialog.trigger(
                    rx.link(
                        rx.button(
                            rx.icon("briefcase", size=18),
                            rx.text(app.action),
                            color_scheme="blue",
                        ),
                        href=app.monitor
                    )
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
                    header_cell("中间件名称", "square-user-round"),
                    # header_cell("所属命名空间", "briefcase"),
                    header_cell("访问地址", "briefcase"),
                    header_cell("用户名", "briefcase"),
                    header_cell("密码", "briefcase"),
                    header_cell("监控", "cog"),
                ),
            ),
            rx.table.body(rx.foreach(ApplicationsState.applications, _show_applications)),
            variant="surface",
            size="3",
            width="100%",
        ),
    )