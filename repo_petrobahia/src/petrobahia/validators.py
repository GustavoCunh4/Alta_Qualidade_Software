"""Validacoes de entrada para entidades PetroBahia."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable

EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
CNPJ_REGEX = re.compile(r"^\d{14}$")


@dataclass(slots=True)
class ValidationResult:
    """Consolida o resultado de uma validacao."""

    is_valid: bool
    messages: list[str]

    @classmethod
    def valid(cls) -> "ValidationResult":
        """Retorna um resultado valido sem mensagens."""
        return cls(is_valid=True, messages=[])

    @classmethod
    def invalid(cls, *messages: str) -> "ValidationResult":
        """Retorna um resultado invalido com as mensagens fornecidas."""
        return cls(is_valid=False, messages=list(messages))

    def extend(self, messages: Iterable[str]) -> None:
        """Adiciona mensagens ao resultado de validacao."""
        self.messages.extend(messages)


class CustomerValidator:
    """Conjunto de validacoes relacionadas a clientes."""

    required_fields = ("nome", "email", "cnpj")

    def validate_registration(self, payload: dict) -> ValidationResult:
        """Valida campos obrigatorios e regras basicas de cadastro."""
        messages: list[str] = []

        missing = [field for field in self.required_fields if field not in payload]
        if missing:
            messages.append("faltou campo")

        name = str(payload.get("nome", "")).strip()
        if not name:
            messages.append("nome invalido")

        cnpj = str(payload.get("cnpj", "")).strip()
        if not CNPJ_REGEX.match(cnpj):
            messages.append("cnpj invalido (esperado 14 digitos numericos)")

        if messages:
            return ValidationResult.invalid(*messages)

        return ValidationResult.valid()

    def validate_email(self, email: str) -> ValidationResult:
        """Valida o formato do email fornecido."""
        if EMAIL_REGEX.match(email):
            return ValidationResult.valid()
        return ValidationResult.invalid("email invalido")

