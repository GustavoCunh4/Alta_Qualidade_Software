"""Processamento de pedidos PetroBahia."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from .discounts import DiscountEngine, FlatCouponDiscount, PercentageCouponDiscount
from .models import Order
from .pricing import (
    DieselPricingStrategy,
    EthanolPricingStrategy,
    GasolinePricingStrategy,
    LubricantPricingStrategy,
    PriceCalculator,
    UnknownProductStrategy,
)


@dataclass(slots=True)
class OrderProcessor:
    """Serviço que coordena precificação, descontos e arredondamentos."""

    price_calculator: PriceCalculator
    discount_engine: DiscountEngine

    def process(self, payload: Mapping[str, object]) -> float:
        """Processa o pedido e retorna o preço final."""
        order = self._map_payload(payload)
        if order.quantity == 0:
            print("qtd zero, retornando 0")
            return 0.0

        price = self.price_calculator.calculate(order)
        if price < 0:
            print("algo deu errado, preco negativo")
            price = 0.0

        price = self.discount_engine.apply(price, order)
        price = self._apply_rounding(order, price)
        quantity_to_display = self._format_quantity(order.quantity)

        print("pedido ok:", order.customer_name, order.product, quantity_to_display, "=>", price)
        return price

    @staticmethod
    def _map_payload(payload: Mapping[str, object]) -> Order:
        return Order(
            customer_name=str(payload.get("cliente", "")),
            product=str(payload.get("produto", "")),
            quantity=float(payload.get("qtd", 0)),
            coupon=payload.get("cupom") if payload.get("cupom") else None,
        )

    @staticmethod
    def _apply_rounding(order: Order, price: float) -> float:
        if order.product == "diesel":
            return round(price, 0)
        if order.product == "gasolina":
            return round(price, 2)

        return float(int(price * 100) / 100.0)

    @staticmethod
    def _format_quantity(quantity: float) -> float | int:
        if float(quantity).is_integer():
            return int(quantity)
        return quantity


def build_default_order_processor() -> OrderProcessor:
    """Constrói o processador com as estratégias padrão do domínio."""
    price_calculator = PriceCalculator(
        strategies=[
            DieselPricingStrategy(),
            GasolinePricingStrategy(),
            EthanolPricingStrategy(),
            LubricantPricingStrategy(),
            UnknownProductStrategy(),
        ]
    )
    discount_engine = DiscountEngine(
        strategies=[
            PercentageCouponDiscount("MEGA10", 0.10),
            PercentageCouponDiscount("NOVO5", 0.05),
            FlatCouponDiscount("LUB2", value=2, required_product="lubrificante"),
        ]
    )
    return OrderProcessor(price_calculator=price_calculator, discount_engine=discount_engine)
