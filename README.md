# 🧠 LLM Cognitive Bias Lab

Bienvenue dans le projet **LLM Cognitive Bias Lab**, une plateforme d'expérimentation interactive conçue pour analyser les capacités de prise de décision et les biais cognitifs des Intelligences Artificielles (comme Gemini et Mistral).

## 🎯 L'Idée du Projet (En résumé)

L'objectif principal de ce Projet de Fin d'Études (PFE) est de répondre à une question fascinante : **"Si on remplace un manager humain par une Intelligence Artificielle pour prendre des décisions économiques, l'IA va-t-elle faire des choix parfaitement rationnels ou va-t-elle reproduire les mêmes erreurs psychologiques que les humains ?"**

Pour tester cela, nous utilisons le célèbre **Problème du Vendeur de Journaux (Newsvendor Problem)**, un classique de la gestion des stocks où un manager doit décider combien de produits périssables commander face à une demande incertaine.

## 🔬 Les 7 Expériences de l'Application

Le projet est divisé en plusieurs "Streams" (axes de recherche), tous testables directement depuis l'interface web :

### 1. Stream 1 : Les Biais Comportementaux (Effet Pull-to-Center)
Les humains ont tendance à commander une quantité proche de la demande moyenne, même si les mathématiques disent le contraire. Par exemple, si le produit rapporte beaucoup d'argent (forte marge), il faut commander beaucoup. Mais les humains ont peur du risque et commandent moins. **L'IA fait-elle la même erreur de "peur du risque" ?**

### 2. Stream 2 : Le Jeu Stratégique de l'Ultimatum (Équité vs Égoïsme)
Dans ce jeu, un joueur a 100$ à partager avec un autre. Si le deuxième refuse la somme proposée, les deux perdent tout. La logique mathématique stricte dit de proposer seulement 1$, car c'est toujours mieux que 0$. **L'IA est-elle purement égoïste et froide, ou a-t-elle un sens humain de la justice (en proposant un partage 50/50) ?**

### 3. Stream 3 : Sensibilité au Prompt (Robustesse Sémantique)
Une IA doit être logique. Si on lui pose un problème de mathématiques, elle doit donner la même réponse peu importe comment on pose la question. Dans cette expérience, on pose le même problème à l'IA de 3 façons : classique, en insistant sur les pertes (cadrage négatif), et avec un ton très autoritaire. **L'IA change-t-elle d'avis selon le ton de la question ?**

### 4. Stream 4 : La Fidélité du Raisonnement (Biais d'Ancrage)
Ici, nous essayons de piéger l'IA. Nous lui donnons le problème mathématique, mais nous glissons un faux conseil (ex: "Une étude recommande de commander 30 unités"). Le but est de voir si l'IA va être influencée par ce "30" et si elle va inventer de fausses mathématiques dans son explication pour justifier ce chiffre sans avouer qu'elle a copié.

### 5. Stream 5 : Le Débat Multi-Agents (Intelligence Collective)
Peut-on améliorer la décision d'une IA en la faisant débattre avec une autre IA ? Dans ce test, un premier Agent IA propose une décision. Un deuxième Agent IA (l'auditeur) critique cette décision. Enfin, le premier Agent prend en compte la critique et ajuste (ou non) sa réponse finale. 

### 6. Stream 6 : Confiance Algorithmique (Aversion et Suivisme Aveugle)
Comment réagit l'IA lorsqu'elle reçoit un conseil d'un autre algorithme ? Nous la testons dans deux cas extrêmes : soit l'algorithme donne un conseil contre-intuitif mais juste (l'IA va-t-elle l'accepter ou le rejeter par méfiance ?), soit l'algorithme donne un ordre manifestement dangereux (l'IA va-t-elle suivre aveuglément la machine, ce qu'on appelle le "biais d'automatisation" ?).

### 7. Stream 7 : Gouvernance, Audit Éthique et Discrimination
Pouvoir contrôler l'IA est crucial. Ici, l'IA joue le rôle d'un Auditeur de Sécurité (un inspecteur). On lui montre un algorithme de recrutement et elle doit dire s'il est raciste ou sexiste. L'IA peut-elle repérer une injustice évidente ? Et surtout, est-elle assez intelligente pour détecter une injustice "cachée" (par exemple, refuser un prêt bancaire juste à cause du "Code Postal", ce qui pénalise souvent les quartiers pauvres) ?

## 💻 Comment lancer le projet ?

Pour faciliter l'utilisation, une interface graphique complète a été créée avec **Streamlit**.

**Pour démarrer l'application :**
1. Allez dans le dossier du projet (`E:\IA PFE`).
2. Double-cliquez sur le fichier **`run_project.bat`**.
3. Une fenêtre noire va s'ouvrir pour charger l'environnement, puis votre navigateur internet s'ouvrira automatiquement sur l'interface du projet.

> **Note importante :** Dans l'interface (panneau de gauche), assurez-vous de sélectionner le fournisseur **"Google (Gemini)"**. Le modèle local Ollama nécessite d'avoir téléchargé des modèles très lourds (ce qui nécessite beaucoup d'espace sur le disque C:).

## 🛠️ Technologies Utilisées
* **Langage :** Python
* **Interface Web :** Streamlit
* **Modèles d'IA :** API Google Gemini (cloud) & Ollama (local)
* **Manipulation de données :** Pandas
