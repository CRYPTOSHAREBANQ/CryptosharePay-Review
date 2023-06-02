

class CustomHttpRequest:
    def __init__(self, method = "GET", headers = None, data = None) -> None:
        
        self.method = method
        self.headers = headers
        self.data = data
