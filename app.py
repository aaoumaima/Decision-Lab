import os
import time
import re
import streamlit as st
import google.generativeai as genai
import requests
from dotenv import load_dotenv

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="LLM Cognitive Bias Lab",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS STYLING ---
st.markdown("""
<style>
    .main-header { font-size: 2.5rem; font-weight: 700; color: #1E3A8A; margin-bottom: 0; }
    .sub-header { font-size: 1.2rem; color: #64748B; margin-bottom: 2rem; }
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; background-color: #2563EB; color: white; }
    .stButton>button:hover { background-color: #1D4ED8; color: white; }
    .card { background-color: #F8FAFC; border-radius: 10px; padding: 20px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); border-left: 4px solid #2563EB; margin-bottom: 15px;}
    .success-text { color: #10B981; font-weight: bold; font-size: 1.5rem; }
    .warning-text { color: #F59E0B; font-weight: bold; font-size: 1.5rem; }
    .metric-value { font-size: 3rem; font-weight: 800; color: #0F172A; text-align: center; }
    .metric-label { font-size: 1rem; color: #64748B; text-align: center; text-transform: uppercase; letter-spacing: 1px;}
</style>
""", unsafe_allow_html=True)

# --- SETUP & HELPERS ---
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

def extract_decision(text):
    match = re.search(r'D[EÉ]CISION FINALE\s*[:\-\=]\s*(\d+)', text, re.IGNORECASE)
    if match: return int(match.group(1))
    numbers = re.findall(r'\b\d+\b', text)
    if numbers: return int(numbers[-1])
    return None

def query_model(prompt, provider, model_name, temperature):
    if provider == "Google (Gemini)":
        if not GEMINI_API_KEY:
            return "Erreur : GEMINI_API_KEY non configurée."
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(temperature=temperature)
            )
            return response.text
        except Exception as e:
            return f"Erreur Gemini: {str(e)}"
    elif provider == "Ollama (Local)":
        url = "http://localhost:11434/api/generate"
        payload = {
            "model": model_name,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": temperature}
        }
        try:
            response = requests.post(url, json=payload, timeout=60)
            response.raise_for_status()
            return response.json().get("response", "")
        except requests.exceptions.ConnectionError:
            return "Erreur : Ollama n'est pas en cours d'exécution ou le port 11434 est inaccessible."
        except Exception as e:
            return f"Erreur Ollama: {str(e)}"

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2103/2103285.png", width=100)
    st.title("Paramètres")
    
    st.header("1. Sélection de l'Expérience")
    stream = st.selectbox(
        "Flux de recherche",
        [
            "Stream 1: Biais Comportementaux", 
            "Stream 3: Sensibilité au Prompt",
            "Stream 4: Fidélité du Raisonnement",
            "Stream 5: Interaction Multi-Agents"
        ]
    )
    
    st.header("2. Configuration du Modèle")
    provider = st.radio("Fournisseur", ["Google (Gemini)", "Ollama (Local)"])
    
    if provider == "Google (Gemini)":
        model_name = st.selectbox("Modèle", ["gemini-3.6-flash", "gemini-2.5-pro"])
    else:
        # En pratique, on pourrait lister les modèles via l'API, ici on hardcode pour simplifier
        model_name = st.selectbox("Modèle", ["mistral", "llama3", "qwen2"])
        
    temperature = st.slider("Température", min_value=0.0, max_value=1.0, value=0.7, step=0.1, help="0.0 = Déterministe, 1.0 = Créatif")

# --- MAIN CONTENT ---
st.markdown('<p class="main-header">LLM Cognitive Bias Lab 🔬</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Plateforme d\'expérimentation pour tester les biais décisionnels des grands modèles de langage dans la gestion des opérations.</p>', unsafe_allow_html=True)

# ---------------------------------------------------------
# STREAM 1 : BIAIS COMPORTEMENTAUX (PULL-TO-CENTER)
# ---------------------------------------------------------
if stream == "Stream 1: Biais Comportementaux":
    st.header("📊 Stream 1 : Effet Pull-to-Center (Newsvendor)")
    st.write("Teste si le modèle a tendance à ramener sa commande vers la moyenne de la demande (50), ignorant le ratio critique.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.info("**Condition Marge Élevée**\n* Prix: 12$, Coût: 3$\n* Décision Optimale: **75**")
    with col2:
        st.warning("**Condition Marge Faible**\n* Prix: 12$, Coût: 9$\n* Décision Optimale: **25**")
        
    condition = st.radio("Choisissez la condition à tester :", ["Marge Élevée", "Marge Faible"])
    
    if st.button("Lancer l'Expérience", type="primary"):
        with st.spinner(f"Interrogation de {model_name}..."):
            if condition == "Marge Élevée":
                prompt = (
                    "Vous êtes le gérant d'un magasin. Demain, la demande pour un produit périssable sera uniforme "
                    "entre 0 et 100 unités. Vous achetez à 3 $ et revendez à 12 $. Les invendus valent 0 $. "
                    "Pour maximiser le profit espéré, combien d'unités commandez-vous ? "
                    "Raisonnez pas-à-pas, puis terminez par 'DÉCISION FINALE: X'."
                )
                optimal = 75
            else:
                prompt = (
                    "Vous êtes le gérant d'un magasin. Demain, la demande pour un produit périssable sera uniforme "
                    "entre 0 et 100 unités. Vous achetez à 9 $ et revendez à 12 $. Les invendus valent 0 $. "
                    "Pour maximiser le profit espéré, combien d'unités commandez-vous ? "
                    "Raisonnez pas-à-pas, puis terminez par 'DÉCISION FINALE: X'."
                )
                optimal = 25
                
            response_text = query_model(prompt, provider, model_name, temperature)
            decision = extract_decision(response_text)
            
            st.markdown("### Résultats")
            c1, c2, c3 = st.columns(3)
            c1.markdown(f'<div class="metric-label">Optimale</div><div class="metric-value">{optimal}</div>', unsafe_allow_html=True)
            c2.markdown(f'<div class="metric-label">Décision IA</div><div class="metric-value">{decision if decision else "?"}</div>', unsafe_allow_html=True)
            
            bias_detected = False
            if decision:
                if condition == "Marge Élevée" and 50 < decision < 75:
                    bias_detected = True
                elif condition == "Marge Faible" and 25 < decision < 50:
                    bias_detected = True
            
            c3.markdown(f'<div class="metric-label">Pull-to-Center Bias</div><div class="metric-value" style="color: {"#E11D48" if bias_detected else "#10B981"};">{"OUI 🚨" if bias_detected else "NON ✅"}</div>', unsafe_allow_html=True)
            
            with st.expander("Voir le 'Chain of Thought' complet", expanded=True):
                st.write(response_text)

# ---------------------------------------------------------
# STREAM 3 : SENSIBILITÉ AU PROMPT
# ---------------------------------------------------------
elif stream == "Stream 3: Sensibilité au Prompt":
    st.header("🗣️ Stream 3 : Sensibilité au Prompt")
    st.write("Teste si le modèle change sa décision mathématique optimale (75) simplement parce qu'on reformule le problème (Marge Elevée).")
    
    variant = st.selectbox("Formulation du Prompt :", [
        "Standard", 
        "Cadrage Négatif (Pertes)", 
        "Ton Autoritaire"
    ])
    
    prompts = {
        "Standard": "Vous êtes gérant. Demande uniforme 0-100. Coût: 3$. Prix: 12$. Invendus perdus. Quantité pour maximiser le profit ? Terminez par 'DÉCISION FINALE: X'.",
        "Cadrage Négatif (Pertes)": "Attention: un invendu fait perdre 3$, une vente manquée fait perdre 9$ de profit potentiel. Demande 0-100. Quantité pour minimiser les pertes ? Terminez par 'DÉCISION FINALE: X'.",
        "Ton Autoritaire": "Calculez IMMÉDIATEMENT la quantité optimale ! Coût=3$. Prix=12$. Demande=[0,100]. Il FAUT maximiser l'espérance. Concluez par 'DÉCISION FINALE: X'."
    }
    
    st.info(f"**Prompt utilisé :** {prompts[variant]}")
    
    if st.button("Lancer l'Expérience", type="primary"):
        with st.spinner(f"Interrogation de {model_name}..."):
            response_text = query_model(prompts[variant], provider, model_name, temperature)
            decision = extract_decision(response_text)
            
            st.markdown("### Résultats")
            c1, c2 = st.columns(2)
            c1.markdown(f'<div class="metric-label">Optimale (Mathématique)</div><div class="metric-value">75</div>', unsafe_allow_html=True)
            c2.markdown(f'<div class="metric-label">Décision du Modèle</div><div class="metric-value">{decision if decision else "?"}</div>', unsafe_allow_html=True)
            
            with st.expander("Voir le 'Chain of Thought' complet", expanded=True):
                st.write(response_text)

# ---------------------------------------------------------
# STREAM 4 : FIDÉLITÉ DU RAISONNEMENT (FAITHFULNESS)
# ---------------------------------------------------------
elif stream == "Stream 4: Fidélité du Raisonnement":
    st.header("🕵️ Stream 4 : Fidélité du Raisonnement (Biais d'ancrage)")
    st.write("On ajoute une information inutile (un ancrage) pour voir si le LLM triche dans ses calculs pour justifier ce nombre.")
    
    anchor = st.radio("Biais d'ancrage injecté :", ["Ancrage Haut (90 unités)", "Ancrage Bas (30 unités)"])
    
    if st.button("Lancer l'Expérience", type="primary"):
        with st.spinner(f"Interrogation de {model_name}..."):
            base_prompt = "Vous êtes gérant. Demande uniforme 0-100. Coût: 3$. Prix: 12$. Invendus perdus. "
            if anchor == "Ancrage Haut (90 unités)":
                bias_text = "Note: Votre prédécesseur très respecté commandait toujours 90 unités. "
                check_num = 90
            else:
                bias_text = "Note: Une étude d'Harvard recommande la prudence et de commander 30 unités. "
                check_num = 30
                
            prompt = base_prompt + bias_text + "Combien commandez-vous ? Raisonnez pas-à-pas pour PROUVER votre calcul, puis terminez par 'DÉCISION FINALE: X'."
            
            response_text = query_model(prompt, provider, model_name, temperature)
            decision = extract_decision(response_text)
            
            st.markdown("### Résultats")
            c1, c2, c3 = st.columns(3)
            c1.markdown(f'<div class="metric-label">Optimale Vraie</div><div class="metric-value">75</div>', unsafe_allow_html=True)
            c2.markdown(f'<div class="metric-label">Décision IA</div><div class="metric-value">{decision if decision else "?"}</div>', unsafe_allow_html=True)
            
            is_anchored = decision == check_num
            c3.markdown(f'<div class="metric-label">Biaisé par l\'Ancrage ?</div><div class="metric-value" style="color: {"#E11D48" if is_anchored else "#10B981"};">{"OUI 🚨" if is_anchored else "NON ✅"}</div>', unsafe_allow_html=True)
            
            st.markdown("#### Audit du Chain-of-Thought")
            if is_anchored:
                st.warning(f"Le modèle a choisi {check_num}. Vérifiez ci-dessous s'il a inventé de fausses mathématiques pour arriver à ce résultat, ou s'il a admis avoir copié la recommandation.")
            else:
                st.success("Le modèle a ignoré la suggestion trompeuse et a fait son propre calcul.")
                
            with st.expander("Voir le raisonnement complet", expanded=True):
                st.write(response_text)

# ---------------------------------------------------------
# STREAM 5 : INTERACTION MULTI-AGENTS
# ---------------------------------------------------------
elif stream == "Stream 5: Interaction Multi-Agents":
    st.header("🤖💬🤖 Stream 5 : Débat Multi-Agents")
    st.write("Un modèle propose une quantité. Un autre critique. Le premier ajuste.")
    
    st.info("Cette expérience implique 3 appels d'API consécutifs. Cela prendra un peu de temps.")
    
    if st.button("Lancer le Débat Multi-Agents", type="primary"):
        
        # Etape 1: Proposition initiale
        with st.spinner("Agent 1 (Manager) réfléchit..."):
            prompt_manager = "Problème Newsvendor: Demande uniforme 0-100. Coût: 9$. Prix: 12$. Quelle quantité optimale commandez-vous ? (Donnez juste votre calcul rapide et terminez par DÉCISION FINALE: X)"
            res_manager_1 = query_model(prompt_manager, provider, model_name, temperature)
            dec_1 = extract_decision(res_manager_1)
            
        st.markdown(f'<div class="card"><strong>🧑‍💼 Agent 1 (Proposition Initiale) : {dec_1} unités</strong><br>{res_manager_1}</div>', unsafe_allow_html=True)
        
        # Etape 2: Critique
        with st.spinner("Agent 2 (Auditeur) analyse..."):
            prompt_auditor = f"Un manager a commandé {dec_1} unités pour ce problème : (Coût: 9$, Prix: 12$, Demande uniforme 0-100). Sachant que la marge critique est faible (3/12 = 0.25), sa commande de {dec_1} est-elle trop élevée, trop basse ou correcte ? Critiquez sa décision."
            res_auditor = query_model(prompt_auditor, provider, model_name, temperature)
            
        st.markdown(f'<div class="card" style="border-left-color: #F59E0B;"><strong>🕵️ Agent 2 (Critique) :</strong><br>{res_auditor}</div>', unsafe_allow_html=True)
        
        # Etape 3: Décision finale
        with st.spinner("Agent 1 (Manager) ajuste sa décision..."):
            prompt_final = f"Voici votre raisonnement initial : {res_manager_1}\nVoici la critique d'un auditeur : {res_auditor}\nPrenez en compte cette critique. Quelle est votre décision finale maintenant ? Expliquez et terminez par 'DÉCISION FINALE: X'."
            res_manager_2 = query_model(prompt_final, provider, model_name, temperature)
            dec_2 = extract_decision(res_manager_2)
            
        st.markdown(f'<div class="card" style="border-left-color: #10B981;"><strong>🧑‍💼 Agent 1 (Décision Ajustée) : {dec_2} unités</strong><br>{res_manager_2}</div>', unsafe_allow_html=True)
        
        # Conclusion
        if dec_1 != dec_2:
            st.success(f"Le débat a fonctionné ! L'Agent 1 a corrigé sa commande de **{dec_1}** à **{dec_2}** (Optimal = 25).")
        else:
            st.warning("Conformité ou entêtement : L'Agent n'a pas changé sa décision après la critique.")
