from dataclasses import dataclass, field


@dataclass
class VMDetails:
    id: str  # noqa: A003
    cloud_provider_id: str
    uid: str
    vm_custom_params: dict = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data):
        """Create VMDetails from the dictionary data.

        :param dict data:
        :rtype: VMDetails
        """
        return cls(
            id=data.get("id"),
            cloud_provider_id=data.get("cloudProviderId"),
            uid=data.get("uid"),
            vm_custom_params=data.get("vmCustomParams"),
        )


@dataclass
class DeployedApp:
    GENERIC_APP_MODEL = "Generic App Model"
    GENERIC_APP_FAMILY = "Generic App Family"
    DEPLOYMENT_PATH = ""

    name: str = ""
    family: str = ""
    model: str = ""
    deployment_service_model: str = ""
    private_ip: str = ""
    vmdetails: VMDetails = None
    attributes: dict = field(default_factory=dict)
    cs_api: "cloudshell.api.cloudshell_api.CloudShellAPISession" = None  # noqa: F821
    _password: str = None

    def __post_init__(self):
        try:
            namespace = ""
            _ = self.attributes[f"{namespace}User"]
        except KeyError:
            namespace = f"{self.model}."
            _ = self.attributes[f"{namespace}User"]
        self._namespace = namespace

    def update_public_ip(self, public_ip):
        """Update Public IP Attribute on the CloudShell.

        :param public_ip:
        :return:
        """
        self.cs_api.SetAttributeValue(
            resourceFullPath=self.name,
            attributeName=f"{self._namespace}Public IP",
            attributeValue=public_ip,
        )

    def update_private_ip(self, resource_name: str, private_ip: str):
        # todo use self.name, we don't need attr resource_name
        self.cs_api.UpdateResourceAddress(resource_name, private_ip)

    @property
    def user(self):
        return self.attributes[f"{self._namespace}User"]

    @property
    def password(self):
        if self._password is None:
            self._password = self.cs_api.DecryptPassword(
                self.attributes[f"{self._namespace}Password"]
            ).Value

        return self._password

    @property
    def public_ip(self):
        return self.attributes[f"{self._namespace}Public IP"]
