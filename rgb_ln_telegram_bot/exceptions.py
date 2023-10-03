"""Exceptions module."""


class APIException(Exception):
    """API error."""


class AllocationsAlreadyAvailable(Exception):
    """Allocations already available error."""


class InvalidTransportEndpoints(Exception):
    """Invalid transport endpoints error."""


class RecipientIDAlreadyUsed(Exception):
    """Recipient ID already used error."""
