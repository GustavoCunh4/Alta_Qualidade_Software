import tempfile
from pathlib import Path

from petrobahia.models import Customer
from petrobahia.repositories import (
    BaseFileRepository,
    FileCustomerRepository,
)


# ---------------------------
# BaseFileRepository
# ---------------------------

def test_basefilerepository_creates_directory():
    with tempfile.TemporaryDirectory() as tmp_dir:
        repo_path = Path(tmp_dir) / "nested" / "repo.txt"

        # Diretório "nested" ainda não existe
        assert not repo_path.parent.exists()

        BaseFileRepository(repo_path)

        # Após instanciação o diretório deve existir
        assert repo_path.parent.exists()


# ---------------------------
# FileCustomerRepository
# ---------------------------

def test_filecustomerrepository_saves_customer():
    with tempfile.TemporaryDirectory() as tmp_dir:
        repo_path = Path(tmp_dir) / "customers.txt"
        repo = FileCustomerRepository(repo_path)

        customer = Customer(
            name="Maria",
            email="maria@example.com",
            cnpj="123456789"
        )

        repo.save(customer)

        # O arquivo precisa agora existir
        assert repo_path.exists()

        # O registro deve ter sido escrito corretamente
        content = repo_path.read_text(encoding="utf-8").strip()
        assert content == "{'nome': 'Maria', 'email': 'maria@example.com', 'cnpj': '123456789'}"


def test_filecustomerrepository_appends_multiple_records():
    with tempfile.TemporaryDirectory() as tmp_dir:
        repo_path = Path(tmp_dir) / "customers.txt"
        repo = FileCustomerRepository(repo_path)

        c1 = Customer("Maria", "m@example.com", "1")
        c2 = Customer("João", "j@example.com", "2")

        repo.save(c1)
        repo.save(c2)

        lines = repo_path.read_text("utf-8").strip().splitlines()

        assert len(lines) == 2
        assert lines[0] == "{'nome': 'Maria', 'email': 'm@example.com', 'cnpj': '1'}"
        assert lines[1] == "{'nome': 'João', 'email': 'j@example.com', 'cnpj': '2'}"
