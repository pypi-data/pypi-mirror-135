import json
from dataclasses import dataclass, field

from cloudshell.cp.core.request_actions.models.app_security_group import (
    AppSecurityGroup,
)


@dataclass
class SetAppSecurityGroupsRequestActions:
    security_groups: list = field(default_factory=list)

    @classmethod
    def from_request(cls, request):
        """Create SetAppSecurityGroupsRequestActions object from the string request.

        :param str request:
        :rtype: SetAppSecurityGroupsRequestActions
        """
        data = json.loads(request)
        security_groups = []

        for security_group_data in data:
            security_group = AppSecurityGroup.from_dict(security_group_data)
            security_groups.append(security_group)

        return cls(security_groups=security_groups)
