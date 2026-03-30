# 🤖 LLM-Powered Support Analytics Dashboard

An AI-powered support ticket system that automatically **classifies** and **summarizes** tickets using Hugging Face Transformers (PyTorch). Built with FastAPI, React, PostgreSQL, and Docker.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green)
![React](https://img.shields.io/badge/React-18-61dafb)
![PyTorch](https://img.shields.io/badge/PyTorch-2.4-red)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED)

## Features

- **AI Ticket Classification** — Automatically categorizes tickets as `bug`, `feature`, `question`, or `documentation` using DistilBERT + keyword heuristics
- **AI Summarization** — Generates one-sentence summaries using DistilBART
- **REST API** — FastAPI backend with Swagger docs at `/docs`
- **Analytics Dashboard** — React frontend with Chart.js bar chart showing ticket distribution
- **Containerized** — Full Docker Compose setup (backend + PostgreSQL + frontend)

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python, FastAPI, SQLAlchemy, Pydantic |
| ML/AI | Hugging Face Transformers, PyTorch, DistilBERT, DistilBART |
| Database | PostgreSQL |
| Frontend | React 18, Vite, Chart.js |
| DevOps | Docker, Docker Compose |

## Architecture

```
┌─────────────┐     HTTP      ┌──────────────────┐     SQL      ┌────────────┐
│  React UI   │ ──────────▶   │  FastAPI Backend  │ ──────────▶  │ PostgreSQL │
│ (port 3000) │   ◀──────────  │   (port 8000)    │  ◀──────────  │ (port 5432)│
└─────────────┘               │                  │              └────────────┘
                              │  ┌────────────┐  │
                              │  │ HF Models  │  │
                              │  │DistilBERT  │  │
                              │  │DistilBART  │  │
                              │  └────────────┘  │
                              └──────────────────┘
```

---

## 🚀 Getting Started (Step-by-Step for Beginners)

### Prerequisites

You need these installed on your computer:

1. **Python 3.10+** — [Download here](https://www.python.org/downloads/)
2. **Node.js 18+** — [Download here](https://nodejs.org/) (includes npm)
3. **Docker Desktop** — [Download here](https://www.docker.com/products/docker-desktop/)
4. **Git** — [Download here](https://git-scm.com/downloads)
5. **VS Code** (recommended) — [Download here](https://code.visualstudio.com/)

### Option A: Run Everything with Docker (Easiest)

This is the simplest way — one command starts everything:

```bash
# 1. Clone this repo
git clone https://github.com/YOUR_USERNAME/llm-support-dashboard.git
cd llm-support-dashboard

# 2. Start all services (this will take a few minutes the first time)
docker-compose up --build

# 3. Open in your browser:
#    - Frontend:  http://localhost:3000
#    - Backend:   http://localhost:8000
#    - API Docs:  http://localhost:8000/docs
```

### Option B: Run Each Piece Separately (Better for Learning)

#### Phase 1 — Start the Database

```bash
# Start ONLY PostgreSQL in Docker
docker-compose up db -d

# The -d flag means "run in the background"
# Verify it's running:
docker ps
```

#### Phase 2 — Start the Backend

```bash
# Open a terminal and go to the backend folder
cd backend

# Create a virtual environment (isolates your Python packages)
python -m venv venv

# Activate it:
# On Mac/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the backend server
# NOTE: First run downloads ~1.5 GB of AI models. Be patient!
uvicorn main:app --reload --port 8000

# You should see:
# ⏳ Loading AI models (this may take a minute on first run)...
# ✅ AI models loaded successfully!
# INFO: Uvicorn running on http://0.0.0.0:8000
```

**Test the backend** — Open http://localhost:8000/docs to see the interactive API documentation.

#### Phase 3 — Seed Sample Data

```bash
# In a NEW terminal (keep the backend running!)
cd backend

# Activate venv again (each terminal needs this)
source venv/bin/activate   # or venv\Scripts\activate on Windows

# Install requests (needed for the seed script)
pip install requests

# Run the seed script
python seed_tickets.py
```

You should see each ticket being created with its AI-assigned category and summary!

#### Phase 4 — Start the Frontend

```bash
# In a NEW terminal
cd frontend

# Install JavaScript dependencies
npm install

# Start the development server
npm run dev

# Open http://localhost:3000 in your browser
```

---

## 📁 Project Structure

```
llm-support-dashboard/
├── backend/
│   ├── main.py           # FastAPI app — API endpoints
│   ├── database.py       # PostgreSQL connection setup
│   ├── models.py         # SQLAlchemy database model (Ticket table)
│   ├── schemas.py        # Pydantic schemas (input/output validation)
│   ├── ml.py             # Hugging Face AI classification & summarization
│   ├── seed_tickets.py   # Script to populate sample data
│   ├── requirements.txt  # Python dependencies
│   └── Dockerfile        # Container config for backend
├── frontend/
│   ├── src/
│   │   ├── main.jsx      # React entry point
│   │   └── App.jsx       # Main dashboard component
│   ├── index.html        # HTML template
│   ├── vite.config.js    # Vite build tool config
│   ├── package.json      # JavaScript dependencies
│   └── Dockerfile        # Container config for frontend
├── docker-compose.yml    # Orchestrates all services
├── .gitignore
└── README.md
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Health check |
| `POST` | `/tickets` | Create a ticket (AI auto-classifies & summarizes) |
| `GET` | `/tickets` | List all tickets |
| `GET` | `/metrics/tickets` | Get ticket count by category |

### Example: Create a Ticket

```bash
curl -X POST http://localhost:8000/tickets \
  -H "Content-Type: application/json" \
  -d '{"title": "Login broken", "description": "The login page shows a 500 error when I click submit. This bug is blocking all users."}'
```

Response:
```json
{
  "id": 1,
  "title": "Login broken",
  "description": "The login page shows a 500 error...",
  "category": "bug",
  "summary": "The login page shows a 500 error when users click submit.",
  "created_at": "2025-01-15T10:30:00Z"
}
```

---

## 🧠 How the AI Works

### Classification (`ml.py → classify_ticket`)

1. **Keyword matching** (first pass) — Scans the ticket text for words like "bug", "crash", "feature", "how", "docs", etc.
2. **Sentiment fallback** — If no keywords match, uses DistilBERT (a smaller, faster version of BERT) to determine sentiment. Negative sentiment → `bug`, Positive → `feature`.

### Summarization (`ml.py → summarize_ticket`)

Uses **DistilBART** (a distilled version of the BART model from Facebook) to generate a concise one-sentence summary of the ticket description.

> **Interview talking point:** "I used a hybrid approach — keyword heuristics for reliable classification combined with transformer-based sentiment analysis as a fallback. In production, I'd fine-tune a multi-class classifier on labeled ticket data."

---

## ☁️ Cloud Deployment (AWS EC2 / GCP / IBM Cloud)

### Step-by-step for AWS EC2:

```bash
# 1. Create an EC2 instance (Ubuntu 22.04, t2.medium or larger)
# 2. SSH into your instance
ssh -i your-key.pem ubuntu@YOUR_EC2_IP

# 3. Install Docker
sudo apt update
sudo apt install -y docker.io docker-compose
sudo usermod -aG docker $USER
# Log out and log back in for group change to take effect

# 4. Clone your repo
git clone https://github.com/YOUR_USERNAME/llm-support-dashboard.git
cd llm-support-dashboard

# 5. Update the frontend API URL to point to your server
# Edit frontend/Dockerfile and change VITE_API_URL:
#   ENV VITE_API_URL=http://YOUR_EC2_IP:8000

# 6. Build and run
docker-compose up --build -d

# 7. Open port 3000 and 8000 in your EC2 Security Group
# Then visit: http://YOUR_EC2_IP:3000
```

---

## 🔍 Troubleshooting

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError` | Make sure your virtual environment is activated |
| Models downloading slowly | First run downloads ~1.5 GB. Use `USE_REAL_MODELS=false` to skip |
| `connection refused` to database | Make sure PostgreSQL container is running: `docker-compose up db -d` |
| CORS errors in browser | The backend already includes CORS middleware; make sure you're hitting the right port |
| `docker-compose` not found | Try `docker compose` (without hyphen) on newer Docker versions |

### Run Without AI Models (for faster testing)

```bash
USE_REAL_MODELS=false uvicorn main:app --reload --port 8000
```

This starts the backend without downloading models. Tickets will get a default category of "question" and a truncated description as the summary.

---

## 📝 Resume Bullet Points

Use these on your resume under a "Projects" section:

> **LLM-Powered Support Analytics Dashboard** | Python, FastAPI, React, PyTorch, Docker
> - Designed and built a full-stack support ticket system with **AI-powered classification and summarization** using Hugging Face Transformers (DistilBERT, DistilBART), achieving automated categorization into bug, feature, question, and documentation classes
> - Developed a **RESTful API** with FastAPI and PostgreSQL (SQLAlchemy ORM), serving ticket CRUD operations and real-time analytics metrics consumed by a React dashboard with Chart.js visualizations
> - Containerized the entire application stack with **Docker Compose** (backend, database, frontend) and deployed to a cloud VM, demonstrating end-to-end MLOps and software engineering practices

---

## 📚 Resources for Further Learning

- [FastAPI Official Tutorial](https://fastapi.tiangolo.com/tutorial/) — Great step-by-step guide
- [Hugging Face Transformers Docs](https://huggingface.co/docs/transformers/) — Pipeline documentation
- [React Official Tutorial](https://react.dev/learn) — Interactive React guide
- [Docker Getting Started](https://docs.docker.com/get-started/) — Docker fundamentals
- [SQLAlchemy Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/) — Database ORM guide

---

## License

MIT — free to use for personal and commercial projects.
