# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

**Install dependencies:**
```
.venv\Scripts\pip install -r requirements.txt
```

**Run the server:**
```
.venv\Scripts\uvicorn app.main:app --reload
```

Interactive API docs are available at `http://127.0.0.1:8000/docs` when the server is running.

**Environment config** lives in `.env` at the project root. Variables: `DATABASE_URL`, `SECRET_KEY`, `ALGORITHM`, `ACCESS_TOKEN_EXPIRE_MINUTES`.

## Architecture

All application code lives in the `app/` package:

```
app/
├── main.py          — FastAPI app, exception handler, router registration, create_all
├── database.py      — SQLAlchemy engine / SessionLocal / Base (reads DATABASE_URL from config)
├── dependencies.py  — get_db session dependency (used across all routes)
├── core/
│   ├── config.py    — loads .env via python-dotenv, exposes DATABASE_URL / SECRET_KEY / etc.
│   └── auth.py      — password hashing, JWT encode/decode, get_current_user dependency
├── models/
│   ├── user.py      — User ORM model (id, email, name, username, hashed_password, created_at)
│   └── product.py   — Product ORM model (id, name, price, user_id FK → users.id)
├── schemas/
│   ├── user.py      — SignupRequest, LoginRequest, SignupResponse, LoginResponse, UserOut
│   └── product.py   — ProductCreate, ProductRead
└── routes/
    ├── auth.py      — POST /auth/signup, POST /auth/login
    └── products.py  — full CRUD under /products, all routes protected by get_current_user
```

**Import chain (no circular dependencies):**
`core/config` → `database` → `models/*` → `dependencies` → `core/auth` → `routes/*` → `main`

## Key conventions

- All routes except `/`, `/auth/signup`, and `/auth/login` require a Bearer token. Auth is enforced exclusively via `Depends(get_current_user)` — no per-route token logic.
- All error responses are `{"message": "..."}`. This is achieved by a global `@app.exception_handler(HTTPException)` in `main.py` that rewrites FastAPI's default `{"detail": "..."}` format. Routes use plain `raise HTTPException(...)`.
- Products are user-scoped: `Product` has a `user_id` FK, and all product queries filter by `current_user.id`. PUT/DELETE return `403` if the requester is not the owner.
- The `/products/search` route is declared **before** `/{product_id}` in `routes/products.py` to prevent FastAPI matching `search` as an integer path parameter.
- No migrations (Alembic is not set up); schema is managed entirely by `create_all`. If the `products` table already exists without the `user_id` column, drop it manually (`DROP TABLE products CASCADE;`) before first run.
- `echo=True` on the engine logs all SQL to stdout.
- `app/main.py` imports `app.models.user` and `app.models.product` explicitly (even though unused directly) to ensure both models are registered with `Base.metadata` before `create_all` runs.
