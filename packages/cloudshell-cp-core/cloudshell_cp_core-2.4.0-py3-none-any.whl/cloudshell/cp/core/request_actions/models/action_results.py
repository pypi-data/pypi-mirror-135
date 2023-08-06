from __future__ import annotations

from dataclasses import dataclass, field

from .base import Attribute, BaseRequestAction, BaseRequestObject


@dataclass
class BaseActionResult(BaseRequestAction):
    type: str = ""  # noqa: A003
    actionId: str = ""
    success: bool = True
    infoMessage: str = ""
    errorMessage: str = ""


@dataclass
class VmDetailsData:
    vmInstanceData: list = field(default_factory=list)
    vmNetworkData: list = field(default_factory=list)
    appName: str = ""
    errorMessage: str = ""


@dataclass
class DeployAppResult(BaseActionResult):
    type: str = "DeployApp"  # noqa: A003
    vmUuid: str = ""
    vmName: str = ""
    deployedAppAddress: str = ""
    deployedAppAttributes: list = field(default_factory=list)
    deployedAppAdditionalData: dict = field(default_factory=dict)
    vmDetailsData: VmDetailsData = None


@dataclass
class VmDetailsProperty:
    key: str = ""
    value: str = ""
    hidden: bool = False


@dataclass
class VmDetailsNetworkInterface(BaseRequestObject):
    interfaceId: str = ""
    networkId: str = ""
    isPrimary: bool = False
    isPredefined: bool = False
    networkData: list = field(default_factory=list)
    privateIpAddress: str = ""
    publicIpAddress: str = ""


@dataclass
class PrepareCloudInfraResult(BaseActionResult):
    type: str = "PrepareNetwork"  # noqa: A003


@dataclass
class PrepareSubnetActionResult(BaseActionResult):
    type: str = "PrepareSubnet"  # noqa: A003
    subnetId: str = ""


@dataclass
class ConnectToSubnetActionResult(BaseActionResult):
    type: str = "ConnectToSubnet"  # noqa: A003
    interface: str = ""


@dataclass
class CreateKeysActionResult(BaseActionResult):
    type: str = "CreateKeys"  # noqa: A003
    accessKey: str = ""


@dataclass
class SaveAppResult(BaseActionResult):
    type: str = "SaveApp"  # noqa: A003
    artifacts: list[Artifact] = field(default_factory=list)
    savedEntityAttributes: list[Attribute] = field(default_factory=list)
    saveDeploymentModel: str = ""
    additionalData: list = field(default_factory=list)


@dataclass
class DeleteSavedAppResult(BaseActionResult):
    type: str = "DeleteSavedApp"  # noqa: A003


@dataclass
class SetVlanResult(BaseActionResult):
    type: str = "setVlan"  # noqa: A003
    updatedInterface: str = ""


@dataclass
class RemoveVlanResult(BaseActionResult):
    type: str = "removeVlan"  # noqa: A003


@dataclass
class CleanupNetworkResult(BaseActionResult):
    type: str = "CleanupNetwork"  # noqa: A003


@dataclass
class TrafficMirroringResult(BaseActionResult):
    type: str = "CreateTrafficMirroring"  # noqa: A003
    sessionId: str = ""


@dataclass
class RemoveTrafficMirroringResult(BaseActionResult):
    type: str = "RemoveTrafficMirroring"  # noqa: A003


@dataclass
class Artifact(BaseRequestObject):
    artifactRef: str = ""
    artifactName: str = ""


@dataclass
class DataElement:
    name: str
    value: str


@dataclass
class ValidateAttributesResponse(BaseActionResult):
    type: str = "ValidateAttributes"  # noqa: A003
