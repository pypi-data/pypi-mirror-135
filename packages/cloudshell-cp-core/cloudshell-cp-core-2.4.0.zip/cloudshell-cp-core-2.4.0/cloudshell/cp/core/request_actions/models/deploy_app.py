import itertools
from dataclasses import dataclass, field

from .base import BaseRequestAction, BaseRequestObject


@dataclass
class AppResourceInfo(BaseRequestObject):
    attributes: dict = field(default_factory=dict)


@dataclass
class DeployAppDeploymentInfo(BaseRequestObject):
    deploymentPath: str = ""
    attributes: dict = field(default_factory=dict)
    customModel: object = None


@dataclass
class DeployAppParams(BaseRequestObject):
    appName: str = ""
    deployment: DeployAppDeploymentInfo = None
    appResource: AppResourceInfo = None


@dataclass
class DeployApp(BaseRequestAction):
    DEPLOYMENT_PATH = ""

    actionParams: DeployAppParams = None
    attributes: dict = field(default_factory=dict)

    _cs_api: "cloudshell.api.cloudshell_api.CloudShellAPISession" = None  # noqa: F821
    _password: str = None

    def __post_init__(self):
        for attr in itertools.chain(
            self.actionParams.appResource.attributes,
            self.actionParams.deployment.attributes,
        ):
            self.attributes[attr.attributeName] = attr.attributeValue

    def set_cloudshell_api(self, api):
        """Set CloudShell API.

        :param cloudshell.api.cloudshell_api.CloudShellAPISession api:
        :return:
        """
        self._cs_api = api

    def _get_app_resource_attribute(self, attr_name):
        """Get App Resource attribute by its name.

        :param str attr_name:
        :return:
        """
        for attr, value in self.attributes.items():
            if any([attr == attr_name, attr.endswith(f".{attr_name}")]):
                return value

    def _decrypt_password(self, password):
        """Decrypt CloudShell password.

        :param str password:
        :rtype: str
        """
        if self._cs_api is None:
            raise Exception("Cannot decrypt password, CloudShell API is not defined")

        return self._cs_api.DecryptPassword(password).Value

    @property
    def app_name(self) -> str:
        return self.actionParams.appName.lower().replace(" ", "-")

    @property
    def user(self):
        return self._get_app_resource_attribute("User")

    @property
    def password(self):
        if self._password is None:
            password = self._get_app_resource_attribute("Password")
            if password:
                password = self._decrypt_password(password=password)
            self._password = password
        return self._password

    @property
    def public_ip(self):
        return self._get_app_resource_attribute("Public IP")
