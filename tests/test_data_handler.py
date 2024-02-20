import pytest
import pandas as pd
from decimal import Decimal
from fastapi import UploadFile
from app.data_handler import (
    process_file,
    clean_cpf_cnpj,
    treat_null_value,
    tickets_to_decimal,
    validate_document,
)


@pytest.fixture
def sample_file(tmp_path):
    content = """'CPF                PRIVATE     INCOMPLETO  DATA DA ÚLTIMA COMPRA TICKET MÉDIO          TICKET DA ÚLTIMA COMPRA LOJA MAIS FREQUÊNTE LOJA DA ÚLTIMA COMPRA
                742.460.460-00     0           0           2013-11-07            60,37                 60,37                   79.379.491/0008-50  79.379.491/0008-50
            """
    file_path = tmp_path / "sample_file.txt"
    with open(file_path, "w") as f:
        f.write(content)
    return file_path


def test_process_file(sample_file):
    file_upload = UploadFile(
        filename="sample_file.txt", file=open(sample_file, "rb"))
    data = process_file(file_upload)

    assert len(data) == 1
    assert data[0]["cpf"] == "74246046000"
    assert data[0]["private"] == 0
    assert data[0]["incompleto"] == 0
    assert data[0]["data_ultima_compra"] == "2013-11-07"
    assert data[0]["ticket_medio"] == Decimal('60.37')
    assert data[0]["ticket_ultima_compra"] == Decimal('60.37')
    assert data[0]["loja_mais_frequente"] == "79379491000850"
    assert data[0]["loja_ultima_compra"] == "79379491000850"


def test_clean_cpf_cnpj():
    assert clean_cpf_cnpj("123.456.789-09") == "12345678909"
    assert clean_cpf_cnpj("12a3b4c5678909") == "12345678909"
    assert clean_cpf_cnpj(None) is None


def test_treat_null_value():
    assert treat_null_value("Test") == "Test"
    assert treat_null_value(None) is None
    assert treat_null_value(pd.NA) is None


def test_tickets_to_decimal():
    assert tickets_to_decimal("100.50") == 100.50
    assert tickets_to_decimal(None) is None


def test_validate_document():
    assert validate_document("123.456.789-09")
    assert not validate_document("111.111.111-11")
    assert not validate_document("123.456.789/0001-23")
    assert not validate_document("11a2b3c4d5e6f7g8h9i0j")
