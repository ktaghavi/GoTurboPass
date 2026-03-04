.PHONY: help dev db-init db-migrate db-upgrade migrate seed install-backend install-frontend install clean

help:
	@echo "GoTurboPass — Development Commands"
	@echo ""
	@echo "Setup (run once, in order):"
	@echo "  make install          Install all dependencies (backend + frontend)"
	@echo "  make db-init          Create migrations/ directory (one-time only)"
	@echo "  make db-migrate       Generate migration from current models"
	@echo "  make db-upgrade       Apply pending migrations to the database"
	@echo "  make seed             Seed CA counties + courts"
	@echo ""
	@echo "Day-to-day:"
	@echo "  make dev              Start backend + frontend concurrently"
	@echo "  make migrate          Shortcut: db-migrate + db-upgrade"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean            Remove build artifacts and venv"

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

db-init:
	@echo "🗄️  Initialising Flask-Migrate (one-time)..."
	cd backend && . venv/bin/activate && flask db init
	@echo "✅ migrations/ directory created"

db-migrate:
	@echo "🔄 Generating migration..."
	cd backend && . venv/bin/activate && flask db migrate -m "$(MSG)"
	@echo "✅ Migration generated — review backend/migrations/versions/ before upgrading"

db-upgrade:
	@echo "⬆️  Applying migrations..."
	cd backend && . venv/bin/activate && flask db upgrade
	@echo "✅ Database up to date"

migrate: db-migrate db-upgrade

seed:
	@echo "🌱 Seeding CA counties + courts..."
	cd backend && . venv/bin/activate && python seed_geo_full.py
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
	find backend -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	rm -rf backend/venv
	rm -rf frontend/node_modules frontend/dist
	@echo "✅ Clean complete"
