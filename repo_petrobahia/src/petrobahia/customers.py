"""Servicos relacionados a clientes PetroBahia."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from .models import Customer
from .repositories import CustomerRepository
from .validators import CustomerValidator, ValidationResult


@dataclass(slots=True)
class CustomerService:
    """Cadastro e validacao de clientes."""

    repository: CustomerRepository
    validator: CustomerValidator

    def register(self, payload: Mapping[str, str]) -> bool:
        """Valida os dados do cliente, salva no repositorio
        e retorna True quando o cadastro e realizado."""
        registration_result = self.validator.validate_registration(dict(payload))
        self._emit_messages(registration_result)
        if not registration_result.is_valid:
            return False

        email_result = self.validator.validate_email(payload["email"])
        self._emit_messages(email_result)
        if not email_result.is_valid:
            return False

        customer = Customer(
            name=payload["nome"],
            email=payload["email"],
            cnpj=payload["cnpj"],
        )
        self.repository.save(customer)
        print("enviando mensagem de boas vindas para", customer.name)
        return True

    @staticmethod
    def _emit_messages(result: ValidationResult) -> None:
        for message in result.messages:
            print(message)

