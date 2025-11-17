"""Estratégias de desconto aplicáveis a pedidos."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Protocol

from .models import Order


class DiscountStrategy(Protocol):
    """Contrato para estratégias de desconto."""

    def supports(self, order: Order) -> bool:
        """Indica se a estratégia pode ser usada para o pedido informado."""

    def apply(self, price: float, order: Order) -> float:
        """Calcula o novo preço após aplicar o desconto."""


@dataclass(slots=True)
class PercentageCouponDiscount:
    """Desconto percentual aplicado via cupom."""

    coupon_code: str
    percentage: float  # 0.1 = 10%

    def supports(self, order: Order) -> bool:
        """Retorna True se o cupom do pedido for o mesmo desta estratégia."""
        return order.coupon == self.coupon_code

    def apply(self, price: float, _order: Order) -> float:
        """Aplica a porcentagem configurada ao preço informado."""
        return price - (price * self.percentage)


@dataclass(slots=True)
class FlatCouponDiscount:
    """Desconto fixo aplicado via cupom."""

    coupon_code: str
    value: float
    required_product: str | None = None

    def supports(self, order: Order) -> bool:
        """Verifica se o desconto é aplicável ao pedido."""
        if order.coupon != self.coupon_code:
            return False
        if self.required_product and order.product != self.required_product:
            return False
        return True

    def apply(self, price: float, _order: Order) -> float:
        """Aplica o desconto ao preço."""
        return price - self.value


# pylint: disable=R0903  # motor tem apenas a operação de aplicar descontos
class DiscountEngine:
    """Aplica a primeira estratégia compatível com o pedido."""

    def __init__(self, strategies: Iterable[DiscountStrategy]) -> None:
        """Inicializa o motor de descontos com as estratégias fornecidas."""
        self._strategies = list(strategies)

    def apply(self, price: float, order: Order) -> float:
        """Aplica o desconto ao preço do pedido, se aplicável."""
        for strategy in self._strategies:
            if strategy.supports(order):
                return strategy.apply(price, order)
        return price
