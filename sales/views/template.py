import reflex as rx

from ..backend.template import Template
from ..backend.template import TemplateState
from ..backend.applicationsets import ApplicationSetsState
from ..components.form_field import form_field
from ..components.header_cell import header_cell

def _show_templates(tp: Template):
    return rx.table.row(
        rx.table.row_header_cell(tp.alias_name),
        rx.table.cell(tp.description),
        # rx.table.cell(tp.action),
        rx.table.cell(
            rx.dialog.root(
                rx.dialog.trigger(
                    rx.button(
                        rx.icon("briefcase", size=18),
                        rx.text(tp.action),
                        color_scheme="blue",
                        # on_click=State.create_application(tp),
                        # loading=State.gen_response,
                        style={
                            "margin_right": "1em",
                        },
                    ),
                ),
                _create_application_from_template(tp.name)
            ),
            rx.link(
                rx.button(
                    rx.icon("briefcase", size=18),
                    rx.text("view"),
                    color_scheme="blue",
                    on_click=ApplicationSetsState.list_applicationsets_by_template(tp),
                    # loading=State.gen_response,
                ),
                href=f"/applicationsets/{tp.name}",
            ),
        ),
        style={"_hover": {"bg": rx.color("accent", 2)}},
        align="center",
    )


def _create_application_from_template(tp_name: str) -> rx.Component:
    return rx.dialog.content(
        rx.box(
            rx.form.root(
                rx.vstack(
                    # 对话框标题
                    rx.heading("创建应用", font_size="20px", color="blue.500", margin_bottom="10px"),
                    # 应用名称输入框
                    form_field(
                        "Name",
                        "Application Name",
                        "text",
                        "Name",
                        "user"
                    ),
                    # 命名空间输入框
                    form_field(
                        "Namespace",
                        "Application Namespace",
                        "text",
                        "Namespace",
                        "map-pinned"
                    ),
                    # 隐藏的模板名称输入框
                    rx.form.field(
                        rx.input(
                            type="text",
                            default_value=tp_name,
                            value=tp_name,
                            display="none",
                            name="Template"
                        ),
                        name="Template"
                    ),
                    # 按钮容器
                    rx.hstack(
                        # 关闭按钮
                        rx.dialog.close(
                            rx.button(
                                "Close",
                                variant="soft",
                                color_scheme="gray",
                                padding_x="15px",
                                padding_y="8px",
                                border_radius="5px",
                            ),
                        ),
                        # 提交按钮
                        rx.form.submit(
                            rx.button(
                                "Submit",
                                color_scheme="blue",
                                padding_x="15px",
                                padding_y="8px",
                                border_radius="5px",
                            ),
                        ),
                        justify="end",
                        margin_top="15px",
                    ),
                ),
                on_submit=ApplicationSetsState.create_applicationset,
                reset_on_submit=False,
            ),
            padding="20px",  # 内边距
            background_color="white",  # 背景色
            border=f"2px solid {rx.color('accent', 7)}",
            border_radius="15px",  # 圆角
            box_shadow="0 4px 8px rgba(0, 0, 0, 0.1)",  # 阴影
        ),
        width="100%",
        max_width="450px",
        justify=["end", "end", "start"],
        padding="0",  # 移除对话框内容的额外空白
    )


def main_table():
    return rx.fragment(
        rx.table.root(
            rx.table.header(
                rx.table.row(
                    header_cell("模板名称", "square-user-round"),
                    header_cell("描述", "briefcase"),
                    header_cell("操作", "cog"),
                ),
            ),
            rx.table.body(rx.foreach(TemplateState.templates, _show_templates)),
            variant="surface",
            size="3",
            width="100%",
        ),
    )
