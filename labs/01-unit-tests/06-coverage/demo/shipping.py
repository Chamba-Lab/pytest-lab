"""Shipping cost. This module is finished: the lab is about measuring its tests."""

BASE = 5.0
PER_KG = 1.5  # for each kilogram above 2
FREE_FROM = 20.0  # members ship free when the cost is above this


def shipping_cost(weight_kg: float, express: bool = False, member: bool = False) -> float:
    if weight_kg <= 0:
        raise ValueError("weight must be positive")
    cost = BASE
    if weight_kg > 2:
        cost += (weight_kg - 2) * PER_KG
    if express:
        cost *= 2
    if member and cost > FREE_FROM:
        cost = 0.0
    return round(cost, 2)
