from requests import HTTPError


class PDError(HTTPError):
    """
    Base error class.

    Subclassing HTTPError to avoid breaking existing code that expects only HTTPErrors.
    """


class PDBadRequest(PDError):
    """Most 40X and 501 status codes"""


class PDUnauthorized(PDError):
    """401 Unauthorized"""


class PDAccessDenied(PDError):
    """403 Forbidden"""


class PDNotFound(PDError):
    """404"""


class PDRateLimited(PDError):
    """429 Rate Limit Reached"""


class PDServerError(PDError):
    """50X errors"""


class PDUnsupportedMediaTypeError(PDError):
    """Feature is not enabled"""


class PDUnprocessableEntity(PDError):
    """Webhooks limit reached"""


class PDGone(PDError):
    """Old resource permanently unavailable"""


class PDMethodNotAllowed(PDError):
    """Incorrect request method"""


class BadDealPostBody(Exception):
    pass


class UnAuthorizedWebhook(Exception):
    pass

