

# 🎬 UserMovieService

![GitHub Repo Size](https://img.shields.io/github/repo-size/ArturRabello/UserMovieService?style=for-the-badge) ![Linguagens](https://img.shields.io/github/languages/count/ArturRabello/UserMovieService?style=for-the-badge&logoWidth=40&labelWidth=100)

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white) ![openapi initiative](https://img.shields.io/badge/openapiinitiative-%23000000.svg?style=for-the-badge&logo=openapiinitiative&logoColor=white) ![Swagger](https://img.shields.io/badge/-Swagger-%23Clojure?style=for-the-badge&logo=swagger&logoColor=white) ![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)

A UserMovieService API é uma aplicação independente, responsável por gerenciar a relação dos usuários com seus filmes. Seu principal objetivo é oferecer um meio simples e organizado para que cada pessoa registre os títulos assistidos, associe notas e avaliações personalizadas e mantenha um histórico individual de obras.

Por ser independente, a UserMovieService pode ser integrada a qualquer sistema de cinema, streaming ou catálogo de filmes, não estando limitada apenas ao CineKeep. Ela possibilita operações essenciais como adicionar filmes à conta do usuário, atualizar avaliações, remover títulos e consultar a lista completa de obras relacionadas, garantindo praticidade e consistência no gerenciamento de dados.

Essa flexibilidade torna a UserMovieService uma ferramenta reutilizável e versátil, permitindo que diferentes plataformas ofereçam recursos de acompanhamento de filmes de forma centralizada, sem depender de implementações específicas em cada sistema.

## 🎯 Propósito

Este projeto foi desenvolvido como parte do programa de **Pós-Graduação em Desenvolvimento Full Stack da PUC Rio**, tendo como objetivo principal a **consolidação prática de conceitos teóricos estudados durante o curso**.

O desenvolvimento dessa aplicação, me permitiu aprimorar as minhas habilidades com as arquiteturas de desenvolvimento de software, implantação de containers atravez do docker e uma maior aprofundamento da ferramenta React

A ideia desse projeto foi simular uma pequena arquitetura de microsserviços, onde cada API é independente e autônoma, ou seja, consegue viver e operar sem depender diretamente dos outros serviços.

## Diagrama

![alt text](./assets/diagrama.png)

## 🔗 Componentes do Projeto CineKeep

- **[CineKeep](https://github.com/ArturRabello/CineKeep)** → Aplicação front-end
- **[AuthService](https://github.com/ArturRabello/AuthService)** → Api responsável por armazenar e gerenciar os filmes avaliados/salvos pelos usuários.
- **[API OMDB](https://www.omdbapi.com/)** → Api responsavel por fornece os dados dos filmes. 

## 🚀 Tecnologias

- **Flask** (framework web)
- **PostgreSQL** (banco de dados relacional (via psycopg2))
- **JWT** (autenticação com tokens)
- **Marshmallow** (validação e serialização de dados)
-  **Flask-CORS** (abilitação de CORS)
- **Docker** (Container)
- **Flask-Smorest / OpenAPI / Swagger** (documentação da API)



## 🛠️ Como utilizar 

### 2️⃣Clone o repositório:
```bash
git clone https://github.com/ArturRabello/UserMovieService.git
```
### 3️⃣ Instale as dependências:

```bash
(env)$ pip install -r requirements.txt
```

### 4️⃣ Executar localmente com NPM

**OBS**:Para rodar a aplicação, é necessário criar manualmente a tabela no PostgreSQL., [instale aqui.](https://www.postgresql.org/download/)

O nome da tabela deve ser **UserMovies**

No arquivo **database.py** você deve subistituir:


```bash
    DataBase_Url = os.getenv("DATABASE_URL")
```
 Por: 
````Bash
    DATABASE_URL = "postgresql://[SEU_USUARIO]:[SUA_SENHA]@localhost:5432/[NOME_DO_BANCO]"
````

**Execute a API atráves do flask:**
```bash
(env)$ flask run --host 0.0.0.0 --port 5100
```
**Em modo de desenvolvimento é recomendado executar utilizando o parâmetro reload, que reiniciará o servidor automaticamente após uma mudança no código fonte.**
```bash
(env)$ flask run --host 0.0.0.0 --port 5100 --reload
```

### 5️⃣ Execute em um container Docker
**Será necessario que você tenha o Docker Desktop instalado em sua maquina.**
- [Windows](https://docs.docker.com/desktop/setup/install/windows-install/)
- [Linux](https://docs.docker.com/desktop/setup/install/linux/)
- [Mac](https://docs.docker.com/desktop/setup/install/mac-install/)

**Caso seu sistema operacional seja Windows ou Mac, será necessário instalar o [WSL 2](https://learn.microsoft.com/pt-br/windows/wsl/install)**

#### DockerFile
O Dockerfile define como a aplicação Python será construída e executada.

- **Imagem base** → Python 3.13.3, que fornece todas as bibliotecas padrão do Python.

- **Diretório de trabalho** → /app, onde o código será copiado e executado.

- **Instalação de dependências** → pip instala todos os pacotes listados em requirements.txt sem cache, garantindo que a imagem fique leve.

- **Variáveis de ambiente** → definem a configuração do Flask (app, host, porta e modo de desenvolvimento).

- **CMD** → comando para iniciar o Flask quando o container subir.


**Eu recomendo utilizar esse dockerfile.**

```
FROM python:3.13.3

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=development
ENV FLASK_RUN_PORT=5100

CMD [ "flask", "run" ]
```

#### Docker Compose

O Docker Compose permite orquestrar múltiplos containers, incluindo o banco de dados e o AuthService.

- **db (Postgres)**

    - Imagem oficial do PostgreSQL 17.

    - Define usuário, senha e banco de dados.

    - Porta 5532 mapeada para acesso local.

    - Volume persistente para manter os dados mesmo que o container seja recriado.

- **web (AuthService)**

    - Constrói a imagem usando o Dockerfile local.

    - Porta 5100 exposta para acessar a API via navegador ou frontend.

    - Variável de ambiente DATABASE_URL conecta a aplicação ao Postgres.

    - depends_on garante que o banco de dados seja iniciado antes do serviço.

    - Volume mapeia a pasta local /app para dentro do container, facilitando alterações no código em tempo de execução.

```
services:
  db:
    image: postgres:17
    container_name: postegres_db_movieUser
    restart: always
    environment:
      POSTGRES_USER: postgres_db_movieUser
      POSTGRES_PASSWORD: postgres_db_movieUser
      POSTGRES_DB: postgres_db_movieUser
    ports:
      - "5532:5532"
    volumes:
      - pgdata:/var/lib/postegresql/data

  web:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: movieUser_service
    ports:
      - 5100:5100
    environment:
      - DATABASE_URL=postgresql://postgres_db_movieUser:postgres_db_movieUser@db/postgres_db_movieUser
    depends_on:
      - db
    volumes:
      - ./app:/app

volumes:
  pgdata:
```

#### Construir a imagem e subir o container

**Controi a imagem**
```
docker compose build
```

**Cria containers (se não existirem) e sobe eles. Pode rebuildar imagens se necessário.**

```
docker compose up
```

**Inicia o container**
```
docker compose start
```

## 🔍 funcionalidades

**UserMovieService**

O UserMovieService é uma API responsável por gerenciar a associação entre usuários e filmes. Permite que cada usuário adicione filmes à sua lista, atualize avaliações, verifique filmes adicionados e recupere suas listas de forma segura, usando autenticação baseada em token.

- **Adicionar filme à lista do usuário** - POST /movieUser/addMovies

- **Remover filme da lista do usuário** - DELETE /movieUser/removeMovies

- **Atualizar avaliação de um filme** - PUT /movieUser/setScore

- **Listar filmes do usuário** - GET /movieUser/getList

- **Verificar se um filme já foi adicionado** - GET /movieUser/verifyMovie

- **Obter avaliação de um filme** - GET /movieUser/getScore

- **Testar autenticação** - GET /movieUser/testAuth

- **Gerar token de desenvolvimento** - POST /movieUser/setTokenDev

## 📂 Estrutra do projeto

```
📦 UserMovieService - Back-end
├── 📂 app
│   ├── ⚙️ app.py              → Arquivo principal da aplicação Flask
│   ├── ⚙️ database.py         → Configuração do banco de dados e conexão via SQLAlchemy
│   ├── ⚙️ models.py           → Modelos de dados (ex: User)
│   ├── ⚙️ schemas.py          → Esquemas de validação e serialização (Marshmallow)
│   ├── ⚙️ token_services.py   → Serviços de geração e validação de tokens JWT
│   └── 📂 __pycache__         → Arquivos compilados automaticamente pelo Python
├── 🐳 docker-compose.yml      → Orquestração dos containers (Flask + PostgreSQL)
├── 🐳 Dockerfile              → Instruções para build da imagem Docker do serviço
├── 📜 requirements.txt        → Dependências do projeto (Flask, SQLAlchemy, JWT, etc)
└── 📌 README.md               → Documentação geral do projeto
```
# 📌 Documentação da API – Movie Service

### 🔹 Adicionar Filme
```bash
POST /movieUser/addMovies
```
| Parâmetro   | Tipo    | Descrição |
|-------------|---------|------------|
| `movie_id`  | integer | **Obrigatório.** ID do filme |
| `score`     | float   | **Obrigatório.** Pontuação do filme |

**Requer token válido (cookie `token` ou header `Authorization: Bearer <token>`).**

**Respostas:**
| Código | Descrição |
|--------|------------|
| 201 | Filme adicionado com sucesso |
| 400 | Erro de validação |
| 401 | Token expirado ou inválido |
| 409 | Filme já existe |
| 500 | Erro no banco de dados |

---

### 🔹 Remover Filme
```bash
DELETE /movieUser/removeMovies?movie_id={movie_id}
```
| Parâmetro   | Tipo    | Descrição |
|-------------|---------|------------|
| `movie_id`  | integer | **Obrigatório.** ID do filme a ser removido |

**Requer token válido (cookie `token` ou header `Authorization: Bearer <token>`).**

**Respostas:**
| Código | Descrição |
|--------|------------|
| 201 | Filme removido com sucesso |
| 400 | Erro de validação |
| 401 | Token expirado ou inválido |
| 409 | Usuário não encontrado |
| 500 | Erro no banco de dados |

---

### 🔹 Atualizar Pontuação
```bash
PUT /movieUser/setScore
```
| Parâmetro   | Tipo    | Descrição |
|-------------|---------|------------|
| `movie_id`  | integer | **Obrigatório.** ID do filme |
| `score`     | float   | **Obrigatório.** Nova pontuação do filme |

**Requer token válido (cookie `token` ou header `Authorization: Bearer <token>`).**

**Respostas:**
| Código | Descrição |
|--------|------------|
| 201 | Pontuação atualizada com sucesso |
| 400 | Erro de validação |
| 401 | Token expirado ou inválido |
| 409 | Usuário não encontrado |
| 500 | Erro no banco de dados |

---

### 🔹 Obter Lista de Filmes
```bash
GET /movieUser/getList
```

**Requer token válido (cookie `token` ou header `Authorization: Bearer <token>`).**

**Respostas:**
| Código | Descrição |
|--------|------------|
| 200 | Lista de filmes retornada com sucesso |
| 400 | Erro de validação |
| 401 | Token expirado ou inválido |
| 409 | Usuário não encontrado |
| 500 | Erro no banco de dados |

---

### 🔹 Verificar Filme
```bash
GET /movieUser/verifyMovie?movie_id={movie_id}
```
| Parâmetro   | Tipo    | Descrição |
|-------------|---------|------------|
| `movie_id`  | integer | **Obrigatório.** ID do filme a ser verificado |

**Requer token válido (cookie `token` ou header `Authorization: Bearer <token>`).**

**Respostas:**
| Código | Descrição |
|--------|------------|
| 200 | Filme já foi adicionado |
| 400 | Erro de validação |
| 401 | Token expirado ou inválido |
| 404 | Filme não encontrado |

---

### 🔹 Obter Pontuação do Filme
```bash
GET /movieUser/getScore?movie_id={movie_id}
```
| Parâmetro   | Tipo    | Descrição |
|-------------|---------|------------|
| `movie_id`  | integer | **Obrigatório.** ID do filme |

**Requer token válido (cookie `token` ou header `Authorization: Bearer <token>`).**

**Respostas:**
| Código | Descrição |
|--------|------------|
| 201 | Pontuação encontrada com sucesso |
| 400 | Erro de validação |
| 401 | Token expirado ou inválido |
| 409 | Usuário não encontrado |
| 500 | Erro no banco de dados |

---

## 🔐 Autenticação

Esta API utiliza autenticação baseada em tokens JWT. O token pode ser fornecido de duas formas:

1. **Cookie:** `token` (configurado automaticamente pelo endpoint `/setTokenDev`)
2. **Header:** `Authorization: Bearer <token>`

### Exemplo de uso com header:
```bash
curl -X GET "http://localhost:5000/movieUser/getList" \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
```

## 🌐 CORS

A API está configurada para aceitar requisições de `http://localhost:3000` com suporte a credenciais.