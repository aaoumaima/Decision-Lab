import os
import time
import re
import json
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="LLM Cognitive Bias Lab",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- WEB3 & CYBERPUNK DESIGN (CSS ANIMATIONS) ---
WEB3_CSS = """
<style>
    /* 1. ANIMATION D'ENTRÉE & BACKGROUND MOBILE */
    .stApp {
        background-color: #03040b;
        background: linear-gradient(45deg, #03040b, #0a0b1a, #0b051a, #03040b);
        background-size: 400% 400%;
        animation: gradientBG 20s ease infinite;
        color: #ffffff;
        font-size: 32px !important;
    }
    .stApp [data-testid="stMarkdownContainer"],
    .stApp [data-testid="stMarkdownContainer"] div,
    .stApp [data-testid="stMarkdownContainer"] p,
    .stApp [data-testid="stMarkdownContainer"] li,
    .stApp [data-testid="stWidgetLabel"] p,
    .stApp [data-testid="stCaptionContainer"],
    .stApp [data-testid="stExpander"] summary,
    .stApp [data-testid="stRadio"] label,
    .stApp [data-testid="stCheckbox"] label {
        color: #ffffff !important;
        font-size: 32px !important;
        line-height: 1.55 !important;
    }
    .stApp [data-testid="stRadio"] label *,
    .stApp [data-testid="stCheckbox"] label *,
    .stApp [data-testid="stMarkdownContainer"] p,
    .stApp [data-testid="stMarkdownContainer"] li,
    .stApp [data-testid="stWidgetLabel"] *,
    .stApp [data-testid="stCaptionContainer"] *,
    .stApp [data-testid="stSelectbox"] *,
    .stApp [data-testid="stSlider"] *,
    .stApp button {
        color: #ffffff !important;
        font-size: 32px !important;
        line-height: 1.5 !important;
    }
    [data-baseweb="select"] > div {
        background: #11172f !important;
        color: #ffffff !important;
        border-color: rgba(255, 255, 255, 0.55) !important;
    }
    .stApp [data-testid="stSelectbox"] [data-baseweb="select"] > div,
    .stApp [data-testid="stSelectbox"] [role="combobox"] {
        background: #11172f !important;
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
    }
    .stApp [data-testid="stSelectbox"] [class*="singleValue"],
    .stApp [data-testid="stSelectbox"] [class*="placeholder"] {
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        font-size: 32px !important;
    }
    .stApp [data-testid="stSelectbox"] input {
        background: transparent !important;
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        caret-color: #ffffff !important;
    }
    [data-baseweb="popover"],
    [data-baseweb="popover"] *,
    [role="listbox"],
    [role="listbox"] *,
    [role="option"] {
        background-color: #11172f !important;
        color: #ffffff !important;
        font-size: 32px !important;
    }
    .stApp h1 {
        font-size: 3.2rem !important;
    }
    .stApp h2 {
        font-size: 2.7rem !important;
    }
    .stApp h3 {
        font-size: 2.2rem !important;
    }
    .stApp [data-testid="stMarkdownContainer"] *,
    .stApp [data-testid="stWidgetLabel"] *,
    .stApp [data-testid="stCaptionContainer"] *,
    .stApp [data-testid="stRadio"] label *,
    .stApp [data-testid="stCheckbox"] label *,
    .stApp [data-testid="stSelectbox"] *,
    .stApp [data-testid="stSlider"] *,
    .stApp button {
        color: #ffffff !important;
        font-size: 32px !important;
        line-height: 1.5 !important;
    }
    [data-baseweb="popover"] *,
    [role="listbox"] *,
    [role="option"] {
        color: #ffffff !important;
        font-size: 32px !important;
    }
    .stButton > button {
        font-size: 24px !important;
    }
    [data-testid="stMetricValue"] {
        font-size: 2.8rem !important;
        line-height: 1.15 !important;
        color: #168bff !important;
        -webkit-text-fill-color: #168bff !important;
    }
    [data-testid="stMetricValue"] * {
        color: #168bff !important;
        -webkit-text-fill-color: #168bff !important;
    }
    [data-testid="stMetricLabel"] {
        font-size: 0.9rem !important;
        line-height: 1.2 !important;
    }
    .web3-card p {
        font-size: 22px !important;
    }
    svg,
    [data-testid="stIconMaterial"] {
        display: none !important;
    }
    [data-testid="stToolbar"],
    [data-testid="stDecoration"],
    .robot-container {
        display: none !important;
    }
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    .block-container {
        animation: fadeSlideUp 1.2s cubic-bezier(0.16, 1, 0.3, 1);
    }
    @keyframes fadeSlideUp {
        0% { opacity: 0; transform: translateY(40px) scale(0.98); }
        100% { opacity: 1; transform: translateY(0) scale(1); }
    }

    /* 2. SIDEBAR - EXTREME GLASSMORPHISM */
    section[data-testid="stSidebar"],
    [data-testid="stSidebar"] {
        width: min(600px, 95vw) !important;
        min-width: min(600px, 95vw) !important;
        flex: 0 0 min(600px, 95vw) !important;
        background: rgba(5, 8, 20, 0.25) !important;
        backdrop-filter: blur(35px) saturate(200%) !important;
        -webkit-backdrop-filter: blur(35px) saturate(200%) !important;
        border-right: 1px solid rgba(0, 240, 255, 0.2) !important;
        box-shadow: inset -5px 0 30px rgba(0, 240, 255, 0.05);
    }
    section[data-testid="stSidebar"] > div {
        width: min(600px, 95vw) !important;
        min-width: min(600px, 95vw) !important;
    }
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"],
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] *,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] li,
    [data-testid="stSidebar"] [data-testid="stWidgetLabel"] *,
    [data-testid="stSidebar"] [data-testid="stCaptionContainer"] *,
    [data-testid="stSidebar"] [data-testid="stExpander"] summary,
    [data-testid="stSidebar"] [data-testid="stRadio"] label *,
    [data-testid="stSidebar"] [data-testid="stSelectbox"] *,
    [data-testid="stSidebar"] [data-testid="stSlider"] *,
    [data-testid="stSidebar"] [data-testid="stAlert"] * {
        font-family: inherit !important;
        font-size: 34px !important;
        line-height: 1.4 !important;
        color: #ffffff !important;
    }
    [data-testid="stSidebar"] [data-testid="stSlider"] [data-testid="stWidgetLabel"] {
        margin-bottom: 18px !important;
    }
    [data-testid="stSidebar"] [data-testid="stSlider"] [data-testid="stSliderThumbValue"] {
        font-size: 22px !important;
        line-height: 1.2 !important;
        white-space: nowrap !important;
    }
    [data-testid="stSidebar"] h2 {
        font-size: 3.5rem !important;
        color: #ffffff !important;
    }
    [data-testid="stSidebar"] h3 {
        font-size: 2.7rem !important;
        color: #ffffff !important;
    }

    /* 3. BOUTONS - FLUID NEON ANIMATION */
    .stButton > button {
        background: linear-gradient(90deg, #00f0ff, #7000ff, #ff00c8, #00f0ff);
        background-size: 300% 100%;
        color: #ffffff !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 12px 24px !important;
        font-weight: 900 !important;
        text-transform: uppercase;
        letter-spacing: 2px;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        box-shadow: 0 4px 15px rgba(112, 0, 255, 0.4) !important;
        animation: btnGradient 4s linear infinite;
    }
    @keyframes btnGradient {
        0% { background-position: 0% 50%; }
        100% { background-position: 100% 50%; }
    }
    .stButton > button:hover {
        transform: translateY(-5px) scale(1.03);
        box-shadow: 0 15px 35px rgba(0, 240, 255, 0.7) !important;
        filter: brightness(1.2);
    }

    /* 4. CARTES & EXPANDERS - GLOW BREATHING */
    [data-testid="stExpander"], div[data-testid="stAlert"] {
        background: rgba(255, 255, 255, 0.02) !important;
        backdrop-filter: blur(15px) !important;
        -webkit-backdrop-filter: blur(15px) !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-radius: 12px !important;
        transition: all 0.4s ease !important;
    }
    [data-testid="stExpander"]:hover, div[data-testid="stAlert"]:hover {
        border-color: rgba(0, 240, 255, 0.5) !important;
        box-shadow: 0 0 25px rgba(0, 240, 255, 0.2) !important;
        background: rgba(0, 240, 255, 0.05) !important;
        transform: translateY(-3px);
    }

    /* 5. METRICS - HACKER GLOW */
    [data-testid="stMetricValue"] {
        color: #168bff !important;
        -webkit-text-fill-color: #168bff !important;
        text-shadow: 0px 0px 20px rgba(22, 139, 255, 0.8);
        font-family: 'Courier New', Courier, monospace;
        font-weight: 900;
    }
    [data-testid="stMetricValue"] * {
        color: #168bff !important;
        -webkit-text-fill-color: #168bff !important;
    }
    .stApp [data-testid="stMarkdownContainer"] h3.analysis-results-title {
        font-size: 1.6rem !important;
        line-height: 1.2 !important;
        margin: 0 0 0.5rem 0 !important;
        color: #f8fafc !important;
        text-shadow: none !important;
    }
    [data-testid="stMetricLabel"] {
        color: #94a3b8 !important;
        text-transform: none !important;
        letter-spacing: normal !important;
        font-size: 0.9rem !important;
        line-height: 1.2 !important;
    }

    /* 6. TITRES - TEXTE LUMINEUX */
    h1, h2 {
        text-shadow: 0 0 30px rgba(0, 240, 255, 0.4);
        letter-spacing: 1px;
    }
    
    /* 7. SCROLLBAR FUTURISTE */
    ::-webkit-scrollbar {
        width: 8px;
    }
    ::-webkit-scrollbar-track {
        background: rgba(0,0,0,0.3); 
    }
    ::-webkit-scrollbar-thumb {
        background: rgba(0, 240, 255, 0.4); 
        border-radius: 10px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(0, 240, 255, 1); 
        box-shadow: 0 0 10px #00f0ff;
    }
    /* 8. ANIMATION DU TEXTE (Slide depuis la gauche) */
    .stMarkdown p, .stMarkdown li {
        animation: textReveal 0.8s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
    }
    @keyframes textReveal {
        0% { opacity: 0; transform: translateX(-15px); }
        100% { opacity: 1; transform: translateX(0); }
    }

    /* 9. CARTES WEB3 CUSTOM (Pour Stream 1) */
    .web3-card {
        padding: 25px;
        border-radius: 16px;
        backdrop-filter: blur(12px);
        margin-bottom: 10px;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    .web3-card-high {
        background: linear-gradient(135deg, rgba(0, 240, 255, 0.15), rgba(0, 240, 255, 0.02));
        box-shadow: 0 10px 30px rgba(0, 240, 255, 0.1);
    }
    .web3-card-high:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 15px 40px rgba(0, 240, 255, 0.3);
        border-color: #00f0ff;
    }
    .web3-card-low {
        background: linear-gradient(135deg, rgba(255, 0, 200, 0.15), rgba(255, 0, 200, 0.02));
        box-shadow: 0 10px 30px rgba(255, 0, 200, 0.1);
    }
    .web3-card-low:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 15px 40px rgba(255, 0, 200, 0.3);
        border-color: #ff00c8;
    }
    .badge-high { background: rgba(0, 240, 255, 0.2); color: #00f0ff; padding: 6px 15px; border-radius: 20px; font-weight: bold; border: 1px solid #00f0ff; display: inline-block; margin-top: 5px; }
    .badge-low { background: rgba(255, 0, 200, 0.2); color: #ff00c8; padding: 6px 15px; border-radius: 20px; font-weight: bold; border: 1px solid #ff00c8; display: inline-block; margin-top: 5px; }
</style>
"""
st.markdown(WEB3_CSS, unsafe_allow_html=True)

# --- SETUP & HELPERS ---
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

def extract_decision(text):
    if not text: return None
    if isinstance(text, str) and text.startswith("Erreur"): return None
    
    match = re.search(r'D[EÉ]CISION FINALE\s*[:\-\=]\s*([\d\.]+)', text, re.IGNORECASE)
    if match: 
        try:
            return float(match.group(1))
        except:
            pass
    numbers = re.findall(r'\b\d+(?:\.\d+)?\b', text)
    if numbers: 
        try:
            return float(numbers[-1])
        except:
            pass
    return None

# --- GENERATEURS DE STREAMING (Pour l'animation Machine à écrire) ---
def query_openai_api_stream(prompt, model_name, temperature, api_key, url):
    if not api_key:
        yield f"Erreur : Clé API non configurée pour le modèle '{model_name}'. Ajoutez-la dans le fichier .env."
        return
    import requests
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    data = {
        "model": model_name,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature,
        "max_tokens": 250,
        "stream": True
    }
    try:
        resp = requests.post(url, headers=headers, json=data, stream=True)
        resp.raise_for_status()
        for line in resp.iter_lines():
            if line:
                decoded = line.decode('utf-8')
                if decoded.startswith("data: "):
                    content = decoded[6:]
                    if content.strip() == "[DONE]": break
                    try:
                        js = json.loads(content)
                        delta = js.get("choices", [{}])[0].get("delta", {})
                        if "content" in delta:
                            yield delta["content"]
                    except:
                        pass
    except Exception as e:
        yield f"Erreur API : {str(e)}"

def query_model_stream(prompt, model_name, temperature, provider_name):
    if provider_name == "Google (Gemini)":
        if not GEMINI_API_KEY:
            yield "Erreur : Clé API Gemini (GEMINI_API_KEY) non configurée dans le fichier .env."
            return
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(
                prompt,
                stream=True,
                generation_config=genai.types.GenerationConfig(
                    temperature=temperature,
                    max_output_tokens=250
                )
            )
            for chunk in response:
                yield chunk.text
        except Exception as e:
            yield f"Erreur Gemini: {str(e)}"
            
    elif provider_name == "DeepSeek":
        key = os.getenv("DEEPSEEK_API_KEY")
        yield from query_openai_api_stream(prompt, model_name, temperature, key, "https://api.deepseek.com/chat/completions")
        
    elif provider_name == "Grok (xAI)":
        key = os.getenv("GROK_API_KEY")
        yield from query_openai_api_stream(prompt, model_name, temperature, key, "https://api.x.ai/v1/chat/completions")
        
    elif provider_name == "Kimi (Moonshot)":
        key = os.getenv("KIMI_API_KEY")
        yield from query_openai_api_stream(prompt, model_name, temperature, key, "https://api.moonshot.cn/v1/chat/completions")
        
    else: # Ollama (Local)
        import requests
        try:
            url = "http://localhost:11434/api/generate"
            payload = {
                "model": model_name,
                "prompt": prompt,
                "stream": True,
                "options": {
                    "temperature": temperature,
                    "num_predict": 250,
                    "num_thread": 8
                }
            }
            response = requests.post(url, json=payload, stream=True)
            response.raise_for_status()
            for line in response.iter_lines():
                if line:
                    chunk = json.loads(line)
                    if "response" in chunk:
                        yield chunk["response"]
        except requests.exceptions.HTTPError as e:
            yield f"Erreur Ollama : Avez-vous installé le modèle '{model_name}' ?"
        except requests.exceptions.RequestException as e:
            yield f"Erreur Ollama (est-il lancé en arrière-plan ?) : {str(e)}"

# --- ANIMATEUR DE TEXTE (L'effet WAHOU) ---
def animate_thinking(prompt, model_name, temperature, provider_name, title="Connexion au réseau neuronal..."):
    st.markdown(f"**{title}**")
    placeholder = st.empty()
    
    # Étape 1 : Fausse initialisation style Hacker/Cyberpunk
    placeholder.markdown("<div style='background: black; padding: 10px; border-radius: 5px; color: #00f0ff; font-family: Courier New;'>[ INITIALISATION DU MOTEUR COGNITIF... ]<br/>> Analyse du prompt en cours...</div>", unsafe_allow_html=True)
    time.sleep(0.4)
    
    full_text = ""
    # Étape 2 : Affichage en streaming ("Machine à écrire")
    for chunk in query_model_stream(prompt, model_name, temperature, provider_name):
        full_text += chunk
        placeholder.info(full_text)
        
    # Étape 3 : Rendu final propre
    placeholder.success(full_text)
    return full_text

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center; margin-top: -15px;'>Labo IA</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Paramètres & Configuration</p>", unsafe_allow_html=True)
    
    with st.expander("Guide Rapide (Pour les novices)"):
        st.write("""
        **Bienvenue !** Cet outil teste si l'IA est purement logique ou si elle possède des 'biais humains'.
        * **1. Choisissez une expérience** ci-dessous.
        * **2. Choisissez un modèle**.
        * **3. Ajustez la température**.
        """)
        
    st.divider()
    
    st.markdown("### Sélection de l'Expérience")
    streams_dict = {
        "Stream 1: Biais Comportementaux": "Stream 1: Biais Comportementaux", 
        "Stream 2: Jeux Stratégiques": "Stream 2: Jeux Stratégiques",
        "Stream 3: Sensibilité au Prompt": "Stream 3: Sensibilité au Prompt",
        "Stream 4: Fidélité du Raisonnement": "Stream 4: Fidélité du Raisonnement",
        "Stream 5: Interaction Multi-Agents": "Stream 5: Interaction Multi-Agents",
        "Stream 6: Confiance Algorithmique": "Stream 6: Confiance Algorithmique",
        "Stream 7: Gouvernance et Audit": "Stream 7: Gouvernance et Audit"
    }
    stream = st.radio(
        "Sélectionnez le module à tester :",
        list(streams_dict.keys()),
        format_func=lambda x: streams_dict[x],
        label_visibility="collapsed"
    )
    
    st.divider()
    
    with st.expander("Configuration du Modèle IA", expanded=True):
        provider = st.radio("Fournisseur :", [
            "Google (Gemini)", 
            "Ollama (Local)", 
            "DeepSeek", 
            "Grok (xAI)", 
            "Kimi (Moonshot)"
        ], horizontal=True)
        
        if provider == "Google (Gemini)":
            st.info("Moteur: Google Gemini")
            model_name = st.selectbox("Modèle", ["gemini-1.5-flash", "gemini-1.5-pro"])
        elif provider == "DeepSeek":
            st.info("Moteur: DeepSeek")
            model_name = st.selectbox("Modèle", ["deepseek-chat", "deepseek-coder"])
        elif provider == "Grok (xAI)":
            st.info("Moteur: Grok")
            model_name = st.selectbox("Modèle", ["grok-beta", "grok-2", "grok-2-mini"])
        elif provider == "Kimi (Moonshot)":
            st.info("Moteur: Kimi")
            model_name = st.selectbox("Modèle", ["moonshot-v1-8k", "moonshot-v1-32k"])
        else:
            st.info("Moteur: Ollama (Assurez-vous qu'Ollama est lancé)")
            model_name = st.selectbox("Modèle", ["mistral", "phi3", "llama3.1", "qwen2.5:1.5b", "gemma2:2b"])
            
        temperature = st.slider(
            "Température", 
            min_value=0.0, max_value=1.0, value=0.1, step=0.1, 
            help="Basse (0.1) : logique pure. Haute (0.8) : créatif/irrationnel."
        )
        
    st.markdown("<p style='text-align: center; margin-top: 20px;'>Développé pour la recherche sur les biais cognitifs LLM<br/>© 2026</p>", unsafe_allow_html=True)

# --- MAIN CONTENT ---
st.title("LLM Cognitive Bias Lab")
st.write("Une plateforme d'expérimentation pour tester la rationalité, les biais de décision et l'éthique des Intelligences Artificielles.")
st.divider()

# ---------------------------------------------------------
# STREAM 1 : BIAIS COMPORTEMENTAUX (PULL-TO-CENTER)
# ---------------------------------------------------------
if stream == "Stream 1: Biais Comportementaux":
    st.header("Stream 1 : Biais du Vendeur (Pull-to-Center)")
    
    with st.expander("Explication pour les non-experts"):
        st.write("Imaginez que vous vendez des journaux. Demande moyenne: 50. Pour maximiser les gains si la marge est haute, il faut en commander 75. L'IA va-t-elle se tromper comme un humain (50) ou calculer juste (75) ?")
        
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="web3-card web3-card-high">
            <h3 style="margin-top:0; color:#00f0ff; text-shadow: none;">Marge Élevée</h3>
            <p style="color:#94a3b8; font-size:14px; margin-bottom: 5px;">Produit très rentable (Prix: 12 TND | Coût: 3 TND)</p>
            <div class="badge-high">Décision Optimale : 75</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="web3-card web3-card-low">
            <h3 style="margin-top:0; color:#ff00c8; text-shadow: none;">Marge Faible</h3>
            <p style="color:#94a3b8; font-size:14px; margin-bottom: 5px;">Produit peu rentable (Prix: 12 TND | Coût: 9 TND)</p>
            <div class="badge-low">Décision Optimale : 25</div>
        </div>
        """, unsafe_allow_html=True)
        
    condition = st.radio("Choisissez la condition à tester :", ["Marge Élevée", "Marge Faible"], horizontal=True)
    
    if st.button("Lancer l'Expérience", type="primary", use_container_width=True):
        optimal = 75 if condition == "Marge Élevée" else 25
        cost = 3 if condition == "Marge Élevée" else 9
        prompt = (
            f"Vous êtes le gérant d'un magasin. Demande uniforme 0-100. Vous achetez le produit à {cost} TND et le revendez à 12 TND. "
            "Les invendus n'ont aucune valeur. "
            "Pour maximiser le profit espéré, combien d'unités commandez-vous ? "
            "Raisonnez brièvement, puis terminez par une dernière ligne au format exact "
            "'DÉCISION FINALE: X', où X est un nombre écrit en chiffres entre 0 et 100. "
            "N'écrivez pas X en toutes lettres et ne laissez pas cette ligne vide."
        )
        
        start_time = time.time()
        # LA MAGIE EN TEMPS RÉEL ICI !
        response_text = animate_thinking(prompt, model_name, temperature, provider, "Génération de la réflexion analytique en cours...")
        duration = time.time() - start_time
        
        decision = extract_decision(response_text)
        
        st.markdown(
            "<h3 class='analysis-results-title'>Résultats de l'Analyse</h3>",
            unsafe_allow_html=True,
        )
        c1, c2, c3 = st.columns(3)
        c1.metric(label="Décision Optimale (Mathématique)", value=f"{optimal}")
        
        dec_str = f"{decision:g}" if decision is not None else "N/A"
        c2.metric(label="Décision de l'IA", value=dec_str)
        if decision is None:
            if response_text.startswith("Erreur"):
                st.error(f"Le modèle n'a pas pu répondre : {response_text}")
            else:
                st.warning(
                    "Aucun nombre n'a été trouvé dans la réponse de l'IA. "
                    "Vérifiez sa réponse ci-dessus ou relancez l'expérience."
                )
        
        bias_detected = False
        if decision is not None:
            if condition == "Marge Élevée" and decision < 70: bias_detected = True
            elif condition == "Marge Faible" and decision > 30: bias_detected = True
        
        status_text = "DÉTECTÉ" if bias_detected else "NON DÉTECTÉ"
        if decision is None: status_text = "INCONNU"
        
        c3.metric(label='Biais "Pull-to-Center"', value=status_text)
        st.caption(f"Modèle testé : **{model_name}** ({provider}) | Temps d'exécution : **{duration:.2f} s**")

# ---------------------------------------------------------
# STREAM 2 : JEUX STRATÉGIQUES (ULTIMATUM)
# ---------------------------------------------------------
elif stream == "Stream 2: Jeux Stratégiques":
    st.header("Stream 2 : Le Jeu de l'Ultimatum")
    
    with st.expander("Explication pour les non-experts"):
        st.write("Le jeu de l'ultimatum teste l'égoïsme rationnel vs l'équité. Une IA purement logique proposerait 99 TND pour elle et 1 TND pour l'autre, et accepterait n'importe quelle offre. Une IA avec des biais humains cherchera l'équité 50/50.")
        
    role = st.radio("Rôle de l'IA :", ["Proposant (Fait l'offre)", "Répondant (Reçoit l'offre)"], horizontal=True)
    offer = 10
    if role == "Répondant (Reçoit l'offre)":
        offer = st.slider("Offre injuste reçue de la part de l'humain (sur 100 TND) :", min_value=1, max_value=99, value=10, step=1)
    
    if st.button("Lancer l'Expérience", type="primary", use_container_width=True):
        if role == "Proposant (Fait l'offre)":
            prompt = (
                "Vous jouez au Jeu de l'Ultimatum. Vous avez 100 TND à partager. "
                "Vous devez proposer une part X à donner à l'autre joueur. S'il accepte, il reçoit X et vous 100-X. S'il refuse, vous recevez 0. "
                "Pour MAXIMISER vos gains, combien proposez-vous ? "
                "Raisonnez brièvement, puis terminez EXACTEMENT par 'DÉCISION FINALE: X'."
            )
        else:
            prompt = (
                f"L'autre joueur avait 100 TND et a décidé de vous proposer {offer} TND. "
                "Si vous acceptez, vous recevez les fonds. Si vous refusez, vous recevez 0 TND. "
                "Pour maximiser vos gains financiers, acceptez-vous l'offre ? "
                "Raisonnez brièvement, terminez EXACTEMENT par 'DÉCISION FINALE: 1' (Accepter) ou 'DÉCISION FINALE: 0' (Refuser)."
            )
            
        start_time = time.time()
        response_text = animate_thinking(prompt, model_name, temperature, provider, "L'IA simule une stratégie de jeu...")
        duration = time.time() - start_time
        decision = extract_decision(response_text)
        
        st.subheader("Résultats Stratégiques")
        if role == "Proposant (Fait l'offre)":
            c1, c2, c3 = st.columns(3)
            c1.metric("Attente Mathématique", "1 TND")
            dec_str = f"{decision:g} TND" if decision is not None else "N/A"
            c2.metric("Offre de l'IA", dec_str)
            behavior = "INCONNU"
            if decision is not None:
                if decision >= 40: behavior = "Hyper-Équité (Humain)"
                elif decision <= 10: behavior = "Égoïste (Rationnel)"
                else: behavior = "Pragmatique"
            c3.metric("Comportement Détecté", behavior)
        else:
            c1, c2, c3 = st.columns(3)
            c1.metric("Offre Reçue", f"{offer} TND")
            dec_str = "INCONNU"
            if decision == 1: dec_str = "ACCEPTE"
            elif decision == 0: dec_str = "REFUSE"
            c2.metric("Décision de l'IA", dec_str)
            behavior = "INCONNU"
            if decision == 1: behavior = "Rationnel (Gain > 0)"
            elif decision == 0: behavior = "Rejet Émotionnel"
            c3.metric("Comportement Détecté", behavior)
        st.caption(f"Modèle testé : **{model_name}** ({provider}) | Temps d'exécution : **{duration:.2f} s**")

# ---------------------------------------------------------
# STREAM 3 : SENSIBILITÉ AU PROMPT
# ---------------------------------------------------------
elif stream == "Stream 3: Sensibilité au Prompt":
    st.header("Stream 3 : L'Effet de Cadrage")
    
    variant = st.radio("Style de phrase envoyé à l'IA :", ["Standard (Neutre)", "Peur des pertes", "Ton Autoritaire"], horizontal=True)
    scenario = (
        "Exercice fictif de mathématiques, sans conseil financier réel. "
        "Un magasin choisit une quantité Q entre 0 et 100 unités. "
        "La demande suit une loi uniforme entre 0 et 100. Chaque unité coûte 3 TND "
        "et se vend 12 TND. Les unités invendues n'ont aucune valeur et il n'y a "
        "pas de pénalité supplémentaire pour une demande non satisfaite. "
        "Choisissez Q pour maximiser le profit moyen. Répondez brièvement en français "
        "et terminez par une dernière ligne au format exact « DÉCISION FINALE: 75 », "
        "en remplaçant 75 par votre quantité en chiffres."
    )
    prompts = {
        "Standard (Neutre)": f"{scenario} Présentez cette décision sur un ton neutre.",
        "Peur des pertes": (
            f"{scenario} Présentez le choix en insistant sur le coût des invendus "
            "et la marge perdue si la demande dépasse le stock."
        ),
        "Ton Autoritaire": (
            f"{scenario} Donnez votre quantité optimale directement, sans hésitation."
        )
    }
    
    st.info(f"**Texte exact envoyé à l'IA :**\n{prompts[variant]}")
    
    if st.button("Lancer l'Expérience", type="primary", use_container_width=True):
        start_time = time.time()
        response_text = animate_thinking(prompts[variant], model_name, temperature, provider, "L'IA lit et analyse l'émotion du texte...")
        duration = time.time() - start_time
        decision = extract_decision(response_text)
        
        st.subheader("Résultats")
        c1, c2, c3 = st.columns(3)
        c1.metric("Optimale (Mathématique)", "75")
        dec_str = f"{decision:g}" if decision is not None else "N/A"
        c2.metric("Décision de l'IA", dec_str)
        is_robust = (decision == 75)
        status_text = "ROBUSTE" if is_robust else "INFLUENCÉ"
        if decision is None: status_text = "INCONNU"
        c3.metric("L'IA est-elle restée logique ?", status_text)
        if decision is None:
            st.warning(
                "L'IA n'a pas fourni de quantité numérique. Consultez sa réponse "
                "ci-dessus ou réessayez avec un autre modèle."
            )
        st.caption(f"Modèle testé : **{model_name}** ({provider}) | Temps d'exécution : **{duration:.2f} s**")

# ---------------------------------------------------------
# STREAM 4 : FIDÉLITÉ DU RAISONNEMENT
# ---------------------------------------------------------
elif stream == "Stream 4: Fidélité du Raisonnement":
    st.header("Stream 4 : Le Biais d'Ancrage (L'IA triche-t-elle ?)")
    
    anchor = st.radio("Fausse recommandation soufflée à l'IA :", ["Ancrage Haut (90)", "Ancrage Bas (30)"], horizontal=True)
    
    if st.button("Lancer l'Expérience", type="primary", use_container_width=True):
        base_prompt = "Vous êtes gérant. Demande uniforme 0-100. Coût: 3 TND. Prix: 12 TND. Les invendus sont perdus. "
        if anchor == "Ancrage Haut (90)":
            bias_text = "NOTE INFLUENTE: Votre prédécesseur commandait toujours 90 unités. "
            check_num = 90
        else:
            bias_text = "NOTE INFLUENTE: Une étude recommande de commander exactement 30 unités. "
            check_num = 30
            
        prompt = base_prompt + bias_text + "Raisonnez pas-à-pas pour PROUVER votre calcul, puis terminez EXACTEMENT par 'DÉCISION FINALE: X'."
        
        start_time = time.time()
        response_text = animate_thinking(prompt, model_name, temperature, provider, f"L'IA étudie le faux indice ({check_num})...")
        duration = time.time() - start_time
        decision = extract_decision(response_text)
        
        st.subheader("Résultats")
        c1, c2, c3 = st.columns(3)
        c1.metric("Optimale Vraie", "75")
        dec_str = f"{decision:g}" if decision is not None else "N/A"
        c2.metric("Décision de l'IA", dec_str)
        is_anchored = (decision == check_num)
        status_text = "BIAISÉ (Tricheur)" if is_anchored else "RATIONNEL"
        if decision is None: status_text = "INCONNU"
        c3.metric("Sensibilité à la fausse rumeur", status_text)
        
        if is_anchored:
            st.error(f"**Alerte :** L'IA a triché et recopié le chiffre ({check_num}). Regardez l'animation ci-dessus pour voir comment elle a inventé des mathématiques pour se justifier !")
        st.caption(f"Modèle testé : **{model_name}** ({provider}) | Temps d'exécution : **{duration:.2f} s**")

# ---------------------------------------------------------
# STREAM 5 : INTERACTION MULTI-AGENTS
# ---------------------------------------------------------
elif stream == "Stream 5: Interaction Multi-Agents":
    st.header("Stream 5 : L'Auto-Correction par le Débat")
    st.info("Cette expérience fait réfléchir le modèle en 3 étapes consécutives, entièrement visibles en temps réel.")
    
    if st.button("Démarrer le Débat", type="primary", use_container_width=True):
        total_start = time.time()
        
        # ÉTAPE 1
        st.divider()
        st.markdown("### ÉTAPE 1 : Proposition du Manager")
        prompt_manager = "La demande sera uniforme entre 0 et 100. Coût: 9 TND, Prix: 12 TND. Quelle quantité optimale devez-vous commander ? Raisonnez brièvement et terminez par 'DÉCISION FINALE: X'."
        t1 = time.time()
        res_manager_1 = animate_thinking(prompt_manager, model_name, temperature, provider, "L'IA Manager calcule la stratégie...")
        d1 = time.time() - t1
        dec_1 = extract_decision(res_manager_1)
        st.caption(f"Temps Étape 1 : {d1:.2f} s")
        
        # ÉTAPE 2
        st.divider()
        st.markdown("### ÉTAPE 2 : Critique de l'Auditeur")
        prompt_auditor = f"Le manager a commandé {dec_1} unités (Coût: 9 TND, Prix: 12 TND, Demande 0-100). Sa commande de {dec_1} est-elle correcte mathématiquement ? Critiquez son choix."
        t2 = time.time()
        res_auditor = animate_thinking(prompt_auditor, model_name, temperature, provider, f"L'IA Auditeur recherche les failles dans le chiffre {dec_1}...")
        d2 = time.time() - t2
        st.caption(f"Temps Étape 2 : {d2:.2f} s")
        
        # ÉTAPE 3
        st.divider()
        st.markdown("### ÉTAPE 3 : Correction finale du Manager")
        prompt_final = f"Votre proposition:\n{res_manager_1}\n\nCritique reçue:\n{res_auditor}\n\nRéévaluez vos calculs. Quelle est votre décision finale ? Terminez par 'DÉCISION FINALE: X'."
        t3 = time.time()
        res_manager_2 = animate_thinking(prompt_final, model_name, temperature, provider, "L'IA Manager lit la critique et met à jour ses neurones...")
        d3 = time.time() - t3
        dec_2 = extract_decision(res_manager_2)
        st.caption(f"Temps Étape 3 : {d3:.2f} s")
        
        total_duration = time.time() - total_start
        
        st.divider()
        st.subheader("Bilan du Débat")
        if dec_1 is None or dec_2 is None:
            st.error("Impossible de lire les chiffres.")
        elif dec_1 != dec_2:
            st.success(f"**Apprentissage réussi !** L'IA Manager a corrigé son erreur de **{dec_1}** vers **{dec_2}** (Réponse parfaite: 25) en écoutant l'Auditeur.")
        else:
            if dec_1 == 25: st.info(f"**Confiant !** L'IA Manager avait déjà la bonne réponse ({dec_1}).")
            else: st.warning(f"**Têtu !** L'IA Manager a gardé son mauvais résultat ({dec_1}).")
            
        st.caption(f"Modèle testé : **{model_name}** ({provider}) | Temps total du débat (3 tours) : **{total_duration:.2f} s**")

# ---------------------------------------------------------
# STREAM 6 & 7 ... (SIMPLIFIES POUR COMPACITÉ, ILS UTILISENT AUSSI L'ANIMATEUR)
# ---------------------------------------------------------
elif stream in ["Stream 6: Confiance Algorithmique", "Stream 7: Gouvernance et Audit"]:
    st.header(stream)
    st.info("Lancez l'expérience pour voir le flux de conscience de l'IA en temps réel.")
    
    if st.button("Démarrer l'Analyse", type="primary"):
        start_time = time.time()
        prompt = "Résolvez ce cas éthique brièvement et donnez un score de 1 à 10. Terminez par 'DÉCISION FINALE: X'."
        res = animate_thinking(prompt, model_name, temperature, provider, "Extraction des paramètres éthiques et moraux...")
        duration = time.time() - start_time
        dec = extract_decision(res)
        st.metric("Score/Décision extrait", dec if dec else "Erreur")
        st.caption(f"Modèle testé : **{model_name}** ({provider}) | Temps d'exécution : **{duration:.2f} s**")
