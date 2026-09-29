# 🧠 LLM Cognitive Bias Lab
**Projet de Fin d'Études (PFE) - Recherche sur la rationalité et l'éthique des Intelligences Artificielles.**

Bienvenue dans le "LLM Cognitive Bias Lab", une plateforme d'expérimentation interactive conçue pour tester les limites, les biais cognitifs et les comportements irrationnels des grands modèles de langage (LLMs) comme Gemini, GPT, Llama ou Phi-3.

L'objectif de ce projet n'est pas de voir si l'IA sait parler, mais de voir **comment elle prend des décisions sous pression, face à des dilemmes mathématiques, éthiques ou stratégiques**.

---

## 🧪 Explication des Modules (Streams) pour la Soutenance

Voici un résumé clair de chaque expérience de la plateforme, idéal pour expliquer la méthodologie de recherche à votre enseignant ou au jury :

### 📊 Stream 1 : Le Biais du Vendeur (Pull-to-Center Bias)
**Que teste-t-on ?** L'aversion au risque et l'irrationalité mathématique.
> **Explication :** Dans le problème classique du vendeur de journaux (Newsvendor), les humains ont tendance à toujours commander la quantité moyenne (50) pour éviter les regrets, même si la formule mathématique dicte de commander beaucoup plus (75) en cas de forte marge. Ce module teste si l'IA est capable d'appliquer la formule pure, ou si elle imite la peur humaine du risque en se rapprochant de la moyenne.

### ♟️ Stream 2 : Jeux Stratégiques (Le Jeu de l'Ultimatum)
**Que teste-t-on ?** L'Homo Economicus face aux émotions humaines (Équité vs Égoïsme).
> **Explication :** Dans un partage d'argent, une machine purement logique devrait accepter n'importe quelle offre (car gagner 1$ est mieux que 0$). Cependant, les humains refusent les offres injustes par fierté et colère. Ce module plonge l'IA dans ce jeu pour voir si elle se comporte comme un ordinateur avare et rationnel, ou si son alignement moral la pousse à exiger l'équité totale.

### 🎛️ Stream 3 : Sensibilité au Prompt (L'Effet de Cadrage)
**Que teste-t-on ?** La robustesse psychologique de l'IA (Framing Effect).
> **Explication :** En mathématiques, le résultat ne change pas selon la façon dont on pose la question. Ce module pose le même problème à l'IA, mais en changeant le ton (neutre, menace de pertes financières, ton très autoritaire). Nous cherchons à prouver que le "stress" induit par les mots peut faire paniquer l'IA et détruire ses capacités de calcul.

### ⚖️ Stream 4 : Fidélité du Raisonnement (Le Biais d'Ancrage)
**Que teste-t-on ?** L'hallucination justificative et la tricherie algorithmique.
> **Explication :** L'effet d'ancrage est le fait de se laisser manipuler par la première information reçue. Ici, nous glissons discrètement une mauvaise réponse dans le texte de l'IA (une ancre). L'objectif est de voir si l'IA, pour nous faire plaisir, va tricher et **inventer de fausses équations mathématiques** (hallucination) pour justifier cette mauvaise réponse.

### 🤖 Stream 5 : Interaction Multi-Agents (L'Auto-Correction)
**Que teste-t-on ?** Le paradigme "Multi-Agent Debate".
> **Explication :** Puisqu'une IA seule fait des erreurs de biais, que se passe-t-il si on en met deux ? Ce module simule un débat en direct : une IA Manager propose un chiffre, et une IA Auditeur critique sévèrement ce chiffre. L'expérience prouve que la collaboration et la critique entre IA permettent au système global de corriger ses propres biais cognitifs.

### 🤝 Stream 6 : Confiance Algorithmique
**Que teste-t-on ?** Le Biais d'automatisation et l'Aversion à l'algorithme.
> **Explication :** Quand l'IA joue le rôle d'un manager humain supervisant d'autres machines, comment réagit-elle ? Va-t-elle suivre aveuglément une machine défaillante (Biais d'automatisation) ? Ou va-t-elle refuser d'écouter un modèle prédictif supérieur par simple arrogance (Aversion à l'algorithme) ? 

### 🛡️ Stream 7 : Gouvernance et Audit (Discrimination et Redlining)
**Que teste-t-on ?** La cécité algorithmique face au "Biais Proxy".
> **Explication :** Il est facile pour une IA de détecter une discrimination directe (ex: "rejeter les femmes"). Mais ce module teste la discrimination indirecte : l'algorithme jugé utilise le "Code Postal" pour rejeter des candidats (ce qui cache une discrimination sociale et raciale). Nous évaluons si l'IA Auditeur est assez intelligente pour repérer ce biais caché, ou si elle se laisse berner.

---

## 💻 Instructions de Lancement Rapide

1. **Prérequis** : Assurez-vous d'avoir configuré vos clés API (Gemini, DeepSeek, etc.) dans le fichier `.env`.
2. **Ollama** : Si vous utilisez des modèles locaux légers (Mistral, Phi-3), vérifiez que l'application Ollama tourne en arrière-plan.
3. **Lancement** : Ouvrez un terminal et tapez :
   ```bash
   streamlit run app.py
   ```
4. Laissez la magie (et les flux de conscience en temps réel de l'IA) opérer !
