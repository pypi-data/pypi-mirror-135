from __future__ import annotations

from dataclasses import dataclass

from cloudshell.cp.core.request_actions.base import BaseRequestActions
from cloudshell.cp.core.request_actions.models import DeleteSavedApp, SaveApp


@dataclass
class SaveRestoreRequestActions(BaseRequestActions):
    save_app_actions: list[SaveApp]
    delete_saved_app_actions: list[DeleteSavedApp]

    @classmethod
    def from_request(cls, request: str, cs_api=None) -> SaveRestoreRequestActions:
        actions = cls._parse_request_actions(request, cs_api)

        save_app_actions = []
        delete_saved_app_actions = []
        for action in actions:
            if isinstance(action, SaveApp):
                save_app_actions.append(action)
            elif isinstance(action, DeleteSavedApp):
                delete_saved_app_actions.append(action)
        return cls(save_app_actions, delete_saved_app_actions)
