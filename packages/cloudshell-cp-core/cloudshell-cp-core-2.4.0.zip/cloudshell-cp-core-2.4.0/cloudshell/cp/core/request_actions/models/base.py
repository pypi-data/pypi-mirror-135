from dataclasses import dataclass


class BaseRequestObject:
    def __str__(self):
        return f"{type(self)}:\t{vars(self)}"

    def __repr__(self):
        return str(self)


@dataclass
class Attribute(BaseRequestObject):
    attributeName: str = ""
    attributeValue: str = ""


@dataclass
class BaseRequestAction(BaseRequestObject):
    actionId: str = ""
