"""Estratégias de desconto aplicáveis a pedidos."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Protocol

from .models import Order


class DiscountStrategy(Protocol):
    """Contrato para estratégias de desconto."""

    def supports(self, order: Order) -> bool:
        ...

    def apply(self, price: float, order: Order) -> float:
        ...


@dataclass(slots=True)
class PercentageCouponDiscount:
    """Desconto percentual aplicado via cupom."""

    coupon_code: str
    percentage: float  # 0.1 = 10%

    def supports(self, order: Order) -> bool:
        return order.coupon == self.coupon_code

    def apply(self, price: float, order: Order) -> float:
        return price - (price * self.percentage)


@dataclass(slots=True)
class FlatCouponDiscount:
    """Desconto fixo aplicado via cupom."""

    coupon_code: str
    value: float
    required_product: str | None = None

    def supports(self, order: Order) -> bool:
        if order.coupon != self.coupon_code:
            return False
        if self.required_product and order.product != self.required_product:
            return False
        return True

    def apply(self, price: float, order: Order) -> float:
        return price - self.value


class DiscountEngine:
    """Aplica a primeira estratégia compatível com o pedido."""

    def __init__(self, strategies: Iterable[DiscountStrategy]) -> None:
        self._strategies = list(strategies)

    def apply(self, price: float, order: Order) -> float:
        for strategy in self._strategies:
            if strategy.supports(order):
                return strategy.apply(price, order)
        return price
