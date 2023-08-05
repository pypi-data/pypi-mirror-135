class PDModel(object):
    _keys = None

    def __init__(self, **kwargs):
        self._keys = set()
        for k, v in kwargs.items():
            setattr(self, k, v)
            self._keys.add(k)
        """if "custom_field" in kwargs.keys() and len(kwargs["custom_field"]) > 0:
            custom_fields = kwargs.pop("custom_field")
            kwargs.update(custom_fields)
        for k, v in kwargs.items():
            if hasattr(Ticket, k):
                k = '_' + k
            setattr(self, k, v)
            self._keys.add(k)
        self.created_at = self._to_timestamp(self.created_at)
        self.updated_at = self._to_timestamp(self.updated_at)"""

    """def _to_timestamp(self, timestamp_str):
        Converts a timestamp string as returned by the API to
        a native datetime object and return it.
        return dateutil.parser.parse(timestamp_str)"""


class Deal(PDModel):
    def __str__(self):
        return self.data["title"]

    def __repr__(self):
        return '<DealTitle: \'{}\', DealID: \'{}\'>'.format(self.data["title"], self.data["id"])


class Person(PDModel):
    def __str__(self):
        return self.data["name"]

    def __repr__(self):
        return '<PersonName: \'{}\', PersonID: \'{}\'>'.format(self.data["name"], self.data["id"])


class Organization(PDModel):
    def __str__(self):
        return self.data["name"]

    def __repr__(self):
        return '<OrgName: \'{}\', OrgID: \'{}\'>'.format(self.data["name"], self.data["id"])


class Activites(PDModel):
    def __str__(self):
        return self.data["subject"]

    def __repr__(self):
        return '<Activity Subject: \'{}\', DealID: \'{}\'>'.format(self.data["subject"], self.data["deal_id"])


class Notes(PDModel):
    def __str__(self):
        return self.data["deal_id"]

    def __repr__(self):
        return '<Deal_ID: \'{}\', Content: \'{}\'>'.format(self.data["deal_id"], self.data["content"])


class Search(PDModel):
    def __str__(self):
        return "Search Result Object"

    def __repr__(self):
        return "Search Result Object"

    def get(self, *args):
        if self.data["items"]:
            for i in self.data["items"]:
                if i["item"].get("type") in args[0]:
                    return globals()[i["item"]["type"].capitalize()](**{"data": i["item"]})
        else:
            return None
