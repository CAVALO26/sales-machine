import os
import time
import streamlit as st
import requests

# No Railway, BACKEND_URL é setado como variável de ambiente apontando para o serviço backend
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

st.set_page_config(
    page_title="AI Sales Machine",
    page_icon="🤖",
    layout="centered"
)

# ── Estilos ──────────────────────────────────────────────
st.markdown("""
<style>
    .main { background: #0f0f0f; }
    .stTextInput > div > div > input {
        background: #1a1a1a;
        color: #fff;
        border: 1px solid #333;
        border-radius: 8px;
    }
    .stButton > button {
        background: linear-gradient(135deg, #6c63ff, #3ecf8e);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 2rem;
        font-size: 1rem;
        font-weight: 600;
        width: 100%;
    }
    .step-card {
        background: #1a1a1a;
        border: 1px solid #2a2a2a;
        border-radius: 10px;
        padding: 1rem 1.2rem;
        margin: 0.4rem 0;
        font-size: 0.9rem;
        color: #ccc;
    }
    .step-active  { border-left: 3px solid #6c63ff; color: #fff; }
    .step-done    { border-left: 3px solid #3ecf8e; color: #3ecf8e; }
    .step-pending { border-left: 3px solid #333; }
</style>
""", unsafe_allow_html=True)

# ── Header ───────────────────────────────────────────────
st.markdown("## 🤖 AI Sales Machine")
st.markdown("Preencha os dados abaixo e clique em **Iniciar**. O sistema faz o resto automaticamente.")
st.divider()

# ── Formulário ───────────────────────────────────────────
with st.form("campaign_form"):
    col1, col2 = st.columns(2)
    with col1:
        url    = st.text_input("🔗 URL da Página Validada", placeholder="https://...")
        niche  = st.text_input("🏷️ Nicho", placeholder="ex: fitness, emagrecimento")
        country = st.text_input("🌍 País", placeholder="ex: BR, US")
    with col2:
        price  = st.text_input("💰 Preço do Produto", placeholder="ex: 47")
        target = st.text_input("👥 Público-Alvo", placeholder="ex: mulheres 30-50 anos")
        st.markdown("<br>", unsafe_allow_html=True)

    submitted = st.form_submit_button("🚀 Iniciar Máquina de Vendas")

# ── Pipeline ─────────────────────────────────────────────
STEPS = [
    ("scraping",            "🌐 Fazendo scraping da página"),
    ("extracting",          "🔍 Extraindo estrutura (headline, bullets, CTA)"),
    ("generating_copy",     "✍️  Gerando copy com Template Engine"),
    ("validating",          "✅ Validando copy"),
    ("building_funnel",     "🏗️  Publicando funil no WordPress"),
    ("generating_creative", "🎨 Criando imagem do anúncio"),
    ("creating_ads",        "📣 Criando campanha no Meta Ads"),
]

def render_steps(current_step: str, done: bool = False):
    step_keys = [s[0] for s in STEPS]
    current_idx = step_keys.index(current_step) if current_step in step_keys else -1
    html = ""
    for i, (key, label) in enumerate(STEPS):
        if done or i < current_idx:
            css = "step-done"
            icon = "✔"
        elif i == current_idx:
            css = "step-active"
            icon = "⏳"
        else:
            css = "step-pending"
            icon = "○"
        html += f'<div class="step-card {css}">{icon} {label}</div>'
    st.markdown(html, unsafe_allow_html=True)

if submitted:
    if not url:
        st.error("Por favor, informe a URL da página.")
    else:
        data = {
            "product_url": url,
            "niche":       niche,
            "country":     country,
            "price":       price,
            "target":      target
        }

        st.divider()
        st.markdown("### ⚙️ Progresso")

        try:
            r = requests.post(f"{BACKEND_URL}/create-campaign", json=data, timeout=10)
            r.raise_for_status()
            task_id = r.json().get("task_id")
            st.caption(f"Task ID: `{task_id}`")

            progress_bar = st.progress(0)
            status_placeholder = st.empty()
            step_placeholder   = st.empty()

            current_step = "scraping"
            for _ in range(120):  # max 10 min
                time.sleep(5)
                try:
                    sr = requests.get(f"{BACKEND_URL}/status/{task_id}", timeout=10)
                    status_data = sr.json()
                except Exception:
                    continue

                task_status = status_data.get("status", "")
                meta = status_data.get("result") or {}

                if isinstance(meta, dict):
                    current_step = meta.get("step", current_step)
                    pct = meta.get("pct", 0)
                    progress_bar.progress(int(pct))

                with step_placeholder.container():
                    render_steps(current_step)

                status_placeholder.caption(f"Status: **{task_status}**")

                if task_status == "SUCCESS":
                    progress_bar.progress(100)
                    with step_placeholder.container():
                        render_steps(current_step, done=True)
                    st.balloons()
                    st.success("🎉 Funil criado com sucesso!")

                    result = status_data.get("result", {})

                    st.divider()
                    st.markdown("### 📋 Resultados")
                    col_a, col_b = st.columns(2)

                    with col_a:
                        st.markdown("**Copy gerada**")
                        copy = result.get("copy", {})
                        st.markdown(f"**Headline:** {copy.get('headline','')}")
                        st.markdown(f"**CTA:** {copy.get('cta','')}")
                        for b in copy.get("bullets", []):
                            st.markdown(f"- {b}")

                    with col_b:
                        st.markdown("**Funil WordPress**")
                        funnel = result.get("funnel", {})
                        if funnel.get("url"):
                            st.markdown(f"🔗 [Abrir landing page]({funnel['url']})")
                        st.markdown("**Meta Ads**")
                        ads = result.get("ads", {})
                        st.code(f"Campaign ID: {ads.get('campaign_id','')}\nAdset ID:    {ads.get('adset_id','')}\nStatus:      {ads.get('status','')}")

                    with st.expander("Ver JSON completo"):
                        st.json(result)
                    break

                elif task_status == "FAILURE":
                    st.error("❌ Erro no pipeline. Verifique os logs do worker.")
                    st.json(status_data)
                    break

        except requests.exceptions.ConnectionError:
            st.error(f"Não foi possível conectar à API em `{BACKEND_URL}`.\nVerifique se o serviço backend está rodando.")
        except Exception as e:
            st.error(f"Erro inesperado: {e}")
