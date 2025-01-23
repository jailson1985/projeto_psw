# Project Breweries Data Importer

Este projeto é uma ferramenta para importar dados de cervejarias de uma API, salvar esses dados em arquivos JSON e armazená-los em um banco de dados.

## Índice

1. [Sobre](#sobre)
2. [Instalação](#instalacao)
3. [Uso](#uso)
4. [Docker](#docker)
5. [Tecnologias](#tecnologias)
6. [Contribuição](#contribuicao)
7. [Licença](#licenca)

## Sobre

Este projeto automatiza o processo de coleta de dados de cervejarias utilizando a API do Open Brewery DB. Ele importa os dados em formato JSON e os salva em um banco de dados. Além disso, realiza a contagem das cervejarias agrupadas por país, estado, cidade e tipo.

## Instalação

Para executar este projeto, siga as instruções abaixo:

1. Clone o repositório:
    ```bash
    git clone https://github.com/seu-usuario/seu-repositorio.git
    ```
2. Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```
3. Configure as variáveis de ambiente, se necessário.

### Uso

Para utilizar este projeto, execute as seguintes tarefas do Celery:

1. `import_breweries_task()`: Importa os dados das cervejarias da API e salva em arquivos JSON.
2. `import_breweries_from_file()`: Lê os dados dos arquivos JSON e os insere no banco de dados.
3. `count_brewery()`: Realiza a contagem das cervejarias agrupadas e salva os resultados no banco de dados.

### Rotas da API

As principais rotas disponíveis na API são:

- `GET /breweries/`: Lista todas as cervejarias.
- `GET /model-contagem/`: Lista a contagem modelada das cervejarias.

### Documentação da API

Você pode acessar a documentação da API gerada pelo Swagger nos seguintes endpoints:

- `GET /swagger/`: Interface do Swagger UI.
- `GET /swagger.json/`: Documentação no formato JSON.

## Docker

Para executar este projeto utilizando Docker:

1. Crie uma imagem Docker a partir do `Dockerfile` incluído no projeto:
    ```bash
    docker build -t breweries-data-importer .
    ```
2. Inicie um contêiner usando a imagem criada:
    ```bash
    docker run -d -p 8000:8000 breweries-data-importer
    ```
## Tecnologias

As principais tecnologias usadas neste projeto são:

- **Python**: Linguagem de programação utilizada.
- **Django**: Framework web utilizado para manipulação de dados.
- **Django REST Framework**: Biblioteca para a construção de APIs RESTful.
- **drf-yasg**: Biblioteca para gerar e documentar APIs usando Swagger.
- **Celery**: Biblioteca para tarefas assíncronas e agendamento de tarefas.
- **Requests**: Biblioteca para realizar requisições HTTP.
- **JSON**: Formato para salvar e manipular dados das cervejarias.
- **SQLite / PostgreSQL**: Banco de dados para armazenar as informações.

## Contribuição

Se você deseja contribuir com este projeto, siga as etapas abaixo:

1. Fork o repositório.
2. Crie uma nova branch (`git checkout -b feature/nova-feature`).
3. Faça as alterações necessárias e commit (`git commit -am 'Adicionar nova feature'`).
4. Push para a branch (`git push origin feature/nova-feature`).
5. Abra um Pull Request.

## Licença

Este projeto está licenciado sob a Licença MIT. Consulte o arquivo `LICENSE`


