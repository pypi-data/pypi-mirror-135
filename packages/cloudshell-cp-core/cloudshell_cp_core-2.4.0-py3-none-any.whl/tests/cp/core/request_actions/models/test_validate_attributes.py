import json

from cloudshell.cp.core.request_actions.models import ValidateAttributes


def test_from_request():
    action_id = "action id"
    deployment_path = "deployment path"
    attr_name1 = "attr name 1"
    attr_name2 = "attr name 2"
    attr_val1 = "attr value 1"
    attr_val2 = "attr value 2"
    request = json.dumps(
        {
            "ActionId": action_id,
            "DeploymentPath": deployment_path,
            "Attributes": [
                {
                    "AttributeName": f"{deployment_path}.{attr_name1}",
                    "AttributeValue": attr_val1,
                },
                {
                    "AttributeName": f"{deployment_path}.{attr_name2}",
                    "AttributeValue": attr_val2,
                },
            ],
        }
    )

    validate_attrs = ValidateAttributes.from_request(request)

    assert validate_attrs.actionId == action_id
    assert validate_attrs.deployment_path == deployment_path
    assert validate_attrs.get(attr_name1) == attr_val1
    assert validate_attrs.get(attr_name2) == attr_val2
    assert validate_attrs.get("missing") is None
