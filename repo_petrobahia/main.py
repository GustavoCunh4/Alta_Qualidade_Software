"""Modulo principal para processamento de pedidos na PetroBahia."""
from __future__ import annotations

import sys
from pathlib import Path

# Garante que o pacote em src esteja disponivel sem depender de PYTHONPATH externo.
BASE_DIR = Path(__file__).resolve().parent
SRC_DIR = BASE_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from petrobahia.customers import CustomerService  # noqa: E402
from petrobahia.orders import build_default_order_processor  # noqa: E402
from petrobahia.repositories import FileCustomerRepository  # noqa: E402
from petrobahia.validators import CustomerValidator  # noqa: E402


CLIENTS_FILE = BASE_DIR / "clientes.txt"

PEDIDOS = [
    {"cliente": "TransLog", "produto": "diesel", "qtd": 1200, "cupom": "MEGA10"},
    {"cliente": "MoveMais", "produto": "gasolina", "qtd": 300, "cupom": None},
    {"cliente": "EcoFrota", "produto": "etanol", "qtd": 50, "cupom": "NOVO5"},
    {"cliente": "PetroPark", "produto": "lubrificante", "qtd": 12, "cupom": "LUB2"},
    {"cliente": "Cliente Invalido", "produto": "diesel", "qtd": 10, "cupom": None},
]

CLIENTES = [
    {
        "nome": "TransLog",
        "email": "contato@translog.com.br",
        "cnpj": "12345678000199",
    },
    {
        "nome": "MoveMais",
        "email": "contato@movemais.com.br",
        "cnpj": "98765432000188",
    },
    {
        "nome": "EcoFrota",
        "email": "contato@ecofrota.com.br",
        "cnpj": "11223344000155",
    },
    {
        "nome": "PetroPark",
        "email": "contato@petropark.com.br",
        "cnpj": "55443322000111",
    },
    {
        "nome": "Cliente Invalido",
        "email": "ana@@petrobahia",
        "cnpj": "123",
    },
]


def main() -> None:
    """Ponto de entrada principal do sistema PetroBahia."""
    print("=" * 60)
    print("        SISTEMA INTERNO PETROBAHIA - DEMO")
    print("=" * 60)

    customer_service = CustomerService(
        repository=FileCustomerRepository(CLIENTS_FILE),
        validator=CustomerValidator(),
    )
    order_processor = build_default_order_processor()

    print("\n--- CADASTRO DE CLIENTES ---")
    valid_customers: list[dict[str, str]] = []
    invalid_customers: list[dict[str, str]] = []

    for cliente in CLIENTES:
        is_valid = customer_service.register(cliente)
        if is_valid:
            print("cliente ok:        ", cliente["nome"])
            valid_customers.append(cliente)
        else:
            print("cliente com problema:", cliente)
            invalid_customers.append(cliente)

    print("\nResumo cadastro de clientes:")
    print(f"  - validos  : {len(valid_customers)}")
    print(f"  - invalidos: {len(invalid_customers)}")

    if valid_customers:
        print("\nClientes aprovados:")
        print(f"{'NOME':<15} {'EMAIL':<30} {'CNPJ':<14}")
        print("-" * 65)
        for c in valid_customers:
            print(f"{c['nome']:<15} {c['email']:<30} {c['cnpj']:<14}")

    if invalid_customers:
        print("\nClientes rejeitados:")
        for c in invalid_customers:
            print("  -", c)

    print("\n--- PROCESSAMENTO DE PEDIDOS ---")
    valores: list[float] = []
    nomes_clientes_validos = {c["nome"] for c in valid_customers}

    for pedido in PEDIDOS:
        if pedido["cliente"] not in nomes_clientes_validos:
            print(
                "pedido rejeitado:",
                pedido["cliente"],
                "- cliente nao cadastrado ou invalido",
            )
            continue
        valor = order_processor.process(pedido)
        valores.append(valor)
        print("pedido:", pedido, "-- valor final:", valor)

    if valores:
        print("\nTOTAL GERAL =", sum(valores))
    else:
        print("\nNenhum pedido valido foi processado.")

    print("\n" + "=" * 60)
    print("           FIM DO PROCESSAMENTO PETROBAHIA")
    print("=" * 60)


if __name__ == "__main__":
    main()
