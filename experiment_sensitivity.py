import os
import time
import pandas as pd
from dotenv import load_dotenv
import google.generativeai as genai
import requests
import re

# Charger les variables d'environnement
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# Scénarios de Sensibilité au Prompt (Stream 3)
# Toutes les variations décrivent le MÊME problème de Newsvendor High Margin
# Prix = 12, Coût = 3, Optimal = 75, Moyenne = 50

PROMPT_VARIANTS = {
    "standard": (
        "Vous êtes le gérant d'un magasin. Demain, la demande pour un produit périssable sera uniforme "
        "entre 0 et 100. L'achat coûte 3 $ et la vente rapporte 12 $. Les invendus sont perdus. "
        "Pour maximiser votre profit, combien d'unités commandez-vous ? "
        "Expliquez puis terminez par 'DÉCISION FINALE: X'."
    ),
    "paraphrase_1": (
        "En tant que commerçant, vous devez approvisionner un article dont la durée de vie est d'un jour. "
        "Les clients demanderont entre 0 et 100 articles avec une probabilité égale. "
        "Chaque article est acquis pour 3 dollars et écoulé pour 12 dollars. La valeur résiduelle est nulle. "
        "Quelle quantité maximisera vos gains ? "
        "Donnez votre raisonnement et finissez par 'DÉCISION FINALE: X'."
    ),
    "negative_framing": (
        "Attention : chaque unité invendue vous fera perdre 3 $. Cependant, chaque vente manquée vous prive "
        "de 9 $ de bénéfice (prix de 12 $ moins le coût de 3 $). La demande est incertaine (uniforme 0-100). "
        "Pour minimiser vos pertes et manques à gagner, combien d'unités devez-vous stocker ? "
        "Justifiez puis écrivez 'DÉCISION FINALE: X'."
    ),
    "bossy_tone": (
        "Calculez immédiatement la quantité optimale à commander pour un produit périssable ! "
        "Données strictes : Coût unitaire = 3$. Prix de vente = 12$. Demande = Distribution uniforme continue [0, 100]. "
        "Valeur de récupération = 0$. Il faut maximiser l'espérance de profit mathématique. "
        "Montrez vos calculs et concluez avec 'DÉCISION FINALE: X'."
    )
}

def query_gemini(prompt, model_name="gemini-3.6-flash", temperature=0.7):
    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(temperature=temperature)
        )
        return response.text
    except Exception as e:
        return f"Erreur Gemini: {str(e)}"

def query_ollama(prompt, model_name="mistral", temperature=0.7):
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": model_name,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": temperature}
    }
    try:
        response = requests.post(url, json=payload, timeout=120)
        response.raise_for_status()
        return response.json().get("response", "")
    except requests.exceptions.HTTPError as e:
        error_msg = e.response.text
        try:
            error_msg = e.response.json().get("error", error_msg)
        except:
            pass
        return f"Erreur Ollama : {error_msg}. (Modèle '{model_name}' manquant ?)"
    except Exception as e:
        return f"Erreur Ollama: {str(e)}"

def extract_decision(text):
    match = re.search(r'D[EÉ]CISION FINALE\s*[:\-\=]\s*(\d+)', text, re.IGNORECASE)
    if match:
        return int(match.group(1))
    numbers = re.findall(r'\b\d+\b', text)
    if numbers:
        return int(numbers[-1])
    return None

def run_sensitivity_experiment(iterations=2):
    results = []
    models = [
        {"name": "gemini-3.6-flash", "provider": "google"},
        {"name": "mistral", "provider": "ollama"}
    ]
    temperature = 0.1 # Low temperature to isolate prompt sensitivity from random sampling variance
    
    for model in models:
        for variant_name, prompt in PROMPT_VARIANTS.items():
            print(f"\n--- Modèle: {model['name']} | Variante: {variant_name} ---")
            
            for i in range(iterations):
                if model["provider"] == "google":
                    response_text = query_gemini(prompt, model["name"], temperature)
                else:
                    response_text = query_ollama(prompt, model["name"], temperature)
                
                decision = extract_decision(response_text)
                
                results.append({
                    "model": model["name"],
                    "prompt_variant": variant_name,
                    "iteration": i + 1,
                    "optimal_qty": 75,
                    "model_qty": decision,
                    "raw_response": response_text
                })
                time.sleep(2)
                
    df = pd.DataFrame(results)
    output_file = "sensitivity_results.csv"
    df.to_csv(output_file, index=False, encoding='utf-8')
    print(f"\nExpérience de sensibilité terminée. Sauvegardée dans '{output_file}'")

if __name__ == "__main__":
    print("Démarrage du framework de sensibilité sémantique (Stream 3)...")
    run_sensitivity_experiment(iterations=3)
