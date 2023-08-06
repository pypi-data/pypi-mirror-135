from unittest.mock import MagicMock

import pytest

from cloudshell.cp.core.reservation_info import ReservationInfo


@pytest.fixture()
def context():
    return MagicMock()


def test_from_resource_context(context):
    reservation_info = ReservationInfo.from_resource_context(context)
    assert reservation_info.reservation_id == context.reservation.reservation_id


def test_from_remote_resource_context(context):
    reservation_info = ReservationInfo.from_remote_resource_context(context)
    assert reservation_info.reservation_id == context.remote_reservation.reservation_id
