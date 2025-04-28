import reflex as rx
import uuid

class Template(rx.Base):
    name: str = ""
    alias_name: str = ""
    description: str = ""
    action: str = ""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class ApplicationSets(rx.Base):
    name: str = ""
    alias_name: str = ""
    description: str = ""
    action: str = ""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class Applications(rx.Base):
    name: str = ""
    namespace: str = ""
    type: str = ""
    cluster_ip: str = ""
    external_port: str = ""
    port: str = ""
    address: str = ""
    username: str = ""
    password: str = ""
    monitor: str = ""
    action: str = ""
    show_password: bool = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class Pods(rx.Base):
    name: str = ""
    status: str = ""
    namespace: str = ""
    parent: str = ""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
