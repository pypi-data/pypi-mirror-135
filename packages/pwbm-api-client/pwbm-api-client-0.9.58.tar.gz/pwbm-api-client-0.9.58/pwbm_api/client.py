from .response import Response


class Client:
    def get(self, query):
        return Response(query.build())
