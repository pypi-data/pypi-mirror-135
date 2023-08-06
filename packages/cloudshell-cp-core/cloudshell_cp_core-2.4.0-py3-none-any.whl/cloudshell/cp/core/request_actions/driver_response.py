import json


# todo: refactor this !!!!
class DriverResponseRoot:
    def __init__(self, driver_response=None):
        """Init command.

        :param DriverResponse driver_response:
        """
        self.driverResponse = driver_response

    def _default_json_dump(self, obj):
        if isinstance(obj, bytes):
            return str(obj)

        return obj.__dict__

    def to_json(self):
        return json.dumps(self, default=self._default_json_dump)


class DriverResponse:
    def __init__(self, action_results=None):
        """Init command.

        :param action_results:
        """
        self.actionResults = action_results or []

    def to_driver_response_json(self):
        """Converts action results to the json.

        :rtype: str
        """
        return DriverResponseRoot(driver_response=self).to_json()
