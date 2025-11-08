# backend/models/db.py
from flask_sqlalchemy import SQLAlchemy

# The single SQLAlchemy instance used across the app & Alembic
db = SQLAlchemy()
