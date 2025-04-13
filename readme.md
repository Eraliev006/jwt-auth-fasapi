# 🔐 FastAPI JWT Auth API

#### A minimalist authentication API built with FastAPI using JWT (JSON Web Tokens). It allows users to register, log in, and access protected routes

---

## 🚀 Features
- ✅ User registration and login
- 🔐 JWT based authentication (access & refresh token)
- ♻️ Token refresh endpoint
- ⚡ Async database interaction with SQLModel (SQLAlchemy core + Pydantic)
- 🧪 Test coverage using Pytest

## 🛠 Tech Stack

- [FastAPI](https://fastapi.tiangolo.com/) — modern Python web framework
- [SQLModel](https://sqlmodel.tiangolo.com/) — combines SQLAlchemy & Pydantic
- [PostgreSQL](https://www.postgresql.org/) — relational database
- [Redis](https://redis.io/) — in-memory store for refresh token sessions
- [Alembic](https://alembic.sqlalchemy.org/) — for database migrations
- [PyJWT](https://pyjwt.readthedocs.io/) — JWT creation and verification
- [Pytest](https://docs.pytest.org/) — testing framework

## 📦 Installation

```bash
git clone https://github.com/Eraliev006/jwt-auth-fastapi.git
cd fastapi-jwt-auth
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt 
```

## ⚙️ Environment Variables

Before running the project, create a `.env` file in the root directory with the following variables:

```env
smtp__sender_email = sender_email
smtp__smtp_server = smtp_server
smtp__smtp_port = smtp_port
smtp__smtp_login = smtp_login
smtp__smtp_password = smtp_password

jwt__secret_key = your_sercret_key
jwt__algorithm = HS256
jwt__email_token_expire_minutes = 5

db__db_url = DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/yourdb

HOST = localhost
PORT = 8000

redis__redis_host = localhost
redis__redis_port = 6379
```

## 🚀 Run the Project

To run the app in development mode:

`uvicorn app.main:app --reload`

This will start the FastAPI app on http://localhost:8000. The interactive Swagger documentation will be available at:

📄 http://localhost:8000/docs

## 🔄 Database Migrations (Alembic)
```
This project uses **Alembic** for managing SQLModel-based database migrations.

### ⚙️ Configuration

Alembic is preconfigured to work with `SQLModel` using a custom `env.py`. The configuration file `alembic.ini` is located in the project root.

### 📦 How to Create and Apply Migrations

1. **Generate a new migration:**

bash alembic revision --autogenerate -m "Add user table"

2. Apply the migration to the database:

alembic upgrade head

3. Downgrade (if needed):

alembic downgrade -1
```

## 📁 Alembic Directory Structure

```
alembic/
├── versions/             # Auto-generated migration scripts
├── env.py                # Migration environment config
├── script.py.mako        # Template for new migrations
alembic.ini   
```

## 🧪 Run Tests
To run tests with Pytest:

`pytest`

## 📁 Project Structure
```commandline
jwt-auth-fastapi/
├── alembic/                  # Alembic migrations script  
├── app/                      # Main application package
│   ├── main.py               # FastAPI app instance and startup logic
│   ├── api/                  # Route definitions (users, auth, etc.)
│   ├── models/               # SQLModel classes (User, Token, etc.)
│   ├── schemas/              # Request/response models (optional overrides)
│   ├── services/             # Business logic (e.g., auth, user management)
│   ├── db/                   # Database and Redis connections
│   ├── core/                 # Config, security, and JWT helpers
├── tests/                    # Unit tests for the app
├── .env                      # Environment configuration (not committed)
├── requirements.txt          # File contains the libraries required to run the application
├── pytest.ini                # Contains configuration for running tests with pytest.
├── alembic.ini               # Stores configuration settings for Alembic database migrations
├── logging_config.py         # Defines the logging configuration used throughout the application
```
# 👨‍💻 Author

Made with ❤️ using FastAPI, SQLModel & Redis

[📬github.com/Eraliev006](github.com/Eraliev006)

Feel free to fork, contribute, or open issues!