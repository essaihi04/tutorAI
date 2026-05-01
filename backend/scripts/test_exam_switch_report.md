# Test — RE-OUVERTURE D'UN NOUVEL EXERCICE BAC

_Généré le 2026-05-01 16:56:36_


Objectif : confirmer que quand un examen est déjà ouvert dans le panneau et que l'utilisateur demande explicitement un AUTRE exercice BAC, le LLM ferme bien l'ancien et émet un nouveau `<exam_exercise>` correspondant à la nouvelle demande.


## Score global : **9/9** — 🎉 TOUT VERT


| # | Scénario | Mode | Tag émis | Topic OK | Verdict |
|---|---|---|---|---|---|
| 1 | T1 • LIBRE — examen SVT mitose ouvert → demande nouvelle exe | `libre` | ✅ | ✅ | 3/3 ✅ |
| 2 | T2 • LIBRE — examen SVT mitose ouvert → demande un autre BAC | `libre` | ✅ | ✅ | 3/3 ✅ |
| 3 | T3 • COACHING — examen génétique ouvert → demande explicitem | `coaching` | ✅ | ✅ | 3/3 ✅ |

---

## 1. T1 • LIBRE — examen SVT mitose ouvert → demande nouvelle exercice génétique

- **Mode** : `libre`
- **Examen ouvert** : SVT 2025 Rattrapage — Exercice 2 — Mitose et division cellulaire
- **Topic ouvert** : mitose
- **Topic demandé** : ['génétique', 'genetique', 'mendel', 'dihybrid', 'monohybrid']
- **Temps LLM** : 2.1s  •  **Réponse** : 226 chars

**Message envoyé :**
> Merci pour cet exercice ! Maintenant, donne-moi un AUTRE exercice BAC en SVT, mais cette fois sur la GÉNÉTIQUE mendélienne — croisement dihybride avec échiquier. Ferme l'exercice actuel et ouvre le nouveau.

### Tag <exam_exercise> émis
- **Contenu** : `génétique mendélienne croisement dihybride échiquier`

### Checks
| # | Vérification | Statut | Détail |
|---|---|---|---|
| 1 | ⭐ Le LLM a émis un nouveau <exam_exercise> (close + open new) | ✅ PASS | contenu : 'génétique mendélienne croisement dihybride échiquier' |
| 2 | ⭐ Le tag pointe vers la NOUVELLE thématique demandée | ✅ PASS | keywords attendus : ['génétique', 'genetique', 'mendel', 'dihybrid', 'monohybrid'] | trouvé : True |
| 3 | Le LLM n'a PAS refusé de changer d'exercice | ✅ PASS | aucun refus détecté |

### Réponse LLM (226 chars — extrait)
```
D'accord, je ferme l'exercice actuel et je t'ouvre un nouvel exercice BAC sur la génétique mendélienne — croisement dihybride avec échiquier.

<exam_exercise>génétique mendélienne croisement dihybride échiquier</exam_exercise>
```

---

## 2. T2 • LIBRE — examen SVT mitose ouvert → demande un autre BAC SVT (même thème)

- **Mode** : `libre`
- **Examen ouvert** : SVT 2025 Rattrapage — Exercice 2 — Mitose
- **Topic ouvert** : mitose
- **Topic demandé** : ['mitose', 'division cellulaire', 'cellule', 'cellulaire', 'chromosome']
- **Temps LLM** : 1.9s  •  **Réponse** : 170 chars

**Message envoyé :**
> J'ai fini cet exercice. Donne-moi un AUTRE exercice BAC SVT (année différente) toujours sur la mitose / division cellulaire pour m'entraîner sur un autre énoncé.

### Tag <exam_exercise> émis
- **Contenu** : `mitose division cellulaire méiose`

### Checks
| # | Vérification | Statut | Détail |
|---|---|---|---|
| 1 | ⭐ Le LLM a émis un nouveau <exam_exercise> (close + open new) | ✅ PASS | contenu : 'mitose division cellulaire méiose' |
| 2 | ⭐ Le tag pointe vers la NOUVELLE thématique demandée | ✅ PASS | keywords attendus : ['mitose', 'division cellulaire', 'cellule', 'cellulaire', 'chromosome'] | trouvé : True |
| 3 | Le LLM n'a PAS refusé de changer d'exercice | ✅ PASS | aucun refus détecté |

### Réponse LLM (170 chars — extrait)
```
D'accord, je te lance un autre exercice BAC SVT sur la mitose pour t'entraîner avec un énoncé différent.

<exam_exercise>mitose division cellulaire méiose</exam_exercise>
```

---

## 3. T3 • COACHING — examen génétique ouvert → demande explicitement un autre

- **Mode** : `coaching`
- **Examen ouvert** : SVT 2024 Normale — Exercice 3 — Génétique mendélienne
- **Topic ouvert** : génétique
- **Topic demandé** : ['brassage', 'interchromos', 'génétique', 'genetique', 'dihybrid']
- **Temps LLM** : 1.8s  •  **Réponse** : 189 chars

**Message envoyé :**
> Cet exercice je l'ai fait. Donne-moi un autre exercice BAC SVT sur le brassage interchromosomique (génétique), une autre année. Ferme l'examen actuel et ouvre le nouveau.

### Tag <exam_exercise> émis
- **Contenu** : `brassage interchromosomique dihybridisme génétique`

### Checks
| # | Vérification | Statut | Détail |
|---|---|---|---|
| 1 | ⭐ Le LLM a émis un nouveau <exam_exercise> (close + open new) | ✅ PASS | contenu : 'brassage interchromosomique dihybridisme génétique' |
| 2 | ⭐ Le tag pointe vers la NOUVELLE thématique demandée | ✅ PASS | keywords attendus : ['brassage', 'interchromos', 'génétique', 'genetique', 'dihybrid'] | trouvé : True |
| 3 | Le LLM n'a PAS refusé de changer d'exercice | ✅ PASS | aucun refus détecté |

### Réponse LLM (189 chars — extrait)
```
D'accord, je ferme l'examen actuel et je t'ouvre un autre exercice BAC sur le brassage interchromosomique.

<exam_exercise>brassage interchromosomique dihybridisme génétique</exam_exercise>
```

---

**Score final : 9/9** — 🎉 TOUT VERT
