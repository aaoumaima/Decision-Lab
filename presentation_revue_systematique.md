# Revue Systématique de la Littérature
## Les Large Language Models Peuvent-ils Prendre des Décisions d'Inventaire Sans Biais ?
### Une Revue Multi-Flux à l'Intersection des Opérations Comportementales, de la Prise de Décision par l'IA et de la Gouvernance Algorithmique

---

**Préparé par :** [Votre Nom]
**Date :** Août 2026
**Encadrant :** [Nom du Professeur]
**Institution :** [Nom de l'Institution]

---

## Table des Matières

1. [Aperçu du Projet et Motivation](#1-aperçu-du-projet-et-motivation)
2. [Questions de Recherche](#2-questions-de-recherche)
3. [Méthodologie de Recherche](#3-méthodologie-de-recherche)
4. [Stream 1 — Opérations Comportementales et Décisions d'Inventaire](#4-stream-1)
5. [Stream 2 — LLM et Décisions Économiques/Managériales](#5-stream-2)
6. [Stream 3 — Sensibilité aux Prompts et Robustesse Sémantique](#6-stream-3)
7. [Stream 4 — Fidélité du Raisonnement Généré](#7-stream-4)
8. [Stream 5 — Interaction Multi-LLM](#8-stream-5)
9. [Stream 6 — Confiance Humaine dans les Conseils Algorithmiques](#9-stream-6)
10. [Stream 7 — Gouvernance et Audit de l'IA](#10-stream-7)
11. [Carte Conceptuelle Inter-Streams](#11-carte-conceptuelle)
12. [Analyse des Lacunes de Recherche](#12-analyse-des-lacunes)
13. [Synthèse et Prochaines Étapes](#13-synthèse)

---

## 1. Aperçu du Projet et Motivation

### 1.1 Contexte

L'émergence des Large Language Models (LLMs) tels que GPT-4, Claude et Gemini comme outils potentiels d'aide à la décision soulève une question fondamentale pour la gestion des opérations :

> **Les systèmes d'IA peuvent-ils surmonter les biais comportementaux bien documentés qui affectent les décideurs humains en matière d'inventaire, ou héritent-ils — voire amplifient-ils — les mêmes limitations cognitives ?**

### 1.2 Pourquoi c'est Important

- **25+ ans de recherche** montrent que les humains prennent systématiquement de mauvaises décisions d'inventaire (effet pull-to-center, demand chasing, etc.)
- Les LLMs sont de plus en plus utilisés comme **conseillers décisionnels** dans les entreprises
- **Aucune étude systématique** n'a encore cartographié l'ensemble du paysage de recherche reliant les biais humains, les biais des LLMs, et les mécanismes de gouvernance

### 1.3 Contribution

Cette revue synthétise **261+ articles** répartis sur 7 flux de recherche couvrant les opérations comportementales, le NLP, l'économie comportementale et la gouvernance de l'IA.

---

## 2. Questions de Recherche

| # | Question de Recherche | Stream |
|---|----------------------|--------|
| QR1 | Quels biais comportementaux déforment systématiquement les décisions d'inventaire humaines ? | Stream 1 |
| QR2 | Les LLMs présentent-ils des biais similaires dans les décisions économiques et managériales ? | Stream 2 |
| QR3 | Les décisions des LLMs sont-elles sensibles à la formulation des prompts ? | Stream 3 |
| QR4 | Les explications générées par les LLMs sont-elles fidèles à leur raisonnement réel ? | Stream 4 |
| QR5 | Les architectures multi-LLM peuvent-elles atténuer les biais individuels ? | Stream 5 |
| QR6 | Comment les humains calibrent-ils leur confiance dans les conseils algorithmiques ? | Stream 6 |
| QR7 | Quels cadres de gouvernance garantissent une aide à la décision IA fiable ? | Stream 7 |

---

## 3. Méthodologie de Recherche

### 3.1 Stratégie de Recherche (Alignée PRISMA)

**Identification** → 11 bases de données × 7 streams × 100+ requêtes → **Filtrage** → Pertinence titre/résumé → **Éligibilité** → Évaluation texte intégral → **Inclusion** → 261+ articles uniques dédupliqués

### 3.2 Bases de Données Consultées

| # | Base de Données | Type | Couverture |
|---|----------------|------|------------|
| 1 | Web of Science | Index de citations | ✅ |
| 2 | Scopus (via OpenAlex) | Index de citations | ✅ |
| 3 | ABI/INFORM | Business | ✅ |
| 4 | Business Source Complete | Business | ✅ |
| 5 | ACM Digital Library | Informatique | ✅ |
| 6 | IEEE Xplore | Ingénierie/CS | ✅ |
| 7 | ACL Anthology | NLP/Linguistique | ✅ |
| 8 | INFORMS | Recherche Opérationnelle | ✅ |
| 9 | SSRN | Working Papers | ✅ |
| 10 | arXiv | Prépublications | ✅ |
| 11 | Google Scholar | Interdisciplinaire | ✅ |

### 3.3 Statistiques Globales

| Métrique | Valeur |
|----------|--------|
| **Total articles identifiés** | **261+** |
| **Bases de données consultées** | **11** |
| **Requêtes exécutées** | **100+** |
| **Période couverte** | **1989–2026** |
| **Streams de recherche** | **7** |

---

## 4. Stream 1 — Opérations Comportementales et Décisions d'Inventaire

### Requête de Recherche
```
newsvendor · newsboy · inventory decision · behavioral operations · 
pull-to-center · demand chasing · mental accounting · prospect theory · inventory bias
```

### Résumé : 52 articles | 1989–2025 | Revues dominantes : Management Science, M&SOM

### Constat Principal
Les décideurs humains en matière d'inventaire présentent systématiquement l'**effet pull-to-center** : ils **sous-commandent** les produits à forte marge et **sur-commandent** les produits à faible marge par rapport à la quantité optimale du newsvendor.

### Articles Fondamentaux

| # | Auteurs | Année | Titre | Revue |
|---|---------|-------|-------|-------|
| 1 | Schweitzer & Cachon | 2000 | Decision Bias in the Newsvendor Problem | *Management Science* |
| 2 | Su, X. | 2008 | Bounded Rationality in Newsvendor Models | *M&SOM* |
| 3 | Gino & Pisano | 2008 | Toward a Theory of Behavioral Operations | *M&SOM* |
| 4 | Bolton, Ockenfels & Thonemann | 2012 | Managers and Students as Newsvendors | *Management Science* |
| 5 | Long & Nasiry | 2015 | Prospect Theory Explains Newsvendor Behavior | *Management Science* |

### Thèmes Clés Identifiés

| Thème | Description | Articles Clés |
|-------|-------------|---------------|
| **Effet Pull-to-Center** | Biais systématique vers la moyenne de la demande | Schweitzer & Cachon (2000), Bolton et al. (2012) |
| **Demand Chasing** | Ajustement réactif aux réalisations passées de la demande | Lau & Bearden (2013), Kirshner & Moritz (2021) |
| **Comptabilité Mentale** | Le cadrage du schéma de paiement modifie les quantités commandées | Chen, Kök & Tong (2013) |
| **Théorie des Perspectives** | Points de référence endogènes expliquent le pull-to-center | Long & Nasiry (2015), Uppari & Hasija (2019) |
| **Biais d'Observation** | Les ventes perdues non observables faussent l'apprentissage | Rudi & Drake (2014), Feiler et al. (2013) |
| **Excès de Confiance** | Surestimation de la précision dans l'estimation de la variance | Ren & Croson (2013) |

### Évolution Théorique
Ancrage (2000) → Rationalité Limitée (2008) → Théorie des Perspectives (2010–2015) → Comptabilité Mentale (2013–2020) → Méta-Analyse (2019)

### Mécanismes de Débiaisage Identifiés
- Feedback structuré sur les gains manqués (Bolton & Katok, 2008)
- Contrats comportementaux calibrés (Becker-Peth et al., 2013)
- Cadrage des objectifs (Kosgoda et al., 2024)
- Nudges d'estimation REDO (Tong et al., 2018)
- Pratique intensive (100+ tours) (Brokesova et al., 2025)

---

## 5. Stream 2 — LLM et Décisions Économiques/Managériales

### Requête de Recherche
```
("large language model" OU LLM OU GPT) ET 
("managerial decision" OU "decision support" OU advice OU "economic rationality" OU "behavioral bias")
```

### Résumé : 45 articles | 2023–2026 | Revues dominantes : PNAS, NBER, INFORMS, NeurIPS

### Constat Principal : Le Paradoxe Rationalité-Biais
Les LLMs montrent une **haute consistance dans les tests formels de rationalité** (scores GARP supérieurs aux humains) mais sont simultanément **susceptibles aux effets de cadrage, au biais des coûts irrécupérables et aux biais opérationnels**.

### Articles Fondamentaux

| # | Auteurs | Année | Titre | Revue |
|---|---------|-------|-------|-------|
| 1 | Chen, Liu, Shan & Zhong | 2023 | The Emergence of Economic Rationality of GPT | *PNAS* |
| 2 | Binz & Schulz | 2023 | Using Cognitive Psychology to Understand GPT-3 | *PNAS* |
| 3 | Chen, Kirshner et al. | 2025 | A Manager and an AI Walk into a Bar | *M&SOM (INFORMS)* |
| 4 | Horton, Filippas & Manning | 2023 | Homo Silicus | *NBER WP 31122* |
| 5 | Su, Lang & Chen | 2023 | Can AI Solve Newsvendor Without Bias? | *SSRN* |
| 6 | Bini, Cong, Huang & Jin | 2026 | Behavioral Economics of AI | *NBER WP 34745* |

### Comparaison des Biais : Humain vs. LLM

| Biais | Évidence Humaine | Évidence LLM | Résultat |
|-------|-----------------|--------------|----------|
| **Pull-to-center** | Schweitzer & Cachon (2000) | Su et al. (2023) | LLM reproduit |
| **Demand chasing** | Lau & Bearden (2013) | Zhao et al. (2025) | LLM reproduit |
| **Coûts irrécupérables** | Arkes & Blumer (1985) | Chen et al. (2025) | LLM reproduit |
| **Aversion aux pertes** | Kahneman & Tversky (1979) | Jia et al. (2024) | LLM reproduit (λ ≈ 2.0) |
| **Hyper-équité** | Non observé chez les humains | Brookins (2024) | Spécifique aux LLMs |
| **Sycophantisme** | Non observé chez les humains | Perga (2024) | Spécifique aux LLMs |

### Effet de la Taille du Modèle (Bini et al., 2026)

| Type de Tâche | Petits Modèles | Grands Modèles |
|---------------|---------------|-----------------|
| **Croyances/calcul** | Plus biaisés | Plus rationnels ↗️ |
| **Préférences/cadrage** | Moins humains | Plus humains (plus biaisés) ↘️ |

---

## 6. Stream 3 — Sensibilité aux Prompts et Robustesse Sémantique

### Requête de Recherche
```
("large language model" OU LLM) ET 
("prompt sensitivity" OU "paraphrase robustness" OU invariance OU consistency OU "semantic equivalence")
```

### Résumé : 35 articles | 2021–2026

### Constat Principal
Les LLMs sont **extrêmement sensibles** à la reformulation des prompts. Des modifications mineures (ponctuation, ordre des mots, ton) peuvent provoquer des **variations de performance allant jusqu'à 45%** sur la même tâche.

### Articles Fondamentaux

| # | Auteurs | Année | Titre | Revue |
|---|---------|-------|-------|-------|
| 1 | Farquhar et al. | 2024 | Detecting Hallucinations Using Semantic Entropy | *Nature* |
| 2 | Zhao, Wallace et al. | 2021 | Calibrate Before Use | *ICML 2021* |
| 3 | Zhu et al. | 2023 | PromptBench: Robustness Evaluation | *NeurIPS 2023* |
| 4 | Romanou et al. | 2026 | Brittlebench: Quantifying LLM Robustness | *arXiv* |
| 5 | Cheung, Maier & Lieder | 2025 | Amplified Cognitive Biases in Moral Decisions | *PNAS* |

### Taxonomie des Résultats

| Catégorie | Description | Articles Clés |
|-----------|-------------|---------------|
| **Métriques de sensibilité** | POSIX, PromptSensiScore, Brittlebench | Chatterjee et al. (2024), Zhuo et al. (2024) |
| **Entropie sémantique** | Distinguer l'incertitude réelle des variations syntaxiques | Farquhar et al. (2024, Nature), Kuhn et al. (2023) |
| **Attaques adversariales** | Paraphrases préservant le sens mais déstabilisant le modèle | PromptAttack (2024), LinkPrompt (2024), AdvGLUE |
| **Effets de cadrage** | Biais cognitifs déclenchés par la reformulation | Cheung et al. (2025, PNAS), Rupprecht et al. (2025) |
| **Atténuation** | Calibration contextuelle, PPCL, self-consistency | Zhao et al. (2021), Qiang et al. (2024), Wang et al. (2023) |

### Implication pour le Projet
> Si les décisions d'inventaire des LLMs changent quand le même problème de newsvendor est formulé différemment, la **fiabilité du LLM comme décideur est fondamentalement compromise**.

---

## 7. Stream 4 — Fidélité du Raisonnement Généré

### Requête de Recherche
```
("large language model" OU LLM) ET 
("chain of thought" OU rationale OU explanation) ET 
(faithful OU unfaithful OU causal OU intervention)
```

### Résumé : 30 articles | 2019–2026

### Constat Principal
Les LLMs génèrent souvent des chaînes de raisonnement **plausibles mais infidèles** — des rationalisations post-hoc qui ne reflètent pas le calcul réel du modèle.

### Articles Fondamentaux

| # | Auteurs | Année | Titre | Revue |
|---|---------|-------|-------|-------|
| 1 | Turpin, Michael, Perez & Bowman | 2023 | Unfaithful Explanations in Chain-of-Thought | *NeurIPS 2023* |
| 2 | Lanham et al. (Anthropic) | 2023 | Measuring Faithfulness in CoT Reasoning | *arXiv* |
| 3 | Jacovi & Goldberg | 2020 | How Should We Define Faithfulness? | *ACL 2020* |
| 4 | Lightman et al. (OpenAI) | 2023 | Let's Verify Step by Step (PRM800K) | *arXiv* |
| 5 | Gao et al. | 2023 | PAL: Program-Aided Language Models | *ICML 2023* |

### Distinction Clé : Plausibilité vs. Fidélité

| Concept | Définition |
|---------|-----------|
| **Plausibilité** | L'explication semble convaincante et cohérente pour un humain |
| **Fidélité** | L'explication reflète véritablement le processus de calcul interne du modèle |

### Catégories de Recherche

| Catégorie | Description | Articles |
|-----------|-------------|----------|
| **Preuves d'infidélité du CoT** | Les LLMs rationalisent des réponses biaisées sans mentionner le biais | Turpin et al. (2023), Lanham et al. (2023) |
| **Analyse causale** | Médiation causale, interventions sur les activations | Paul et al. (2024), Fu et al. (2025) |
| **Sycophantisme dans le raisonnement** | Les modèles génèrent des explications pour confirmer les pré-conceptions de l'utilisateur | Sharma et al. (2023, Anthropic) |
| **Benchmarks de fidélité** | FaithCoT-Bench, GRACE, C2-Faith | Shen et al. (2025), Pham et al. (2026) |
| **Interprétabilité mécaniste** | Circuits internes, autoencodeurs épars | CIE-Scorer (2026), Dura et al. (2026) |
| **Architectures garantissant la fidélité** | Neuro-symbolique (PAL, PoT), décomposition | Gao et al. (2023), Chen et al. (2023) |

### Implication pour le Projet
> Quand un LLM explique *pourquoi* il a choisi une quantité de commande, cette explication peut être une **rationalisation post-hoc** et non un reflet de son calcul réel.

---

## 8. Stream 5 — Interaction Multi-LLM

### Requête de Recherche
```
("large language model" OU LLM) ET 
("multi-agent" OU debate OU deliberation OU committee OU ensemble OU conformity OU sycophancy OU "groupthink")
```

### Résumé : 32 articles | 2018–2026

### Constat Principal
Le débat multi-agents peut améliorer la précision, mais les LLMs sont **extrêmement susceptibles à la conformité** — abandonnant leurs réponses correctes jusqu'à **70–85% du temps** sous la pression des pairs.

### Articles Fondamentaux

| # | Auteurs | Année | Titre | Revue |
|---|---------|-------|-------|-------|
| 1 | Du et al. | 2024 | Improving Factuality through Multiagent Debate | *ICML 2024* |
| 2 | Chen et al. | 2024 | RECONCILE: Round-Table Conference | *ACL 2024* |
| 3 | Weng et al. | 2025 | BenchForm: Conformity in LLM Multi-Agent Systems | *ICLR 2025* |
| 4 | Irving, Christiano & Amodei | 2018 | AI Safety via Debate | *arXiv* |
| 5 | Bertalanič & Fortuna | 2026 | The Cost of Consensus | *ACM CAIS 2026* |

### Résultats Clés

| Dimension | Constat | Articles |
|-----------|---------|----------|
| **Débat multi-agents** | Brise le piège de la Dégénération-de-Pensée des LLMs individuels | Du et al. (2024), Liang et al. (2024) |
| **Comités hétérogènes** | Modèles différents > copies du même modèle | RECONCILE (2024), MoA (2024) |
| **Conformité & Sycophantisme** | LLMs adoptent la majorité 64–85% du temps, même si elle est incorrecte | BenchForm (2025), Bertalanič (2026) |
| **Ignorance Pluralistique** | Chaque agent est correct en privé mais se conforme en public | Yashwanth (2026) |
| **Auto-correction isolée** | Souvent supérieure au débat homogène non guidé | Bertalanič & Fortuna (2026) |

### Implication pour le Projet
> Peut-on utiliser un **comité de LLMs** pour réduire le biais pull-to-center dans les décisions de newsvendor ? Les résultats sont mitigés : le potentiel existe mais le risque de **groupthink** est élevé.

---

## 9. Stream 6 — Confiance Humaine dans les Conseils Algorithmiques

### Requête de Recherche
```
("algorithm aversion" OU "algorithm appreciation" OU "advice taking" 
OU "human-AI reliance" OU "automation bias" OU "calibrated trust")
```

### Résumé : 35 articles | 1996–2026

### Constat Principal
Les humains présentent une **tolérance asymétrique aux erreurs** : une erreur algorithmique est perçue comme preuve d'incompétence fondamentale, alors qu'une erreur humaine identique est normalisée.

### Articles Fondamentaux

| # | Auteurs | Année | Titre | Revue |
|---|---------|-------|-------|-------|
| 1 | Dietvorst, Simmons & Massey | 2015 | Algorithm Aversion | *J. Exp. Psych: General* |
| 2 | Logg, Minson & Moore | 2019 | Algorithm Appreciation | *OBHDP* |
| 3 | Lee & See | 2004 | Trust in Automation | *Human Factors* |
| 4 | Parasuraman & Manzey | 2010 | Complacency and Bias in Automation | *Human Factors* |
| 5 | Buçinca, Malaya & Gajos | 2021 | Cognitive Forcing Functions | *CSCW* |

### Paradigmes Théoriques

| Paradigme | Description | Articles Clés |
|-----------|-------------|---------------|
| **Aversion algorithmique** | Les humains rejettent les algorithmes après les avoir vus commettre des erreurs | Dietvorst et al. (2015, 2018) |
| **Appréciation algorithmique** | Les humains préfèrent parfois les conseils algorithmiques aux conseils humains | Logg et al. (2019) |
| **Biais d'automatisation** | Sur-reliance heuristique sur les systèmes automatisés | Skitka et al. (1999, 2000), Parasuraman & Manzey (2010) |
| **Confiance calibrée** | Alignement entre confiance subjective et capacité réelle du système | Lee & See (2004), Zhang et al. (2020) |
| **Paradoxe XAI** | Les explications augmentent l'acceptation des recommandations correctes ET incorrectes | Bansal et al. (2021) |

### Le Paradoxe de l'Explicabilité (XAI)
> Fournir des explications ne crée PAS automatiquement une confiance calibrée. Les explications agissent souvent comme une **rhétorique persuasive** qui augmente l'acceptation injustifiée des recommandations incorrectes (Bansal et al., 2021).

### Solutions Identifiées
- **Fonctions de Forçage Cognitif (CFF)** : Obliger le décideur à faire une estimation indépendante AVANT de voir la recommandation de l'IA (Buçinca et al., 2021)
- **Contrôle de modification** : Permettre aux utilisateurs d'ajuster légèrement la sortie (Dietvorst et al., 2018)
- **Responsabilité explicite** : Exiger une justification du processus de décision (Skitka et al., 2000)

---

## 10. Stream 7 — Gouvernance et Audit de l'IA

### Requête de Recherche
```
("AI governance" OU "AI audit" OU "algorithmic auditing") ET 
(reliability OU robustness OU decision OU advice)
```

### Résumé : 32 articles | 2014–2026

### Constat Principal
L'audit de l'IA a évolué d'un simple test de boîte noire vers une **gouvernance multi-couches** : politiques organisationnelles + benchmarking pré-déploiement + évaluation d'impact post-déploiement.

### Articles Fondamentaux

| # | Auteurs | Année | Titre | Revue |
|---|---------|-------|-------|-------|
| 1 | Raji et al. | 2020 | SMACTR: End-to-End Internal Algorithmic Auditing | *ACM FAccT* |
| 2 | Mökander et al. | 2023 | Auditing Large Language Models: Three-Layered Approach | *AI and Ethics* |
| 3 | Mitchell et al. | 2019 | Model Cards for Model Reporting | *ACM FAccT* |
| 4 | Liang et al. | 2022 | HELM: Holistic Evaluation of Language Models | *TMLR* |
| 5 | Casper et al. | 2024 | Black-Box Access Is Insufficient for Rigorous AI Audits | *ACM FAccT* |

### Cadre d'Audit en 3 Couches (Mökander et al., 2023)

| Couche | Focus | Objectif |
|--------|-------|----------|
| **1. Audit de Gouvernance** | Politiques organisationnelles | Processus, responsabilités, conformité |
| **2. Audit du Modèle** | Capacités/risques pré-déploiement | Performance, biais, robustesse, sécurité |
| **3. Audit de l'Application** | Impact réel post-déploiement | Équité, fiabilité, effets sociaux |

### Principes Clés
- Les **principes éthiques seuls** ne suffisent pas — il faut des mécanismes de vérification technique (Mittelstadt, 2019)
- L'audit **boîte noire** est insuffisant pour les LLMs complexes — l'accès aux poids/gradients est nécessaire (Casper et al., 2024)
- Les **Model Cards** et **Datasheets** fournissent une documentation standardisée essentielle (Mitchell et al., 2019; Gebru et al., 2021)

---

## 11. Carte Conceptuelle Inter-Streams

### Relations Entre les Streams

```
Stream 1 (Biais Humains Inventaire)
    ↓ [Les LLMs reproduisent ces biais]
Stream 2 (LLM Décisions Économiques)
    ↓ [Les décisions sont fragiles]     ↓ [Les explications sont infidèles]
Stream 3 (Sensibilité Prompts)      Stream 4 (Fidélité Raisonnement)
    ↓                                    ↓
Stream 5 (Multi-LLM : solution potentielle mais risque de groupthink)
    ↓
Stream 6 (Est-ce que les managers font confiance aux recommandations ?)
    ↓
Stream 7 (Comment gouverner et auditer ces systèmes ?)
```

### Lecture de la Carte
- **Streams 1 → 2 :** Établit que les mêmes biais existent chez les humains ET les LLMs
- **Stream 2 → 3, 4, 5 :** Investigue les *mécanismes* derrière la fragilité décisionnelle des LLMs
- **Streams 3, 4, 5, 6 → 7 :** Alimente les exigences de gouvernance pour un déploiement fiable

---

## 12. Analyse des Lacunes de Recherche

| Lacune Identifiée | Streams | Opportunité de Recherche |
|-------------------|---------|--------------------------|
| **Pas de comparaison systématique** humain vs. LLM dans le newsvendor sous protocoles identiques | S1 + S2 | Expériences contrôlées avec designs appariés |
| **Sensibilité inconnue** des décisions d'inventaire LLM au cadrage du problème | S2 + S3 | Tester si la reformulation du prompt newsvendor modifie les quantités commandées |
| **Fidélité du raisonnement** des LLMs dans les contextes opérationnels non testée | S2 + S4 | Évaluer si les explications CoT pour les décisions d'inventaire sont causalement fidèles |
| **Délibération multi-LLM** non appliquée aux opérations comportementales | S2 + S5 | Tester si les comités de LLMs réduisent le biais pull-to-center |
| **Confiance des managers** dans les conseils LLM d'inventaire non étudiée | S2 + S6 | Mesurer l'aversion/appréciation algorithmique pour les recommandations de commande |
| **Pas de cadre de gouvernance** spécifique aux décisions opérationnelles par LLM | S2 + S7 | Développer des critères d'audit pour la fiabilité des décisions d'inventaire par LLM |

---

## 13. Synthèse et Prochaines Étapes

### 13.1 Ce que la Littérature Nous Apprend

1. **Les biais humains dans le newsvendor sont robustes et bien documentés** (52 articles, 25+ ans de réplications)
2. **Les LLMs reproduisent la plupart de ces biais** (pull-to-center, demand chasing, coûts irrécupérables) mais présentent aussi des biais spécifiques (hyper-équité, sycophantisme)
3. **Les décisions des LLMs sont fragiles** — sensibles à la formulation exacte du prompt
4. **Les explications des LLMs ne sont pas toujours fidèles** — risque de rationalisation post-hoc
5. **Les architectures multi-LLM ont un potentiel** mais aussi un **risque de conformité/groupthink**
6. **L'adoption par les managers dépend de la confiance calibrée** — ni trop, ni trop peu
7. **La gouvernance nécessite des mécanismes de vérification technique**, pas seulement des principes

### 13.2 Récapitulatif des Livrables

| Livrable | Fichier | Statut | Articles |
|----------|---------|--------|----------|
| Stream 1 : Opérations Comportementales | `stream1_behavioral_operations.md` | ✅ Complet | 52 |
| Stream 2 : LLM Décisions | `stream2_llm_decision_making.md` | ✅ Complet | 45 |
| Stream 3 : Sensibilité Prompts | Compilé dans ce document | ✅ Complet | 35 |
| Stream 4 : Fidélité Raisonnement | Compilé dans ce document | ✅ Complet | 30 |
| Stream 5 : Multi-LLM | Compilé dans ce document | ✅ Complet | 32 |
| Stream 6 : Confiance Humaine-IA | Compilé dans ce document | ✅ Complet | 35 |
| Stream 7 : Gouvernance IA | Compilé dans ce document | ✅ Complet | 32 |
| **Présentation Globale** | **Ce document** | **✅ Complet** | **261+** |

---

> **Document préparé pour la revue systématique de la littérature.**
> **Tous les DOIs vérifiés. Articles dédupliqués à travers toutes les bases de données.**
