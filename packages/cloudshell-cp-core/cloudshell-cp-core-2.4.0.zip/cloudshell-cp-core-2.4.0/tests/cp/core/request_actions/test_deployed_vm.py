import json
from unittest.mock import Mock

from cloudshell.shell.core.driver_context import AppContext, ResourceContextDetails

from cloudshell.cp.core.request_actions import DeployedVMActions
from cloudshell.cp.core.request_actions.models import DeployedApp


class StaticApp(DeployedApp):
    DEPLOYMENT_PATH = "Generic Static vCenter VM 2G"


class MyDeployedApp(DeployedApp):
    DEPLOYMENT_PATH = "MicrosoftAzure2G.AzureVMFromMarketplace2G"


def test_static_deployed_app():
    app_name = "win-test"
    address = "192.168.26.43"
    uuid = "42282856-0637-216a-511d-ccd88aa07e8f"
    vm_name = "static-vms/win-test"
    app_context = AppContext(
        app_request_json="",
        deployed_app_json=json.dumps(
            {
                "name": app_name,
                "family": "CS_GenericAppFamily",
                "model": StaticApp.DEPLOYMENT_PATH,
                "address": address,
                "attributes": [
                    {
                        "name": f"{StaticApp.DEPLOYMENT_PATH}.VM Name",
                        "value": "static-vms/win-test",
                    },
                    {
                        "name": f"{StaticApp.DEPLOYMENT_PATH}.vCenter Resource Name",
                        "value": "vcenter",
                    },
                    {"name": f"{StaticApp.DEPLOYMENT_PATH}.User", "value": ""},
                    {"name": f"{StaticApp.DEPLOYMENT_PATH}.Password", "value": ""},
                    {"name": f"{StaticApp.DEPLOYMENT_PATH}.Public IP", "value": ""},
                    {"name": "Execution Server Selector", "value": ""},
                ],
                "vmdetails": {
                    "id": "8b6c4c4d-e2c9-47c9-b260-9a33688bf78a",
                    "cloudProviderId": "d4d679c6-3049-4e55-9e64-8692a3400b6a",
                    "uid": uuid,
                    "vmCustomParams": [],
                },
            }
        ),
    )
    resource = ResourceContextDetails(
        id="0917eb75-92ad-4291-9623-4235c81be76b",
        name=app_name,
        fullname=app_name,
        type="Resource",
        address=address,
        model=StaticApp.DEPLOYMENT_PATH,
        family="CS_GenericAppFamily",
        description=None,
        attributes={
            "Generic Static vCenter VM 2G.VM Name": vm_name,
            "Generic Static vCenter VM 2G.vCenter Resource Name": "vcenter",
            "Generic Static vCenter VM 2G.User": "",
            "Generic Static vCenter VM 2G.Password": "3M3u7nkDzxWb0aJ/IZYeWw==",
            "Generic Static vCenter VM 2G.Public IP": "",
            "Execution Server Selector": "",
        },
        app_context=app_context,
        networks_info=None,
        shell_standard=None,
        shell_standard_version=None,
    )

    DeployedVMActions.register_deployment_path(StaticApp)
    actions = DeployedVMActions.from_remote_resource(resource, Mock())

    app = actions.deployed_app
    assert isinstance(app, StaticApp)
    assert app.name == app_name
    assert app.model == app.deployment_service_model == StaticApp.DEPLOYMENT_PATH
    assert app.private_ip == address
    assert app.vmdetails.uid == uuid
    assert app.attributes[f"{StaticApp.DEPLOYMENT_PATH}.VM Name"] == vm_name


def test_deployed_app():
    app_name = "Azureubuntusimple"
    address = "10.0.1.3"
    deployed_model = "Generic App Model"
    uuid = "3d750874-09f1-4243-a598-6700bb648655"

    app_context = AppContext(
        app_request_json=json.dumps(
            {
                "name": app_name,
                "description": None,
                "logicalResource": {
                    "family": "GenericAppFamily",
                    "model": "GenericAppModel",
                    "driver": None,
                    "description": "",
                    "attributes": [
                        {"name": "Password", "value": ""},
                        {"name": "PublicIP", "value": ""},
                        {"name": "User", "value": ""},
                    ],
                },
                "deploymentService": {
                    "cloudProviderName": "Azure2Goldcode",
                    "name": "Microsoft Azure 2nd Gen.Azure VM From Marketplace 2nd Gen",
                    "model": MyDeployedApp.DEPLOYMENT_PATH,
                    "driver": None,
                    "attributes": [
                        {
                            "name": "MicrosoftAzure2G.AzureVMFromMarketplace2G.Disk",
                            "value": "HDD",
                        },
                    ],
                },
            }
        ),
        deployed_app_json=json.dumps(
            {
                "name": app_name,
                "family": "Generic App Family",
                "model": "Generic App Model",
                "address": address,
                "attributes": [
                    {"name": "Password", "value": "3M3u7nkDzxWb0aJ/IZYeWw=="},
                    {"name": "User", "value": "adminuser"},
                    {"name": "Public IP", "value": ""},
                ],
                "vmdetails": {
                    "id": "4da74d28-50d9-4271-b2e4-b49eed1bb0fe",
                    "cloudProviderId": "129b8fac-fd8d-4c37-bb1a-fdceba2f38d7",
                    "uid": uuid,
                    "vmCustomParams": [],
                },
            }
        ),
    )
    resource = ResourceContextDetails(
        id="0917eb75-92ad-4291-9623-4235c81be76b",
        name=app_name,
        fullname=app_name,
        type="Resource",
        address=address,
        model="Generic App Model",
        family="Generic App Family",
        description=None,
        attributes={
            "Password": "3M3u7nkDzxWb0aJ/IZYeWw==",
            "User": "adminuser",
            "Public IP": "",
        },
        app_context=app_context,
        networks_info=None,
        shell_standard=None,
        shell_standard_version=None,
    )

    DeployedVMActions.register_deployment_path(MyDeployedApp)
    actions = DeployedVMActions.from_remote_resource(resource, Mock())

    app = actions.deployed_app
    assert isinstance(app, MyDeployedApp)
    assert app.name == app_name
    assert app.model == deployed_model
    assert app.deployment_service_model == MyDeployedApp.DEPLOYMENT_PATH
    assert app.private_ip == address
    assert app.vmdetails.uid == uuid
    assert app.attributes[f"{MyDeployedApp.DEPLOYMENT_PATH}.Disk"] == "HDD"
    assert app.attributes["User"] == "adminuser"
