from .errors import UnAuthorizedWebhook
from .models import *


class Added(object):
    def __init__(self, webhook):
        self.webhook = webhook
        setattr(
            self,
            self.webhook.obj,
            self.webhook.json_data.get("current", dict())
        )


class Updated(object):
    def __init__(self, webhook):
        self.webhook = webhook
        self.current = self.webhook.json_data.get("current", dict())
        self.previous = self.webhook.json_data.get("previous", dict())
        self.change = list()
        for key in self.current.keys():
            current_value = self.current.get(key, None)
            previous_value = self.previous.get(key, None)
            if current_value != previous_value and current_value is not None:
                self.change.append(
                    dict(
                        key=key,
                        current_value=current_value,
                        previous_value=previous_value
                    )
                )


class Merged(object):
    def __init__(self, webhook):
        self.webhook = webhook


class Deleted(object):
    def __init__(self, webhook):
        self.webhook = webhook


class Webhook(object):
    def __init__(self, *args, **kwargs):
        webhook_auth = kwargs.get("webhook_auth", None)
        self.request = kwargs.get("request")
        if webhook_auth is not None:
            self.username = webhook_auth.get("username")
            self.password = webhook_auth.get("password")
            self.auth()
            self.json_data = self.request.get("json_data")
        self.event = self.json_data["event"].split(".")[0].lower()
        self.obj = self.json_data["event"].split(".")[1].lower()
        self.obj_id = self.json_data["current"]["id"]
        setattr(self, self.event, globals()[self.event.capitalize()](self))

    def auth(self):
        _auth = self.request.get("auth", None)
        if _auth is None:
            raise UnAuthorizedWebhook
        if _auth["username"] != self.username and _auth["password"] != self.password:
            raise UnAuthorizedWebhook

