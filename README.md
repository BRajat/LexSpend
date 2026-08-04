# LexSpend
AI-Powered Legal Invoice Tracking & Spend Management

## Local Development

### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL 14+

---

### 1. Clone the repository

```bash
git clone https://github.com/BRajat/LexSpend.git
cd LexSpend
```

---

### 2. Backend (FastAPI)

#### Set up a virtual environment and install dependencies

```bash
cd backend
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

#### Configure environment variables

Create a `.env` file inside the `backend/` directory:

```env
DATABASE_URL=******localhost:5432/lexspend
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o-mini
CORS_ORIGINS=["http://localhost:3000"]
SECRET_KEY=change-me-in-production
```

#### Create the database and run migrations

```bash
# Create the database (one-time)
createdb lexspend

# Apply Alembic migrations
alembic upgrade head
```

#### Start the development server

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`.  
Interactive docs are at `http://localhost:8000/docs`.

---

### 3. Frontend (Next.js)

#### Install dependencies

```bash
cd frontend
npm install
```

#### Start the development server

```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`.

---

### 4. Running both together

Open two terminal tabs — one for the backend and one for the frontend — and start each server as described above. The frontend is pre-configured to proxy API requests to `http://localhost:8000`.

---

## Docker

The project ships with a `docker-compose.yml` that wires up three services:

| Service    | Description                              | Default port |
|------------|------------------------------------------|--------------|
| `db`       | PostgreSQL 16                            | 5432         |
| `backend`  | FastAPI (uvicorn)                        | 8000         |
| `frontend` | Next.js (standalone production build)   | 3000         |

### 1. Configure environment variables

```bash
cp .env.example .env
# Edit .env and fill in OPENAI_API_KEY and any other values you want to change
```

### 2. Build and start all services

```bash
docker compose up --build
```

The API will be available at `http://localhost:8000` and the frontend at `http://localhost:3000`.

### 3. Run database migrations

On first run (or after schema changes) apply Alembic migrations:

```bash
docker compose exec backend alembic upgrade head
```

### 4. Stop and clean up

```bash
docker compose down          # stop containers
docker compose down -v       # stop containers AND remove the postgres volume
```
