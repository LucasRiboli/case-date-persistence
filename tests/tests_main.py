import pytest
from fastapi.testclient import TestClient
from app.main import app, create_table, save_to_database


@pytest.fixture
def client():
    client = TestClient(app)
    return client


def test_create_table(client):
    response = client.post("/table/")
    assert response.status_code == 201
    assert response.json() == {'message': 'Table created or already exists'}


def test_create_upload_file(client, tmp_path):
    content = """CPF PRIVATE INCOMPLETO DATA DA ÚLTIMA COMPRA TICKET MÉDIO TICKET DA ÚLTIMA COMPRA LOJA MAIS FREQUÊNTE LOJA DA ÚLTIMA COMPRA
            123.456.789-09 1 False 2022-01-01 100.50 150.75 StoreA StoreB
            """
    file_path = tmp_path / "sample_file.txt"
    with open(file_path, "w") as f:
        f.write(content)

    files = {'file': open(file_path, 'rb')}
    response = client.post("/persistence/", files=files)
    assert response.status_code == 201
    assert response.json() == {'message': 'Data persisted successfully!'}
