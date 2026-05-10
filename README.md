# FastAPI Practice

A RESTful API built with FastAPI, SQLAlchemy, and PostgreSQL featuring JWT authentication and user-scoped product management.

## Features

- User registration and login with JWT Bearer tokens
- Full CRUD for products, scoped per authenticated user
- PostgreSQL via SQLAlchemy ORM
- Password hashing with bcrypt
- Consistent `{"message": "..."}` error responses

## Tech Stack

- **FastAPI** — web framework
- **SQLAlchemy** — ORM
- **PostgreSQL** — database (via psycopg2)
- **python-jose** — JWT encoding/decoding
- **passlib / bcrypt** — password hashing
- **pydantic** — request/response validation
- **python-dotenv** — environment config

## Project Structure

```
app/
├── main.py            # App entry point, router registration, exception handler
├── database.py        # SQLAlchemy engine and session
├── dependencies.py    # get_db session dependency
├── core/
│   ├── config.py      # Loads .env variables
│   └── auth.py        # JWT logic, get_current_user dependency
├── models/
│   ├── user.py        # User ORM model
│   └── product.py     # Product ORM model (FK → users)
├── schemas/
│   ├── user.py        # User request/response schemas
│   └── product.py     # Product request/response schemas
└── routes/
    ├── auth.py        # POST /auth/signup, POST /auth/login
    └── products.py    # GET/POST/PUT/DELETE /products (protected)
```

## Setup

1. **Clone the repo and create a virtual environment:**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   .venv\Scripts\pip install -r requirements.txt
   ```

3. **Configure environment variables** — create a `.env` file at the project root:
   ```env
   DATABASE_URL=postgresql://user:password@localhost:5432/dbname
   SECRET_KEY=your-secret-key
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

4. **Run the server:**
   ```bash
   .venv\Scripts\uvicorn app.main:app --reload
   ```

The API will be available at `http://127.0.0.1:8000`.  
Interactive docs: `http://127.0.0.1:8000/docs`

## API Endpoints

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/auth/signup` | No | Register a new user |
| POST | `/auth/login` | No | Login, returns JWT token |
| GET | `/products` | Yes | List current user's products |
| POST | `/products` | Yes | Create a product |
| GET | `/products/search` | Yes | Search products by name |
| GET | `/products/{id}` | Yes | Get a product by ID |
| PUT | `/products/{id}` | Yes | Update a product (owner only) |
| DELETE | `/products/{id}` | Yes | Delete a product (owner only) |

All protected routes require `Authorization: Bearer <token>` header.
