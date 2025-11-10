"""Camada principal da aplicação PetroBahia moderna.

Os módulos deste pacote substituem o código contido em ``legacy`` e
organizam as responsabilidades em torno de clientes, pedidos,
precificação e descontos seguindo PEP8, Clean Code e princípios SOLID.
"""

from .models import Customer, Order  # noqa: F401
