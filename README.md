# GMS BCB API (Monitoramento de Normativos do Banco Central)

API e Bot desenvolvidos em Python para o monitoramento automatizado de normativos publicados pelo Banco Central do Brasil (BCB). A aplicação verifica periodicamente a página do Banco Central, captura as atualizações, armazena-as em um banco de dados PostgreSQL (para evitar envio em duplicidade) e realiza disparos de notificações formatadas para um grupo/contato do WhatsApp através da [Evolution API](https://github.com/EvolutionAPI/evolution-api).

## 🚀 Tecnologias e Ferramentas

- **Linguagem:** Python 3.14+
- **Gerenciador de Pacotes e Ambientes:** [uv](https://github.com/astral-sh/uv)
- **Agendamento de Tarefas:** APScheduler (Roda verificações a cada 10 minutos, entre 6h e 22h)
- **Banco de Dados:** PostgreSQL (utlizando SQLAlchemy ORM e Alembic para migrations)
- **Integração:** Evolution API (Envios pro WhatsApp) e Requests (Busca na API pública do BCB)
- **Infraestrutura:** Docker & Docker Compose (Stack completa: App, Evolution API, Postgres, Redis)
- **Qualidade de Código e Scripts:** Ruff, Taskipy, typos

## ⚙️ Normativos Monitorados

A aplicação monitora e notifica sempre que um dos seguintes tipos de normativos for detectado:

- 🔴 Resolução Conjunta
- 🔴 Resolução CMN
- 🔴 Resolução BCB
- 🔵 Instrução Normativa Conjunta
- 🔵 Instrução Normativa BCB
- 🟢 Portaria Conjunta
- 🟢 Ato Normativo Conjunto
- 🟢 Decisão Conjunta

## 📦 Como Instalar e Executar

### Pré-requisitos
- [Docker](https://docs.docker.com/get-docker/) e [Docker Compose](https://docs.docker.com/compose/install/) (se for rodar via contêineres).
- [uv](https://docs.astral.sh/uv/) instalado globalmente no seu ambiente de desenvolvimento.

### Instalação (Ambiente de Desenvolvimento)

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/matheusfabiao/api-banco-central-gms.git
   cd gms-bcb-api
   ```

2. **Sincronize as dependências e crie o ambiente virtual (automático com o uv):**
   ```bash
   uv sync
   ```

### Configuração do Ambiente (.env)

O primeiro passo antes de rodar qualquer coisa é configurar as variáveis de ambiente essenciais.

1. Faça uma cópia do arquivo de exemplo:
   ```bash
   cp .env.example .env
   ```
2. Edite o `.env` e foque nas variáveis indispensáveis:
   - Configurações da **Evolution API**: `AUTHENTICATION_API_KEY`, `EVOLUTION_INSTANCE_NAME`, `EVOLUTION_GROUP_JID` (ex: `123456789@g.us`).
   - Credenciais do **PostgreSQL** e **Redis**: `DATABASE_CONNECTION_URI`, `APP_DATABASE_URL`, etc.

### Executando o Projeto

O projeto pode ser executado de duas formas, dependendo do seu ambiente e necessidade:

#### 1. Modo Produção (Comandos Docker Compose)

Para ambientes onde não temos ferramentas de desenvolvimento instaladas (como o `uv` e `taskipy`), você deve utilizar os comandos nativos do Docker Compose. Siga a ordem recomendada:

1. **Inicie o banco de dados PostgreSQL:**
   Primeiramente, suba o container do banco de dados:
   ```bash
   docker compose up -d postgres
   ```
   *Dica: Você pode conferir as tabelas criadas no banco acessando-o via terminal:*
   ```bash
   docker compose exec postgres psql -U postgres
   ```
   *E posteriormente digitando `\dt`. Para ver o conteúdo das tabelas, utilize o comando `SELECT * FROM <nome_da_tabela>;`. Em caso de bug ou testes, você pode limpar os dados da tabela com comandos de exclusão como `TRUNCATE TABLE <nome_da_tabela>;`.*

2. **Inicie o serviço do Evolution API:**
   Após verificar a saúde do container do PostgreSQL, suba o Evolution API:
   ```bash
   docker compose up -d evolution-api
   ```
   > ⚠️ **IMPORTANTE:** Acesse o manager do Evolution API (por exemplo, `http://localhost:8080/manager`), efetue o login e gerencie a configuração da sua instância do WhatsApp. Pular essa etapa poderá gerar erros na aplicação principal, que depende dessa instância devidamente configurada no Evolution API para funcionar completamente e realizar o envio das mensagens.

3. **Inicie a aplicação principal (App):**
   Com a instância configurada, suba o serviço da aplicação web:
   ```bash
   docker compose up --build app
   ```
   *(Para execuções posteriores, você pode usar apenas `docker compose up app`)*

#### 2. Modo Desenvolvimento (Atalhos com Taskipy)

Para o desenvolvimento local, o arquivo `pyproject.toml` expõe atalhos rápidos via Taskipy para facilitar sua vida e evitar comandos longos. Com o ambiente `uv` em uso, você pode executar:

- **Subir o banco de dados em background:**
  ```bash
  uv run task db_up
  ```
- **Acessar o terminal do banco (psql):**
  ```bash
  uv run task db_shell
  ```
- **Subir a Evolution API:**
  ```bash
  uv run task evo_up
  ```
- **Fazer o build e subir a aplicação:**
  ```bash
  uv run task app_up
  ```
- **Subir a aplicação (sem rebuild):**
  ```bash
  uv run task app_run
  ```
- **Derrubar os containers:**
  ```bash
  uv run task down
  ```
  *(Dica: Caso queira excluir os dados do banco e Redis durante a derrubada, rode `uv run task downv`)*

## 📱 Exemplo de Notificação (WhatsApp)

Quando a aplicação detectar novos normativos desde a última varredura, uma requisição será enviada para a Evolution API e a seguinte mensagem deve aparecer no seu WhatsApp:

```text
⚪ *NORMA XPTO N° 43.746*  
Publicado em: 26/8/2025 às 09:35  
  
*Assunto:*
Divulga nome aprovado de pessoas eleitas/nomeadas para cargos de órgãos estatutários ou contratuais de sociedades autorizadas a funcionar pelo Banco Central do Brasil.  
  
Responsável: *DEORF*

🔗 *Link Oficial:* [url_oficial_do_bcb]
```

## 🗄️ Trabalhando com Banco de Dados e Migrations

As migrations ficam a cargo do `Alembic` localizando-se na pasta `migrations/`.

- **Criar uma nova migration:** (após editar/adicionar os models no diretório `models/`).
  ```bash
  uv run alembic revision --autogenerate -m "Descrição objetiva da alteração"
  ```
- **Aplicar as migrations:** (O banco precisa estar rodando)
  ```bash
  uv run alembic upgrade head
  ```

## 🛠️ Utilitários (Taskipy)

Existem várias configurações prontas para limpar o código e padronizar. Inicie qualquer task rodando o comando com `uv run`. Exemplos:

- `uv run task lint` → Roda o avaliador da estrutura do código e aponta problemas.
- `uv run task format` → Aplica as formatações e estilizações usando Ruff.
- `uv run task pre_lint` → Busca e avisa sobre variados "typos" enraizados no código.
