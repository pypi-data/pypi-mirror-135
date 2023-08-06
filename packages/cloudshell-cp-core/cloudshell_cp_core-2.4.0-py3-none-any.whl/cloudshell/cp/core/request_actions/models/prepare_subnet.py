from dataclasses import dataclass, field

from .base import BaseRequestObject
from .connectivity import BaseConnectivityAction


@dataclass
class PrepareSubnetParams(BaseRequestObject):
    cidr: str = ""
    isPublic: bool = True
    alias: str = ""
    subnetServiceAttributes: list = field(default_factory=list)


@dataclass
class PrepareSubnet(BaseConnectivityAction):
    actionParams: PrepareSubnetParams = None
    attributes: dict = field(default_factory=dict)

    def get_cidr(self):
        return self.actionParams.cidr

    def get_alias(self):
        return self.actionParams.alias

    def get_attribute(self, name):
        return next(
            (
                attr.attributeValue
                for attr in self.actionParams.subnetServiceAttributes or []
                if attr.attributeName == name
            ),
            None,
        )

    def is_private(self):
        return not self.actionParams.isPublic
