"""Testes do modulo de precificacao (pricing)."""

from __future__ import annotations

import pytest

from petrobahia.models import Order
from petrobahia.pricing import (
    BASE_PRICES,
    DieselPricingStrategy,
    EthanolPricingStrategy,
    GasolinePricingStrategy,
    LubricantPricingStrategy,
    PriceCalculator,
)


def _order(product: str, quantity: float) -> Order:
    return Order(customer_name="Cliente", product=product, quantity=quantity)


def test_diesel_pricing_strategy_supports_and_applies_tiers() -> None:
    strategy = DieselPricingStrategy()
    base = BASE_PRICES["diesel"]

    assert strategy.supports(_order("diesel", 1)) is True
    assert strategy.supports(_order("gasolina", 1)) is False

    low = strategy.calculate(_order("diesel", 400))
    mid = strategy.calculate(_order("diesel", 600))
    high = strategy.calculate(_order("diesel", 1200))

    assert low == pytest.approx(base * 400)
    assert mid == pytest.approx(base * 600 * 0.95)
    assert high == pytest.approx(base * 1200 * 0.9)


def test_gasoline_pricing_strategy_supports_and_applies_bonus() -> None:
    strategy = GasolinePricingStrategy()
    base = BASE_PRICES["gasolina"]

    assert strategy.supports(_order("gasolina", 1)) is True
    assert strategy.supports(_order("diesel", 1)) is False

    regular = strategy.calculate(_order("gasolina", 100))
    with_bonus = strategy.calculate(_order("gasolina", 300))

    assert regular == pytest.approx(base * 100)
    assert with_bonus == pytest.approx(base * 300 - strategy.bonus_value)


def test_ethanol_pricing_strategy_supports_and_bulk_discount() -> None:
    strategy = EthanolPricingStrategy()
    base = BASE_PRICES["etanol"]

    assert strategy.supports(_order("etanol", 1)) is True
    assert strategy.supports(_order("diesel", 1)) is False

    small = strategy.calculate(_order("etanol", 50))
    large = strategy.calculate(_order("etanol", 100))

    assert small == pytest.approx(base * 50)
    assert large == pytest.approx(base * 100 * 0.97)


def test_lubricant_pricing_strategy_supports_and_linear_price() -> None:
    strategy = LubricantPricingStrategy()
    base = BASE_PRICES["lubrificante"]

    assert strategy.supports(_order("lubrificante", 1)) is True
    assert strategy.supports(_order("diesel", 1)) is False

    price = strategy.calculate(_order("lubrificante", 12))
    assert price == pytest.approx(base * 12)


def test_price_calculator_requires_at_least_one_strategy() -> None:
    with pytest.raises(ValueError):
        PriceCalculator(strategies=[])


def test_price_calculator_uses_matching_strategy_and_prints_debug(
    capsys: pytest.CaptureFixture[str],
) -> None:
    calculator = PriceCalculator(strategies=[DieselPricingStrategy()])
    order = _order("diesel", 100)

    price = calculator.calculate(order)
    out = capsys.readouterr().out

    assert price == pytest.approx(BASE_PRICES["diesel"] * 100)
    assert "calc diesel" in out


class DummyFallbackStrategy:
    """Estrategia de fallback usada apenas para testes."""

    def __init__(self) -> None:
        self.called_with: list[Order] = []

    def supports(self, _order: Order) -> bool:
        return False

    def calculate(self, order: Order) -> float:
        self.called_with.append(order)
        return 0.0

    def debug_message(self, price: float) -> str:
        assert price == pytest.approx(0.0)
        return "tipo desconhecido, devolvendo 0"


def test_price_calculator_uses_fallback_when_no_strategy_supports(
    capsys: pytest.CaptureFixture[str],
) -> None:
    fallback = DummyFallbackStrategy()
    calculator = PriceCalculator(strategies=[fallback])
    order = _order("desconhecido", 10)

    price = calculator.calculate(order)
    out = capsys.readouterr().out

    assert price == pytest.approx(0.0)
    assert fallback.called_with == [order]
    assert "tipo desconhecido" in out
