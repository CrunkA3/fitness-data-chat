# Fitness Data Chat

An AI-powered fitness data analysis web application with a chat interface. Connect your Strava and Garmin accounts to get insights, trends, and visualizations from your training data using natural language.

## Screenshots

### Landing Page
![Fitness Data Chat – Landing Page](https://github.com/user-attachments/assets/cf75e3bc-2016-4c45-ba1b-6b901cdb3cda)

### AI Chat Interface
![Fitness Data Chat – Chat Interface](https://github.com/user-attachments/assets/83c226c0-1090-4156-8a5f-b47ecf1f8b7a)

### Analytics Dashboard
![Fitness Data Chat – Dashboard](https://github.com/user-attachments/assets/66a3948f-abdb-4bff-a7b1-6aae4e5eaee9)

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
git clone https://github.com/CrunkA3/fitness-data-chat.git
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

Create your environment files from the provided examples:

```bash
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env.local
```

Then edit each file with your own credentials as described below.

---

#### Backend (`backend/.env`)

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

| Variable | Required | Description |
|----------|----------|-------------|
| `DATABASE_URL` | ✅ Yes | PostgreSQL connection string in the format `postgresql://<user>:<password>@<host>:<port>/<dbname>`. The default example uses `localhost:5432` and a database named `fitness_data`. When using Docker Compose this is automatically set to the internal `postgres` service. |
| `OPENAI_API_KEY` | ✅ Yes | Your OpenAI API key used to power the GPT-4 Turbo chat interface. Obtain one from the [OpenAI API platform](https://platform.openai.com/api-keys). The key starts with `sk-`. Without this key the chat and analytics features will not work. |
| `STRAVA_CLIENT_ID` | ⚙️ Optional | The numeric Client ID for your Strava API application. Required only if you want to connect Strava accounts. Create an app at [Strava API Settings](https://www.strava.com/settings/api) to get this value. |
| `STRAVA_CLIENT_SECRET` | ⚙️ Optional | The Client Secret for your Strava API application. Found alongside the Client ID on the [Strava API Settings](https://www.strava.com/settings/api) page. Keep this value private and never commit it to source control. |
| `STRAVA_REDIRECT_URI` | ⚙️ Optional | The OAuth 2.0 callback URL that Strava redirects to after a user authorizes the app. Must exactly match the **Authorization Callback Domain** registered in your Strava app settings. Default: `http://localhost:8000/api/strava/callback`. Change the host/port for production deployments. |
| `GARMIN_EMAIL` | ⚙️ Optional | The email address of the Garmin Connect account whose data you want to import. Required only if you want to sync Garmin device data. |
| `GARMIN_PASSWORD` | ⚙️ Optional | The password for the Garmin Connect account above. **Never commit real passwords to source control.** In production, consider using a secrets manager instead of a plain `.env` file. |
| `CORS_ORIGINS` | ✅ Yes | Comma-separated list of frontend origins that are allowed to call the backend API (e.g. `http://localhost:3000` for local development or `https://your-app.example.com` for production). Multiple origins can be specified: `http://localhost:3000,https://app.example.com`. |
| `REDIS_URL` | ✅ Yes | Connection URL for the Redis instance used for caching. Format: `redis://<host>:<port>`. Default: `redis://localhost:6379`. When using Docker Compose this is automatically set to `redis://redis:6379`. |
| `SECRET_KEY` | ✅ Yes | A long, random secret string used for signing tokens and securing sessions. **Change this to a strong, unique value in production** (see the generation command below). |

To generate a secure value for `SECRET_KEY`, run:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

##### How to obtain Strava credentials

1. Go to [https://www.strava.com/settings/api](https://www.strava.com/settings/api) and log in.
2. Click **Create & Manage Your App**.
3. Fill in the application name, website, and set the **Authorization Callback Domain** to `localhost` (for development) or your production domain.
4. After saving, copy the **Client ID** and **Client Secret** into `STRAVA_CLIENT_ID` and `STRAVA_CLIENT_SECRET`.

##### How to obtain an OpenAI API key

1. Sign in or create an account at [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys).
2. Click **Create new secret key**.
3. Copy the key (it starts with `sk-`) and paste it into `OPENAI_API_KEY`. Store it securely — it will not be shown again.

---

#### Frontend (`frontend/.env.local`)

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

| Variable | Required | Description |
|----------|----------|-------------|
| `NEXT_PUBLIC_API_URL` | ✅ Yes | The full base URL of the backend API. Because it is prefixed with `NEXT_PUBLIC_`, Next.js exposes it to the browser at build time. Set this to `http://localhost:8000` for local development. For production, replace it with your deployed backend URL (e.g. `https://api.your-app.example.com`). All frontend API calls — including chat, Strava/Garmin auth, and analytics — are routed through this URL. |

> **Note:** `NEXT_PUBLIC_` variables are embedded into the browser bundle at build time. Do **not** place sensitive secrets in frontend environment variables.

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
├── frontend/                 # Next.js 15 React frontend
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
- **Frontend**: Next.js 15, React 18, TypeScript, Tailwind CSS, Recharts
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
