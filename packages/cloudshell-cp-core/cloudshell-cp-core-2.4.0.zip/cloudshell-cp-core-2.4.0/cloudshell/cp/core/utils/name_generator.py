from __future__ import annotations

import re
import uuid


def generate_name(name: str, postfix: str | None = None, max_length: int = 24) -> str:
    """Generate name based on the given one with a maximum allowed length.

    Will replace all special characters (some Azure resources have this requirements).
    :param name: App name
    :param postfix: If postfix is empty method will generate unique 8 char long id
    :param max_length: Maximum allowed length for the generated name
    :return: (str) generated name
    """
    if postfix is None:
        postfix = generate_short_unique_string()
    if len(postfix) >= max_length:
        raise ValueError(f"Postfix '{postfix}' is bigger than name length {max_length}")

    # replace special characters. Remove dash character only if at the beginning.
    name = re.sub("[^a-zA-Z0-9-]|^-+", "", name)

    name = name[: max_length - len(postfix) - 1]
    name.rstrip("-")

    return f"{name}-{postfix}"


def generate_short_unique_string() -> str:
    """Generate a short unique string.

    Method generates an uuid and return the first 8 characters of the new uuid
    """
    unique_id = str(uuid.uuid4())[:8]
    return unique_id
