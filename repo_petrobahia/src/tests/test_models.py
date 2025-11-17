"""Testes para os modelos de domínio."""

from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from petrobahia.models import Customer, Order


def test_customer_dataclass_is_immutable_and_keeps_values() -> None:
    customer = Customer(name="Empresa X", email="contato@empresa.com", cnpj="123")

    assert customer.name == "Empresa X"
    assert customer.email == "contato@empresa.com"
    assert customer.cnpj == "123"

    with pytest.raises(FrozenInstanceError):
        customer.name = "Outra"


def test_order_defaults_coupon_to_none_and_accepts_override() -> None:
    order = Order(customer_name="Empresa", product="diesel", quantity=100)
    assert order.coupon is None

    second = Order(
        customer_name="Empresa",
        product="gasolina",
        quantity=50.5,
        coupon="MEGA10",
    )
    assert second.coupon == "MEGA10"
    assert second.quantity == pytest.approx(50.5)
