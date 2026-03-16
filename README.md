# 🤖 AI Sales Machine — Deploy 100% Gratuito

Sem cartão. Sem instalar nada. Três serviços gratuitos combinados:

| Serviço | Função | Plano gratuito |
|---------|--------|----------------|
| Render | Roda o backend, worker e frontend | 750h/mês |
| Supabase | Banco PostgreSQL | 500 MB grátis |
| Upstash | Redis (fila Celery) | 10.000 req/dia grátis |

---

## Passo a passo

### 1. Supabase (banco)
1. supabase.com → New project (anote a senha)
2. Settings → Database → Connection string → URI → copie

### 2. Upstash (Redis)
1. upstash.com → Create Database → Redis → Free tier
2. Details → copie REDIS_URL

### 3. GitHub
git init && git add . && git commit -m "first"
Crie repo no github.com e faça push

### 4. Render — 3 serviços

Backend: New Web Service → Docker → uvicorn backend.api.main:app --host 0.0.0.0 --port $PORT
Worker:  New Background Worker → Docker → celery -A backend.tasks.celery_app.celery worker --loglevel=info
Frontend: New Web Service → Docker → streamlit run frontend/app.py --server.port $PORT --server.address 0.0.0.0 --server.headless true

Variáveis em todos: DATABASE_URL, REDIS_URL, CLAUDE_API_KEY
Variável só no frontend: BACKEND_URL = URL pública do backend

### 5. Pronto
Abra a URL do frontend e use.
