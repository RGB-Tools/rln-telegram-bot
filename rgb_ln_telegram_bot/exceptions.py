"""Exceptions module."""


class APIException(Exception):
    """API error."""


class AllocationsAlreadyAvailable(APIException):
    """Allocations already available error."""


class InvalidTransportEndpoints(APIException):
    """Invalid transport endpoints error."""


class RecipientIDAlreadyUsed(APIException):
    """Recipient ID already used error."""
