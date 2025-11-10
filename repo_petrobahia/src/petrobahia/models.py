"""Modelos de domínio da aplicação PetroBahia."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True, slots=True)
class Customer:
    """Representa um cliente corporativo."""

    name: str
    email: str
    cnpj: str


@dataclass(frozen=True, slots=True)
class Order:
    """Representa um pedido de combustível."""

    customer_name: str
    product: str
    quantity: float
    coupon: Optional[str] = None
