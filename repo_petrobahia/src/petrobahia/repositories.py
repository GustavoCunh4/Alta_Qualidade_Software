"""Repositórios e persistência para entidades PetroBahia."""

from __future__ import annotations

from abc import ABC
from pathlib import Path
from typing import Protocol

from .models import Customer


class CustomerRepository(Protocol):
    """Contrato para persistência de clientes."""
    # pylint: disable=too-few-public-methods, unnecessary-pass

    def save(self, customer: Customer) -> None:
        """Persiste um cliente no meio de armazenamento."""
        pass


class BaseFileRepository(ABC):
    """Comportamentos comuns a repositórios baseados em arquivo."""
    # pylint: disable=too-few-public-methods

    def __init__(self, file_path: Path) -> None:
        """Inicializa o repositório garantindo que o diretório de destino existe."""
        self._file_path = file_path
        self._file_path.parent.mkdir(parents=True, exist_ok=True)


class FileCustomerRepository(BaseFileRepository, CustomerRepository):
    """Persiste clientes em um arquivo texto simples."""
    # pylint: disable=too-few-public-methods

    def save(self, customer: Customer) -> None:
        """Salva um cliente no arquivo configurado."""
        record = {
            "nome": customer.name,
            "email": customer.email,
            "cnpj": customer.cnpj,
        }
        with self._file_path.open("a", encoding="utf-8") as handle:
            handle.write(f"{record}\n")
