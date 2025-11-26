import pytest
from unittest.mock import Mock

from petrobahia.orders import OrderProcessor
from petrobahia.models import Order


# -------------------------------------------------------------------
# Helpers
# -------------------------------------------------------------------

def make_processor(mock_price, mock_discount):
    price_calc = Mock()
    price_calc.calculate.return_value = mock_price

    discount_engine = Mock()
    discount_engine.apply.return_value = mock_discount

    return OrderProcessor(
        price_calculator=price_calc,
        discount_engine=discount_engine
    )


# -------------------------------------------------------------------
# TESTES
# -------------------------------------------------------------------

def test_process_quantity_zero_returns_zero():
    processor = make_processor(mock_price=100, mock_discount=100)

    payload = {"cliente": "Maria", "produto": "diesel", "qtd": 0}
    result = processor.process(payload)

    assert result == 0.0


def test_process_diesel_rounds_to_integer():
    # preço calculado = 101.7 → desconto mantém → arredonda para 102
    processor = make_processor(mock_price=101.7, mock_discount=101.7)

    payload = {"cliente": "João", "produto": "diesel", "qtd": 10}
    result = processor.process(payload)

    assert result == 102.0


def test_process_gasoline_rounds_two_decimals():
    processor = make_processor(mock_price=7.1299, mock_discount=7.1299)

    payload = {"cliente": "Ana", "produto": "gasolina", "qtd": 5}
    result = processor.process(payload)

    assert result == 7.13  # arredondamento de gasolina


def test_process_unknown_product_truncates_two_decimals():
    processor = make_processor(mock_price=10.6789, mock_discount=10.6789)

    payload = {"cliente": "Pedro", "produto": "qualquer", "qtd": 2}
    result = processor.process(payload)

    assert result == 10.67  # trunca


def test_process_negative_price_becomes_zero():
    # price_calc retorna -50 → processador corrige para 0
    # discount_engine.apply deve receber price=0 e retornar 0
    processor = make_processor(mock_price=-50, mock_discount=0)

    payload = {"cliente": "Maria", "produto": "diesel", "qtd": 10}
    result = processor.process(payload)

    assert result == 0.0



def test_process_applies_discount_engine():
    price_calc = Mock()
    price_calc.calculate.return_value = 100

    discount_engine = Mock()
    discount_engine.apply.return_value = 80  # desconto aplicado

    processor = OrderProcessor(price_calculator=price_calc, discount_engine=discount_engine)

    payload = {"cliente": "Mario", "produto": "diesel", "qtd": 10}

    result = processor.process(payload)

    assert result == 80  # antes do arredondamento (diesel → arredonda)
    discount_engine.apply.assert_called_once()


def test_map_payload_creates_order_correctly():
    payload = {
        "cliente": "Maria",
        "produto": "gasolina",
        "qtd": 15,
        "cupom": "MEGA10",
    }

    order = OrderProcessor._map_payload(payload)

    assert isinstance(order, Order)
    assert order.customer_name == "Maria"
    assert order.product == "gasolina"
    assert order.quantity == 15
    assert order.coupon == "MEGA10"


def test_format_quantity_integer():
    assert OrderProcessor._format_quantity(10.0) == 10


def test_format_quantity_float():
    assert OrderProcessor._format_quantity(10.5) == 10.5
