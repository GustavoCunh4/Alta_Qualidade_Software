"""Testes do módulo de descontos."""

from __future__ import annotations

import pytest

from petrobahia.discounts import (
    DiscountEngine,
    FlatCouponDiscount,
    PercentageCouponDiscount,
)
from petrobahia.models import Order


def _order(coupon: str | None = None, product: str = "diesel") -> Order:
    return Order(customer_name="Cliente", product=product, quantity=100, coupon=coupon)


def test_percentage_coupon_discount_supports_and_applies() -> None:
    discount = PercentageCouponDiscount("MEGA10", 0.10)
    order = _order(coupon="MEGA10")

    assert discount.supports(order) is True
    assert discount.apply(500.0, order) == pytest.approx(450.0)


def test_flat_coupon_discount_requires_matching_product() -> None:
    discount = FlatCouponDiscount("LUB2", value=2, required_product="lubrificante")

    assert discount.supports(_order(coupon="LUB2", product="diesel")) is False
    applicable_order = _order(coupon="LUB2", product="lubrificante")
    assert discount.supports(applicable_order) is True
    assert discount.apply(100.0, applicable_order) == pytest.approx(98.0)


def test_discount_engine_uses_first_supported_strategy() -> None:
    strategies = [
        PercentageCouponDiscount("NOVO5", 0.05),
        FlatCouponDiscount("LUB2", value=2, required_product="lubrificante"),
    ]
    engine = DiscountEngine(strategies=strategies)
    order = _order(coupon="LUB2", product="lubrificante")

    # primeira estratégia não suporta, segunda sim -> aplica 2 reais de desconto.
    assert engine.apply(50.0, order) == pytest.approx(48.0)


def test_discount_engine_returns_original_price_when_no_match() -> None:
    engine = DiscountEngine([PercentageCouponDiscount("NOVO5", 0.05)])
    order = _order(coupon="MEGA10")

    assert engine.apply(200.0, order) == pytest.approx(200.0)
