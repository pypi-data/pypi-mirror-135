from __future__ import annotations

from dataclasses import dataclass, field

from . import Artifact, Attribute, BaseRequestAction, BaseRequestObject


@dataclass
class SaveAppParams(BaseRequestObject):
    saveDeploymentModel: str = ""
    savedSandboxId: str = ""
    sourceVmUuid: str = ""
    sourceAppName: str = ""
    deploymentPathAttributes: list[Attribute] = field(default_factory=list)


@dataclass
class SaveApp(BaseRequestAction):
    actionParams: SaveAppParams = None


@dataclass
class DeleteSavedAppParams(BaseRequestObject):
    saveDeploymentModel: str = ""
    savedSandboxId: str = ""
    artifacts: list[Artifact] = field(default_factory=list)
    savedAppName: str = ""


@dataclass
class DeleteSavedApp(BaseRequestAction):
    actionParams: DeleteSavedAppParams = None
