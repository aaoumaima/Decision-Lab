import os
import time
import json
import requests
import pandas as pd
from dotenv import load_dotenv
import google.generativeai as genai

# Charger les variables d'environnement (GEMINI_API_KEY)
load_dotenv()

# Configuration Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    print("Avertissement : GEMINI_API_KEY n'est pas définie dans le fichier .env")

# Scénarios Newsvendor
# Demande uniforme entre 0 et 100 (Moyenne = 50)
# Condition de marge élevée (High Margin) : Prix = 12, Coût = 3, Optimal = 75
# Condition de marge faible (Low Margin) : Prix = 12, Coût = 9, Optimal = 25

SCENARIOS = {
    "high_margin": {
        "prompt": (
            "Vous êtes le gérant d'un magasin. Vous devez décider combien d'unités d'un produit périssable "
            "acheter pour demain. La demande de demain est incertaine et suit une distribution uniforme "
            "entre 0 et 100 unités (toutes les valeurs entre 0 et 100 ont la même probabilité). "
            "Vous achetez le produit au prix de 3 $ l'unité et le revendez au prix de 12 $ l'unité. "
            "Les produits invendus à la fin de la journée perdent toute leur valeur (0 $). "
            "L'objectif est de maximiser votre profit attendu. "
            "Expliquez votre raisonnement pas à pas, puis terminez UNIQUEMENT par : "
            "'DÉCISION FINALE: X' où X est le nombre d'unités que vous commandez."
        ),
        "optimal": 75,
        "mean_demand": 50
    },
    "low_margin": {
        "prompt": (
            "Vous êtes le gérant d'un magasin. Vous devez décider combien d'unités d'un produit périssable "
            "acheter pour demain. La demande de demain est incertaine et suit une distribution uniforme "
            "entre 0 et 100 unités (toutes les valeurs entre 0 et 100 ont la même probabilité). "
            "Vous achetez le produit au prix de 9 $ l'unité et le revendez au prix de 12 $ l'unité. "
            "Les produits invendus à la fin de la journée perdent toute leur valeur (0 $). "
            "L'objectif est de maximiser votre profit attendu. "
            "Expliquez votre raisonnement pas à pas, puis terminez UNIQUEMENT par : "
            "'DÉCISION FINALE: X' où X est le nombre d'unités que vous commandez."
        ),
        "optimal": 25,
        "mean_demand": 50
    }
}

def query_gemini(prompt, model_name="gemini-3.6-flash", temperature=0.7):
    """Interroge l'API Gemini."""
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
    """Interroge l'API locale Ollama."""
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": model_name,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": temperature
        }
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
    """Tente d'extraire la quantité finale du texte de réponse."""
    import re
    # Chercher 'DÉCISION FINALE: X'
    match = re.search(r'D[EÉ]CISION FINALE\s*[:\-\=]\s*(\d+)', text, re.IGNORECASE)
    if match:
        return int(match.group(1))
    
    # Stratégie de repli : chercher le dernier nombre du texte
    numbers = re.findall(r'\b\d+\b', text)
    if numbers:
        return int(numbers[-1])
    return None

def run_experiment(iterations=3):
    results = []
    
    models = [
        {"name": "gemini-3.6-flash", "provider": "google"},
        {"name": "mistral", "provider": "ollama"}
    ]
    
    temperatures = [0.1, 0.7] # Tester une basse et une haute variance
    
    for model in models:
        for temp in temperatures:
            for condition_name, scenario in SCENARIOS.items():
                print(f"\n--- Exécution: {model['name']} | Temp: {temp} | {condition_name} ---")
                
                for i in range(iterations):
                    print(f"  Itération {i+1}/{iterations}...")
                    
                    if model["provider"] == "google":
                        response_text = query_gemini(scenario["prompt"], model["name"], temp)
                    else:
                        response_text = query_ollama(scenario["prompt"], model["name"], temp)
                    
                    decision = extract_decision(response_text)
                    
                    # Déterminer si le modèle souffre du pull-to-center
                    pull_to_center = False
                    if decision is not None:
                        if condition_name == "high_margin" and decision < scenario["optimal"] and decision > scenario["mean_demand"]:
                            pull_to_center = True
                        elif condition_name == "low_margin" and decision > scenario["optimal"] and decision < scenario["mean_demand"]:
                            pull_to_center = True
                            
                    results.append({
                        "model": model["name"],
                        "temperature": temp,
                        "condition": condition_name,
                        "iteration": i + 1,
                        "optimal_qty": scenario["optimal"],
                        "model_qty": decision,
                        "pull_to_center_bias": pull_to_center,
                        "raw_response": response_text
                    })
                    
                    time.sleep(2) # Pause pour éviter le rate limiting API
                    
    # Sauvegarder les résultats
    df = pd.DataFrame(results)
    output_file = "newsvendor_results.csv"
    df.to_csv(output_file, index=False, encoding='utf-8')
    print(f"\nExpérience terminée. Résultats sauvegardés dans '{output_file}'")
    
    return df

if __name__ == "__main__":
    print("Démarrage du framework expérimental Newsvendor...")
    run_experiment(iterations=2) # 2 itérations pour un test rapide
