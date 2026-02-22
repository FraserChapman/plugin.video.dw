import requests

class DWGraphQL:
    BASE = "https://webapi.dw.com/graphql"

    def __init__(self, session=None, timeout=60):
        self.s = session or requests.Session()
        self.timeout = timeout

    def execute(self, operation_name: str, query: str, variables: dict):
        payload = {
            "operationName": operation_name,
            "query": query,
            "variables": variables
        }
        r = self.s.post(self.BASE, json=payload, timeout=self.timeout)
        r.raise_for_status()
        data = r.json()
        if "errors" in data:
            raise RuntimeError(data["errors"])
        return data["data"]