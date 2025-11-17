"""Módulo principal para processamento de pedidos na PetroBahia."""
from __future__ import annotations
import sys
from pathlib import Path

from petrobahia.customers import CustomerService  # noqa: E402
from petrobahia.orders import build_default_order_processor  # noqa: E402
from petrobahia.repositories import FileCustomerRepository  # noqa: E402
from petrobahia.validators import CustomerValidator  # noqa: E402


# Garante que o pacote em src esteja disponível sem depender de PYTHONPATH externo.
BASE_DIR = Path(__file__).resolve().parent
SRC_DIR = BASE_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

# from petrobahia.customers import CustomerService  # noqa: E402
# from petrobahia.orders import build_default_order_processor  # noqa: E402
# from petrobahia.repositories import FileCustomerRepository  # noqa: E402
# from petrobahia.validators import CustomerValidator  # noqa: E402


CLIENTS_FILE = BASE_DIR / "clientes.txt"

PEDIDOS = [
    {"cliente": "TransLog", "produto": "diesel", "qtd": 1200, "cupom": "MEGA10"},
    {"cliente": "MoveMais", "produto": "gasolina", "qtd": 300, "cupom": None},
    {"cliente": "EcoFrota", "produto": "etanol", "qtd": 50, "cupom": "NOVO5"},
    {"cliente": "PetroPark", "produto": "lubrificante", "qtd": 12, "cupom": "LUB2"},
]

CLIENTES = [
    {"nome": "Ana Paula", "email": "ana@@petrobahia", "cnpj": "123"},
    {"nome": "Carlos", "email": "carlos@petrobahia.com", "cnpj": "456"},
]


def main() -> None:
    """Ponto de entrada principal do sistema PetroBahia."""
    print("==== Inicio processamento PetroBahia ====")

    customer_service = CustomerService(
        repository=FileCustomerRepository(CLIENTS_FILE),
        validator=CustomerValidator(),
    )
    order_processor = build_default_order_processor()

    for cliente in CLIENTES:
        is_valid = customer_service.register(cliente)
        if is_valid:
            print("cliente ok:", cliente["nome"])
        else:
            print("cliente com problema:", cliente)

    valores = []
    for pedido in PEDIDOS:
        valor = order_processor.process(pedido)
        valores.append(valor)
        print("pedido:", pedido, "-- valor final:", valor)

    print("TOTAL =", sum(valores))
    print("==== Fim processamento PetroBahia ====")


if __name__ == "__main__":
    main()
