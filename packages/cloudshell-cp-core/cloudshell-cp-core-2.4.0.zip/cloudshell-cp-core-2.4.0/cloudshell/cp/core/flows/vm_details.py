from abc import ABC, abstractmethod

import jsonpickle


class AbstractVMDetailsFlow(ABC):
    def __init__(self, logger):
        """Init command.

        :param logging.Logger logger:
        """
        self._logger = logger

    @abstractmethod
    def _get_vm_details(self, deployed_app):
        """Get VM Details.

        :param cloudshell.cp.core.request_actions.DeployedApp deployed_app:
        :rtype: cloudshell.cp.core.request_actions.models.VmDetailsData
        """
        pass

    def get_vm_details(self, request_actions):
        """Get VM Details.

        :param cloudshell.cp.core.request_actions.GetVMDetailsRequestActions request_actions:  # noqa: E501
        :rtype: str
        """
        results = []

        for deployed_app in request_actions.deployed_apps:
            vm_details_data = self._get_vm_details(deployed_app=deployed_app)
            results.append(vm_details_data)

        json_data = jsonpickle.encode(results, unpicklable=False)
        self._logger.debug(f"VM details: {json_data}")
        return json_data
