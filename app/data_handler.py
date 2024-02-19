import pandas as pd
from decimal import Decimal


def process_file(file):
    # Define dataframe
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
