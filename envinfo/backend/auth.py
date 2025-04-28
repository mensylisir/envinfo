import reflex as rx

class AuthState(rx.State):
    token: str = rx.LocalStorage(sync=True)
    endpoints: str = rx.LocalStorage(sync=True)

    def set_token(self, token: str):
        self.token = token

    def set_endpoints(self, endpoints: str):
        self.endpoints = endpoints