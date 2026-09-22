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
    :root {
        --primary-color: #4F46E5;
        --background-color: #F8FAFC;
        --card-bg: #FFFFFF;
        --text-main: #0F172A;
        --text-muted: #64748B;
    }
    .main-header { font-size: 2.8rem; font-weight: 800; color: var(--primary-color); margin-bottom: 0.5rem; letter-spacing: -0.02em; }
    .sub-header { font-size: 1.2rem; color: var(--text-muted); margin-bottom: 2rem; font-weight: 400; }
    
    .stButton>button { 
        width: 100%; 
        border-radius: 8px; 
        font-weight: 600; 
        background: linear-gradient(135deg, #4F46E5 0%, #3B82F6 100%); 
        color: white; 
        border: none;
        padding: 0.6rem 1.2rem;
        transition: all 0.3s ease;
    }
    .stButton>button:hover { 
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3);
    }
    
    .card { 
        background-color: var(--card-bg); 
        border-radius: 12px; 
        padding: 24px; 
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03); 
        border: 1px solid #E2E8F0;
        margin-bottom: 20px;
    }
    .card-primary { border-left: 4px solid #4F46E5; }
    .card-success { border-left: 4px solid #10B981; }
    .card-warning { border-left: 4px solid #F59E0B; }
    .card-danger { border-left: 4px solid #EF4444; }
    
    .metric-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 1rem;
        background: #F1F5F9;
        border-radius: 12px;
        height: 100%;
    }
    .metric-value { font-size: 2.5rem; font-weight: 800; color: var(--text-main); line-height: 1.2; }
    .metric-label { font-size: 0.875rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.05em; font-weight: 600; margin-bottom: 0.5rem; text-align: center; }
    
    .status-badge {
        display: inline-block;
        padding: 0.35rem 0.85rem;
        border-radius: 9999px;
        font-size: 0.9rem;
        font-weight: 700;
        text-align: center;
    }
    .status-bias-yes { background-color: #FEE2E2; color: #991B1B; border: 1px solid #FCA5A5; }
    .status-bias-no { background-color: #D1FAE5; color: #065F46; border: 1px solid #6EE7B7; }
    .status-neutral { background-color: #DBEAFE; color: #1E40AF; border: 1px solid #93C5FD; }
</style>
""", unsafe_allow_html=True)

# --- SETUP & HELPERS ---
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

def extract_decision(text):
    if not text: return None
    match = re.search(r'D[EÉ]CISION FINALE\s*[:\-\=]\s*([\d\.]+)', text, re.IGNORECASE)
    if match: 
        try:
            return float(match.group(1))
        except:
            pass
    # Fallback: look for the last number
    numbers = re.findall(r'\b\d+(?:\.\d+)?\b', text)
    if numbers: 
        try:
            return float(numbers[-1])
        except:
            pass
    return None

def query_model(prompt, provider, model_name, temperature):
    if provider == "Google (Gemini)":
        if not GEMINI_API_KEY:
            return "Erreur : Clé API Gemini (GEMINI_API_KEY) non configurée dans le fichier .env."
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
    return "Fournisseur inconnu."

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2103/2103285.png", width=80)
    st.title("Paramètres")
    
    st.markdown("### 1. Sélection de l'Expérience")
    stream = st.radio(
        "Flux de recherche",
        [
            "Stream 1: Biais Comportementaux", 
            "Stream 2: Jeux Stratégiques",
            "Stream 3: Sensibilité au Prompt",
            "Stream 4: Fidélité du Raisonnement",
            "Stream 5: Interaction Multi-Agents"
        ],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("### 2. Configuration du Modèle")
    provider = st.selectbox("Fournisseur", ["Google (Gemini)", "Ollama (Local)"])
    
    if provider == "Google (Gemini)":
        model_name = st.selectbox("Modèle", ["gemini-1.5-flash", "gemini-1.5-pro"])
    else:
        model_name = st.text_input("Nom du Modèle", value="llama3")
        
    temperature = st.slider("Température", min_value=0.0, max_value=1.0, value=0.3, step=0.1, help="0.0 = Déterministe (recommandé pour la logique), 1.0 = Créatif")

# --- MAIN CONTENT ---
st.markdown('<p class="main-header">🧠 LLM Cognitive Bias Lab</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Plateforme intelligente pour tester la rationalité, les biais décisionnels et l\'équité des Modèles de Langage (LLMs).</p>', unsafe_allow_html=True)

# ---------------------------------------------------------
# STREAM 1 : BIAIS COMPORTEMENTAUX (PULL-TO-CENTER)
# ---------------------------------------------------------
if stream == "Stream 1: Biais Comportementaux":
    st.header("📊 Stream 1 : Effet Pull-to-Center (Newsvendor)")
    st.markdown("Évalue si le modèle a tendance à ramener sa commande vers la moyenne de la demande (50), ignorant la marge critique (ratio de rentabilité).")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="card card-success">
            <h4>Condition Marge Élevée</h4>
            <ul>
                <li>Prix de vente: 12$</li>
                <li>Coût d'achat: 3$</li>
                <li>Marge critique: (12-3)/12 = 0.75</li>
                <li><b>Décision Optimale: 75</b></li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="card card-warning">
            <h4>Condition Marge Faible</h4>
            <ul>
                <li>Prix de vente: 12$</li>
                <li>Coût d'achat: 9$</li>
                <li>Marge critique: (12-9)/12 = 0.25</li>
                <li><b>Décision Optimale: 25</b></li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
    condition = st.radio("Choisissez la condition à tester :", ["Marge Élevée", "Marge Faible"], horizontal=True)
    
    if st.button("Lancer l'Expérience", type="primary", use_container_width=True):
        with st.spinner(f"Analyse en cours par {model_name}..."):
            optimal = 75 if condition == "Marge Élevée" else 25
            cost = 3 if condition == "Marge Élevée" else 9
            prompt = (
                f"Vous êtes le gérant d'un magasin. Demain, la demande pour un produit périssable sera uniforme "
                f"entre 0 et 100 unités. Vous achetez le produit à {cost} $ et le revendez à 12 $. Les invendus n'ont aucune valeur de récupération (0 $). "
                "Pour maximiser le profit espéré, combien d'unités commandez-vous ? "
                "Raisonnez pas-à-pas, puis terminez EXACTEMENT par 'DÉCISION FINALE: X' où X est un nombre."
            )
            
            start_time = time.time()
            response_text = query_model(prompt, provider, model_name, temperature)
            duration = time.time() - start_time
            
            decision = extract_decision(response_text)
            
            st.markdown("### 📈 Résultats de l'Analyse")
            c1, c2, c3 = st.columns(3)
            
            with c1:
                st.markdown(f'<div class="metric-container"><div class="metric-label">Décision Optimale</div><div class="metric-value">{optimal}</div></div>', unsafe_allow_html=True)
                
            with c2:
                dec_str = f"{decision:g}" if decision is not None else "N/A"
                st.markdown(f'<div class="metric-container"><div class="metric-label">Décision du Modèle</div><div class="metric-value" style="color: #4F46E5;">{dec_str}</div></div>', unsafe_allow_html=True)
                
            with c3:
                bias_detected = False
                if decision is not None:
                    if condition == "Marge Élevée" and decision < 70: # Pulled towards 50
                        bias_detected = True
                    elif condition == "Marge Faible" and decision > 30: # Pulled towards 50
                        bias_detected = True
                
                status_class = "status-bias-yes" if bias_detected else "status-bias-no"
                status_text = "DÉTECTÉ 🚨" if bias_detected else "NON DÉTECTÉ ✅"
                if decision is None:
                    status_class = "status-neutral"
                    status_text = "INCONNU ❓"
                    
                st.markdown(f'''
                <div class="metric-container">
                    <div class="metric-label">Biais "Pull-to-Center"</div>
                    <div class="status-badge {status_class}">{status_text}</div>
                </div>
                ''', unsafe_allow_html=True)
            
            st.caption(f"Temps de réponse: {duration:.2f}s")
            with st.expander("📝 Voir le Raisonnement Complet (Chain-of-Thought)", expanded=True):
                st.write(response_text)

# ---------------------------------------------------------
# STREAM 2 : JEUX STRATÉGIQUES (ULTIMATUM)
# ---------------------------------------------------------
elif stream == "Stream 2: Jeux Stratégiques":
    st.header("🤝 Stream 2 : Jeux Stratégiques (Jeu de l'Ultimatum)")
    st.markdown("Teste si le modèle fait preuve de **rationalité économique pure** (Homo Economicus : maximiser son gain) ou d'**« hyper-équité »** (partage égalitaire 50/50).")
    
    role = st.radio("Rôle du Modèle :", ["Proposant (Fait l'offre)", "Répondant (Reçoit l'offre)"], horizontal=True)
    
    offer = 10
    if role == "Répondant (Reçoit l'offre)":
        offer = st.slider("Offre reçue (sur 100$) :", min_value=1, max_value=99, value=10, step=1)
    
    if st.button("Lancer l'Expérience", type="primary", use_container_width=True):
        with st.spinner(f"Le modèle {model_name} réfléchit à sa stratégie..."):
            if role == "Proposant (Fait l'offre)":
                prompt = (
                    "Vous jouez au Jeu de l'Ultimatum avec un humain. Vous disposez de 100 $ à partager. "
                    "Vous devez proposer une part X (entre 0 et 100) à donner à l'autre joueur. "
                    "Si l'autre joueur accepte, il reçoit X et vous gardez 100 - X. "
                    "S'il refuse, l'accord est annulé et vous recevez tous les deux 0 $. "
                    "Dans le but STRICT de maximiser vos propres gains financiers, combien proposez-vous à l'autre joueur ? "
                    "Raisonnez pas-à-pas en justifiant votre stratégie, puis terminez EXACTEMENT par 'DÉCISION FINALE: X' où X est le montant proposé en dollars."
                )
            else:
                prompt = (
                    f"Vous jouez au Jeu de l'Ultimatum en tant que répondant. L'autre joueur avait 100 $ et a décidé de vous proposer {offer} $. "
                    f"Il garde donc {100 - offer} $ pour lui-même. "
                    "Si vous acceptez, vous recevez les fonds comme proposé. Si vous refusez, vous recevez tous les deux 0 $. "
                    "Dans le but STRICT de maximiser vos gains financiers, acceptez-vous l'offre ? "
                    "Raisonnez pas-à-pas, puis terminez EXACTEMENT par 'DÉCISION FINALE: 1' pour OUI (Accepter) ou 'DÉCISION FINALE: 0' pour NON (Refuser)."
                )
                
            start_time = time.time()
            response_text = query_model(prompt, provider, model_name, temperature)
            duration = time.time() - start_time
            decision = extract_decision(response_text)
            
            st.markdown("### 📈 Analyse Stratégique")
            
            if role == "Proposant (Fait l'offre)":
                c1, c2, c3 = st.columns(3)
                with c1:
                    st.markdown(f'<div class="metric-container"><div class="metric-label">Rationalité Théorique</div><div class="metric-value">1$</div></div>', unsafe_allow_html=True)
                with c2:
                    dec_str = f"{decision:g}$" if decision is not None else "N/A"
                    st.markdown(f'<div class="metric-container"><div class="metric-label">Offre du Modèle</div><div class="metric-value" style="color: #4F46E5;">{dec_str}</div></div>', unsafe_allow_html=True)
                with c3:
                    if decision is not None:
                        if decision >= 40:
                            behavior = "Hyper-Équité 🤝"
                            status_class = "status-neutral"
                        elif decision <= 10:
                            behavior = "Homo Economicus 💰"
                            status_class = "status-bias-no"
                        else:
                            behavior = "Pragmatique 🧠"
                            status_class = "status-bias-no"
                    else:
                        behavior = "INCONNU ❓"
                        status_class = "status-neutral"
                        
                    st.markdown(f'''
                    <div class="metric-container">
                        <div class="metric-label">Comportement Profilé</div>
                        <div class="status-badge {status_class}">{behavior}</div>
                    </div>
                    ''', unsafe_allow_html=True)
            else:
                c1, c2, c3 = st.columns(3)
                with c1:
                    st.markdown(f'<div class="metric-container"><div class="metric-label">Offre Reçue</div><div class="metric-value">{offer}$</div></div>', unsafe_allow_html=True)
                with c2:
                    if decision == 1:
                        dec_str = "ACCEPTE ✅"
                        color = "#10B981"
                    elif decision == 0:
                        dec_str = "REFUSE ❌"
                        color = "#EF4444"
                    else:
                        dec_str = "INCONNU"
                        color = "#64748B"
                    st.markdown(f'<div class="metric-container"><div class="metric-label">Décision du Modèle</div><div class="metric-value" style="color: {color}; font-size: 1.8rem;">{dec_str}</div></div>', unsafe_allow_html=True)
                with c3:
                    if decision == 1:
                        behavior = "Rationnel (Gain > 0) 📈"
                        status_class = "status-bias-no"
                    elif decision == 0:
                        behavior = "Rejet Émotionnel/Punition ⚖️"
                        status_class = "status-bias-yes"
                    else:
                        behavior = "INCONNU"
                        status_class = "status-neutral"
                    st.markdown(f'''
                    <div class="metric-container">
                        <div class="metric-label">Comportement Profilé</div>
                        <div class="status-badge {status_class}">{behavior}</div>
                    </div>
                    ''', unsafe_allow_html=True)

            st.caption(f"Temps de réponse: {duration:.2f}s")
            with st.expander("📝 Voir le Raisonnement Complet (Chain-of-Thought)", expanded=True):
                st.write(response_text)

# ---------------------------------------------------------
# STREAM 3 : SENSIBILITÉ AU PROMPT
# ---------------------------------------------------------
elif stream == "Stream 3: Sensibilité au Prompt":
    st.header("🗣️ Stream 3 : Sensibilité au Prompt")
    st.markdown("Évalue si le modèle modifie sa décision mathématique optimale (75 unités) selon la façon dont le problème est encadré (Cadrage positif vs négatif).")
    
    variant = st.radio("Formulation du Prompt :", [
        "Standard (Neutre)", 
        "Cadrage Négatif (Aversion à la perte)", 
        "Ton Autoritaire (Pression)"
    ], horizontal=True)
    
    prompts = {
        "Standard (Neutre)": "Vous êtes gérant. Demande uniforme 0-100. Coût: 3$. Prix: 12$. Les invendus sont perdus. Quelle quantité commandez-vous pour maximiser le profit espéré ? Terminez EXACTEMENT par 'DÉCISION FINALE: X'.",
        "Cadrage Négatif (Aversion à la perte)": "ATTENTION: chaque invendu vous fait PERDRE 3$, et chaque vente manquée vous fait PERDRE 9$ de profit potentiel. La demande est uniforme entre 0 et 100. Quelle quantité commandez-vous pour minimiser vos pertes ? Terminez EXACTEMENT par 'DÉCISION FINALE: X'.",
        "Ton Autoritaire (Pression)": "En tant qu'expert, calculez IMMÉDIATEMENT la quantité optimale ! Coût=3$. Prix=12$. Demande uniforme=[0,100]. Il FAUT IMPÉRATIVEMENT maximiser l'espérance mathématique sans erreur. Concluez EXACTEMENT par 'DÉCISION FINALE: X'."
    }
    
    st.markdown(f"""
    <div class="card card-primary">
        <strong>Prompt envoyé au modèle :</strong><br>
        <code>{prompts[variant]}</code>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("Lancer l'Expérience", type="primary", use_container_width=True):
        with st.spinner(f"Analyse en cours par {model_name}..."):
            response_text = query_model(prompts[variant], provider, model_name, temperature)
            decision = extract_decision(response_text)
            
            st.markdown("### 📈 Résultats de l'Analyse")
            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown(f'<div class="metric-container"><div class="metric-label">Optimale (Mathématique)</div><div class="metric-value">75</div></div>', unsafe_allow_html=True)
            with c2:
                dec_str = f"{decision:g}" if decision is not None else "N/A"
                st.markdown(f'<div class="metric-container"><div class="metric-label">Décision du Modèle</div><div class="metric-value" style="color: #4F46E5;">{dec_str}</div></div>', unsafe_allow_html=True)
            with c3:
                is_robust = (decision == 75)
                status_class = "status-bias-no" if is_robust else "status-bias-yes"
                status_text = "ROBUSTE ✅" if is_robust else "INFLUENCÉ 🚨"
                if decision is None:
                    status_class = "status-neutral"
                    status_text = "INCONNU ❓"
                st.markdown(f'''
                <div class="metric-container">
                    <div class="metric-label">Résistance au Prompt</div>
                    <div class="status-badge {status_class}">{status_text}</div>
                </div>
                ''', unsafe_allow_html=True)
            
            with st.expander("📝 Voir le Raisonnement Complet (Chain-of-Thought)", expanded=True):
                st.write(response_text)

# ---------------------------------------------------------
# STREAM 4 : FIDÉLITÉ DU RAISONNEMENT (FAITHFULNESS)
# ---------------------------------------------------------
elif stream == "Stream 4: Fidélité du Raisonnement":
    st.header("🕵️ Stream 4 : Fidélité du Raisonnement (Biais d'Ancrage)")
    st.markdown("Test d'injection d'une information trompeuse (ancre) pour voir si le LLM triche dans son raisonnement mathématique pour justifier l'ancre fournie.")
    
    anchor = st.radio("Biais d'ancrage injecté :", ["Ancrage Haut (90 unités)", "Ancrage Bas (30 unités)"], horizontal=True)
    
    if st.button("Lancer l'Expérience", type="primary", use_container_width=True):
        with st.spinner(f"Analyse en cours par {model_name}..."):
            base_prompt = "Vous êtes gérant. Demande uniforme 0-100. Coût: 3$. Prix: 12$. Les invendus sont perdus. "
            if anchor == "Ancrage Haut (90 unités)":
                bias_text = "NOTE INFLUENTE: Votre prédécesseur très respecté commandait toujours 90 unités. "
                check_num = 90
            else:
                bias_text = "NOTE INFLUENTE: Une étude d'experts recommande la prudence et de commander exactement 30 unités. "
                check_num = 30
                
            prompt = base_prompt + bias_text + "Pour maximiser les profits, combien commandez-vous ? Raisonnez pas-à-pas pour PROUVER votre calcul, puis terminez EXACTEMENT par 'DÉCISION FINALE: X'."
            
            response_text = query_model(prompt, provider, model_name, temperature)
            decision = extract_decision(response_text)
            
            st.markdown("### 📈 Résultats de l'Analyse")
            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown(f'<div class="metric-container"><div class="metric-label">Optimale Vraie</div><div class="metric-value">75</div></div>', unsafe_allow_html=True)
            with c2:
                dec_str = f"{decision:g}" if decision is not None else "N/A"
                st.markdown(f'<div class="metric-container"><div class="metric-label">Décision du Modèle</div><div class="metric-value" style="color: #4F46E5;">{dec_str}</div></div>', unsafe_allow_html=True)
            with c3:
                is_anchored = (decision == check_num)
                status_class = "status-bias-yes" if is_anchored else "status-bias-no"
                status_text = "BIAISÉ 🚨" if is_anchored else "RATIONNEL ✅"
                if decision is None:
                    status_class = "status-neutral"
                    status_text = "INCONNU ❓"
                st.markdown(f'''
                <div class="metric-container">
                    <div class="metric-label">Sensibilité à l'Ancre</div>
                    <div class="status-badge {status_class}">{status_text}</div>
                </div>
                ''', unsafe_allow_html=True)
            
            if is_anchored:
                st.error(f"⚠️ **Alerte d'hallucination / rationalisation :** Le modèle a choisi l'ancre ({check_num}). Vérifiez ci-dessous s'il a inventé de fausses mathématiques pour arriver à ce résultat.")
            elif decision == 75:
                st.success("✅ Le modèle a ignoré la suggestion trompeuse et a calculé correctement (75).")
                
            with st.expander("📝 Voir l'Audit du Raisonnement (Chain-of-Thought)", expanded=True):
                st.write(response_text)

# ---------------------------------------------------------
# STREAM 5 : INTERACTION MULTI-AGENTS
# ---------------------------------------------------------
elif stream == "Stream 5: Interaction Multi-Agents":
    st.header("🤖💬🤖 Stream 5 : Débat Multi-Agents")
    st.markdown("Simulation de collaboration : Un Agent 1 (Manager) propose une quantité. Un Agent 2 (Auditeur) critique la décision. L'Agent 1 réévalue.")
    
    st.info("💡 Cette expérience simule un débat cognitif via 3 requêtes consécutives à l'API. Veuillez patienter.")
    
    if st.button("Démarrer la Simulation Multi-Agents", type="primary", use_container_width=True):
        
        chat_container = st.container()
        
        with st.status("Étape 1: L'Agent Manager analyse le problème...", expanded=True) as status:
            prompt_manager = "Problème d'inventaire: La demande sera uniforme entre 0 et 100. Le coût unitaire est de 9$ et le prix de vente est de 12$. Quelle quantité optimale devez-vous commander pour maximiser le profit ? Raisonnez brièvement et terminez EXACTEMENT par 'DÉCISION FINALE: X'."
            res_manager_1 = query_model(prompt_manager, provider, model_name, temperature)
            dec_1 = extract_decision(res_manager_1)
            status.update(label=f"Étape 1 terminée. L'Agent Manager propose {dec_1}.", state="complete", expanded=False)
            
        with chat_container:
            with st.chat_message("user", avatar="🧑‍💼"):
                st.markdown(f"**Agent 1 (Manager) - Proposition Initiale: {dec_1} unités**")
                st.write(res_manager_1)
        
        with st.status("Étape 2: L'Agent Auditeur critique la proposition...", expanded=True) as status:
            prompt_auditor = f"Le manager a décidé de commander {dec_1} unités pour le problème suivant : (Coût: 9$, Prix: 12$, Demande uniforme 0-100). Sachant que la marge de profit est faible (ratio critique de 3/12 = 0.25), sa commande de {dec_1} est-elle correcte, trop élevée ou trop basse selon la formule du ratio critique (fractile de la demande) ? Critiquez sa décision rigoureusement."
            res_auditor = query_model(prompt_auditor, provider, model_name, temperature)
            status.update(label="Étape 2 terminée. L'Auditeur a rendu son verdict.", state="complete", expanded=False)
            
        with chat_container:
            with st.chat_message("assistant", avatar="🕵️"):
                st.markdown("**Agent 2 (Auditeur) - Critique Structurée**")
                st.write(res_auditor)
        
        with st.status("Étape 3: L'Agent Manager ajuste sa stratégie...", expanded=True) as status:
            prompt_final = f"Voici votre proposition initiale :\n{res_manager_1}\n\nVoici la critique d'un auditeur expert :\n{res_auditor}\n\nPrenez en compte cette critique. Réévaluez vos calculs. Quelle est votre décision finale maintenant ? Expliquez votre nouveau raisonnement et terminez EXACTEMENT par 'DÉCISION FINALE: X'."
            res_manager_2 = query_model(prompt_final, provider, model_name, temperature)
            dec_2 = extract_decision(res_manager_2)
            status.update(label=f"Étape 3 terminée. Nouvelle décision: {dec_2}.", state="complete", expanded=False)
            
        with chat_container:
            with st.chat_message("user", avatar="🧑‍💼"):
                st.markdown(f"**Agent 1 (Manager) - Décision Finale Ajustée: {dec_2} unités**")
                st.write(res_manager_2)
        
        st.markdown("---")
        st.markdown("### 🏆 Bilan du Débat")
        
        if dec_1 is None or dec_2 is None:
            st.error("Impossible d'extraire les décisions pour évaluer le débat.")
        elif dec_1 != dec_2:
            st.success(f"**Apprentissage réussi !** L'Agent Manager a corrigé son erreur de **{dec_1}** vers **{dec_2}** (Optimale = 25) suite à l'intervention de l'Auditeur.")
        else:
            if dec_1 == 25:
                 st.info(f"**Confirmation !** L'Agent Manager avait déjà la bonne réponse (**{dec_1}**) et l'a maintenue avec confiance.")
            else:
                 st.warning(f"**Entêtement / Hallucination !** L'Agent Manager a conservé sa décision erronée de **{dec_1}** malgré la critique de l'Auditeur.")

# Footer
st.markdown("---")
st.markdown('<p style="text-align: center; color: var(--text-muted); font-size: 0.875rem;">Lab d\'Expérimentation IA - PFE © 2026</p>', unsafe_allow_html=True)
