class CloudShellCPBaseException(Exception):
    """Base CloudShell Cloud Providers Exception."""


class CancellationContextException(CloudShellCPBaseException):
    """Cancellation Exception."""
