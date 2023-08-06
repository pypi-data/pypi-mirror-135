import json

from cloudshell.cp.core.request_actions import models


class BaseRequestActions:
    REGISTERED_DEPLOYMENT_PATH_MODELS = {}

    @classmethod
    def _parse_request_actions(cls, request, cs_api):
        """Parse driver request actions.

        :param str request:
        :param cloudshell.api.cloudshell_api.CloudShellAPISession cs_api:
        :return:
        """
        request = json.loads(request)
        return cls._parse(
            data=request["driverRequest"].get("actions", []), cs_api=cs_api
        )

    @classmethod
    def from_request(cls, request, cs_api=None):
        """Create BaseRequestActions object from the string request.

        :param str request:
        :param cloudshell.api.cloudshell_api.CloudShellAPISession cs_api:
        :rtype: BaseRequestActions
        """
        return cls()

    @classmethod
    def _normalize_class_name(cls, class_name):
        """Change class name to the valid camel case format.

        :param str class_name:
        :rtype: str
        """
        return class_name[0].upper() + class_name[1:]

    @classmethod
    def _parse(cls, data, cs_api=None):
        """Parse data into the corresponding models.

        :param Any data:
        :param cloudshell.api.cloudshell_api.CloudShellAPISession cs_api:
        :rtype: Any
        """
        if isinstance(data, list):
            parsed_data = []
            for nested_data in data:
                parsed_data.append(cls._parse(data=nested_data, cs_api=cs_api))

            return parsed_data

        elif isinstance(data, dict):
            try:
                class_name = cls._normalize_class_name(data.pop("type"))
            except KeyError:
                parsed_params = {}
                for param_key, param in data.items():
                    parsed_params[param_key] = cls._parse(data=param, cs_api=cs_api)

                return parsed_params

            parsed_kwargs = cls._parse(data=data, cs_api=cs_api)
            parsed_cls = getattr(models, class_name)

            if issubclass(parsed_cls, models.DeployApp):
                parsed_cls = cls.REGISTERED_DEPLOYMENT_PATH_MODELS.get(
                    parsed_kwargs["actionParams"].deployment.deploymentPath, parsed_cls
                )
                parsed_obj = parsed_cls(**parsed_kwargs)
                parsed_obj.set_cloudshell_api(api=cs_api)
            else:
                parsed_obj = parsed_cls(**parsed_kwargs)

            return parsed_obj

        elif isinstance(data, str):
            if data.lower() in ("true", "false"):
                data = data.lower() == "true"

        return data
