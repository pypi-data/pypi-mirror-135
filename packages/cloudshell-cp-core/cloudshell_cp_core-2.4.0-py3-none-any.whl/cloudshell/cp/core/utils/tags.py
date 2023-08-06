class BaseTagsManager:
    class DefaultTagNames:
        created_by = "CreatedBy"
        owner = "Owner"
        blueprint = "Blueprint"
        sandbox_id = "SandboxId"
        domain = "Domain"

    class DefaultTagValues:
        created_by = "CloudShell"

    def __init__(self, reservation_info, resource_config):
        self._reservation_info = reservation_info
        self._resource_config = resource_config

    def get_default_tags(self):
        """Get pre-defined CloudShell tags."""
        return {
            self.DefaultTagNames.created_by: self.DefaultTagValues.created_by,
            self.DefaultTagNames.owner: self._reservation_info.owner,
            self.DefaultTagNames.blueprint: self._reservation_info.blueprint,
            self.DefaultTagNames.sandbox_id: self._reservation_info.reservation_id,
            self.DefaultTagNames.domain: self._reservation_info.domain,
        }
