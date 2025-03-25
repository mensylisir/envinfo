class HttpResponse:
    def __init__(self, code=200, status="success", data=None, message=""):
        self.code = code
        self.status = status
        self.data = data
        self.message = message

    def to_dict(self):
        return {
            "code": self.code,
            "status": self.status,
            "data": self.data,
            "message": self.message
        }
