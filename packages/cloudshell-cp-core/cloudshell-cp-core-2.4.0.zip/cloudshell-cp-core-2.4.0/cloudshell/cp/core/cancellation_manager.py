from cloudshell.cp.core.exceptions import CancellationContextException


class CancellationContextManager:
    def __init__(self, cancellation_context):
        """Init command.

        :param cloudshell.shell.core.driver_context.CancellationContext cancellation_context:  # noqa: E501
        """
        self.cancellation_context = cancellation_context

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cancellation_context.is_cancelled:
            raise CancellationContextException("Command was cancelled from the portal")
