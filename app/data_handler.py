import pandas as pd
from decimal import Decimal
import logging

def process_file(file: any) -> list:
    """Processo de tratamento de dados e validacao

    Args:
        file (any): arquivo recebido via chamada

    Returns:
        list: lista de dados a serem persistidos
    """
    try:
        with open(file.filename, "wb") as f:
            f.write(file.file.read())

        df = pd.read_csv(
            file.filename, delim_whitespace=True, skiprows=1, header=None,
            names=[
                "CPF",
                "PRIVATE",
                "INCOMPLETO",
                "DATA DA ÚLTIMA COMPRA",
                "TICKET MÉDIO",
                "TICKET DA ÚLTIMA COMPRA",
                "LOJA MAIS FREQUÊNTE",
                "LOJA DA ÚLTIMA COMPRA"])

        df.columns = df.columns.str.strip()
        data = []
        # Intera lista de dados para persistencia baseado no dataframe
        for _, row in df.iterrows():
            if validate_document(row["CPF"]):
                data.append({
                    "cpf": clean_cpf_cnpj(row["CPF"]),
                    "private": row["PRIVATE"],
                    "incompleto": row["INCOMPLETO"],
                    "data_ultima_compra": treat_null_value(
                        row["DATA DA ÚLTIMA COMPRA"]),
                    "ticket_medio": tickets_to_decimal(row["TICKET MÉDIO"]),
                    "ticket_ultima_compra": tickets_to_decimal(row[
                        "TICKET DA ÚLTIMA COMPRA"]),
                    "loja_mais_frequente": clean_cpf_cnpj(
                        treat_null_value(row["LOJA MAIS FREQUÊNTE"])),
                    "loja_ultima_compra": clean_cpf_cnpj(
                        treat_null_value(row["LOJA DA ÚLTIMA COMPRA"])),
                })
        return data
    except Exception as e:
        logging.ERROR(e)


def clean_cpf_cnpj(cpf_cnpj: str) -> str:
    """limpa string do cpf para apenas digitos

    Args:
        cpf_cnpj (str): cpf ou cnpj

    Returns:
        str: retorna apenas os digitos em string
    """
    if cpf_cnpj is not None:
        cpf_cnpj_numerico = ''.join(c for c in cpf_cnpj if c.isdigit())
        return cpf_cnpj_numerico


def treat_null_value(data: str) -> str:
    """Em casos de null/nan retorna None

    Args:
        data (str): string a ser valida

    Returns:
        str/None
    """
    if pd.isna(data):
        return None
    return data


def tickets_to_decimal(tickets: str) -> Decimal:
    """Torna os string ticket em Decimal

    Args:
        tickets (str): string ticket

    Returns:
        Decimal: ticket como decimal
    """
    if pd.isna(tickets):
        return None
    return Decimal(tickets.replace(',', '.'))


def validate_document(document: str) -> bool:
    """Valida o CPF/CNPJ
    ***funcao apresentado regras de validacao de CPF/CNPJ***
    Args:
        document (str): CPF/CNPJ

    Returns:
        bool: True: se for valido. False: se não for valido
    """
    document = ''.join(c for c in document if c.isdigit())

    if len(document) == 11:
        if document == document[0] * 11:
            return False

        def calculate_cpf_digit(position):
            total = sum(
                int(document[i]) * (position - i + 1) for i in range(position))
            remainder = total % 11
            return 0 if remainder < 2 else 11 - remainder

        return (
            calculate_cpf_digit(9) == int(document[9])
            and calculate_cpf_digit(10) == int(document[10])
        )

    elif len(document) == 14:
        if document == document[0] * 14:
            return False

        def calculate_cnpj_digit(position):
            total = sum(
                int(document[i]) * (position - i + 1) for i in range(position))
            remainder = total % 11
            return 0 if remainder < 2 else 11 - remainder

        return (
            calculate_cnpj_digit(12) == int(document[12])
            and calculate_cnpj_digit(13) == int(document[13])
        )

    else:
        return False
