# FastAPI Data Persistence

Projeto voltado para persistencia de dados em um banco de dados relacional (PostgreSQL).
Case feito em cima do processo técnico da NeoWay pensando em seu processo seletivo. 

## Requisitos Obrigatórios

- Python 3.8 ou superior
- Docker e Docker Compose

## Configuração do Ambiente

1. Clone o repositório:

    ```bash
        git clone https://github.com/LucasRiboli/case-date-persistence.git
        cd case-date-persistence
    ```

2. Instale as dependências:

    ```bash
        pip install -r app/requirements.txt
    ```

## Executando o Projeto

1. Inicie o projeto usando o Docker Compose:

    ```bash
    docker-compose up --build
    ```

2. A API estará disponível em [http://localhost:8000](http://localhost:8000).

## Endpoints

### Criar Tabela no Banco de Dados


##### - *Necessario executar primeiro para se ter a tabela onde ser persistido os dados* 

- **Endpoint:** `/table/`
- **Método:** POST
- **Descrição:** Cria a tabela padrão "dados" no banco de dados.
- **Exemplo de Uso:**

    ```bash
    curl -X POST http://localhost:8000/table/
    ```

### Upload de Arquivo para Persistência de Dados

- **Endpoint:** `/persistence/`
- **Método:** POST
- **Descrição:** Realiza a persistência dos dados contidos no arquivo enviado (formatos .txt ou .csv).
- **Exemplo de Uso:**

    ```bash
    curl -X POST -F "file=@files/base_teste.txt" http://localhost:8000/persistence/
    ```

    Adicione o seu path como um sufixo para "/files/base_teste.txt" e assim ter o caminho real do arquivo do teste do case.

### Visualizando os dados persistidos no banco

1. Pegando id do container case-date-persistence-db-1
    ```bash
    docker-compose ps
    ```
2. Acessando o terminal do container 
    ```bash
    docker exec -it {id} /bin/bash 
    ```
3. Dentro do Container acesso o banco 
    ```bash
    psql -U postgres -d persistencia 
    ```
4. Por fim faça um select na tabela
    ```sql
    SELECT * FROM dados;
    ```
### Encerrando projeto

1. Encerre com projeto:

    ```bash
    docker-compose down
    ```

## Observações

- Certifique-se de que o Docker e o Docker Compose estão instalados na sua máquina.
- Personalize as configurações de conexão do banco de dados no arquivo `db_handler.py` para rodar local.