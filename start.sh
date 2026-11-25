#!/bin/bash
# ─────────────────────────────────────────────
#  AI Sales Analyst — Servidor Local
# ─────────────────────────────────────────────

set -e

echo ""
echo "  ╔════════════════════════════════════╗"
echo "  ║   🤖  AI Sales Analyst  v1.0.0    ║"
echo "  ╚════════════════════════════════════╝"
echo ""

# Check Python
if ! command -v python3 &>/dev/null; then
    echo "  ❌ Python3 não encontrado. Instale em https://python.org"
    exit 1
fi

# Virtual env
if [ ! -d ".venv" ]; then
    echo "  📦 Criando ambiente virtual..."
    python3 -m venv .venv
fi

source .venv/bin/activate

# Install deps
echo "  📥 Instalando dependências..."
pip install -r requirements.txt -q

echo ""
echo "  ✅ Backend: http://localhost:8000"
echo "  ✅ Docs API: http://localhost:8000/docs"
echo "  📂 Frontend: abra frontend/index.html no navegador"
echo "     OU use: python3 -m http.server 3000 -d frontend"
echo ""
echo "  Iniciando servidor FastAPI..."
echo ""

# Start backend
uvicorn api.index:app --host 0.0.0.0 --port 8000 --reload
