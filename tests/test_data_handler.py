import pytest
import pandas as pd
from decimal import Decimal
from app.data_handler import process_file, clean_cpf_cnpj, treat_null_value, tickets_to_decimal


@pytest.fixture
def sample_csv_file(tmp_path):
    # Cria um arquivo CSV de exemplo para testar
    content = """CPF PRIVATE INCOMPLETO DATA DA ÚLTIMA COMPRA TICKET MÉDIO TICKET DA ÚLTIMA COMPRA LOJA MAIS FREQUÊNTE LOJA DA ÚLTIMA COMPRA
    12345678900 1 0 2022-01-01 100.00 150.00 12345678900 12345678900
    """
    file_path = tmp_path / "sample_data.csv"
    file_path.write_text(content)
    return str(file_path)


def test_process_file(sample_csv_file):
    # Chama a função que você quer testar
    data = process_file(sample_csv_file)

    # Verifica se a lista de dados foi gerada corretamente
    assert data == [
        {
            "cpf": "12345678900",
            "private": 1,
            "incompleto": 0,
            "data_ultima_compra": "2022-01-01",
            "ticket_medio": Decimal("100.00"),
            "ticket_ultima_compra": Decimal("150.00"),
            "loja_mais_frequente": "12345678900",
            "loja_ultima_compra": "12345678900"
        }
    ]

def test_clean_cpf_cnpj():
    assert clean_cpf_cnpj("12.345.678/900-00") == "1234567890000"
    assert clean_cpf_cnpj("123.456.789-00") == "12345678900"
    assert clean_cpf_cnpj(None) is None

def test_treat_null_value():
    assert treat_null_value("Teste") == "Teste"
    assert treat_null_value(None) is None
    assert treat_null_value(pd.NA) is None

def test_tickets_to_decimal():
    assert tickets_to_decimal("100,00") == Decimal("100.00")
    assert tickets_to_decimal("150.50") == Decimal("150.50")
    assert tickets_to_decimal(None) is None
    assert tickets_to_decimal(pd.NA) is None