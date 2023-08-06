import itertools
import json
from dataclasses import dataclass
from typing import Dict

from cloudshell.cp.core.request_actions import models


@dataclass
class DeployedVMActions:
    REGISTERED_DEPLOYMENT_PATH_MODELS = {}  # type: Dict[str, models.DeployedApp]
    deployed_app: models.DeployedApp = None

    @classmethod
    def register_deployment_path(cls, deployment_path_cls):
        """Register deployment path class.

        :param cloudshell.cp.core.models.DeployedApp deployment_path_cls:
        :return:
        """
        cls.REGISTERED_DEPLOYMENT_PATH_MODELS[
            deployment_path_cls.DEPLOYMENT_PATH
        ] = deployment_path_cls

    @classmethod
    def from_data(cls, app_request_data, deployed_app_data, cs_api):
        """Create DeployedApp from the dictionaries.

        :param dict|None app_request_data: in the static App app_request is empty
        :param dict deployed_app_data:
        :param cloudshell.api.cloudshell_api.CloudShellAPISession cs_api:
        :rtype: DeployedVMActions
        """
        model = deployed_app_data["model"]
        app_request_attrs = {}
        deployment_service_model = model
        if app_request_data:
            app_request_attrs = app_request_data["deploymentService"]["attributes"]
            deployment_service_model = app_request_data["deploymentService"]["model"]
        attributes = {
            attr["name"]: attr["value"]
            for attr in itertools.chain(
                deployed_app_data["attributes"],
                app_request_attrs,
            )
        }

        deployed_app_cls = cls.REGISTERED_DEPLOYMENT_PATH_MODELS.get(
            deployment_service_model, models.DeployedApp
        )

        deployed_app = deployed_app_cls(
            family=deployed_app_data["family"],
            model=model,
            name=deployed_app_data["name"],
            cs_api=cs_api,
            deployment_service_model=deployment_service_model,
            private_ip=deployed_app_data["address"],
            attributes=attributes,
            vmdetails=models.VMDetails.from_dict(deployed_app_data["vmdetails"]),
        )

        return cls(deployed_app=deployed_app)

    @classmethod
    def from_remote_resource(cls, resource, cs_api):
        """Create DeployedApp from the resource.

        :param cloudshell.api.cloudshell_api.CloudShellAPISession cs_api:
        :param cloudshell.shell.core.driver_context.ResourceContextDetails resource:
        :rtype: DeployedVMActions
        """
        app_request_json = resource.app_context.app_request_json
        app_request_data = json.loads(app_request_json) if app_request_json else None
        return cls.from_data(
            app_request_data=app_request_data,
            deployed_app_data=json.loads(resource.app_context.deployed_app_json),
            cs_api=cs_api,
        )
