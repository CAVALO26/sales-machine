import os
from dotenv import load_dotenv

load_dotenv()

# ── Banco de dados ─────────────────────────────────────────────────────────────
# Supabase entrega "postgresql://..." — já no formato certo para SQLAlchemy
# Fallback: SQLite local para desenvolvimento
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./salesmachine.db")

# Render/Heroku às vezes entregam "postgres://" — corrigimos aqui
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# ── Redis ──────────────────────────────────────────────────────────────────────
# Upstash entrega "rediss://..." (com SSL) — Celery aceita normalmente
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# ── APIs externas ──────────────────────────────────────────────────────────────
CLAUDE_API_KEY    = os.getenv("CLAUDE_API_KEY")
WP_URL            = os.getenv("WP_URL", "http://localhost:8080")
WP_USER           = os.getenv("WP_USER", "admin")
WP_PASS           = os.getenv("WP_PASS", "password")
META_ACCESS_TOKEN = os.getenv("META_ACCESS_TOKEN")
META_AD_ACCOUNT   = os.getenv("META_AD_ACCOUNT")
HF_TOKEN          = os.getenv("HF_TOKEN")

# ── URL pública do backend (usada pelo Streamlit) ─────────────────────────────
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
