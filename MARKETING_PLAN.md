# Plan Marketing & Backlinks — Moalim BAC 2026

> Objectif : 10 000 visites uniques / mois sur moalim.online d'ici septembre 2026 (saison BAC).

---

## 📅 Calendrier réaliste

| Période | Action | KPI cible |
|---|---|---|
| **Semaine 1** | Setup GSC + Bing + IndexNow | Indexation 100% des URLs |
| **Semaine 2-4** | Acquisition backlinks (groupes FB, Reddit) | 20-50 backlinks |
| **Mois 2** | Création contenu social (TikTok, Insta) | 1 000 abonnés |
| **Mois 3** | Partenariat lycées + témoignages | 5 témoignages réels |
| **Mois 4-6** | Optimisation conversion + SEO continu | 500-2 000 visites/jour |

---

## 1. SETUP TRACKING (obligatoire — semaine 1)

### Google Search Console (5 min)

1. Va sur https://search.google.com/search-console
2. **Ajouter une propriété** → `https://moalim.online/`
3. Vérification : le fichier `a7f3c89e2d4b16058fc91ab3e7d204cb.txt` est déjà en place. Sinon télécharge le fichier de vérif Google et place-le dans `frontend/public/`
4. Soumets le sitemap : `sitemap.xml`
5. **Inspection URL** → demande l'indexation manuelle de :
   - `/` (home)
   - `/blog/predictions-bac-2026-maroc.html` ⭐ priorité absolue
   - `/blog/correction-bac-svt-2025-session-normale.html`
   - `/blog/correction-bac-physique-2025-session-normale.html`
   - `/blog/seuil-fmp-rabat-casablanca-2026.html`
   - `/about.html`

### Bing Webmaster Tools (3 min)

1. https://www.bing.com/webmasters
2. **Importer depuis Google Search Console** (1 clic)
3. Bing alimente **ChatGPT Search**, **Copilot**, **DuckDuckGo**

### Google Analytics 4 (10 min)

1. https://analytics.google.com → créer compte → propriété `moalim.online`
2. Récupère le tag `G-XXXXXXXXXX`
3. Ajoute dans `frontend/index.html` (à demander à Cascade pour intégration propre)

---

## 2. BACKLINKS — Plan d'attaque ciblé (semaine 2-4)

### A. Reddit (effort : 30 min, impact : très haut)

**Subreddits cibles** :
- r/Morocco (1.2M membres)
- r/MoroccoFinance (250k)
- r/Casablanca (50k)
- r/Rabat (30k)

**Posts à publier** :

1. **Subreddit : r/Morocco**
   - Titre : "J'ai analysé 20 ans d'examens BAC marocains, voici ce qui devrait tomber en 2026"
   - Contenu : résumé de l'article, lien vers `/blog/predictions-bac-2026-maroc.html`
   - Timing : dimanche soir (peak engagement)

2. **r/Morocco**
   - Titre : "Dépression post-BAC : prof de SVT, je lance une plateforme IA gratuite pour aider les élèves"
   - Histoire personnelle + lien

3. **r/MoroccoFinance** ou **r/Morocco**
   - Titre : "Seuil ENSA et FMP 2026 : voici les notes minimales attendues"
   - Lien vers `/blog/seuil-fmp-rabat-casablanca-2026.html`

⚠️ **Règle Reddit** : 90% valeur, 10% promo. Pas de spam direct.

### B. Facebook Groups (effort : 1h, impact : très haut au Maroc)

**Groupes cibles à rejoindre** (recherche FB "Bac Maroc" / "2bac" / "élèves Maroc") :

| Groupe | Taille approx |
|---|---|
| Bac Maroc 2026 | 50k+ |
| 2 BAC SVT Maroc | 30k+ |
| 2 BAC PC Maroc | 25k+ |
| Bachelier·es du Maroc | 100k+ |
| Orientation post-bac Maroc | 80k+ |
| Étudiants Maroc | 200k+ |

**Stratégie** :
1. Rejoindre 10 groupes (ne pas spammer)
2. **Pendant 2 semaines** : commenter avec valeur sur 5 posts/jour, pas de lien direct
3. **Semaine 3** : poster un lien blog (1 par groupe, espacé)
4. Créer une **page FB Moalim** pour partager les articles

**Posts type** :
- "🎯 Prédictions BAC SVT 2026 : analyse de 20 ans d'examens nationaux. Voici les chapitres probables…" → lien
- "📊 Seuils ENSA 2026 : voici les notes minimales par école…" → lien
- "🧬 Cycle de Krebs expliqué simplement pour le BAC" → lien

### C. TikTok (effort : moyen, impact : explosif si ça marche)

**Format gagnant pour le BAC** :
- Vidéos de 30-60 secondes
- Hook fort : "Le piège #1 de la génétique au BAC SVT"
- Contenu : explication courte + appel à l'action « lien dans bio »

**Calendrier** :
- 2 vidéos/semaine pendant 8 semaines
- Sujets : un chapitre par vidéo (Krebs, subduction, Hardy-Weinberg, dosage…)
- Lier toujours vers un article blog correspondant

**Compte** : @moalim.bac ou @moalim.online

### D. YouTube Shorts (recyclage des TikToks)

Même contenu que TikTok, repositionné pour SEO :
- Titre optimisé : "Cycle de Krebs BAC SVT Maroc 2026 - explication 1 minute"
- Description : lien vers `/blog/cycle-krebs-explication-bac-svt.html`
- Tags : `#bac2026 #svt #maroc #cyclekrebs #moalim`

### E. Quora (effort : 30 min, impact : long terme)

Réponds aux questions suivantes (recherche sur Quora.com) :
- "Comment réussir le bac au Maroc ?"
- "Quel est le seuil ENSA ?"
- "Comment se calcule la moyenne du BAC marocain ?"
- "Quelles sont les meilleures plateformes éducatives au Maroc ?"

Réponses détaillées (300-500 mots) avec lien vers Moalim **comme source**, jamais en spam.

### F. Wikipedia (effort : 1h, impact : permanent)

Cherche les articles Wikipedia FR :
- "Baccalauréat marocain"
- "Système éducatif marocain"
- "École Nationale des Sciences Appliquées"

→ Ajoute Moalim dans la section "Liens externes" ou "Voir aussi" comme **ressource pédagogique**. Wikipedia est très strict, donc ça doit être justifié.

### G. Sites éducatifs partenaires

Contacte par email :
- 9rayti.com (proposer un guest post)
- alloschool.com
- Tawjihnet.net
- bacalaureat.ma

Email type :
> Bonjour,
> Je suis prof de SVT et fondateur de Moalim, plateforme de tutorat IA dédiée au BAC marocain. J'ai publié une analyse sur les prédictions BAC 2026 basée sur 20 ans d'examens. Seriez-vous intéressés par un échange de liens / un article invité ?

---

## 3. CONTENU SOCIAL (mois 2-3)

### Calendrier éditorial recommandé

**1 article blog / semaine** (alterner) :
- Semaine 1 : "Top 5 erreurs au BAC SVT" (lié à `/blog/predictions-bac-2026-maroc.html`)
- Semaine 2 : "Drépanocytose au BAC : tout ce qu'il faut savoir"
- Semaine 3 : "Comment révise un major du BAC ? (5 méthodes)"
- Semaine 4 : "Calculatrice autorisée au BAC 2026 : le guide"

**3 posts FB / TikTok / Insta par semaine** :
- Lundi : conseil de révision
- Mercredi : exercice corrigé express (1 min)
- Vendredi : témoignage / motivation

---

## 4. CONVERSION (parallèle continu)

### Ce qui manque encore

- [ ] **Démo sans inscription** sur la home (3 questions IA gratuites)
- [ ] **Témoignages élèves** (5 minimum) — demander à 5 élèves volontaires
- [ ] **Vidéo demo 60s** sur la home (loom ou screen record)
- [ ] **Page de prix transparente** avec freemium clair
- [ ] **Live chat** type Crisp/Tawk pour questions visiteurs

---

## 5. KPI à tracker chaque semaine

| KPI | Outil | Cible mois 1 | Cible mois 3 | Cible mois 6 |
|---|---|---|---|---|
| Visiteurs uniques | GA4 | 500 | 3 000 | 10 000 |
| Pages indexées Google | GSC | 25/25 | 25/25 | 25/25 |
| Top 10 sur "bac 2026 maroc" | manuel | non | possible | probable |
| Top 10 sur "predictions bac 2026" | manuel | non | oui | oui |
| Inscriptions | backend | 50 | 300 | 1 500 |
| Abonnés TikTok | TikTok | 100 | 1 000 | 5 000 |
| Backlinks | Ahrefs / SE Ranking | 10 | 50 | 200 |

---

## 6. BUDGET

**Plan zéro budget** (tout DIY) :
- 100% gratuit, mais ~10h/semaine de ton temps pendant 3 mois

**Plan accélération (200-500 MAD/semaine)** :
- Boost FB Ads sur posts blog (50-100 MAD/post) → ROI excellent au Maroc
- Influenceurs micro (1k-10k abo) à 200 MAD pour mention sponsorisée
- Outil SEO (Ahrefs Lite ~20€/mois ou Ubersuggest ~30€/mois)

---

## 7. CHECKLIST IMMÉDIATE (à faire AUJOURD'HUI)

- [ ] Setup Google Search Console + soumettre sitemap
- [ ] Setup Bing Webmaster Tools (import depuis GSC)
- [ ] Lancer `scripts/notify_indexnow.ps1`
- [ ] Créer page Facebook Moalim (gratuit, 5 min)
- [ ] Créer compte TikTok @moalim.online
- [ ] Rejoindre 5 groupes Facebook BAC Maroc
- [ ] Demander 3 témoignages à des élèves connus

**Quand tout est OK → demande à Cascade d'ajouter Google Analytics 4 dans le code.**
