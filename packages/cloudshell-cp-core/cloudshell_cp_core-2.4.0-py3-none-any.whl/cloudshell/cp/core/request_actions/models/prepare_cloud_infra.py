from dataclasses import dataclass

from .base import BaseRequestObject
from .connectivity import BaseConnectivityAction


@dataclass
class PrepareCloudInfraParams(BaseRequestObject):
    cidr: str = ""


@dataclass
class PrepareCloudInfra(BaseConnectivityAction):
    actionParams: PrepareCloudInfraParams = None

    def get_sandbox_cidr(self):
        return self.actionParams.cidr
