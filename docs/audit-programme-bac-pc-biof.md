# Audit conformité curriculum — BAC 2BAC PC BIOF (Maroc)

> Référence officielle : `backend/cours 2bac pc/cadres de references 2BAC PC/*.json`
> (Cadres de référence officiels du ministère, 2BAC Sciences Physiques BIOF)

## 1. Périmètre officiel par matière (source de vérité)

### Mathématiques (coef 7) — `cadre-de-reference-de-l-examen-national-maths-sciences-experimentales.json`
**Domaine 1 — Analyse (≈ 55%)**
- Suites numériques (≈ 15%)
- Continuité, dérivation et étude de fonctions, log/exp, équations différentielles **y' = ay + b** (1.2.23) **et y'' + ay' + by = 0** (1.2.24) (≈ 25%)
- Calcul intégral — primitives, **intégration par parties** (1.3.1), aires, volumes de révolution (≈ 15%)

**Domaine 2 — Algèbre & Géométrie (≈ 45%)**
- Produit scalaire et géométrie dans l'espace V₃ (≈ 15%)
- Nombres complexes — module, argument, transformations (translation, homothétie, rotation) (≈ 20%)
- Probabilités — calcul, conditionnelles, indépendance, **loi binomiale (2.5.6)** (≈ 10%)

### Physique (sur 67% de l'épreuve PC, coef 7)
- Mécanique 27% — cinématique, lois de Newton, mouvements dans champs uniformes, oscillateurs
- Électricité 21% — RC, RL, RLC, oscillations
- Ondes 11% — mécaniques, lumière, diffraction
- Nucléaire 8% — radioactivité, fission/fusion

### Chimie (sur 33% de l'épreuve PC)
- SD1 — Transformations rapides/lentes (cinétique macroscopique, suivi temporel)
- SD2 — Transformations non totales (acide-base Brönsted, Ka/pKa, dosage)
- SD3 — Sens d'évolution (Qr/K, piles, électrolyse, quantité d'électricité Q = I·t)
- SD4 — Contrôle de l'évolution (**estérification**, hydrolyse, **saponification**, anhydrides, catalyse)

### SVT (coef 5) — `cadre-de-reference-de-l-examen-national-svt-sciences-physiques (1).json`
- Domaine 1 (25%) — Consommation matière organique : respiration, fermentation, muscle strié squelettique, ATP
- Domaine 2 (25%) — Information génétique : ADN, mitose, méiose, brassage, code génétique, synthèse protéines
- Domaine 3 (25%) — Utilisation matières organiques/inorganiques : déchets, pollution, recyclage, radioactivité environnementale
- Domaine 4 (25%) — Géodynamique interne : subduction/collision, déformations tectoniques, métamorphisme, granitisation

## 2. Sujets HORS-PROGRAMME fréquemment confondus

| Matière | Hors-programme | Programme d'origine |
|---|---|---|
| **Maths** | Algèbre linéaire, matrices, déterminants, structures (groupes/anneaux), arithmétique modulaire, courbes paramétrées, séries numériques, intégrales impropres, **loi normale/Poisson/exponentielle**, dérivées partielles | 2BAC SM ou supérieur |
| **Physique** | Relativité, **thermodynamique** (1er/2e principe), **équations de Maxwell**, théorème d'Ampère, optique géométrique (lentilles), Schrödinger, mécanique des fluides | 2BAC SM ou 1ère année |
| **Chimie** | Chimie organique générale (alcanes/alcènes/alcools/aldéhydes/cétones standalone), nomenclature IUPAC complète, **mécanismes SN1/SN2/E1/E2**, **RMN/IR**, thermochimie, cristallographie, **équation de Nernst détaillée**, **Henderson-Hasselbalch** | Supérieur ou SM |
| **SVT** | **Photosynthèse**, **immunologie**, **communication nerveuse** (neurone/synapse), **régulation glycémie** (insuline/glucagon), **reproduction humaine**, évolution, écosystèmes/chaînes alimentaires | **2BAC SVT track**, PAS PC |

## 3. Bug détecté & corrigé

**Bug critique #1** — `backend/app/services/llm_service.py` `_OFF_PROGRAM_TOPICS["Mathematiques"]` listait :
> "équations différentielles d'ordre 2 ou non linéaires (hors PC ; PC voit seulement y' = ay + b en physique)"

**FAUX.** Le cadre officiel exige explicitement la résolution de **y'' + ay' + by = 0** (objectif 1.2.24).
**Correction appliquée** : reformulé en *« équations différentielles non linéaires ou d'ordre > 2 (PC voit UNIQUEMENT y' = ay + b et y'' + ay' + by = 0 — ces deux-là SONT au programme) »*.

## 4. Renforcements appliqués au LLM

### Source de vérité (déjà en place, conservée)
- `topic_atlas_service.OFFICIAL_WEIGHTS` : poids officiels par sous-domaine
- `llm_service._OFF_PROGRAM_TOPICS` : liste des hors-programme par matière (étendue de 7→9 entrées par matière)
- `llm_service._build_official_program_block()` : injection déterministe du programme + liste hors-programme dans CHAQUE prompt système, pour CHAQUE matière détectée

### Nouveau : protocole SCOPE-CHECK explicite
Ajouté dans **`LIBRE_MODE_PROMPT`** et **`SYSTEM_PROMPT_TEMPLATE`** :
1. Identifier la matière
2. Vérifier dans le bloc `[PROGRAMME OFFICIEL]` si le sujet est listé ou hors-programme
3. **Si hors-programme** → REFUS standardisé avec format imposé : *« 🚫 Ce sujet n'est PAS au programme … je peux t'expliquer plutôt : [alternatives au programme] »* — aucun cours/formule/exercice produit
4. Si au programme → enseigner normalement
5. Si absent du bloc officiel ET du RAG → traiter comme hors-programme

### Listes hors-programme étendues
- **Maths** : +5 entrées (loi normale, intégrales impropres, calcul matriciel, séries, dérivées partielles)
- **Chimie** : +4 entrées (nomenclature IUPAC, mécanismes SN/E, oxydoréduction Nernst détaillée, Henderson-Hasselbalch)
- **Physique/SVT** : déjà couvertes

## 5. Test harness automatisé

**Fichier** : `backend/scripts/audit_curriculum_compliance.py`
- 47 cas piégeux (mix `expect=refuse` et `expect=answer`)
- Construit le system prompt via `LLMService.build_libre_prompt()` (= production)
- Appelle DeepSeek directement (température 0.3 pour reproductibilité)
- Détection regex : motifs FORBIDDEN (le LLM a expliqué hors-programme) + REQUIRED (formule de refus présente / contenu attendu présent)
- Génère `backend/scripts/audit_curriculum_report.md`

**Usage**
```bash
cd backend
python scripts/audit_curriculum_compliance.py                # tous les cas
python scripts/audit_curriculum_compliance.py --limit 10     # rapide
python scripts/audit_curriculum_compliance.py --subject SVT  # une matière
```

**Coût estimé** : ~47 appels × ~600 tokens out × ~3000 tokens in ≈ 0.05 USD par run complet (DeepSeek).

## 6. Recommandations futures

1. **Intégrer le harnais en CI** (action GitHub manuelle) avec seuil de pass-rate ≥ 90% sur la branche main.
2. **Étendre à 100+ cas** en ajoutant des questions piégeuses extraites des examens nationaux passés (`backend/banque dexerciecs corrigés et filtrer/`).
3. **Tester aussi le mode `coaching` / `cours structuré`** (`SYSTEM_PROMPT_TEMPLATE`) qui partage maintenant le même SCOPE-CHECK.
4. **Surveiller le RAG** : si `cadre_reference_service` injecte parfois des notes prioritaires venant d'un autre track (PC vs SVT track), filtrer côté retrieval par `track == "PC"`.
5. **Ajouter une métrique runtime** (Prometheus/Sentry) qui compte les occurrences du préfixe « 🚫 Ce sujet n'est PAS au programme » dans les réponses : pic = élèves qui demandent du hors-programme, signal pédagogique utile.

