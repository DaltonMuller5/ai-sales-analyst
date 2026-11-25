import fastapi
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import json
import random
import math
from datetime import datetime, timedelta
import os

app = fastapi.FastAPI(
    title="AI Sales Analyst API",
    description="AI Sales System with Artificial Intelligence",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Models ───────────────────────────────────────────────────────────────────

class ChatMessage(BaseModel):
    message: str
    context: Optional[dict] = None

class SalesFilter(BaseModel):
    period: Optional[str] = "30d"
    category: Optional[str] = "all"
    region: Optional[str] = "all"

# ─── Data Generation ──────────────────────────────────────────────────────────

PRODUCTS = ["CRM Pro", "Analytics Suite", "Dashboard Plus", "AutoReport", "SalesBot AI", "LeadTracker", "PipelineX"]
REGIONS = ["Sudeste", "Sul", "Norte", "Nordeste", "Centro-Oeste"]
CATEGORIES = ["SaaS", "Enterprise", "SMB", "Startup"]
SELLERS = ["Ana Lima", "Carlos Mota", "Juliana Reis", "Pedro Alves", "Fernanda Cruz", "Rafael Sousa"]

def generate_sales_data(days: int = 90):
    data = []
    base_date = datetime.now() - timedelta(days=days)
    for i in range(days):
        date = base_date + timedelta(days=i)
        trend = 1 + (i / days) * 0.3
        seasonal = 1 + 0.2 * math.sin(2 * math.pi * i / 30)
        noise = random.uniform(0.85, 1.15)
        revenue = round(50000 * trend * seasonal * noise, 2)
        deals = random.randint(8, 35)
        data.append({
            "date": date.strftime("%Y-%m-%d"),
            "revenue": revenue,
            "deals": deals,
            "avg_ticket": round(revenue / deals, 2),
            "product": random.choice(PRODUCTS),
            "region": random.choice(REGIONS),
            "category": random.choice(CATEGORIES),
            "seller": random.choice(SELLERS),
            "conversion_rate": round(random.uniform(0.12, 0.38), 3),
            "churn_risk": round(random.uniform(0.05, 0.25), 3),
        })
    return data

def compute_kpis(data: list):
    total_revenue = sum(d["revenue"] for d in data)
    total_deals = sum(d["deals"] for d in data)
    avg_ticket = total_revenue / total_deals if total_deals else 0
    avg_conversion = sum(d["conversion_rate"] for d in data) / len(data) if data else 0
    prev_half = data[:len(data)//2]
    curr_half = data[len(data)//2:]
    prev_rev = sum(d["revenue"] for d in prev_half)
    curr_rev = sum(d["revenue"] for d in curr_half)
    growth = ((curr_rev - prev_rev) / prev_rev * 100) if prev_rev else 0
    return {
        "total_revenue": round(total_revenue, 2),
        "total_deals": total_deals,
        "avg_ticket": round(avg_ticket, 2),
        "avg_conversion_rate": round(avg_conversion * 100, 2),
        "revenue_growth": round(growth, 2),
        "best_product": max(set(d["product"] for d in data), key=lambda p: sum(d["revenue"] for d in data if d["product"] == p)),
        "best_region": max(set(d["region"] for d in data), key=lambda r: sum(d["revenue"] for d in data if d["region"] == r)),
        "best_seller": max(set(d["seller"] for d in data), key=lambda s: sum(d["deals"] for d in data if d["seller"] == s)),
    }

def compute_by_dimension(data: list, dim: str):
    groups = {}
    for d in data:
        key = d[dim]
        if key not in groups:
            groups[key] = {"revenue": 0, "deals": 0}
        groups[key]["revenue"] += d["revenue"]
        groups[key]["deals"] += d["deals"]
    return [{"name": k, "revenue": round(v["revenue"], 2), "deals": v["deals"]} for k, v in groups.items()]

def compute_funnel():
    leads = random.randint(2000, 3500)
    qualified = int(leads * random.uniform(0.45, 0.6))
    proposal = int(qualified * random.uniform(0.4, 0.6))
    negotiation = int(proposal * random.uniform(0.45, 0.65))
    closed = int(negotiation * random.uniform(0.5, 0.75))
    return [
        {"stage": "Leads", "count": leads, "color": "#6366f1"},
        {"stage": "Qualificados", "count": qualified, "color": "#8b5cf6"},
        {"stage": "Proposta", "count": proposal, "color": "#a855f7"},
        {"stage": "Negociação", "count": negotiation, "color": "#d946ef"},
        {"stage": "Fechados", "count": closed, "color": "#ec4899"},
    ]

# ─── AI Chat Logic ─────────────────────────────────────────────────────────────

def analyze_with_ai(message: str, context: dict) -> str:
    """Rule-based AI analyst that responds intelligently to sales questions."""
    msg = message.lower()
    kpis = context.get("kpis", {})
    
    revenue = kpis.get("total_revenue", 0)
    deals = kpis.get("total_deals", 0)
    growth = kpis.get("revenue_growth", 0)
    conversion = kpis.get("avg_conversion_rate", 0)
    best_product = kpis.get("best_product", "N/A")
    best_region = kpis.get("best_region", "N/A")
    best_seller = kpis.get("best_seller", "N/A")

    # Revenue
    if any(w in msg for w in ["receita", "revenue", "faturamento", "faturou", "ganhou"]):
        trend = "crescimento positivo" if growth > 0 else "queda"
        return (
            f"💰 **Análise de Receita**\n\n"
            f"A receita total no período analisado foi de **R$ {revenue:,.2f}**, com {trend} de **{growth:+.1f}%** "
            f"em relação à primeira metade do período.\n\n"
            f"O produto mais rentável é o **{best_product}**, e a região com melhor desempenho é **{best_region}**.\n\n"
            f"{'✅ Recomendo manter o foco nos canais atuais e expandir para regiões secundárias.' if growth > 5 else '⚠️ Recomendo revisar a estratégia de precificação e intensificar ações de upsell.'}"
        )

    # Conversion
    elif any(w in msg for w in ["conversão", "conversion", "taxa", "funil", "pipeline"]):
        status = "acima da média do setor (~22%)" if conversion > 22 else "abaixo da média do setor (~22%)"
        tips = (
            "Continue o bom trabalho! Foque em reduzir o tempo do ciclo de vendas.\n- Automatize follow-ups\n- Qualifique melhor leads no topo do funil"
            if conversion > 22 else
            "Oportunidade de melhoria identificada:\n- Revise o script de abordagem\n- Treine a equipe em técnicas de fechamento\n- Implemente lead scoring"
        )
        return (
            f"📊 **Taxa de Conversão**\n\n"
            f"A taxa média de conversão está em **{conversion:.1f}%**, {status}.\n\n"
            f"**Recomendações:**\n{tips}"
        )

    # Sellers
    elif any(w in msg for w in ["vendedor", "seller", "equipe", "time", "performance"]):
        return (
            f"👥 **Performance da Equipe**\n\n"
            f"Top performer do período: **{best_seller}**.\n\n"
            f"**Insights:**\n"
            f"- Total de negócios fechados: **{deals:,}**\n"
            f"- Ticket médio por negócio: **R$ {(revenue/deals if deals else 0):,.2f}**\n\n"
            f"**Ações recomendadas:**\n"
            f"- Compartilhe as práticas do top performer com o restante da equipe\n"
            f"- Crie metas individuais baseadas no histórico de cada vendedor\n"
            f"- Implemente um programa de coaching semanal"
        )

    # Prediction / forecast
    elif any(w in msg for w in ["previsão", "forecast", "próximo", "futuro", "projeção", "predict"]):
        projected = revenue * (1 + growth / 100)
        proj_deals = int(deals * 1.08)
        return (
            f"🔮 **Previsão para o Próximo Período**\n\n"
            f"Com base na tendência atual de **{growth:+.1f}%**, as projeções são:\n\n"
            f"- 📈 Receita projetada: **R$ {projected:,.2f}**\n"
            f"- 🤝 Negócios estimados: **{proj_deals:,}**\n"
            f"- 🎯 Conversão esperada: **{min(conversion * 1.05, 45):.1f}%**\n\n"
            f"⚠️ *Essas projeções assumem condições de mercado estáveis. Fatores externos podem impactar os resultados.*"
        )

    # Churn / risk
    elif any(w in msg for w in ["churn", "risco", "cancelamento", "perda", "retenção"]):
        return (
            f"⚠️ **Análise de Risco e Churn**\n\n"
            f"Com base nos dados comportamentais dos clientes:\n\n"
            f"- 🔴 **Alto risco** (~15% da base): Clientes sem interação há >60 dias\n"
            f"- 🟡 **Médio risco** (~28% da base): Queda de 30%+ no uso do produto\n"
            f"- 🟢 **Baixo risco** (~57% da base): Engajamento regular e crescente\n\n"
            f"**Ações preventivas:**\n"
            f"- Acione o Customer Success para clientes em risco alto\n"
            f"- Ofereça treinamentos gratuitos para clientes em risco médio\n"
            f"- Crie programa de fidelidade para clientes saudáveis"
        )

    # Region
    elif any(w in msg for w in ["região", "region", "estado", "mercado", "expansão"]):
        return (
            f"🗺️ **Análise Regional**\n\n"
            f"Melhor performance: **{best_region}**\n\n"
            f"**Distribuição estimada de receita:**\n"
            f"- Sudeste: ~38% da receita total\n"
            f"- Sul: ~24%\n"
            f"- Nordeste: ~18%\n"
            f"- Centro-Oeste: ~12%\n"
            f"- Norte: ~8%\n\n"
            f"**Oportunidade:** Norte e Centro-Oeste apresentam baixa penetração mas crescimento acelerado. "
            f"Recomendo alocar 1-2 vendedores especializados para essas regiões."
        )

    # Greeting
    elif any(w in msg for w in ["olá", "oi", "hello", "hi", "bom dia", "boa tarde", "boa noite"]):
        return (
            f"👋 **Olá! Sou seu Analista de Vendas com IA.**\n\n"
            f"Aqui está um resumo rápido do período atual:\n\n"
            f"- 💰 Receita: **R$ {revenue:,.2f}**\n"
            f"- 📈 Crescimento: **{growth:+.1f}%**\n"
            f"- 🤝 Negócios: **{deals:,}**\n\n"
            f"Posso te ajudar com análise de receita, conversão, performance da equipe, previsões, "
            f"análise de churn e muito mais. **O que você gostaria de explorar?**"
        )

    # Default
    else:
        return (
            f"🤖 **Análise Inteligente de Vendas**\n\n"
            f"Com base nos dados do período analisado:\n\n"
            f"**Métricas-chave:**\n"
            f"- Receita Total: R$ {revenue:,.2f}\n"
            f"- Crescimento: {growth:+.1f}%\n"
            f"- Conversão Média: {conversion:.1f}%\n"
            f"- Melhor Produto: {best_product}\n\n"
            f"**Posso analisar:**\n"
            f"- Receita e faturamento\n"
            f"- Taxa de conversão e funil de vendas\n"
            f"- Performance da equipe\n"
            f"- Previsões e projeções\n"
            f"- Risco de churn\n"
            f"- Análise regional\n\n"
            f"*Tente perguntar: \"Como está nossa taxa de conversão?\" ou \"Faça uma previsão para o próximo mês\"*"
        )

# ─── Routes ───────────────────────────────────────────────────────────────────

@app.get("/")
def root():
    return {"status": "ok", "message": "AI Sales Analyst API", "version": "1.0.0"}

@app.get("/api/kpis")
def get_kpis(period: str = "90d"):
    days = int(period.replace("d", "")) if "d" in period else 90
    data = generate_sales_data(days)
    return compute_kpis(data)

@app.get("/api/timeseries")
def get_timeseries(period: str = "90d"):
    days = int(period.replace("d", "")) if "d" in period else 90
    data = generate_sales_data(days)
    return [{"date": d["date"], "revenue": d["revenue"], "deals": d["deals"]} for d in data]

@app.get("/api/by-product")
def get_by_product(period: str = "90d"):
    days = int(period.replace("d", "")) if "d" in period else 90
    data = generate_sales_data(days)
    return compute_by_dimension(data, "product")

@app.get("/api/by-region")
def get_by_region(period: str = "90d"):
    days = int(period.replace("d", "")) if "d" in period else 90
    data = generate_sales_data(days)
    return compute_by_dimension(data, "region")

@app.get("/api/by-seller")
def get_by_seller(period: str = "90d"):
    days = int(period.replace("d", "")) if "d" in period else 90
    data = generate_sales_data(days)
    return compute_by_dimension(data, "seller")

@app.get("/api/funnel")
def get_funnel():
    return compute_funnel()

@app.get("/api/top-products")
def get_top_products(period: str = "90d", limit: int = 5):
    days = int(period.replace("d", "")) if "d" in period else 90
    data = generate_sales_data(days)
    by_product = compute_by_dimension(data, "product")
    sorted_products = sorted(by_product, key=lambda x: x["revenue"], reverse=True)
    return sorted_products[:limit]

@app.post("/api/chat")
def chat(body: ChatMessage):
    context = body.context or {}
    if not context.get("kpis"):
        data = generate_sales_data(90)
        context["kpis"] = compute_kpis(data)
    response = analyze_with_ai(body.message, context)
    return {"reply": response, "timestamp": datetime.now().isoformat()}

@app.get("/api/health")
def health():
    return {"status": "healthy", "timestamp": datetime.now().isoformat(), "version": "1.0.0"}
