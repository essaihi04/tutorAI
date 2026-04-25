# Pipeline Batch d'extraction d'examens BAC Maroc

Pipeline de traitement batch pour extraire et structurer les examens nationaux SVT (extensible aux autres matières).

## Architecture

```
┌──────────────────────────────────────────────────────────────┐
│  1. Vous déposez les PDFs :                                   │
│     pdfs/sujet.pdf + pdfs/correction.pdf                     │
│                                                                │
│  2. batch_ocr.py                                              │
│     → Rend les pages du PDF en JPEG (PyMuPDF)                │
│     → OCR Mistral en parallèle → extraction.json              │
│                                                                │
│  3. Vous découpez les documents visuels et placez             │
│     les crops dans assets/docXpY.png (X=doc#, Y=page#)       │
│                                                                │
│  4. batch_build_json.py                                       │
│     → Vision Mistral sur chaque crop → description           │
│     → DeepSeek LLM → exam.json structuré                      │
│     → Met à jour index.json                                   │
│     → [AUTO] verify_exam.py → verification_report.md          │
│                                                                │
│  5. validate_exams.py (check rapide)                          │
│     → Vérifie cohérence (points, types, assets)               │
│                                                                │
│  6. verify_exam.py (audit complet)                            │
│     → Compare PDF OCR ↔ JSON via DeepSeek                     │
│     → Détecte omissions, troncatures, fautes OCR              │
│     → Rapport : verification_report.md + verification.json    │
└──────────────────────────────────────────────────────────────┘
```

## Structure dossier par examen

```
backend/data/exams/svt/2019-rattrapage/
├── pdfs/
│   ├── sujet.pdf              ← vous déposez
│   └── correction.pdf         ← vous déposez (optionnel)
├── pages/                     ← auto (étape 2)
│   ├── sujet_p1.jpg
│   ├── sujet_p2.jpg
│   ├── correction_p1.jpg
│   └── ...
├── assets/                    ← vous découpez et placez
│   ├── doc1p1.png             ← doc 1 de la page 1 du sujet
│   ├── doc2p1.png
│   ├── doc1p2.png
│   └── ...
├── extraction.json            ← auto (texte OCR + descriptions)
├── exam.json                  ← auto (JSON structuré)
├── verification_report.md     ← auto (rapport lisible)
├── verification.json          ← auto (données structurées)
└── README.md                  ← instructions
```

## Convention de nommage des documents

**`docXpY.png`** où :
- **X** = numéro du document dans la page (1, 2, 3...)
- **Y** = numéro de la page PDF du sujet (1, 2, 3...)

Exemples :
- `doc1p1.png` = Document 1 de la page 1
- `doc2p1.png` = Document 2 de la page 1
- `doc1p2.png` = Document 1 de la page 2
- `doc3p2.png` = Document 3 de la page 2

Les scripts trient automatiquement par page puis par index de document, donc le nommage global dans `exam.json` sera `Document 1, 2, 3...` dans l'ordre d'apparition.

## Commandes

### Installer les dépendances Python

```bash
pip install PyMuPDF httpx python-dotenv
```
(PyMuPDF est déjà dans `requirements.txt`)

### Variables d'environnement requises (backend/.env)

```env
MISTRAL_API_KEY=...
DEEPSEEK_API_KEY=...
DEEPSEEK_API_URL=https://api.deepseek.com/chat/completions
DEEPSEEK_MODEL=deepseek-chat
```

### Étape A — OCR batch

```bash
# Tous les examens SVT qui ont pdfs/ mais pas extraction.json
python backend/scripts/batch_ocr.py svt

# Un examen spécifique
python backend/scripts/batch_ocr.py svt/2019-rattrapage

# Forcer le re-traitement
python backend/scripts/batch_ocr.py --force svt/2019-rattrapage
```

### Étape B — Découpage manuel

Ouvrez chaque `pages/sujet_pN.jpg` dans Photoshop / Paint / Gimp, découpez chaque document visuel (graphiques, schémas, tableaux) et exportez en PNG :
- `assets/doc1p1.png`, `assets/doc2p1.png`, etc.

**Astuce** : Windows Snipping Tool (Win+Shift+S) + rename rapide.

### Étape C — Vision + JSON structuré

```bash
# Tous les examens SVT prêts (ayant extraction.json + assets/doc*p*.png)
python backend/scripts/batch_build_json.py svt

# Un examen spécifique
python backend/scripts/batch_build_json.py svt/2019-rattrapage

# Forcer même si exam.json existe
python backend/scripts/batch_build_json.py --force svt/2019-rattrapage
```

### Étape D — Validation rapide (structure)

```bash
python backend/scripts/validate_exams.py svt
```

Vérifie :
- Métadonnées (year, session) cohérentes avec le nom du dossier
- Σ des points des parties = `total_points`
- Types de questions valides (`open`, `qcm`, `vrai_faux`, `association`, `schema`)
- QCM ont `choices` + `correct_answer`
- Documents référencés dans `exam.json` existent dans `assets/`

### Étape E — Audit comparatif PDF ↔ JSON (auto après batch_build_json)

```bash
# Relancé automatiquement à la fin de batch_build_json.py
python backend/scripts/verify_exam.py svt/2019-rattrapage

# Sans appel LLM (juste checks structurels)
python backend/scripts/verify_exam.py svt/2019-rattrapage --no-llm

# Pour tous les examens svt ayant exam.json
python backend/scripts/verify_exam.py svt
```

Génère `verification_report.md` (lisible) + `verification.json` (structuré) avec :

**Checks structurels (sans LLM)** :
- Métadonnées cohérentes
- Σ points partie/exercice = déclaré
- Crops dans `assets/` tous référencés + pas de référence orpheline
- Numéros de questions détectés dans OCR vs JSON

**Check sémantique (DeepSeek)** :
- Qualité globale (`excellent`/`good`/`fair`/`poor`)
- Pourcentage de couverture du PDF
- Problèmes critiques : questions manquantes, troncatures, mauvaise classification de type
- Problèmes mineurs : fautes OCR propagées (`Lexiviat` vs `Lixiviat`), corrections incomplètes
- Suggestions d'amélioration

Le LLM compare :
- Texte OCR du sujet (20k chars)
- Texte OCR de la correction (12k chars)
- Résumé structurel du JSON (avec QCM choices, items association, corrections)

Coût par audit : ~1 appel DeepSeek (~$0.01).

## Performance & parallélisation

| Étape | Parallélisme | Concurrence max | Temps ~10 exams |
|---|---|---|---|
| OCR | par page | 4 | 2-4 min |
| Vision | par document | 3 | 1-2 min |
| DeepSeek | par exam (P1+P2 //) | 1 | 3-5 min |
| **Total** | — | — | **~10 min** |

Les limites de concurrence (`SEM`) peuvent être ajustées dans chaque script selon votre plan Mistral/DeepSeek.

## Rate-limit Mistral OCR

Le plan gratuit Mistral est limité à ~1 req/s. Si vous avez beaucoup d'erreurs `429 Too Many Requests`, réduisez `MAX_CONCURRENT_OCR = 2` dans `batch_ocr.py`.

## Workflow complet recommandé

```bash
# 1. Déposer les PDFs dans chaque dossier svt/YYYY-session/pdfs/
# 2. OCR tous les examens en une fois
python backend/scripts/batch_ocr.py svt

# 3. Découper manuellement les documents (étape la plus longue ~30min/10 exams)
#    → Placer dans assets/ avec nommage docXpY.png

# 4. Générer tous les exam.json en une fois
python backend/scripts/batch_build_json.py svt

# 5. Valider
python backend/scripts/validate_exams.py svt

# 6. Tester dans l'UI
cd frontend && npm run dev
```
