import pytest
from mobile_data_plan import overage_charge, recharge_allowed, validity_status


def test_within_included_data():
    assert overage_charge("standard", 3, False, False) == 0


def test_unknown_plan():
    with pytest.raises(ValueError):
        overage_charge("invalid", 3, False, False)


def test_invalid_data_usage():
    with pytest.raises(ValueError):
        overage_charge("standard", -1, False, False)


def test_loyal_customer():
    assert overage_charge("standard", 6, False, True) == 0


def test_non_roaming_overage():
    assert overage_charge("standard", 7, False, False) == 30


def test_roaming_overage():
    assert overage_charge("standard", 7, True, False) == 80


def test_large_non_roaming_overage():
    assert overage_charge("basic", 13, False, False) == 275


def test_large_roaming_overage():
    assert overage_charge("basic", 13, True, False) == 605


def test_recharge_allowed():
    assert recharge_allowed(500, 1, False) is True


def test_kyc_pending():
    assert recharge_allowed(200, 5, True) is True


def test_recharge_over_limit():
    assert recharge_allowed(2500, 1, False) is False


def test_too_many_pending_recharges():
    assert recharge_allowed(500, 3, False) is False


def test_prepaid_active():
    assert validity_status(5, True, False) == "active"


def test_postpaid_with_addon():
    assert validity_status(5, False, True) == "active"


def test_grace_period():
    assert validity_status(-5, True, False) == "grace"


def test_expired():
    assert validity_status(-16, True, False) == "expired"