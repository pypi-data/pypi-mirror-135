from dataclasses import dataclass, field
from typing import Any

from .base import BaseRequestAction, BaseRequestObject


@dataclass
class SetVlanParameter(BaseRequestObject):
    vlanId: str = ""
    mode: int = 0
    vlanServiceAttributes: dict = field(default_factory=dict)


@dataclass
class ActionTarget(BaseRequestObject):
    fullAddress: str = ""
    fullName: str = ""


@dataclass
class BaseConnectivityAction(BaseRequestAction):
    actionTarget: ActionTarget = None
    actionParams: Any = None


@dataclass
class BaseConnectivityVlanAction(BaseConnectivityAction):
    connectionId: str = ""
    connectionParams: SetVlanParameter = None
    connectorAttributes: dict = field(default_factory=dict)
    customActionAttributes: dict = field(default_factory=dict)


@dataclass
class CleanupNetwork(BaseConnectivityAction):
    customActionAttributes: list = field(default_factory=list)


@dataclass
class RemoveVlan(BaseConnectivityVlanAction):
    pass


@dataclass
class SetVlan(BaseConnectivityVlanAction):
    pass


@dataclass
class ConnectToSubnetParams(BaseRequestObject):
    cidr: str = ""
    subnetId: str = ""
    isPublic: bool = True
    subnetServiceAttributes: list = field(default_factory=list)
    vnicName: str = ""


@dataclass
class ConnectSubnet(BaseConnectivityAction):
    actionParams: ConnectToSubnetParams = None

    def is_public(self):
        return self.actionParams.isPublic

    @property
    def subnet_id(self):
        return self.actionParams.subnetId

    @property
    def device_index(self):
        return int(self.actionParams.vnicName or 0)
