from dataclasses import dataclass


@dataclass
class ReservationInfo:
    reservation_id: str
    owner: str
    blueprint: str
    domain: str

    @classmethod
    def _from_reservation_context(cls, reservation):
        """Create ReservationInfo class from the ResourceCommandContext.

        :param cloudshell.shell.core.driver_context.ReservationContextDetails reservation:  # noqa: E501
        :rtype: ReservationInfo
        """
        return cls(
            reservation_id=reservation.reservation_id,
            owner=reservation.owner_user,
            blueprint=reservation.environment_name,
            domain=reservation.domain,
        )

    @classmethod
    def from_resource_context(cls, context):
        """Create ReservationInfo class from the ResourceCommandContext.

        :param cloudshell.shell.core.driver_context.ResourceCommandContext context:
        :rtype: ReservationInfo
        """
        return cls._from_reservation_context(reservation=context.reservation)

    @classmethod
    def from_remote_resource_context(cls, context):
        """Create ReservationInfo class from the ResourceRemoteCommandContext.

        :param cloudshell.shell.core.driver_context.ResourceRemoteCommandContext context:  # noqa: E501
        :rtype: ReservationInfo
        """
        return cls._from_reservation_context(reservation=context.remote_reservation)
