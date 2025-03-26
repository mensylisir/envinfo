# config.py
CLUSTER_CONFIG = {
    "cluster1": {
        "kubernetes": {
            "ip": "172.30.1.12",
            "port": "6443",
            "headers": {
                "Authorization": "eyJhbGciOiJSUzI1NiIsImtpZCI6InZBWUppaENWVWVRcWN0Ykw5ZHhBSGktRE5ndnFTNk5UZ0xiLWtlWFM5eVUifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJ0YWljaHUtYWRtaW4iLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoidGFpY2h1LWFkbWluIiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQudWlkIjoiODVmYWNmMGUtMTg4MC00NDc5LTkwNWQtNzQyNTEyZjQ0MjM1Iiwic3ViIjoic3lzdGVtOnNlcnZpY2VhY2NvdW50Omt1YmUtc3lzdGVtOnRhaWNodS1hZG1pbiJ9.AycjOnhp2_7DweD6tqmD5PkWzs1Gl0_1af1uBdbcFnWcb6bP5BYaaqScntGQ4GXmfuXzJe2xkH2nVDUJDhNv8dEvcliHoAidRYY69A4OqopN75HZZp_nqoK_jXyRfFbs9AdrCkjJ3mL6NPkh_3sastGFas6-vpNZq1TPGqc8OJmKYDPCqwBahAWywp40nqOA7tcfDOKervGEZEWlMIncFGPM0H8Nv1DbywEEERE9eDw1zLfPBJ4aStgimGRRO0cC8mHU0mvt5ogZnhvkQvw9wgz6w5EgqmEujAMZGoWIWklG0lge8f0Xz3U0wgjIxkISzl38XHvDtAJQEWULogJVfA"
            }
        },
        "monitor": {
            "ip": "172.30.1.12",
            "port": "32719"
        }
    },
}

class ConfigWrapper:
    def __init__(self, config):
        self._config = config

    def __getattr__(self, name):
        if name in self._config:
            value = self._config[name]
            if isinstance(value, dict):
                return ConfigWrapper(value)
            return value
        raise AttributeError(f"'ConfigWrapper' object has no attribute '{name}'")

    def __setattr__(self, name, value):
        if name == '_config':
            super().__setattr__(name, value)
        else:
            if isinstance(value, dict):
                self._config[name] = ConfigWrapper(value)
            else:
                self._config[name] = value


    def __getitem__(self, key):
        if key in self._config:
            value = self._config[key]
            if isinstance(value, dict):
                return ConfigWrapper(value)
            return value
        raise KeyError(f"'ConfigWrapper' object has no key '{key}'")

    def __setitem__(self, key, value):
        if isinstance(value, dict):
            self._config[key] = ConfigWrapper(value)
        else:
            self._config[key] = value

wrapped_config = ConfigWrapper(CLUSTER_CONFIG)