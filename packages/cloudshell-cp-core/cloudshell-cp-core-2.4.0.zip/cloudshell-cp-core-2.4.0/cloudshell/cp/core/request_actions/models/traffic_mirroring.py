from dataclasses import dataclass, field

from .base import BaseRequestAction, BaseRequestObject


@dataclass
class RemoveTrafficMirroring(BaseRequestAction):
    sessionId: str = ""
    targetNicId: str = ""


@dataclass
class PortRange(BaseRequestObject):
    fromPort: str = ""
    toPort: str = ""


@dataclass
class TrafficFilterRule(BaseRequestObject):
    direction: str = ""
    destinationCidr: str = ""
    destinationPortRange: PortRange = None
    sourceCidr: str = ""
    sourcePortRange: PortRange = None
    protocol: str = ""


@dataclass
class CreateTrafficMirroringParams(BaseRequestObject):
    sourceNicId: str = ""
    targetNicId: str = ""
    sessionNumber: str = ""
    filterRules: list = field(default_factory=list)


@dataclass
class CreateTrafficMirroring(BaseRequestAction):
    actionParams: CreateTrafficMirroringParams = None
