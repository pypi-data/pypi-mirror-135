from abc import ABC, abstractmethod

import jsonpickle as jsonpickle

from cloudshell.cp.core.request_actions.models import SetAppSecurityGroupActionResult


class AbstractAppSecurityGroupsFlow(ABC):
    def __init__(self, logger):
        """Init command.

        :param logging.Logger logger:
        """
        self._logger = logger

    @abstractmethod
    def _set_app_security_group(self, security_group):
        """Set App Security Groups.

        :param security_group:
        :rtype:
        """
        pass

    def set_app_security_groups(self, request_actions):
        """Set App Security Groups.

        :param cloudshell.cp.core.request_actions.SetAppSecurityGroupsRequestActions request_actions:  # noqa: E501
        :rtype: str
        """
        results = []

        for security_group in request_actions.security_groups:
            vm_name = security_group.deployed_app.name
            set_group_result = SetAppSecurityGroupActionResult(appName=vm_name)

            try:
                self._set_app_security_group(security_group=security_group)
            except Exception:
                message = (
                    f"Setting custom App Security rules failed for the VM '{vm_name}'"
                )
                self._logger.warning(message, exc_info=True)
                set_group_result.errorMessage = f"{message}. See logs for the details"
                set_group_result.success = False

            results.append(set_group_result)

        json_data = jsonpickle.encode(results)
        self._logger.debug(f"Set App Security Group details: {json_data}")
        return json_data
