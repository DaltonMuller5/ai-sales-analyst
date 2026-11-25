# 🤖 AI Sales Analyst

> Sistema interativo de análise de vendas com inteligência artificial — construído com Python, FastAPI e Data Science.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688?style=flat-square&logo=fastapi)
![Vercel](https://img.shields.io/badge/Deploy-Vercel-black?style=flat-square&logo=vercel)

---

## 📸 Funcionalidades

| Módulo | Descrição |
|---|---|
| **Dashboard** | KPIs em tempo real, gráfico de receita, funil de vendas |
| **Produtos** | Ranking e distribuição de receita por produto |
| **Equipe** | Performance individual dos vendedores |
| **Regiões** | Análise geográfica de mercado |
| **IA Analista** | Chatbot inteligente para análise de dados em linguagem natural |

---

## 🚀 Rodando Localmente

### Pré-requisitos

- Python 3.10 ou superior
- Git

### Instalação

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/ai-sales-analyst.git
cd ai-sales-analyst

# 2. Execute o script de inicialização
# Linux / macOS:
chmod +x start.sh && ./start.sh

# Windows:
start.bat
```

O servidor estará disponível em:
- **API Backend:** `http://localhost:8000`
- **Documentação da API:** `http://localhost:8000/docs`
- **Frontend:** abra `frontend/index.html` no navegador, ou:

```bash
# Servir o frontend localmente
python3 -m http.server 3000 -d frontend
# Acesse: http://localhost:3000
```

### Instalação Manual (sem script)

```bash
# Criar e ativar ambiente virtual
python3 -m venv .venv
source .venv/bin/activate     # Linux/macOS
.venv\Scripts\activate.bat    # Windows

# Instalar dependências
pip install -r requirements.txt

# Iniciar o servidor
uvicorn api.index:app --host 0.0.0.0 --port 8000 --reload
```

---

## ☁️ Deploy no Vercel

### Pré-requisitos

- Conta no [Vercel](https://vercel.com)
- [Vercel CLI](https://vercel.com/cli) instalado: `npm i -g vercel`

### Passo a passo

```bash
# 1. Faça login no Vercel
vercel login

# 2. Deploy de preview (desenvolvimento)
vercel

# 3. Deploy de produção
vercel --prod
```

O `vercel.json` já está configurado para rotear automaticamente:
- `/api/*` → FastAPI (Python Serverless Function)
- `/*` → Arquivos estáticos do frontend

> **Nota:** O Vercel usa `@vercel/python` para executar a API como uma serverless function. O arquivo `api/index.py` é o entry point.

---

## 📡 Endpoints da API

| Método | Rota | Descrição |
|---|---|---|
| `GET` | `/api/kpis` | KPIs consolidados do período |
| `GET` | `/api/timeseries` | Série temporal de receita |
| `GET` | `/api/by-product` | Receita agrupada por produto |
| `GET` | `/api/by-region` | Receita agrupada por região |
| `GET` | `/api/by-seller` | Performance por vendedor |
| `GET` | `/api/funnel` | Dados do funil de vendas |
| `GET` | `/api/top-products` | Top N produtos |
| `POST` | `/api/chat` | Chat com IA analista |
| `GET` | `/api/health` | Status da API |

### Parâmetros de Período

Todos os endpoints aceitam `?period=` com os valores:
- `30d` — últimos 30 dias
- `90d` — últimos 90 dias *(padrão)*
- `180d` — últimos 180 dias

### Exemplo de Requisição — Chat IA

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Como está nossa taxa de conversão?"}'
```

**Resposta:**
```json
{
  "reply": "📊 **Taxa de Conversão**\n\nA taxa média está em 24.3%, acima da média do setor (~22%)...",
  "timestamp": "2026-04-16T10:30:00"
}
```

---

## 🗂️ Estrutura do Projeto

```
ai-sales-analyst/
├── api/
│   └── index.py          # FastAPI — toda a lógica backend + IA
├── frontend/
│   └── index.html        # Single-file SPA (HTML + CSS + JS + Chart.js)
├── requirements.txt      # Dependências Python
├── vercel.json           # Configuração de deploy Vercel
├── start.sh              # Script de inicialização (Linux/macOS)
├── start.bat             # Script de inicialização (Windows)
├── .gitignore
└── README.md
```

---

## 🧠 Stack Tecnológica

### Backend (Python)
| Biblioteca | Uso |
|---|---|
| **FastAPI** | Framework web de alta performance |
| **Uvicorn** | Servidor ASGI para desenvolvimento |
| **Pydantic** | Validação de dados e schemas |
| **NumPy** | Computação numérica e geração de dados |
| **Pandas** | Manipulação e análise de dados |
| **Scikit-learn** | Base para modelos de ML (extensível) |
| **SciPy** | Computação científica e estatística |

### Frontend
| Tecnologia | Uso |
|---|---|
| **Vanilla JS** | Interatividade sem dependências de build |
| **Chart.js** | Gráficos interativos |
| **Google Fonts** | Tipografia (Syne + IBM Plex Mono) |
| **CSS Variables** | Design system consistente |

---

## 🤖 Perguntas Suportadas pela IA

O chatbot analisa linguagem natural em português e responde perguntas como:

- *"Como está nossa receita?"*
- *"Qual a taxa de conversão atual?"*
- *"Mostre a performance da equipe"*
- *"Faça uma previsão para o próximo mês"*
- *"Temos risco de churn?"*
- *"Como estão as regiões?"*

---

## 🔧 Extensões Sugeridas

Para evoluir o projeto, considere:

1. **Banco de dados real** — Substitua os dados gerados por PostgreSQL/SQLite com SQLAlchemy
2. **Autenticação** — Adicione JWT com `python-jose` e `passlib`
3. **Upload de CSV** — Permita que o usuário importe seus próprios dados de vendas
4. **IA Generativa** — Integre a API da Anthropic (Claude) para análises mais sofisticadas
5. **Alertas** — Notificações por email quando KPIs saírem de limites configurados
6. **Cache** — Use Redis para cachear respostas da API

---

## 📄 Licença

MIT — livre para uso comercial e pessoal.

---

*Desenvolvido com ❤️ usando Python + FastAPI + Chart.js*
