from __future__ import annotations

from dataclasses import dataclass, field

import jsonpickle

from . import BaseRequestAction


@dataclass
class ValidateAttributes(BaseRequestAction):
    deployment_path: str = ""
    attributes: dict = field(default_factory=dict)

    @classmethod
    def from_request(cls, request: str) -> ValidateAttributes:
        request = jsonpickle.decode(request)
        attrs = {a["AttributeName"]: a["AttributeValue"] for a in request["Attributes"]}
        return cls(
            actionId=request["ActionId"],
            deployment_path=request["DeploymentPath"],
            attributes=attrs,
        )

    def get(self, name: str):
        return self.attributes.get(f"{self.deployment_path}.{name}")
