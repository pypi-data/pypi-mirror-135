from abc import ABC, abstractmethod

from cloudshell.cp.core.request_actions import DriverResponse
from cloudshell.cp.core.request_actions.models import ConnectToSubnetActionResult


class AbstractDeployFlow(ABC):
    def __init__(self, logger):
        """Init command.

        :param logging.Logger logger:
        """
        self._logger = logger

    @abstractmethod
    def _deploy(self, request_actions):
        """Deploy Virtual Machine.

        :param cloudshell.cp.core.request_actions.DeployVMRequestActions request_actions:  # noqa: E501
        :rtype: cloudshell.cp.core.request_actions.models.DeployAppResult
        """
        pass

    def _prepare_connect_to_subnet_results(self, request_actions):
        """Prepare Connect to Subnet Action results.

        :param cloudshell.cp.core.request_actions.DeployVMRequestActions request_actions:  # noqa: E501
        :rtype: list[cloudshell.cp.core.request_actions.models.ConnectToSubnetActionResult]
        """
        return [
            ConnectToSubnetActionResult(actionId=action.actionId)
            for action in request_actions.connect_subnets
        ]

    def deploy(self, request_actions):
        """Deploy Virtual Machine.

        :param cloudshell.cp.core.request_actions.DeployVMRequestActions request_actions:  # noqa: E501
        :rtype: str
        """
        deploy_app_result = self._deploy(request_actions=request_actions)
        connect_to_subnet_results = self._prepare_connect_to_subnet_results(
            request_actions=request_actions
        )

        json_data = DriverResponse(
            [deploy_app_result, *connect_to_subnet_results]
        ).to_driver_response_json()
        self._logger.debug(f"Deploy details: {json_data}")
        return json_data
