from dataclasses import dataclass, field
from typing import Type

from cloudshell.cp.core.request_actions import models
from cloudshell.cp.core.request_actions.base import BaseRequestActions
from cloudshell.cp.core.request_actions.models import DeployApp


@dataclass
class DeployVMRequestActions(BaseRequestActions):
    deploy_app: models.DeployApp = None
    connect_subnets: list = field(default_factory=list)

    @classmethod
    def register_deployment_path(cls, deployment_path_cls: Type[DeployApp]):
        """Register deployment path class."""
        cls.REGISTERED_DEPLOYMENT_PATH_MODELS[
            deployment_path_cls.DEPLOYMENT_PATH
        ] = deployment_path_cls

    @classmethod
    def from_request(cls, request, cs_api=None):
        """Create DeployVMRequestActions object from the string request.

        :param str request:
        :param cloudshell.api.cloudshell_api.CloudShellAPISession cs_api:
        :rtype: DeployVMRequestActions
        """
        actions = cls._parse_request_actions(request=request, cs_api=cs_api)
        obj = cls()

        for action in actions:
            if isinstance(action, models.DeployApp):
                obj.deploy_app = action
            elif isinstance(action, models.ConnectSubnet):
                obj.connect_subnets.append(action)

        obj.connect_subnets.sort(key=lambda x: x.device_index)

        return obj
