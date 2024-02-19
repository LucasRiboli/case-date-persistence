import psycopg2
from psycopg2 import sql

connection_params = {
    "host": "db",
    "database": "persistencia",
    "user": "postgres",
    "password": "postgres",
    "port": 5432
}


def save_to_database(data: list):
    """Persistencia no banco

    Args:
        data (list): lista gerada para ser persistida
    """
    connection = psycopg2.connect(**connection_params)
    cursor = connection.cursor()

    for row in data:
        query = sql.SQL("""
            INSERT INTO dados (
                cpf, private, incompleto, data_ultima_compra,
                ticket_medio, ticket_ultima_compra,
                loja_mais_frequente, loja_ultima_compra
            ) VALUES (
                {}, {}, {}, {}, {}, {}, {}, {}
            )
        """).format(
            sql.Literal(row['cpf']),
            sql.Literal(row['private']),
            sql.Literal(row['incompleto']),
            sql.Literal(row['data_ultima_compra']),
            sql.Literal(row['ticket_medio']),
            sql.Literal(row['ticket_ultima_compra']),
            sql.Literal(row['loja_mais_frequente']),
            sql.Literal(row['loja_ultima_compra'])
        )

        try:
            cursor.execute(query)
        except Exception as e:
            print(row)
            print(f"Erro ao inserir dados: {e}")

    connection.commit()

    cursor.close()
    connection.close()


def create_table():
    """Cria tabela dados no banco

    """
    connection = psycopg2.connect(**connection_params)
    cursor = connection.cursor()

    query = """
        CREATE TABLE IF NOT EXISTS dados (
            id SERIAL PRIMARY KEY,
            cpf VARCHAR(15),
            private INTEGER,
            incompleto INTEGER,
            data_ultima_compra DATE,
            ticket_medio DECIMAL(10, 2),
            ticket_ultima_compra DECIMAL(10, 2),
            loja_mais_frequente VARCHAR(15),
            loja_ultima_compra VARCHAR(15),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """

    try:
        cursor.execute(query)
    except Exception as e:
        print(f"Erro ao criar a tabela: {e}")

    connection.commit()
    cursor.close()
    connection.close()
