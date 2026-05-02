# Plan SEO — Actions concrètes pour Moalim

> Objectif : passer d'un site invisible à un site cité dans **Google, Bing, ChatGPT, Perplexity, Claude**.

---

## 1. Google Search Console (obligatoire, 15 min)

### Étape 1 — Vérifier la propriété

1. Va sur https://search.google.com/search-console
2. Clique sur **Ajouter une propriété** → choisis **Préfixe de l'URL** → entre `https://moalim.online/`
3. Télécharge le fichier HTML de vérification fourni par Google (ex : `google<hash>.html`)
4. Place-le dans `frontend/public/` (il sera servi à la racine du site)
5. Redéploie puis clique **Valider** dans Search Console

**Alternative** : si tu as accès au DNS de `moalim.online`, la vérification via enregistrement TXT est plus propre (fonctionne pour tous les sous-domaines).

### Étape 2 — Soumettre le sitemap

1. Dans Search Console → menu gauche **Sitemaps**
2. Entre : `sitemap.xml`
3. Clique **Envoyer**
4. Google crawle tes 13 URLs dans les 24-72h

### Étape 3 — Demander l'indexation manuelle des articles clés

Pour chaque article stratégique :
1. Copie l'URL (ex : `https://moalim.online/blog/seuils-admission-grandes-ecoles-maroc-2026.html`)
2. Colle-la dans la barre **Inspection de l'URL** en haut de Search Console
3. Clique **Demander une indexation**
4. Répète pour les 10 articles

**Priorités d'indexation manuelle** (ROI maximum) :
1. `/` (homepage)
2. `/blog/`
3. `/blog/seuils-admission-grandes-ecoles-maroc-2026.html`
4. `/blog/examen-national-bac-maroc-2026.html`
5. `/blog/calcul-moyenne-bac-maroc.html`

---

## 2. Bing Webmaster Tools + IndexNow

### Pourquoi Bing ?

- **Bing est la source N°1 de ChatGPT Search**
- **DuckDuckGo** et **Yahoo** utilisent aussi l'index Bing
- **IndexNow** est un protocole soutenu par Microsoft/Yandex qui notifie les moteurs en temps réel

### Étape 1 — Bing Webmaster

1. Va sur https://www.bing.com/webmasters
2. Connecte-toi avec le même compte que Search Console
3. Clique **Importer depuis Google Search Console** (tout est automatique si Google est déjà validé)
4. Sinon, ajoute manuellement `https://moalim.online` et vérifie via balise meta ou fichier XML
5. Soumets le sitemap : `https://moalim.online/sitemap.xml`

### Étape 2 — IndexNow (notifications instantanées)

Ta clé IndexNow a déjà été générée et placée dans `frontend/public/` :

- **Clé** : voir le fichier `frontend/public/<ta-cle>.txt`
- **URL du fichier clé** : `https://moalim.online/<ta-cle>.txt`

Pour notifier Bing/Yandex quand tu publies un nouvel article :

```powershell
# PowerShell — à exécuter à chaque nouvelle publication
$key = Get-Content "frontend/public/INDEXNOW_KEY.txt" -TotalCount 1
$body = @{
    host = "moalim.online"
    key = $key
    keyLocation = "https://moalim.online/$key.txt"
    urlList = @(
        "https://moalim.online/blog/nouvel-article.html"
    )
} | ConvertTo-Json

Invoke-RestMethod -Uri "https://api.indexnow.org/IndexNow" -Method Post -Body $body -ContentType "application/json"
```

---

## 3. Requêtes cibles & réalisme SEO

### Requêtes où tu PEUX ranker #1 (faible concurrence)

| Requête | Volume/mois (Maroc) | Concurrence | Délai estimé |
|---|---|---|---|
| `seuil fmp rabat 2026` | ~500 | 🟢 Faible | 2-3 mois |
| `seuil ensa agadir 2026` | ~300 | 🟢 Faible | 2-3 mois |
| `calcul moyenne 2 bac svt` | ~800 | 🟢 Faible | 3-4 mois |
| `correction bac svt 2025 session normale` | ~1200 | 🟡 Moyenne | 4-6 mois |
| `loi hardy weinberg exercice corrigé` | ~600 | 🟢 Faible | 2-3 mois |
| `dosage acide base bac méthode` | ~400 | 🟢 Faible | 2-3 mois |
| `cycle krebs bac svt schéma` | ~500 | 🟢 Faible | 2-3 mois |

### Requêtes où tu ne rankeras PAS avant 1-2 ans

- `bac maroc` (concurrents : taalimnet, 9rayti, bac2.ma)
- `annales bac` (concurrents nationaux installés)
- `etudes maroc` (portails gouvernementaux)

**Stratégie** : capturer des dizaines de requêtes longue-traîne (5k-10k visites/mois cumulées) plutôt que tenter l'impossible sur les grosses requêtes.

---

## 4. Citations IA (GEO) — ChatGPT, Perplexity, Claude

### Points forts que tu as déjà

✅ `llms.txt` présent à la racine
✅ `robots.txt` autorise GPTBot, ClaudeBot, PerplexityBot, Google-Extended
✅ JSON-LD `Article`, `FAQPage`, `HowTo` dans chaque blog
✅ Contenu factuel, dates, chiffres, tableaux → les LLM adorent

### Ce qu'il faut ajouter

1. **Mentionner "Moalim" dans Wikipedia fr-MA** (si tu as assez de notoriété pour y prétendre — sinon skip)
2. **Citations externes** : faire parler de Moalim sur 3-5 sites autoritaires marocains (forums lycée, blogs profs, LinkedIn)
3. **Structurer chaque article avec des Questions/Réponses explicites** — c'est ce que Perplexity extrait en priorité

### Test de visibilité IA

Dans 3-4 semaines, teste ces prompts sur ChatGPT et Perplexity :
- « Quel est le seuil d'admission à la FMP de Rabat en 2026 ? »
- « Comment calcule-t-on la moyenne du BAC marocain ? »
- « Quelles sont les dates de l'examen national BAC 2026 au Maroc ? »

Si Moalim est cité comme source → victoire GEO.

---

## 5. Plan backlinks (autorité de domaine)

### Liens faciles à obtenir (semaine 1-2)

| Plateforme | Action | Impact |
|---|---|---|
| **LinkedIn** | Post pro avec lien vers chaque blog | 🟡 Moyen |
| **Facebook Groupes BAC Maroc** | Partage d'articles (avec valeur ajoutée, pas spam) | 🟢 Fort |
| **Reddit r/Morocco** | Poster un article utile (seuils, calcul moyenne) | 🟢 Fort |
| **Forums étudiants** (taalimnet, Bac2 forum) | Répondre à des questions en citant un blog comme ressource | 🟢 Fort |
| **Wikipédia fr** | Ajouter Moalim comme ressource externe (si accepté) | 🔴 Très fort |
| **Annuaires éducation Maroc** | Inscription gratuite | 🟡 Moyen |

### Liens intermédiaires (mois 2-3)

- **Articles invités** sur blogs éducation marocains (contact LinkedIn des auteurs)
- **Interview podcast** éducation (Moroccan Academy, BacHelp, etc.)
- **Partenariat avec lycées privés** : logo + backlink en échange d'accès gratuit pour leurs élèves

### Liens premium (mois 4-6)

- **Relations presse** : communiqué à Hespress, Médias24, TelQuel sur l'IA éducative au Maroc
- **Reportage TV/radio** : si tu peux obtenir un passage 2M/Medi1, le backlink officiel vaut +30 DA (autorité de domaine)

---

## 6. Calendrier de publication (cadence idéale)

- **1 article longue-traîne par semaine** pendant 3 mois
- **1 post LinkedIn par jour** (3 jours par article : teaser, extrait, citation client)
- **1 post Facebook/Instagram** à chaque nouvel article
- **Thread X/Twitter** résumant les points clés de chaque article

**Résultat attendu à 6 mois** : 30 à 50 articles publiés, ~40 000 visites organiques/mois, ~500 inscriptions/mois sur Moalim.

---

## 7. Outils à installer

| Outil | Gratuit ? | Usage |
|---|---|---|
| Google Search Console | ✅ | Suivi indexation, requêtes, clics |
| Bing Webmaster | ✅ | Idem pour Bing + ChatGPT |
| Google Analytics 4 ou Plausible | ✅ (Plausible en libre) | Mesure trafic |
| Ubersuggest / AnswerThePublic | ⚠️ Freemium | Trouver nouvelles requêtes |
| Ahrefs Webmaster Tools | ✅ | Analyse backlinks gratuite pour tes sites |

---

## Prochaine étape

Une fois les 10 nouveaux articles longue-traîne publiés :
1. Soumets chaque URL manuellement dans Search Console (5 min)
2. Notifie Bing via IndexNow (script PowerShell ci-dessus)
3. Partage les 10 articles sur LinkedIn + 2 groupes Facebook BAC
4. Attends 2-4 semaines et vérifie le positionnement sur les requêtes cibles
