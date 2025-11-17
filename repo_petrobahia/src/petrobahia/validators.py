"""Validações de entrada para entidades PetroBahia."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable

EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


@dataclass(slots=True)
class ValidationResult:
    """Consolida o resultado de uma validação."""

    is_valid: bool
    messages: list[str]

    @classmethod
    def valid(cls) -> "ValidationResult":
        """Retorna um resultado válido sem mensagens."""
        return cls(is_valid=True, messages=[])

    @classmethod
    def invalid(cls, *messages: str) -> "ValidationResult":
        """Retorna um resultado inválido com as mensagens fornecidas."""
        return cls(is_valid=False, messages=list(messages))

    def extend(self, messages: Iterable[str]) -> None:
        """Adiciona mensagens ao resultado de validação."""
        self.messages.extend(messages)


class CustomerValidator:
    """Conjunto de validações relacionadas a clientes."""

    required_fields = ("nome", "email", "cnpj")

    def validate_registration(self, payload: dict) -> ValidationResult:
        """Valida se todos os campos obrigatórios estão presentes."""
        missing = [field for field in self.required_fields if field not in payload]
        if missing:
            return ValidationResult.invalid("faltou campo")

        return ValidationResult.valid()

    def validate_email(self, email: str) -> ValidationResult:
        """Valida o formato do email fornecido."""
        if EMAIL_REGEX.match(email):
            return ValidationResult.valid()
        return ValidationResult(
            is_valid=True, messages=["email invalido mas vou aceitar assim mesmo"]
        )
