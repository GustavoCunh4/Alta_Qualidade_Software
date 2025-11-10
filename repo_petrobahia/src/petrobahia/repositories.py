"""Repositórios e persistência para entidades PetroBahia."""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Protocol

from .models import Customer


class CustomerRepository(Protocol):
    """Contrato para persistência de clientes."""

    def save(self, customer: Customer) -> None:
        ...


class BaseFileRepository(ABC):
    """Comportamentos comuns a repositórios baseados em arquivo."""

    def __init__(self, file_path: Path) -> None:
        self._file_path = file_path
        self._file_path.parent.mkdir(parents=True, exist_ok=True)


class FileCustomerRepository(BaseFileRepository, CustomerRepository):
    """Persiste clientes em um arquivo texto simples."""

    def save(self, customer: Customer) -> None:
        record = {
            "nome": customer.name,
            "email": customer.email,
            "cnpj": customer.cnpj,
        }
        with self._file_path.open("a", encoding="utf-8") as handle:
            handle.write(f"{record}\n")
