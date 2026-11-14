"""Per-call protected HTTP client. Tokens and results are never globally cached."""
import requests


class DocumentClientError(RuntimeError):
    pass


class DocumentsClient:
    def __init__(self, url, token, *, timeout=65, request=None):
        self.url, self.token, self.timeout = url.rstrip("/"), token, timeout
        self.request = request or requests.request

    def call(self, method, path, body=None):
        response = None
        try:
            response = self.request(method, self.url + "/documents/operator" + path,
                headers={"Authorization": "Bearer " + self.token}, json=body, timeout=(3, self.timeout),
                allow_redirects=False)
            if response.status_code not in {200, 201, 202}:
                status = response.status_code
                raise DocumentClientError({401: "Login expired. Log in again.", 403: "Access denied.",
                    409: "Action requires reconciliation or conflicts with recorded state.",
                    422: "Source or action is unsupported.", 429: "Execution limit or admission capacity reached.",
                    503: "Document service unavailable."}.get(status, "Document request failed."))
            return response.json()
        except (requests.RequestException, ValueError):
            raise DocumentClientError("Document service unavailable.") from None
        finally:
            if response is not None:
                response.close()
