import reflex as rx

class AuthState(rx.State):
    token: str = rx.LocalStorage(sync=True)
    endpoints: str = rx.LocalStorage(sync=True)
    grafana_nodeport: str = rx.LocalStorage(sync=True)

    def set_token(self, token: str):
        self.token = token

    def set_endpoints(self, endpoints: str):
        self.endpoints = endpoints

    def set_grafana_nodeport(self, grafana_nodeport: str):
        self.grafana_nodeport = grafana_nodeport