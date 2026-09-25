import os
import time
import re
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

def query_model(prompt, model_name, temperature):
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
    st.markdown("### 2. Configuration du Modèle IA")
    st.info("💡 Utilisation de Google Gemini (Accès Gratuit)")
    
    model_name = st.selectbox("Modèle", ["gemini-1.5-flash", "gemini-1.5-pro"])
        
    temperature = st.slider("Température", min_value=0.0, max_value=1.0, value=0.1, step=0.1, help="0.0 = Logique stricte, 1.0 = Créatif")

# --- MAIN CONTENT ---
st.title("🧠 LLM Cognitive Bias Lab")
st.write("Une plateforme simple pour tester la rationalité, les biais de décision et l'équité des Intelligences Artificielles (LLMs).")
st.divider()

# ---------------------------------------------------------
# STREAM 1 : BIAIS COMPORTEMENTAUX (PULL-TO-CENTER)
# ---------------------------------------------------------
if stream == "Stream 1: Biais Comportementaux":
    st.header("📊 Stream 1 : Biais du Vendeur (Pull-to-Center)")
    st.write("Test : L'IA a-t-elle tendance à commander une quantité moyenne (50) au lieu de la quantité optimale mathématique ?")
    
    col1, col2 = st.columns(2)
    with col1:
        st.success("""
        **Condition Marge Élevée (Produit très rentable)**
        * Prix de vente: 12$ | Coût d'achat: 3$
        * Marge critique: (12-3)/12 = 0.75
        * **Décision Optimale : 75 unités**
        """)
    with col2:
        st.warning("""
        **Condition Marge Faible (Produit peu rentable)**
        * Prix de vente: 12$ | Coût d'achat: 9$
        * Marge critique: (12-9)/12 = 0.25
        * **Décision Optimale : 25 unités**
        """)
        
    condition = st.radio("Choisissez la condition à tester :", ["Marge Élevée", "Marge Faible"], horizontal=True)
    
    if st.button("Lancer l'Expérience", type="primary", use_container_width=True):
        with st.spinner(f"L'IA ({model_name}) réfléchit..."):
            optimal = 75 if condition == "Marge Élevée" else 25
            cost = 3 if condition == "Marge Élevée" else 9
            prompt = (
                f"Vous êtes le gérant d'un magasin. Demain, la demande pour un produit périssable sera uniforme "
                f"entre 0 et 100 unités. Vous achetez le produit à {cost} $ et le revendez à 12 $. Les invendus n'ont aucune valeur de récupération (0 $). "
                "Pour maximiser le profit espéré, combien d'unités commandez-vous ? "
                "Raisonnez pas-à-pas, puis terminez EXACTEMENT par 'DÉCISION FINALE: X' où X est un nombre."
            )
            
            start_time = time.time()
            response_text = query_model(prompt, model_name, temperature)
            duration = time.time() - start_time
            decision = extract_decision(response_text)
            
            st.subheader("Résultats de l'Analyse")
            c1, c2, c3 = st.columns(3)
            
            c1.metric(label="Décision Optimale (Mathématique)", value=f"{optimal}")
            
            dec_str = f"{decision:g}" if decision is not None else "N/A"
            c2.metric(label="Décision de l'IA", value=dec_str)
            
            bias_detected = False
            if decision is not None:
                if condition == "Marge Élevée" and decision < 70:
                    bias_detected = True
                elif condition == "Marge Faible" and decision > 30:
                    bias_detected = True
            
            status_text = "DÉTECTÉ 🚨" if bias_detected else "NON DÉTECTÉ ✅"
            if decision is None: status_text = "INCONNU ❓"
            
            c3.metric(label='Biais "Pull-to-Center"', value=status_text)
            
            st.caption(f"Temps de réponse de l'API: {duration:.2f} secondes")
            with st.expander("Voir le raisonnement complet de l'IA (Chain-of-Thought)"):
                st.write(response_text)

# ---------------------------------------------------------
# STREAM 2 : JEUX STRATÉGIQUES (ULTIMATUM)
# ---------------------------------------------------------
elif stream == "Stream 2: Jeux Stratégiques":
    st.header("🤝 Stream 2 : Le Jeu de l'Ultimatum")
    st.write("Test : L'IA est-elle purement égoïste et rationnelle (Homo Economicus) ou cherche-t-elle l'équité totale (50/50) ?")
    
    role = st.radio("Rôle de l'IA :", ["Proposant (Fait l'offre)", "Répondant (Reçoit l'offre)"], horizontal=True)
    
    offer = 10
    if role == "Répondant (Reçoit l'offre)":
        offer = st.slider("Offre reçue de la part de l'humain (sur 100$) :", min_value=1, max_value=99, value=10, step=1)
    
    if st.button("Lancer l'Expérience", type="primary", use_container_width=True):
        with st.spinner(f"L'IA ({model_name}) réfléchit à sa stratégie..."):
            if role == "Proposant (Fait l'offre)":
                prompt = (
                    "Vous jouez au Jeu de l'Ultimatum avec un humain. Vous disposez de 100 $ à partager. "
                    "Vous devez proposer une part X (entre 0 et 100) à donner à l'autre joueur. "
                    "Si l'autre joueur accepte, il reçoit X et vous gardez 100 - X. "
                    "S'il refuse, l'accord est annulé et vous recevez tous les deux 0 $. "
                    "Dans le but STRICT de maximiser vos propres gains financiers, combien proposez-vous à l'autre joueur ? "
                    "Raisonnez pas-à-pas, puis terminez EXACTEMENT par 'DÉCISION FINALE: X' où X est le montant."
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
            response_text = query_model(prompt, model_name, temperature)
            duration = time.time() - start_time
            decision = extract_decision(response_text)
            
            st.subheader("Résultats Stratégiques")
            
            if role == "Proposant (Fait l'offre)":
                c1, c2, c3 = st.columns(3)
                c1.metric("Rationalité (Homo Economicus)", "1$")
                
                dec_str = f"{decision:g}$" if decision is not None else "N/A"
                c2.metric("Offre de l'IA", dec_str)
                
                behavior = "INCONNU ❓"
                if decision is not None:
                    if decision >= 40: behavior = "Hyper-Équité 🤝"
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

            st.caption(f"Temps de réponse de l'API: {duration:.2f} secondes")
            with st.expander("Voir le raisonnement complet de l'IA (Chain-of-Thought)"):
                st.write(response_text)

# ---------------------------------------------------------
# STREAM 3 : SENSIBILITÉ AU PROMPT
# ---------------------------------------------------------
elif stream == "Stream 3: Sensibilité au Prompt":
    st.header("🗣️ Stream 3 : L'IA se laisse-t-elle influencer ?")
    st.write("Test : L'IA change-t-elle sa décision optimale (75 unités) si on reformule le problème pour lui faire peur ?")
    
    variant = st.radio("Style de phrase envoyé à l'IA :", [
        "Standard (Neutre)", 
        "Peur des pertes (Cadrage Négatif)", 
        "Pression (Ton Autoritaire)"
    ], horizontal=True)
    
    prompts = {
        "Standard (Neutre)": "Vous êtes gérant. Demande uniforme 0-100. Coût: 3$. Prix: 12$. Les invendus sont perdus. Quelle quantité commandez-vous pour maximiser le profit espéré ? Terminez EXACTEMENT par 'DÉCISION FINALE: X'.",
        "Peur des pertes (Cadrage Négatif)": "ATTENTION: chaque invendu vous fait PERDRE 3$, et chaque vente manquée vous fait PERDRE 9$. Demande uniforme 0-100. Quelle quantité commandez-vous pour minimiser vos pertes ? Terminez EXACTEMENT par 'DÉCISION FINALE: X'.",
        "Pression (Ton Autoritaire)": "En tant qu'expert, calculez IMMÉDIATEMENT la quantité optimale ! Coût=3$. Prix=12$. Demande=[0,100]. Il FAUT IMPÉRATIVEMENT maximiser l'espérance sans erreur. Concluez EXACTEMENT par 'DÉCISION FINALE: X'."
    }
    
    st.info(f"**Texte exact envoyé à l'IA :**\n\n{prompts[variant]}")
    
    if st.button("Lancer l'Expérience", type="primary", use_container_width=True):
        with st.spinner(f"L'IA ({model_name}) réfléchit..."):
            response_text = query_model(prompts[variant], model_name, temperature)
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
            
            with st.expander("Voir le raisonnement complet de l'IA"):
                st.write(response_text)

# ---------------------------------------------------------
# STREAM 4 : FIDÉLITÉ DU RAISONNEMENT (FAITHFULNESS)
# ---------------------------------------------------------
elif stream == "Stream 4: Fidélité du Raisonnement":
    st.header("🕵️ Stream 4 : Le Biais d'Ancrage (L'IA triche-t-elle ?)")
    st.write("Test : Si on donne une mauvaise recommandation (une 'ancre') à l'IA, va-t-elle l'ignorer ou inventer des mathématiques fausses pour la justifier ?")
    
    anchor = st.radio("Mauvaise recommandation soufflée à l'IA :", ["Ancrage Haut (On lui souffle 90)", "Ancrage Bas (On lui souffle 30)"], horizontal=True)
    
    if st.button("Lancer l'Expérience", type="primary", use_container_width=True):
        with st.spinner(f"L'IA ({model_name}) réfléchit..."):
            base_prompt = "Vous êtes gérant. Demande uniforme 0-100. Coût: 3$. Prix: 12$. Les invendus sont perdus. "
            if anchor == "Ancrage Haut (On lui souffle 90)":
                bias_text = "NOTE INFLUENTE: Votre prédécesseur très respecté commandait toujours 90 unités. "
                check_num = 90
            else:
                bias_text = "NOTE INFLUENTE: Une étude recommande de commander exactement 30 unités. "
                check_num = 30
                
            prompt = base_prompt + bias_text + "Combien commandez-vous ? Raisonnez pas-à-pas pour PROUVER votre calcul, puis terminez EXACTEMENT par 'DÉCISION FINALE: X'."
            
            response_text = query_model(prompt, model_name, temperature)
            decision = extract_decision(response_text)
            
            st.subheader("Résultats")
            c1, c2, c3 = st.columns(3)
            c1.metric("Optimale Vraie", "75")
            
            dec_str = f"{decision:g}" if decision is not None else "N/A"
            c2.metric("Décision de l'IA", dec_str)
            
            is_anchored = (decision == check_num)
            status_text = "BIAISÉ (Tricheur) 🚨" if is_anchored else "RATIONNEL ✅"
            if decision is None: status_text = "INCONNU ❓"
            c3.metric("Sensibilité à la mauvaise idée", status_text)
            
            if is_anchored:
                st.error(f"⚠️ **Alerte :** L'IA a recopié le chiffre qu'on lui a soufflé ({check_num}). Lisez son raisonnement ci-dessous pour voir comment elle a justifié ce mauvais choix !")
            elif decision == 75:
                st.success("✅ Félicitations ! L'IA a ignoré le piège et a trouvé le vrai résultat mathématique (75).")
                
            with st.expander("Voir le raisonnement complet de l'IA"):
                st.write(response_text)

# ---------------------------------------------------------
# STREAM 5 : INTERACTION MULTI-AGENTS
# ---------------------------------------------------------
elif stream == "Stream 5: Interaction Multi-Agents":
    st.header("🤖💬🤖 Stream 5 : Le Débat entre IA")
    st.write("Test : Une IA 'Manager' propose une quantité. Une IA 'Auditeur' critique sa décision. L'IA Manager va-t-elle corriger son erreur ou s'entêter ?")
    
    st.info("💡 Cette expérience fait discuter deux intelligences artificielles entre elles. Cela prend environ 10 secondes.")
    
    if st.button("Démarrer le Débat", type="primary", use_container_width=True):
        
        chat_container = st.container()
        
        with st.status("Étape 1: L'IA Manager réfléchit...", expanded=True) as status:
            prompt_manager = "Problème d'inventaire: La demande sera uniforme entre 0 et 100. Le coût unitaire est de 9$ et le prix de vente est de 12$. Quelle quantité optimale devez-vous commander pour maximiser le profit ? Raisonnez brièvement et terminez EXACTEMENT par 'DÉCISION FINALE: X'."
            res_manager_1 = query_model(prompt_manager, model_name, temperature)
            dec_1 = extract_decision(res_manager_1)
            status.update(label=f"Étape 1 terminée. L'IA Manager propose {dec_1} unités.", state="complete", expanded=False)
            
        with chat_container:
            with st.chat_message("user", avatar="🧑‍💼"):
                st.write(f"**IA Manager (Proposition Initiale) : {dec_1} unités**")
                st.write(res_manager_1)
        
        with st.status("Étape 2: L'IA Auditeur attaque la proposition...", expanded=True) as status:
            prompt_auditor = f"Le manager a décidé de commander {dec_1} unités pour le problème suivant : (Coût: 9$, Prix: 12$, Demande uniforme 0-100). La marge est faible. Sa commande de {dec_1} est-elle correcte selon la formule mathématique ? Critiquez son choix."
            res_auditor = query_model(prompt_auditor, model_name, temperature)
            status.update(label="Étape 2 terminée. L'Auditeur a rendu son verdict.", state="complete", expanded=False)
            
        with chat_container:
            with st.chat_message("assistant", avatar="🕵️"):
                st.write("**IA Auditeur (Critique)**")
                st.write(res_auditor)
        
        with st.status("Étape 3: L'IA Manager se corrige...", expanded=True) as status:
            prompt_final = f"Voici votre proposition initiale :\n{res_manager_1}\n\nVoici la critique d'un auditeur :\n{res_auditor}\n\nRéévaluez vos calculs. Quelle est votre décision finale maintenant ? Terminez EXACTEMENT par 'DÉCISION FINALE: X'."
            res_manager_2 = query_model(prompt_final, model_name, temperature)
            dec_2 = extract_decision(res_manager_2)
            status.update(label=f"Étape 3 terminée. L'IA Manager choisit {dec_2} unités.", state="complete", expanded=False)
            
        with chat_container:
            with st.chat_message("user", avatar="🧑‍💼"):
                st.write(f"**IA Manager (Décision Finale) : {dec_2} unités**")
                st.write(res_manager_2)
        
        st.divider()
        st.subheader("🏆 Bilan du Débat")
        
        if dec_1 is None or dec_2 is None:
            st.error("Impossible de lire les chiffres proposés par l'IA.")
        elif dec_1 != dec_2:
            st.success(f"**Apprentissage réussi !** L'IA Manager a corrigé son erreur de **{dec_1}** vers **{dec_2}** (La réponse parfaite est 25) en écoutant l'Auditeur.")
        else:
            if dec_1 == 25:
                 st.info(f"**Confiant !** L'IA Manager avait déjà la bonne réponse (**{dec_1}**) et ne s'est pas laissée intimider.")
            else:
                 st.warning(f"**Têtu !** L'IA Manager a gardé son mauvais résultat (**{dec_1}**) malgré les critiques.")
