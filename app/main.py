from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from data_handler import process_file
from db_handler import save_to_database, create_table
import uvicorn

app = FastAPI(swagger_ui_parameters={"syntaxHighlight": False})


@app.post("/table/")
def create_database_table():
    """Endpoint de criação de tabela padrão "dados"

    Returns:
        json: response da chamada
    """
    try:

        create_table()

        return JSONResponse(
            content={'message': 'Table created or already exists'},
            status_code=201)

    except Exception as e:
        return JSONResponse(content={'error': str(e)}, status_code=500)


@app.post("/persistence/")
def persistence_data_file(file: UploadFile = File(...)):
    """Endpoint de persistencia de dados

    Returns:
        json: response da chamada
    """
    try:

        data = process_file(file)
        save_to_database(data)

        return JSONResponse(
            content={'message': 'Data persisted successfully!'},
            status_code=201)

    except Exception as e:
        return JSONResponse(content={'error': str(e)}, status_code=500)


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
