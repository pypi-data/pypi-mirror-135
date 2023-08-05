import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

DEFAULT_TIMEOUT = 5


class TimeoutHTTPAdapter(HTTPAdapter):
    def __init__(self, *args, **kwargs):
        self.timeout = DEFAULT_TIMEOUT
        if "timeout" in kwargs:
            self.timeout = kwargs["timeout"]
            del kwargs["timeout"]
        super().__init__(*args, **kwargs)

    def send(self, request, **kwargs):
        timeout = kwargs.get("timeout")
        if timeout is None:
            kwargs["timeout"] = self.timeout
        return super().send(request, **kwargs)


request_adapter = requests.Session()
retry_strategy = Retry(
    total=3,
    status_forcelist=[429, 408],
    method_whitelist=["GET", "PUT", "DELETE", "POST"],
    backoff_factor=1
)
request_adapter.mount("https://", TimeoutHTTPAdapter(max_retries=retry_strategy, timeout=10))
