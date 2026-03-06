# Fitness Data Chat

An AI-powered fitness data analysis web application with a chat interface. Connect your Strava and Garmin accounts to get insights, trends, and visualizations from your training data using natural language.

## Features

- 💬 **LLM Chat Interface** – Ask natural language questions about your training data powered by GPT-4
- 🏃 **Strava Integration** – OAuth 2.0 connection to sync all your Strava activities
- ⌚ **Garmin Integration** – Connect Garmin Connect to import your Garmin device data
- 📊 **Interactive Dashboard** – Charts for distance trends, heart rate zones, and activity comparisons
- 🔍 **Smart Analytics** – Pandas-powered data analysis with detailed statistics
- 📡 **Streaming Responses** – Real-time SSE streaming for chat responses

## Prerequisites

- **Node.js** 18+
- **Python** 3.11+
- **PostgreSQL** 16+
- **Docker** & Docker Compose (for containerized setup)
- **Redis** 7+ (for caching)
- OpenAI API key
- Strava API credentials (optional)
- Garmin Connect account (optional)

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-org/fitness-data-chat.git
cd fitness-data-chat
```

### 2. Backend Setup

```bash
cd backend

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file and configure
cp .env.example .env
# Edit .env with your credentials
```

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Copy environment file and configure
cp .env.example .env.local
# Edit .env.local with your API URL
```

### 4. Configure Environment Variables

**Backend** (`backend/.env`):
```env
DATABASE_URL=postgresql://user:password@localhost:5432/fitness_data
OPENAI_API_KEY=sk-...
STRAVA_CLIENT_ID=your_strava_client_id
STRAVA_CLIENT_SECRET=your_strava_client_secret
STRAVA_REDIRECT_URI=http://localhost:8000/api/strava/callback
GARMIN_EMAIL=your_garmin_email
GARMIN_PASSWORD=your_garmin_password
CORS_ORIGINS=http://localhost:3000
REDIS_URL=redis://localhost:6379
SECRET_KEY=your-secret-key-here
```

**Frontend** (`frontend/.env.local`):
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 5. Database Migrations

Ensure PostgreSQL is running, then:

```bash
cd backend
source .venv/bin/activate
python -c "from app.database.db import create_tables; create_tables()"
```

### 6. Start Development Servers

**Backend:**
```bash
cd backend
source .venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

**Frontend:**
```bash
cd frontend
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

## Docker Setup

The easiest way to run the full stack is with Docker Compose:

```bash
# Copy env files
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env.local

# Edit both .env files with your credentials, then:
docker compose up --build
```

Services will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- PostgreSQL: localhost:5432
- Redis: localhost:6379

To stop:
```bash
docker compose down
```

To remove volumes (reset database):
```bash
docker compose down -v
```

## API Documentation

Once the backend is running, interactive API docs are available at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Key Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/chat` | Send a chat message |
| POST | `/api/chat/stream` | Stream a chat response (SSE) |
| GET | `/api/chat/history` | Get chat history |
| GET | `/api/strava/auth` | Get Strava OAuth URL |
| GET | `/api/strava/callback` | Strava OAuth callback |
| POST | `/api/strava/sync` | Sync Strava activities |
| POST | `/api/garmin/auth` | Authenticate with Garmin |
| POST | `/api/garmin/sync` | Sync Garmin activities |
| GET | `/api/analytics/summary` | Get activity summary stats |
| POST | `/api/analytics/query` | Run custom analytics query |
| GET | `/health` | Health check |

## Architecture

```
fitness-data-chat/
├── backend/                  # FastAPI Python backend
│   ├── app/
│   │   ├── api/              # Route handlers (chat, strava, garmin, analytics)
│   │   ├── database/         # SQLAlchemy engine & session
│   │   ├── models/           # ORM models (User, Activity)
│   │   └── services/         # Business logic (LLM, Strava, Garmin, Analytics)
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/                 # Next.js 14 React frontend
│   ├── app/                  # Next.js App Router pages
│   ├── components/           # React components
│   │   ├── chat/             # Chat UI components
│   │   ├── dashboard/        # Charts & stats components
│   │   └── layout/           # Header, Sidebar
│   ├── lib/                  # API client & utilities
│   └── Dockerfile
└── docker-compose.yml
```

**Tech Stack:**
- **Frontend**: Next.js 14, React 18, TypeScript, Tailwind CSS, Recharts
- **Backend**: FastAPI, SQLAlchemy, LangChain, OpenAI GPT-4
- **Database**: PostgreSQL 16
- **Cache**: Redis 7
- **Integrations**: Strava API, Garmin Connect

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -m 'Add my feature'`
4. Push to the branch: `git push origin feature/my-feature`
5. Open a Pull Request

Please ensure your code:
- Passes linting (`ruff check .` for Python, `npm run lint` for TypeScript)
- Follows the existing code style
- Includes appropriate error handling
- Does not commit secrets or credentials

## License

See [LICENSE](./LICENSE) for details.
