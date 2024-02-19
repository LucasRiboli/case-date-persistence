from fastapi import FastAPI
from fastapi import File, UploadFile
from data_handler import process_file
from db_handler import save_to_database, create_table
import uvicorn
import json


app = FastAPI()


@app.post("/table/")
async def create_database_table():
    """Endpoint de criação de tabela padrão "dados"

    Returns:
        json: response da chamada
    """
    try:
        create_table()
        return json.dumps({"message": "Table created or already exists"})
    except Exception as e:
        return json.dumps({'error': str(e)})


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    # Faz persistencia dos dados
    try:
        data = process_file(file)
        save_to_database(data)
        return json.dumps({'message': 'Data persisted successfully!'})
    except Exception as e:
        return json.dumps({'error': str(e)})


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
