import reflex as rx


def navbar(title: str):
    return rx.flex(
        rx.badge(
            rx.icon(tag="mails", size=28),
            rx.heading(title, size="6"),
            radius="large",
            align="center",
            color_scheme="blue",
            variant="surface",
            padding="0.65rem",
        ),
        rx.spacer(),
        rx.hstack(
            # rx.logo(),
            rx.color_mode.button(),
            align="center",
            spacing="3",
        ),
        spacing="2",
        flex_direction=["column", "column", "row"],
        align="center",
        width="100%",
        top="0px",
    )
