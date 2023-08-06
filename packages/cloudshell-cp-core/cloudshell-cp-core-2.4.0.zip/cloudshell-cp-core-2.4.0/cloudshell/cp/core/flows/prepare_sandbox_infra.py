import concurrent.futures
from abc import ABC, abstractmethod

from cloudshell.cp.core.request_actions import DriverResponse
from cloudshell.cp.core.request_actions.models import (
    CreateKeysActionResult,
    PrepareCloudInfraResult,
    PrepareSubnetActionResult,
)


class AbstractPrepareSandboxInfraFlow(ABC):
    def __init__(self, logger):
        """Init command.

        :param logging.Logger logger:
        """
        self._logger = logger

    @abstractmethod
    def prepare_cloud_infra(self, request_actions):
        """Prepare Cloud Infra.

        :param cloudshell.cp.core.request_actions.PrepareSandboxInfraRequestActions request_actions:  # noqa: E501
        :return:
        """
        pass

    @abstractmethod
    def prepare_subnets(self, request_actions):
        """Prepare requested subnets.

        :param cloudshell.cp.core.request_actions.PrepareSandboxInfraRequestActions request_actions:  # noqa: E501
        :return dictionary PrepareSubnet.actionId: subnet_id
        :rtype: dict[str, str]
        """
        pass

    @abstractmethod
    def create_ssh_keys(self, request_actions):
        """Create SSH key pair and returns SSH private key.

        :param cloudshell.cp.core.request_actions.PrepareSandboxInfraRequestActions request_actions:  # noqa: E501
        :return: SSH Access key
        :rtype: str
        """
        pass

    def prepare_common_objects(self, request_actions):
        """Prepare common objects.

        :param cloudshell.cp.core.request_actions.PrepareSandboxInfraRequestActions request_actions:  # noqa: E501
        :return:
        """
        pass

    def _prepare_cloud_infra(self, request_actions):
        """Prepare Cloud Infra.

        :param cloudshell.cp.core.request_actions.PrepareSandboxInfraRequestActions request_actions:  # noqa: E501
        :rtype: cloudshell.cp.core.request_actions.models.PrepareCloudInfraResult
        """
        action = request_actions.prepare_cloud_infra
        self.prepare_cloud_infra(request_actions)

        return PrepareCloudInfraResult(actionId=action.actionId)

    def _prepare_subnets(self, request_actions):
        """Prepare Subnets.

        :param cloudshell.cp.core.request_actions.PrepareSandboxInfraRequestActions request_actions:  # noqa: E501
        :rtype: list[cloudshell.cp.core.request_actions.models.PrepareSubnetActionResult]
        """
        subnet_ids = self.prepare_subnets(request_actions)

        return [
            PrepareSubnetActionResult(
                actionId=action.actionId, subnetId=subnet_ids.get(action.actionId)
            )
            for action in request_actions.prepare_subnets
        ]

    def _create_ssh_keys(self, request_actions):
        """Create SSH Key pair.

        :param cloudshell.cp.core.request_actions.PrepareSandboxInfraRequestActions request_actions:  # noqa: E501
        :rtype: cloudshell.cp.core.request_actions.models.CreateKeysActionResult
        """
        access_key = self.create_ssh_keys(request_actions)

        return CreateKeysActionResult(
            actionId=request_actions.create_keys.actionId, accessKey=access_key
        )

    def prepare(self, request_actions):
        """Prepare Sandbox Infra.

        :param cloudshell.cp.core.request_actions.PrepareSandboxInfraRequestActions request_actions:  # noqa: E501
        :rtype: str
        """
        self.prepare_common_objects(request_actions=request_actions)

        with concurrent.futures.ThreadPoolExecutor() as executor:
            prepare_cloud_infra_task = executor.submit(
                self._prepare_cloud_infra, request_actions=request_actions
            )
            prepare_subnets_task = executor.submit(
                self._prepare_subnets, request_actions=request_actions
            )
            create_ssh_keys_task = executor.submit(
                self._create_ssh_keys, request_actions=request_actions
            )

            concurrent.futures.wait(
                [prepare_cloud_infra_task, prepare_subnets_task, create_ssh_keys_task]
            )

            action_results = [
                prepare_cloud_infra_task.result(),
                create_ssh_keys_task.result(),
                *prepare_subnets_task.result(),
            ]

        json_data = DriverResponse(action_results).to_driver_response_json()
        self._logger.debug(f"Prepare sandbox infra details: {json_data}")
        return json_data
