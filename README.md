# ECD14


Projeto de API de contatos usando FastAPI, Docker e GraphQL para a disciplina Arquitetura de Microsserviços da Especialização em Engenharia de Software para Aplicações de Ciência de Dados.

---

## Como rodar usando Terminal

1. **Execute**

    ```bash
   pip install -r requirements.txt
    ```
    ```bash
   uvicorn app.main:app --reload
   ```  

3. Acesse a API em: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## Como rodar usando Docker

1. **Construa a imagem Docker:**
   ```bash
   docker build -t ecd14-api .
   ```

2. **Execute o container:**
   ```bash
   docker run -d -p 8000:8000 ecd14-api
   ```

3. Acesse a API em: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## Rodando o teste (test_api.py)

1. Certifique-se que a API está rodando.
2. Em outro terminal, execute:
   ```
   python teste_api.py
   ```
3. Siga as instruções para inserir nome, categoria e um ou mais telefones. É possível também consultar os contatos já inseridos.

Por exemplo:

![image](https://github.com/user-attachments/assets/71697531-1cbe-4d2b-9c19-88afe8cc5a4c)

---

## GraphQL

1. Acesse [http://localhost:8000/graphql](http://localhost:8000/graphql) para acessar o playground.
2. As queries a seguir podem ser executadas:

```graphql
query {
  contatos {
    id
    nome
    categoria
    telefones {
      numero
      tipo
    }
  }
}
```

### Mutation para criar um contato

```graphql
mutation {
  criarContato(
    contato: {
      nome: "Jose",
      categoria: "familiar",
      telefones: [
        { numero: "00000000", tipo: "movel" }
      ]
    }
  ) {
    id
    nome
    categoria
    telefones {
      numero
      tipo
    }
  }
}
```

Por exemplo, resultando em:

![image](https://github.com/user-attachments/assets/5f2c4eda-b826-4c27-9caf-822e7ef5a24f)


## Endpoints REST principais

- `POST /contatos/` – cria um contato
- `GET /contatos/` – lista todos os contatos
- `GET /contatos/{id}` – consulta contato por ID

---

## Requisitos

- Python 3.8+
- Docker 
