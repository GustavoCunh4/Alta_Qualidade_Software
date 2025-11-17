"""Serviços relacionados a clientes PetroBahia."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from .models import Customer
from .repositories import CustomerRepository
from .validators import CustomerValidator, ValidationResult


@dataclass(slots=True)
class CustomerService:
    """Cadastro e validação de clientes."""

    repository: CustomerRepository
    validator: CustomerValidator

    def register(self, payload: Mapping[str, str]) -> bool:
        """Valida os dados do cliente, salva no repositório 
        e retorna True quando o cadastro é realizado."""
        registration_result = self.validator.validate_registration(dict(payload))
        self._emit_messages(registration_result)
        if not registration_result.is_valid:
            return False

        email_result = self.validator.validate_email(payload["email"])
        self._emit_messages(email_result)

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
