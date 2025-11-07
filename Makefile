.PHONY: help dev migrate seed install-backend install-frontend install clean

help:
	@echo "GoTurboPass - Phase 1 Development Commands"
	@echo ""
	@echo "Setup:"
	@echo "  make install          Install all dependencies (backend + frontend)"
	@echo "  make install-backend  Install backend dependencies"
	@echo "  make install-frontend Install frontend dependencies"
	@echo ""
	@echo "Database:"
	@echo "  make migrate          Run Alembic migrations"
	@echo "  make seed             Seed database with demo data"
	@echo ""
	@echo "Development:"
	@echo "  make dev              Run backend + frontend concurrently"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean            Remove build artifacts"

install: install-backend install-frontend
	@echo "✅ All dependencies installed"

install-backend:
	@echo "📦 Installing backend dependencies..."
	cd backend && python3 -m venv venv && \
		. venv/bin/activate && \
		pip install --upgrade pip && \
		pip install -r requirements.txt
	@echo "✅ Backend dependencies installed"

install-frontend:
	@echo "📦 Installing frontend dependencies..."
	cd frontend && npm install
	@echo "✅ Frontend dependencies installed"

migrate:
	@echo "🔄 Running database migrations..."
	cd backend && \
		. venv/bin/activate && \
		alembic revision --autogenerate -m "Initial schema" && \
		alembic upgrade head
	@echo "✅ Migrations complete"

seed:
	@echo "🌱 Seeding database..."
	cd backend && \
		. venv/bin/activate && \
		python seed.py
	@echo "✅ Seed complete"

dev:
	@echo "🚀 Starting development servers..."
	@echo "Backend:  http://localhost:5000"
	@echo "Frontend: http://localhost:5173"
	@echo ""
	@trap 'kill 0' EXIT; \
		(cd backend && . venv/bin/activate && python app.py) & \
		(cd frontend && npm run dev)

clean:
	@echo "🧹 Cleaning build artifacts..."
	rm -rf backend/__pycache__ backend/**/__pycache__ backend/**/**/__pycache__
	rm -rf backend/venv
	rm -rf frontend/node_modules frontend/dist
	@echo "✅ Clean complete"
