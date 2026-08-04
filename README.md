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
