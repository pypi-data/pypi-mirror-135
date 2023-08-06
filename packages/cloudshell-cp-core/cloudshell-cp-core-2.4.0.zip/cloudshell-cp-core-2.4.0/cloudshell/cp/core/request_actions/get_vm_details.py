import json
from dataclasses import dataclass, field

from cloudshell.cp.core.request_actions.deployed_vm import DeployedVMActions


@dataclass
class GetVMDetailsRequestActions(DeployedVMActions):
    deployed_apps: list = field(default_factory=list)

    @classmethod
    def from_request(cls, request, cs_api):
        """Create GetVMDetailsRequestActions object from the string request.

        :param str request:
        :param cloudshell.api.cloudshell_api.CloudShellAPISession cs_api:
        :rtype: GetVMDetailsRequestActions
        """
        data = json.loads(request)
        deployed_apps = []
        for item in data["items"]:
            deployed_app_request = cls.from_data(
                app_request_data=item["appRequestJson"],
                deployed_app_data=item["deployedAppJson"],
                cs_api=cs_api,
            )
            deployed_apps.append(deployed_app_request.deployed_app)

        return cls(deployed_apps=deployed_apps)
