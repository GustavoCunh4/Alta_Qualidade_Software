import pytest
from petrobahia.validators import (
    ValidationResult,
    CustomerValidator,
)


# ---------------------------
# ValidationResult
# ---------------------------

def test_validationresult_valid():
    result = ValidationResult.valid()
    assert result.is_valid is True
    assert result.messages == []


def test_validationresult_invalid():
    result = ValidationResult.invalid("erro1", "erro2")
    assert result.is_valid is False
    assert result.messages == ["erro1", "erro2"]


def test_validationresult_extend():
    result = ValidationResult.invalid("a")
    result.extend(["b", "c"])
    assert result.messages == ["a", "b", "c"]


# ---------------------------
# CustomerValidator
# ---------------------------

def test_validate_registration_all_fields_present():
    validator = CustomerValidator()
    payload = {
        "nome": "Maria",
        "email": "maria@example.com",
        "cnpj": "12345678901234"  # CNPJ válido com 14 dígitos
    }

    result = validator.validate_registration(payload)
    assert result.is_valid is True
    assert result.messages == []


def test_validate_registration_missing_fields():
    validator = CustomerValidator()
    payload = {
        "nome": "Maria",
        "email": "maria@example.com",
        # falta cnpj
    }

    result = validator.validate_registration(payload)
    assert result.is_valid is False
    assert result.messages == [
        "faltou campo",
        "cnpj invalido (esperado 14 digitos numericos)"
    ]



def test_validate_registration_invalid_cnpj():
    validator = CustomerValidator()
    payload = {
        "nome": "Maria",
        "email": "maria@example.com",
        "cnpj": "123"  # inválido
    }

    result = validator.validate_registration(payload)
    assert result.is_valid is False
    assert result.messages == ["cnpj invalido (esperado 14 digitos numericos)"]


def test_validate_email_valid():
    validator = CustomerValidator()
    result = validator.validate_email("teste@example.com")

    assert result.is_valid is True
    assert result.messages == []


def test_validate_email_invalid():
    validator = CustomerValidator()

    # Email sem arroba → inválido no seu código
    result = validator.validate_email("email-sem-arroba")

    assert result.is_valid is False
    assert result.messages == ["email invalido"]
