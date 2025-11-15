# GoTurboPass - California DMV-Approved Internet Traffic Violator School

**Phase 1: Core Foundation + Security** (MVP)

A secure, minimal traffic school platform built for California DMV compliance.

---

## Stack

- **Backend**: Flask 3, SQLAlchemy 2, Alembic, PostgreSQL
- **Frontend**: React, Vite, JavaScript, Tailwind CSS
- **Auth**: JWT (Flask-JWT-Extended) with email verification
- **Security**: HTTPS, CORS, CSP, rate-limiting, PII protection

---

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL 14+

### 1. Clone & Setup

```bash
git clone <repo-url>
cd GoTurboPass
```

### 2. Configure Environment

**Backend** (`backend/.env`):
```bash
cd ~/Development/code/GoTurboPass/backend
source venv/bin/activate
python app.py
```

**Frontend** (`frontend/.env`):
```bash
cd ~/Development/code/GoTurboPass/frontend
npm run dev
```

### 3. Install Dependencies

```bash
make install
```

This installs both backend (Python) and frontend (npm) dependencies.

### 4. Setup Database

Create PostgreSQL database:
```bash
psql -U postgres
CREATE DATABASE goturbopass;
\q
```

Run migrations:
```bash
make migrate
```

Seed demo data:
```bash
make seed
```

### 5. Run Development Servers

```bash
make dev
```

This starts:
- **Backend**: http://localhost:5000
- **Frontend**: http://localhost:5173

---

## Demo Credentials

After running `make seed`, use these credentials:

| Role     | Email                         | Password    |
|----------|-------------------------------|-------------|
| Admin    | admin@goturbopass.com         | admin123    |
| Reviewer | reviewer@goturbopass.com      | reviewer123 |

---

## API Endpoints (Phase 1)

### Auth
- `POST /api/auth/register` - Register new user
- `POST /api/auth/verify` - Verify email (stub)
- `POST /api/auth/login` - Login and get JWT
- `GET /api/me` - Get current user (protected)

---

## Project Structure

```
GoTurboPass/
├── backend/
│   ├── app.py              # Flask app
│   ├── config.py           # Configuration
│   ├── models/             # SQLAlchemy models
│   ├── routes/             # API routes
│   ├── services/           # Business logic
│   ├── middleware/         # Security middleware
│   ├── migrations/         # Alembic migrations
│   └── seed.py             # Seed script
├── frontend/
│   ├── src/
│   │   ├── pages/          # React pages
│   │   ├── context/        # Auth context
│   │   ├── utils/          # API client
│   │   └── App.jsx
│   └── package.json
├── Makefile
└── README.md
```

---

## Development Commands

```bash
make help              # Show all commands
make install           # Install dependencies
make migrate           # Run database migrations
make seed              # Seed demo data
make dev               # Run dev servers
make clean             # Clean build artifacts
```

---

## Security Features (Phase 1)

✅ **PII Protection**: Full CA DL numbers are bcrypt-hashed, only last 4 stored plainly
✅ **JWT Auth**: Short-lived access tokens (30 min expiry)
✅ **Email Verification**: Required before course access (stub in Phase 1)
✅ **CORS**: Locked to frontend origin (http://localhost:5173)
✅ **CSP**: Strict Content Security Policy headers
✅ **Rate Limiting**: 10 requests/min on auth endpoints
✅ **Audit Logging**: All auth events logged with PII redaction
✅ **Idle Timeout**: 20-minute inactivity logout (frontend)

See [SECURITY.md](./SECURITY.md) for details.

---

## What's Next? (Phase 2)

- Course timer + linear progress locks
- Quiz engine + scoring
- Final exam (A/B randomization)
- Certificate PDF generation
- Instructor portal + SLA tracking
- Admin CRUD for modules/quizzes
- Screen-prints export

---

## Troubleshooting

### Database connection failed
- Ensure PostgreSQL is running: `brew services start postgresql` (macOS)
- Check `DATABASE_URL` in `backend/.env`

### Frontend can't reach backend
- Check CORS origin in `backend/config.py`
- Ensure backend is running on port 5000

### Alembic migration errors
```bash
cd backend
. venv/bin/activate
alembic stamp head  # Reset migration state
```

---

## License

Proprietary - All Rights Reserved

## Contact

**Operator**: Kamyar Taghavi
**Email**: support@goturbopass.com (placeholder)
