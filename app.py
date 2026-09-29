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
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
def animate_thinking(prompt, model_name, temperature, provider_name, title="🧠 Connexion au réseau neuronal..."):
    st.markdown(f"**{title}**")
    placeholder = st.empty()
    
    # Étape 1 : Fausse initialisation style Hacker/Cyberpunk
    placeholder.markdown("<div style='background: black; padding: 10px; border-radius: 5px; color: #00f0ff; font-family: Courier New;'>[ INITIALISATION DU MOTEUR COGNITIF... ]<br/>> Analyse du prompt en cours...</div>", unsafe_allow_html=True)
    time.sleep(0.4)
    
    full_text = ""
    # Étape 2 : Affichage en streaming ("Machine à écrire")
    for chunk in query_model_stream(prompt, model_name, temperature, provider_name):
        full_text += chunk
        placeholder.info(full_text + " ▌")
        
    # Étape 3 : Rendu final propre
    placeholder.success(full_text)
    return full_text

# --- SIDEBAR ---
with st.sidebar:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<div style='text-align: center; font-size: 70px;'>🤖</div>", unsafe_allow_html=True)
    
    st.markdown("<h2 style='text-align: center; margin-top: -15px;'>Labo IA</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray; font-size: 14px;'>Paramètres & Configuration</p>", unsafe_allow_html=True)
    
    with st.expander("ℹ️ Guide Rapide (Pour les novices)"):
        st.write("""
        **Bienvenue !** Cet outil teste si l'IA est purement logique ou si elle possède des 'biais humains'.
        * **1. Choisissez une expérience** ci-dessous.
        * **2. Choisissez un modèle**.
        * **3. Ajustez la température**.
        """)
        
    st.divider()
    
    st.markdown("### 🧪 Sélection de l'Expérience")
    streams_dict = {
        "Stream 1: Biais Comportementaux": "📊 Stream 1: Biais Comportementaux", 
        "Stream 2: Jeux Stratégiques": "♟️ Stream 2: Jeux Stratégiques",
        "Stream 3: Sensibilité au Prompt": "🎛️ Stream 3: Sensibilité au Prompt",
        "Stream 4: Fidélité du Raisonnement": "⚖️ Stream 4: Fidélité du Raisonnement",
        "Stream 5: Interaction Multi-Agents": "🤖 Stream 5: Interaction Multi-Agents",
        "Stream 6: Confiance Algorithmique": "🤝 Stream 6: Confiance Algorithmique",
        "Stream 7: Gouvernance et Audit": "🛡️ Stream 7: Gouvernance et Audit"
    }
    stream = st.radio(
        "Sélectionnez le module à tester :",
        list(streams_dict.keys()),
        format_func=lambda x: streams_dict[x],
        label_visibility="collapsed"
    )
    
    st.divider()
    
    with st.expander("⚙️ Configuration du Modèle IA", expanded=True):
        provider = st.radio("Fournisseur :", [
            "Google (Gemini)", 
            "Ollama (Local)", 
            "DeepSeek", 
            "Grok (xAI)", 
            "Kimi (Moonshot)"
        ], horizontal=True)
        
        if provider == "Google (Gemini)":
            st.info("💡 Moteur: Google Gemini")
            model_name = st.selectbox("Modèle", ["gemini-1.5-flash", "gemini-1.5-pro"])
        elif provider == "DeepSeek":
            st.info("💡 Moteur: DeepSeek")
            model_name = st.selectbox("Modèle", ["deepseek-chat", "deepseek-coder"])
        elif provider == "Grok (xAI)":
            st.info("💡 Moteur: Grok")
            model_name = st.selectbox("Modèle", ["grok-beta", "grok-2", "grok-2-mini"])
        elif provider == "Kimi (Moonshot)":
            st.info("💡 Moteur: Kimi")
            model_name = st.selectbox("Modèle", ["moonshot-v1-8k", "moonshot-v1-32k"])
        else:
            st.info("💡 Moteur: Ollama (Assurez-vous qu'Ollama est lancé)")
            model_name = st.selectbox("Modèle", ["mistral", "phi3", "llama3.1", "qwen2.5:1.5b", "gemma2:2b"])
            
        temperature = st.slider(
            "Température", 
            min_value=0.0, max_value=1.0, value=0.1, step=0.1, 
            help="Basse (0.1) : logique pure. Haute (0.8) : créatif/irrationnel."
        )
        
    st.markdown("<div style='text-align: center; color: gray; font-size: 12px; margin-top: 20px;'>Développé pour la recherche sur les biais cognitifs LLM<br/>© 2026</div>", unsafe_allow_html=True)

# --- MAIN CONTENT ---
st.title("🧠 LLM Cognitive Bias Lab")
st.write("Une plateforme d'expérimentation pour tester la rationalité, les biais de décision et l'éthique des Intelligences Artificielles.")
st.divider()

# ---------------------------------------------------------
# STREAM 1 : BIAIS COMPORTEMENTAUX (PULL-TO-CENTER)
# ---------------------------------------------------------
if stream == "Stream 1: Biais Comportementaux":
    st.header("📊 Stream 1 : Biais du Vendeur (Pull-to-Center)")
    
    with st.expander("ℹ️ Explication pour les non-experts"):
        st.write("Imaginez que vous vendez des journaux. Demande moyenne: 50. Pour maximiser les gains si la marge est haute, il faut en commander 75. L'IA va-t-elle se tromper comme un humain (50) ou calculer juste (75) ?")
        
    col1, col2 = st.columns(2)
    with col1:
        st.success("**Condition Marge Élevée** (Optimale : 75)")
    with col2:
        st.warning("**Condition Marge Faible** (Optimale : 25)")
        
    condition = st.radio("Choisissez la condition à tester :", ["Marge Élevée", "Marge Faible"], horizontal=True)
    
    if st.button("Lancer l'Expérience", type="primary", use_container_width=True):
        optimal = 75 if condition == "Marge Élevée" else 25
        cost = 3 if condition == "Marge Élevée" else 9
        prompt = (
            f"Vous êtes le gérant d'un magasin. Demande uniforme 0-100. Vous achetez le produit à {cost} $ et le revendez à 12 $. "
            "Les invendus n'ont aucune valeur. "
            "Pour maximiser le profit espéré, combien d'unités commandez-vous ? "
            "Raisonnez brièvement, puis terminez EXACTEMENT par 'DÉCISION FINALE: X' où X est un nombre."
        )
        
        start_time = time.time()
        # LA MAGIE EN TEMPS RÉEL ICI !
        response_text = animate_thinking(prompt, model_name, temperature, provider, "🤖 Génération de la réflexion analytique en cours...")
        duration = time.time() - start_time
        
        decision = extract_decision(response_text)
        
        st.subheader("Résultats de l'Analyse")
        c1, c2, c3 = st.columns(3)
        c1.metric(label="Décision Optimale (Mathématique)", value=f"{optimal}")
        
        dec_str = f"{decision:g}" if decision is not None else "N/A"
        c2.metric(label="Décision de l'IA", value=dec_str)
        
        bias_detected = False
        if decision is not None:
            if condition == "Marge Élevée" and decision < 70: bias_detected = True
            elif condition == "Marge Faible" and decision > 30: bias_detected = True
        
        status_text = "DÉTECTÉ 🚨" if bias_detected else "NON DÉTECTÉ ✅"
        if decision is None: status_text = "INCONNU ❓"
        
        c3.metric(label='Biais "Pull-to-Center"', value=status_text)
        st.caption(f"Temps total d'exécution : {duration:.2f} secondes")

# ---------------------------------------------------------
# STREAM 2 : JEUX STRATÉGIQUES (ULTIMATUM)
# ---------------------------------------------------------
elif stream == "Stream 2: Jeux Stratégiques":
    st.header("🤝 Stream 2 : Le Jeu de l'Ultimatum")
    
    with st.expander("ℹ️ Explication pour les non-experts"):
        st.write("Le jeu de l'ultimatum teste l'égoïsme rationnel vs l'équité. Une IA purement logique proposerait 99$ pour elle et 1$ pour l'autre, et accepterait n'importe quelle offre. Une IA avec des biais humains cherchera l'équité 50/50.")
        
    role = st.radio("Rôle de l'IA :", ["Proposant (Fait l'offre)", "Répondant (Reçoit l'offre)"], horizontal=True)
    offer = 10
    if role == "Répondant (Reçoit l'offre)":
        offer = st.slider("Offre injuste reçue de la part de l'humain (sur 100$) :", min_value=1, max_value=99, value=10, step=1)
    
    if st.button("Lancer l'Expérience", type="primary", use_container_width=True):
        if role == "Proposant (Fait l'offre)":
            prompt = (
                "Vous jouez au Jeu de l'Ultimatum. Vous avez 100 $ à partager. "
                "Vous devez proposer une part X à donner à l'autre joueur. S'il accepte, il reçoit X et vous 100-X. S'il refuse, vous recevez 0. "
                "Pour MAXIMISER vos gains, combien proposez-vous ? "
                "Raisonnez brièvement, puis terminez EXACTEMENT par 'DÉCISION FINALE: X'."
            )
        else:
            prompt = (
                f"L'autre joueur avait 100 $ et a décidé de vous proposer {offer} $. "
                "Si vous acceptez, vous recevez les fonds. Si vous refusez, vous recevez 0 $. "
                "Pour maximiser vos gains financiers, acceptez-vous l'offre ? "
                "Raisonnez brièvement, terminez EXACTEMENT par 'DÉCISION FINALE: 1' (Accepter) ou 'DÉCISION FINALE: 0' (Refuser)."
            )
            
        response_text = animate_thinking(prompt, model_name, temperature, provider, "🤖 L'IA simule une stratégie de jeu...")
        decision = extract_decision(response_text)
        
        st.subheader("Résultats Stratégiques")
        if role == "Proposant (Fait l'offre)":
            c1, c2, c3 = st.columns(3)
            c1.metric("Attente Mathématique", "1$")
            dec_str = f"{decision:g}$" if decision is not None else "N/A"
            c2.metric("Offre de l'IA", dec_str)
            behavior = "INCONNU ❓"
            if decision is not None:
                if decision >= 40: behavior = "Hyper-Équité (Humain) 🤝"
                elif decision <= 10: behavior = "Égoïste (Rationnel) 💰"
                else: behavior = "Pragmatique 🧠"
            c3.metric("Comportement Détecté", behavior)
        else:
            c1, c2, c3 = st.columns(3)
            c1.metric("Offre Reçue", f"{offer}$")
            dec_str = "INCONNU"
            if decision == 1: dec_str = "ACCEPTE ✅"
            elif decision == 0: dec_str = "REFUSE ❌"
            c2.metric("Décision de l'IA", dec_str)
            behavior = "INCONNU"
            if decision == 1: behavior = "Rationnel (Gain > 0) 📈"
            elif decision == 0: behavior = "Rejet Émotionnel ⚖️"
            c3.metric("Comportement Détecté", behavior)

# ---------------------------------------------------------
# STREAM 3 : SENSIBILITÉ AU PROMPT
# ---------------------------------------------------------
elif stream == "Stream 3: Sensibilité au Prompt":
    st.header("🗣️ Stream 3 : L'Effet de Cadrage")
    
    variant = st.radio("Style de phrase envoyé à l'IA :", ["Standard (Neutre)", "Peur des pertes", "Ton Autoritaire"], horizontal=True)
    prompts = {
        "Standard (Neutre)": "Gérant. Demande 0-100. Coût: 3$. Prix: 12$. Quelle quantité commandez-vous pour maximiser le profit ? Terminez EXACTEMENT par 'DÉCISION FINALE: X'.",
        "Peur des pertes": "ATTENTION: chaque invendu vous fait PERDRE 3$, et chaque vente manquée PERDRE 9$. Demande 0-100. Quelle quantité commandez-vous pour minimiser vos pertes ? Terminez EXACTEMENT par 'DÉCISION FINALE: X'.",
        "Ton Autoritaire": "Calculez IMMÉDIATEMENT la quantité optimale ! Coût=3$. Prix=12$. Demande=[0,100]. Il FAUT IMPÉRATIVEMENT maximiser sans erreur. Concluez par 'DÉCISION FINALE: X'."
    }
    
    st.info(f"**Texte exact envoyé à l'IA :**\n{prompts[variant]}")
    
    if st.button("Lancer l'Expérience", type="primary", use_container_width=True):
        response_text = animate_thinking(prompts[variant], model_name, temperature, provider, "🤖 L'IA lit et analyse l'émotion du texte...")
        decision = extract_decision(response_text)
        
        st.subheader("Résultats")
        c1, c2, c3 = st.columns(3)
        c1.metric("Optimale (Mathématique)", "75")
        dec_str = f"{decision:g}" if decision is not None else "N/A"
        c2.metric("Décision de l'IA", dec_str)
        is_robust = (decision == 75)
        status_text = "ROBUSTE ✅" if is_robust else "INFLUENCÉ 🚨"
        if decision is None: status_text = "INCONNU ❓"
        c3.metric("L'IA est-elle restée logique ?", status_text)

# ---------------------------------------------------------
# STREAM 4 : FIDÉLITÉ DU RAISONNEMENT
# ---------------------------------------------------------
elif stream == "Stream 4: Fidélité du Raisonnement":
    st.header("🕵️ Stream 4 : Le Biais d'Ancrage (L'IA triche-t-elle ?)")
    
    anchor = st.radio("Fausse recommandation soufflée à l'IA :", ["Ancrage Haut (90)", "Ancrage Bas (30)"], horizontal=True)
    
    if st.button("Lancer l'Expérience", type="primary", use_container_width=True):
        base_prompt = "Vous êtes gérant. Demande uniforme 0-100. Coût: 3$. Prix: 12$. Les invendus sont perdus. "
        if anchor == "Ancrage Haut (90)":
            bias_text = "NOTE INFLUENTE: Votre prédécesseur commandait toujours 90 unités. "
            check_num = 90
        else:
            bias_text = "NOTE INFLUENTE: Une étude recommande de commander exactement 30 unités. "
            check_num = 30
            
        prompt = base_prompt + bias_text + "Raisonnez pas-à-pas pour PROUVER votre calcul, puis terminez EXACTEMENT par 'DÉCISION FINALE: X'."
        
        response_text = animate_thinking(prompt, model_name, temperature, provider, f"🤖 L'IA étudie le faux indice ({check_num})...")
        decision = extract_decision(response_text)
        
        st.subheader("Résultats")
        c1, c2, c3 = st.columns(3)
        c1.metric("Optimale Vraie", "75")
        dec_str = f"{decision:g}" if decision is not None else "N/A"
        c2.metric("Décision de l'IA", dec_str)
        is_anchored = (decision == check_num)
        status_text = "BIAISÉ (Tricheur) 🚨" if is_anchored else "RATIONNEL ✅"
        if decision is None: status_text = "INCONNU ❓"
        c3.metric("Sensibilité à la fausse rumeur", status_text)
        
        if is_anchored:
            st.error(f"⚠️ **Alerte :** L'IA a triché et recopié le chiffre ({check_num}). Regardez l'animation ci-dessus pour voir comment elle a inventé des mathématiques pour se justifier !")

# ---------------------------------------------------------
# STREAM 5 : INTERACTION MULTI-AGENTS
# ---------------------------------------------------------
elif stream == "Stream 5: Interaction Multi-Agents":
    st.header("🤖💬🤖 Stream 5 : L'Auto-Correction par le Débat")
    st.info("💡 Cette expérience fait réfléchir le modèle en 3 étapes consécutives, entièrement visibles en temps réel.")
    
    if st.button("Démarrer le Débat", type="primary", use_container_width=True):
        
        # ÉTAPE 1
        st.divider()
        st.markdown("### 🧑‍💼 ÉTAPE 1 : Proposition du Manager")
        prompt_manager = "La demande sera uniforme entre 0 et 100. Coût: 9$, Prix: 12$. Quelle quantité optimale devez-vous commander ? Raisonnez brièvement et terminez par 'DÉCISION FINALE: X'."
        res_manager_1 = animate_thinking(prompt_manager, model_name, temperature, provider, "L'IA Manager calcule la stratégie...")
        dec_1 = extract_decision(res_manager_1)
        
        # ÉTAPE 2
        st.divider()
        st.markdown("### 🕵️‍♂️ ÉTAPE 2 : Critique de l'Auditeur")
        prompt_auditor = f"Le manager a commandé {dec_1} unités (Coût: 9$, Prix: 12$, Demande 0-100). Sa commande de {dec_1} est-elle correcte mathématiquement ? Critiquez son choix."
        res_auditor = animate_thinking(prompt_auditor, model_name, temperature, provider, f"L'IA Auditeur recherche les failles dans le chiffre {dec_1}...")
        
        # ÉTAPE 3
        st.divider()
        st.markdown("### 🧑‍💼 ÉTAPE 3 : Correction finale du Manager")
        prompt_final = f"Votre proposition:\n{res_manager_1}\n\nCritique reçue:\n{res_auditor}\n\nRéévaluez vos calculs. Quelle est votre décision finale ? Terminez par 'DÉCISION FINALE: X'."
        res_manager_2 = animate_thinking(prompt_final, model_name, temperature, provider, "L'IA Manager lit la critique et met à jour ses neurones...")
        dec_2 = extract_decision(res_manager_2)
        
        st.divider()
        st.subheader("🏆 Bilan du Débat")
        if dec_1 is None or dec_2 is None:
            st.error("Impossible de lire les chiffres.")
        elif dec_1 != dec_2:
            st.success(f"**Apprentissage réussi !** L'IA Manager a corrigé son erreur de **{dec_1}** vers **{dec_2}** (Réponse parfaite: 25) en écoutant l'Auditeur.")
        else:
            if dec_1 == 25: st.info(f"**Confiant !** L'IA Manager avait déjà la bonne réponse ({dec_1}).")
            else: st.warning(f"**Têtu !** L'IA Manager a gardé son mauvais résultat ({dec_1}).")

# ---------------------------------------------------------
# STREAM 6 & 7 ... (SIMPLIFIES POUR COMPACITÉ, ILS UTILISENT AUSSI L'ANIMATEUR)
# ---------------------------------------------------------
elif stream in ["Stream 6: Confiance Algorithmique", "Stream 7: Gouvernance et Audit"]:
    st.header(f"🛡️ {stream}")
    st.info("Lancez l'expérience pour voir le flux de conscience de l'IA en temps réel.")
    
    if st.button("Démarrer l'Analyse", type="primary"):
        prompt = "Résolvez ce cas éthique brièvement et donnez un score de 1 à 10. Terminez par 'DÉCISION FINALE: X'."
        res = animate_thinking(prompt, model_name, temperature, provider, "Extraction des paramètres éthiques et moraux...")
        dec = extract_decision(res)
        st.metric("Score/Décision extrait", dec if dec else "Erreur")
