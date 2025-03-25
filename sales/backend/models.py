import reflex as rx
import uuid

class Template(rx.Model, table=False):
    id: str
    name: str = ""
    alias_name: str = ""
    description: str = ""
    action: str = ""

    def __init__(self, **kwargs):
        if 'id' not in kwargs:
            kwargs['id'] = str(uuid.uuid4())
        self.id = kwargs['id']
        super().__init__(**kwargs)

class ApplicationSets(rx.Model, table=False):
    id: str
    name: str = ""
    alias_name: str = ""
    description: str = ""
    action: str = ""

    def __init__(self, **kwargs):
        if 'id' not in kwargs:
            kwargs['id'] = str(uuid.uuid4())
        self.id = kwargs['id']
        super().__init__(**kwargs)

class Applications(rx.Model, table=False):
    id: str
    name: str = ""
    namespace: str = ""
    address: str = ""
    username: str = ""
    password: str = ""
    monitor: str = ""
    action: str = ""

    def __init__(self, **kwargs):
        if 'id' not in kwargs:
            kwargs['id'] = str(uuid.uuid4())
        self.id = kwargs['id']
        super().__init__(**kwargs)
