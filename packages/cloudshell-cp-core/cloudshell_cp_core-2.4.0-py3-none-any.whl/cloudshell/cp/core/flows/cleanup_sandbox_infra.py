from abc import ABC, abstractmethod

from cloudshell.cp.core.request_actions import DriverResponse
from cloudshell.cp.core.request_actions.models import CleanupNetworkResult


class AbstractCleanupSandboxInfraFlow(ABC):
    def __init__(self, logger):
        """Init command.

        :param logging.Logger logger:
        """
        self._logger = logger

    @abstractmethod
    def cleanup_sandbox_infra(self, request_actions):
        """Cleanup Sandbox Infra.

        :param cloudshell.cp.core.request_actions.CleanupSandboxInfraRequestActions request_actions:  # noqa: E501
        :return:
        """
        pass

    def _cleanup_sandbox_infra(self, request_actions):
        """Cleanup Sandbox Infra.

        :param cloudshell.cp.core.request_actions.CleanupSandboxInfraRequestActions request_actions:  # noqa: E501
        :rtype: cloudshell.cp.core.request_actions.models.CleanupNetworkResult
        """
        action = request_actions.cleanup_network
        self.cleanup_sandbox_infra(request_actions)

        return CleanupNetworkResult(actionId=action.actionId)

    def cleanup(self, request_actions):
        """Cleanup Sandbox Infra.

        :param cloudshell.cp.core.request_actions.CleanupSandboxInfraRequestActions request_actions:  # noqa: E501
        :rtype: str
        """
        cleanup_sandbox_infra_result = self._cleanup_sandbox_infra(
            request_actions=request_actions
        )

        json_data = DriverResponse(
            [cleanup_sandbox_infra_result]
        ).to_driver_response_json()
        self._logger.debug(f"Cleanup sandbox infra details: {json_data}")
        return json_data
