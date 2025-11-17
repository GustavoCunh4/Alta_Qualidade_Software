"""Testes do módulo petrobahia.customers."""

from __future__ import annotations

from dataclasses import dataclass

import pytest

from petrobahia.customers import CustomerService
from petrobahia.models import Customer
from petrobahia.validators import CustomerValidator, ValidationResult


class DummyRepository:
    """Armazena clientes persistidos em memória para inspeção."""

    def __init__(self) -> None:
        self.saved: list[Customer] = []

    def save(self, customer: Customer) -> None:  # pragma: no cover - simples encaminhamento
        self.saved.append(customer)


@dataclass
class DummyValidator(CustomerValidator):
    """Controla os retornos das validações para facilitar os cenários."""

    registration_result: ValidationResult
    email_result: ValidationResult

    def __init__(
        self,
        registration_result: ValidationResult | None = None,
        email_result: ValidationResult | None = None,
    ) -> None:
        self.registration_result = registration_result or ValidationResult.valid()
        self.email_result = email_result or ValidationResult.valid()
        self.email_called_with: str | None = None

    def validate_registration(self, payload: dict) -> ValidationResult:
        return self.registration_result

    def validate_email(self, email: str) -> ValidationResult:
        self.email_called_with = email
        return self.email_result


def _valid_payload() -> dict[str, str]:
    return {"nome": "Cliente Teste", "email": "cliente@test.com", "cnpj": "123"}


def test_register_returns_false_when_registration_invalid() -> None:
    repository = DummyRepository()
    validator = DummyValidator(registration_result=ValidationResult.invalid("erro"))
    service = CustomerService(repository=repository, validator=validator)

    result = service.register(_valid_payload())

    assert result is False
    assert repository.saved == []
    assert validator.email_called_with is None


def test_register_saves_customer_when_valid() -> None:
    repository = DummyRepository()
    validator = DummyValidator()
    service = CustomerService(repository=repository, validator=validator)
    payload = _valid_payload()

    result = service.register(payload)

    assert result is True
    assert len(repository.saved) == 1
    saved = repository.saved[0]
    assert saved.name == payload["nome"]
    assert saved.email == payload["email"]
    assert saved.cnpj == payload["cnpj"]
    assert validator.email_called_with == payload["email"]
