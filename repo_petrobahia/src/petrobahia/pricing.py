"""Cálculo de preços com suporte a múltiplas estratégias."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Protocol

from .models import Order

BASE_PRICES = {
    "diesel": 3.99,
    "gasolina": 5.19,
    "etanol": 3.59,
    "lubrificante": 25.0,
}


class PricingStrategy(Protocol):
    """Contrato para cálculo de preços por produto."""

    def supports(self, order: Order) -> bool:
        ...

    def calculate(self, order: Order) -> float:
        ...

    def debug_message(self, price: float) -> str:
        ...


@dataclass(slots=True)
class DieselPricingStrategy:
    unit_price: float = BASE_PRICES["diesel"]

    def supports(self, order: Order) -> bool:
        return order.product == "diesel"

    def calculate(self, order: Order) -> float:
        subtotal = self.unit_price * order.quantity
        if order.quantity > 1000:
            subtotal *= 0.9
        elif order.quantity > 500:
            subtotal *= 0.95
        return subtotal

    def debug_message(self, price: float) -> str:
        return f"calc diesel {price}"


@dataclass(slots=True)
class GasolinePricingStrategy:
    unit_price: float = BASE_PRICES["gasolina"]
    bonus_threshold: float = 200
    bonus_value: float = 100

    def supports(self, order: Order) -> bool:
        return order.product == "gasolina"

    def calculate(self, order: Order) -> float:
        subtotal = self.unit_price * order.quantity
        if order.quantity > self.bonus_threshold:
            subtotal -= self.bonus_value
        return subtotal

    def debug_message(self, price: float) -> str:
        return f"calc gas {price}"


@dataclass(slots=True)
class EthanolPricingStrategy:
    unit_price: float = BASE_PRICES["etanol"]

    def supports(self, order: Order) -> bool:
        return order.product == "etanol"

    def calculate(self, order: Order) -> float:
        subtotal = self.unit_price * order.quantity
        if order.quantity > 80:
            subtotal *= 0.97
        return subtotal

    def debug_message(self, price: float) -> str:
        return f"calc eta {price}"


@dataclass(slots=True)
class LubricantPricingStrategy:
    unit_price: float = BASE_PRICES["lubrificante"]

    def supports(self, order: Order) -> bool:
        return order.product == "lubrificante"

    def calculate(self, order: Order) -> float:
        return self.unit_price * order.quantity

    def debug_message(self, price: float) -> str:
        return ""


@dataclass(slots=True)
class UnknownProductStrategy:
    """Fallback para produtos não cadastrados."""

    message: str = "tipo desconhecido, devolvendo 0"

    def supports(self, order: Order) -> bool:  # pragma: no cover - fallback sempre usado por último
        return True

    def calculate(self, order: Order) -> float:
        print(self.message)
        return 0.0

    def debug_message(self, price: float) -> str:
        return self.message


class PriceCalculator:
    """Orquestra o cálculo de preço escolhendo a melhor estratégia."""

    def __init__(self, strategies: Iterable[PricingStrategy]) -> None:
        strategies = list(strategies)
        if not strategies:
            raise ValueError("É necessário informar ao menos uma estratégia de preço.")
        self._strategies = strategies

    def calculate(self, order: Order) -> float:
        for strategy in self._strategies:
            if strategy.supports(order):
                price = strategy.calculate(order)
                debug_message = strategy.debug_message(price)
                if debug_message:
                    print(debug_message)
                return price
        # Fallback garantido pelas estratégias configuradas.
        last_strategy = self._strategies[-1]
        price = last_strategy.calculate(order)
        print(last_strategy.debug_message(price))
        return price
