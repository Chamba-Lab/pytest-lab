"""Tests for shipping.py."""

import pytest

from shipping import shipping_cost


def test_weight_must_be_positive():
    with pytest.raises(ValueError):
        shipping_cost(0)


def test_heavy_parcel_pays_per_extra_kilogram():
    assert shipping_cost(10) == 17.0


def test_members_ship_heavy_express_parcels_for_free():
    assert shipping_cost(10, express=True, member=True) == 0.0
