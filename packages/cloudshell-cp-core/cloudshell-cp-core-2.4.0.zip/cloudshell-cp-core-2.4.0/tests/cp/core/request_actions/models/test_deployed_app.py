import pytest

from cloudshell.cp.core.request_actions.models import DeployedApp

MODEL = "Shell Model"
USERNAME = "username"
PUBLIC_IP = "8.8.8.8"


@pytest.mark.parametrize(
    ("attrs", "namespace"),
    (
        ({f"{MODEL}.User": USERNAME, f"{MODEL}.Public IP": PUBLIC_IP}, f"{MODEL}."),
        ({"User": USERNAME, "Public IP": PUBLIC_IP}, ""),
    ),
)
def test_deployed_app_1_and_2_gen(attrs, namespace):
    app = DeployedApp(model=MODEL, attributes=attrs)
    assert app.public_ip == PUBLIC_IP
