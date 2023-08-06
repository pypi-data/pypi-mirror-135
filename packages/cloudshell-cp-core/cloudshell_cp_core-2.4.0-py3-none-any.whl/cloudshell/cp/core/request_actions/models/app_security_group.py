from dataclasses import dataclass, field

from cloudshell.cp.core.request_actions.models.deployed_app import (
    DeployedApp,
    VMDetails,
)


@dataclass
class AppSecurityGroup:
    security_group_configs: list = field(default_factory=list)
    deployed_app: DeployedApp = None

    @classmethod
    def from_dict(cls, data):
        """Create AppSecurityGroup from the dictionary data.

        :param dict data:
        :rtype: AppSecurityGroup
        """
        deployed_app_data = data["deployedApp"]
        vm_details_data = deployed_app_data.get("vmdetails")

        deployed_app = DeployedApp(
            name=deployed_app_data.get("name"),
            deployment_service_model="",
            private_ip=deployed_app_data.get("address"),
            attributes=deployed_app_data.get("attributes", []),
        )

        if vm_details_data is not None:
            deployed_app.vmdetails = VMDetails.from_dict(vm_details_data)

        security_group_configs = []

        for security_group_config_data in data["securityGroupsConfigurations"]:
            security_group_config = AppSecurityGroupConfig.from_dict(
                security_group_config_data
            )
            security_group_configs.append(security_group_config)

        return cls(
            security_group_configs=security_group_configs, deployed_app=deployed_app
        )


@dataclass
class AppSecurityGroupConfig:
    subnet_id: str
    rules: list = field(default_factory=list)

    @classmethod
    def from_dict(cls, data):
        """Create AppSecurityGroupConfig from the dictionary data.

        :param dict data:
        :rtype: AppSecurityGroupConfig
        """
        return cls(
            subnet_id=data["subnetId"],
            rules=[
                AppSecurityGroupConfigRule.from_dict(rule_data)
                for rule_data in data.get("rules", [])
            ],
        )


@dataclass
class AppSecurityGroupConfigRule:
    from_port: str
    to_port: str
    protocol: str
    source: str

    @classmethod
    def from_dict(cls, data):
        """Create AppSecurityGroupConfigRule from the dictionary data.

        :param dict data:
        :rtype: AppSecurityGroupConfigRule
        """
        return cls(
            from_port=data["fromPort"],
            to_port=data["toPort"],
            protocol=data["protocol"],
            source=data["source"],
        )


@dataclass
class SetAppSecurityGroupActionResult:
    appName: str = ""
    success: bool = True
    error: str = ""
