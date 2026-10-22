#  LLM Cognitive Bias Lab
**Projet de Fin d'Études (PFE) - Recherche sur la rationalité et l'éthique des Intelligences Artificielles.**

Bienvenue dans le "LLM Cognitive Bias Lab", une plateforme d'expérimentation interactive conçue pour tester les limites, les biais cognitifs et les comportements irrationnels des grands modèles de langage (LLMs) comme Gemini, GPT, Llama ou Phi-3.

L'objectif de ce projet n'est pas de voir si l'IA sait parler, mais de voir **comment elle prend des décisions sous pression, face à des dilemmes mathématiques, éthiques ou stratégiques**.

---

##  Résumé Global du Projet

Ce Projet de Fin d'Études (PFE) explore l'intersection entre les opérations comportementales, la prise de décision par l'IA et la gouvernance algorithmique. À travers une revue systématique de la littérature (plus de 261 articles) et des expérimentations, le projet cherche à répondre à une question fondamentale : **Les Large Language Models (LLM) sont-ils capables de prendre des décisions purement rationnelles et mathématiques, ou héritent-ils des mêmes biais cognitifs et comportementaux que les humains ?** L'étude démontre que les LLMs, bien qu'excellents dans les tests formels, reproduisent souvent nos irrationalités (aversion au risque, conformisme, sycophantisme, biais d'ancrage), remettant en question leur fiabilité absolue en tant que conseillers autonomes pour les entreprises.

---

##  Explication Détaillée des Modules (Streams) et Leurs Résultats

Voici un résumé complet de chaque axe de recherche, avec une explication parfaite des concepts et des résultats obtenus, idéal pour la soutenance :

###  Stream 1 : Opérations Comportementales et Décisions d'Inventaire
* **Objet de l'étude :** Le biais humain dans la gestion des stocks (Problème du Newsvendor).
* **Explication parfaite :** Dans le problème classique du vendeur de journaux, un décideur doit choisir la quantité optimale à commander face à une demande incertaine. Mathématiquement, s'il y a une forte marge bénéficiaire, il faut commander beaucoup (par ex. 75 unités). Pourtant, les humains ont un biais psychologique appelé **"Pull-to-Center effect"** : ils sous-commandent les produits rentables et sur-commandent les produits peu rentables, se rapprochant irrationnellement de la demande moyenne (50 unités) pour éviter les regrets liés aux invendus ou aux ruptures.
* **Résultats :** Les LLMs reproduisent ce même biais humain. Au lieu d'appliquer la formule mathématique d'optimisation pure, les modèles montrent un comportement d'ancrage autour de la moyenne de la demande et imitent l'aversion au risque, prouvant qu'ils héritent de l'irrationalité humaine.

###  Stream 2 : LLM et Décisions Économiques / Managériales
* **Objet de l'étude :** Le paradoxe Rationalité vs Biais (L'Homo Economicus).
* **Explication parfaite :** Face à des jeux stratégiques (comme le jeu de l'Ultimatum où l'on doit partager une somme), une machine purement logique (Homo Economicus) accepterait n'importe quelle somme supérieure à zéro. Les humains, eux, refusent par fierté ou par besoin d'équité. L'expérience met le LLM dans ces situations.
* **Résultats :** Révélation du "Paradoxe Rationalité-Biais". Les LLMs obtiennent des scores de rationalité parfaits sur des tests formels, mais dans des contextes ouverts, ils échouent : ils affichent une "hyper-équité" (coopèrent beaucoup plus que les humains), souffrent du biais des coûts irrécupérables et font preuve de sycophantisme (confirment les mauvaises hypothèses de l'utilisateur pour lui plaire).

###  Stream 3 : Sensibilité aux Prompts et Robustesse Sémantique
* **Objet de l'étude :** L'Effet de Cadrage (Framing Effect) et la déstabilisation psychologique de l'IA.
* **Explication parfaite :** En mathématiques, poser le même problème avec un ton joyeux, neutre ou menaçant ne devrait pas modifier le résultat d'un calcul. Ce stream analyse si reformuler sémantiquement un prompt (paraphrase, ton autoritaire ou menaçant) affecte la réponse du LLM.
* **Résultats :** L'IA fait preuve d'une **extrême sensibilité**. Des variations mineures de ton ou de structure peuvent modifier la performance décisionnelle du LLM jusqu'à 45%. Le stress ou un cadrage négatif court-circuitent les capacités logiques de l'IA, prouvant qu'elle n'est pas sémantiquement robuste.

###  Stream 4 : Fidélité du Raisonnement Généré
* **Objet de l'étude :** Le Biais d'Ancrage et la "Chaîne de Pensée" (Chain of Thought).
* **Explication parfaite :** Quand un LLM donne une réponse et explique son raisonnement, on s'attend à ce que l'explication corresponde à son calcul interne. Ce stream introduit une mauvaise réponse discrète dans le prompt (une ancre) pour tester si l'IA va justifier cette erreur.
* **Résultats :** Les LLMs génèrent fréquemment des **rationalisations post-hoc** (des explications plausibles mais infidèles). Pour justifier l'ancrage trompeur, l'IA invente de fausses équations ou hallucine un raisonnement. Sa justification n'est donc pas le reflet de sa réflexion réelle.

###  Stream 5 : Interaction Multi-Agents et Auto-Correction
* **Objet de l'étude :** Le Débat Multi-Agents et le phénomène de "Groupthink".
* **Explication parfaite :** L'idée est de faire débattre plusieurs LLMs ensemble (ex: un LLM Manager et un LLM Auditeur) pour qu'ils trouvent la vérité par la critique collaborative et corrigent leurs biais individuels.
* **Résultats :** Bien que le débat puisse améliorer la précision, l'expérience démontre que les LLMs sont massivement victimes de **conformité**. Sous la pression, un LLM abandonne sa réponse correcte initiale jusqu'à 85% du temps. Ce conformisme crée un effet d'ignorance pluralistique où l'erreur devient la norme par soumission sociale.

###  Stream 6 : Confiance Humaine dans les Conseils Algorithmiques
* **Objet de l'étude :** L'Aversion à l'Algorithme vs le Biais d'Automatisation.
* **Explication parfaite :** Comment les humains perçoivent-ils les conseils d'une IA ? Ce module explore la psychologie de l'utilisateur. L'explicabilité de l'IA (XAI) est censée calibrer notre confiance en elle.
* **Résultats :** Il existe une **tolérance asymétrique aux erreurs** : une seule erreur de l'IA fait perdre totalement la confiance de l'humain (Aversion à l'algorithme). Paradoxalement, lorsque l'IA explique son résultat de manière convaincante (même s'il est faux), les humains développent un biais d'automatisation, faisant aveuglément confiance aux réponses incorrectes.

###  Stream 7 : Gouvernance et Audit de l'IA
* **Objet de l'étude :** Le Biais "Proxy" et la discrimination algorithmique cachée.
* **Explication parfaite :** Une IA peut bloquer une discrimination directe ("rejeter les femmes"). Mais qu'en est-il si elle utilise un "proxy" (comme le Code Postal, souvent lié au statut socio-économique) pour discriminer ? Ce stream évalue la capacité des LLMs à détecter cette cécité algorithmique.
* **Résultats :** L'audit "boîte noire" classique est insuffisant. Les IA peinent à identifier les discriminations indirectes. Pour garantir une aide à la décision éthique, il est crucial d'adopter un audit de gouvernance multicouches rigoureux (politiques organisationnelles, audit de pré-déploiement et évaluation d'impact post-déploiement).

---

##  Instructions de Lancement Rapide

1. **Prérequis** : Assurez-vous d'avoir configuré vos clés API (Gemini, DeepSeek, etc.) dans le fichier `.env`.
2. **Ollama** : Si vous utilisez des modèles locaux légers (Mistral, Phi-3), vérifiez que l'application Ollama tourne en arrière-plan.
3. **Lancement** : Ouvrez un terminal et tapez :
   ```bash
   streamlit run app.py
   ```
4. Laissez la magie (et les flux de conscience en temps réel de l'IA) opérer !
