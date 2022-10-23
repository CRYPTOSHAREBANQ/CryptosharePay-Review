from rest_framework.response  import Response


class GenericCORSResponse:
    def __init__(self, headers = {}, response = {}, status = 200):
        self.headers = {
            'Access-Control-Allow-Headers': 'Content-Type, X-API-Key, X-Customer-Id, X-Email, X-Password',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        }
        self.headers.update(headers)

        self.response = response
        self.status = status

        self.object = Response(
            self.response,
            headers = self.headers,
            status = self.status
        )

    def get_response(self):
        return self.object