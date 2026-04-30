# Audit Protocole Génétique BAC SVT BIOF — Rapport

_Généré le 2026-04-30 17:18:27_


## Résumé

- **Total cas** : 3
- **Réussis** : 3 (100%)
- **Échecs** : 0

Critères de réussite (TOUS requis) :
- au moins un bloc `<ui>{…show_board…}</ui>`
- au moins une ligne `type:table` (échiquier) avec ≥ 4 cellules
- au moins une notation `\dfrac{…}{…}` (génotype chromosomique)
- AUCUN texte inline interdit (« Parents : [..] × [..] », « // », « → »)


## Détails par cas

### [PASS] Monohybridisme F1×F1
- query : `Chez la drosophile, le caractère couleur du corps présente deux phénotypes : corps gris [g+] dominant et corps noir [g] récessif. On croise …`
- has_ui : True
- has_table : True (cells=6)
- has_dfrac : True
- inline_violations : ∅
- elapsed : 20.1s

**Réponse LLM (extrait 2.5k char) :**

```
# Interprétation chromosomique du croisement chez la drosophile

Très bien ! C'est un **monohybridisme** classique (1 seul gène, 2 allèles). Suivons la méthode BAC étape par étape.

<ui>{"actions":[{"type":"whiteboard","action":"show_board","payload":{"title":"Interprétation chromosomique — Monohybridisme","lines":[
  {"type":"title","content":"1er croisement : P1 × P2"},
  {"type":"subtitle","content":"Parents : P1 (mâle) × P2 (femelle)"},
  {"type":"math","content":"\\text{Phénotypes : }\\;[g^+]\\;\\times\\;[g]"},
  {"type":"math","content":"\\text{Génotypes : }\\;\\dfrac{g^+}{g^+}\\;\\times\\;\\dfrac{g}{g}"},
  {"type":"subtitle","content":"Gamètes (avec %)"},
  {"type":"math","content":"P1\\to\\;\\dfrac{g^+}{}\\;(100\\,\\%)"},
  {"type":"math","content":"P2\\to\\;\\dfrac{g}{}\\;(100\\,\\%)"},
  {"type":"subtitle","content":"Fécondation"},
  {"type":"table","content":"","headers":["♀ \\\\ ♂","\\dfrac{g}{}\\;(100\\,\\%)"],"rows":[["\\dfrac{g^+}{}\\;(100\\,\\%)","\\dfrac{g^+}{g}\\;[g^+]"]]},
  {"type":"box","content":"F1 : 100 % [g⁺] — tous hétérozygotes","color":"green"},
  {"type":"separator","content":""},
  {"type":"title","content":"2e croisement : F1 × F1"},
  {"type":"subtitle","content":"Parents : F1 × F1"},
  {"type":"math","content":"\\text{Phénotypes : }\\;[g^+]\\;\\times\\;[g^+]"},
  {"type":"math","content":"\\text{Génotypes : }\\;\\dfrac{g^+}{g}\\;\\times\\;\\dfrac{g^+}{g}"},
  {"type":"subtitle","content":"Gamètes (avec %)"},
  {"type":"math","content":"F1\\to\\;\\dfrac{g^+}{}\\;(50\\,\\%)"},
  {"type":"math","content":"F1\\to\\;\\dfrac{g}{}\\;(50\\,\\%)"},
  {"type":"subtitle","content":"Fécondation (échiquier)"},
  {"type":"table","content":"","headers":["♀ \\\\ ♂","\\dfrac{g^+}{}\\;(50\\,\\%)","\\dfrac{g}{}\\;(50\\,\\%)"],"rows":[
    ["\\dfrac{g^+}{}\\;(50\\,\\%)","\\dfrac{g^+}{g^+}\\;[g^+]","\\dfrac{g^+}{g}\\;[g^+]"],
    ["\\dfrac{g}{}\\;(50\\,\\%)","\\dfrac{g^+}{g}\\;[g^+]","\\dfrac{g}{g}\\;[g]"]
  ]},
  {"type":"box","content":"Résultats F2 — [g⁺] : 3/4 = 75 %  |  [g] : 1/4 = 25 %","color":"orange"},
  {"type":"separator","content":""},
  {"type":"subtitle","content":"📝 À NOTER"},
  {"type":"box","content":"🔑 Formule : F1 × F1 → F2 = 3/4 dominants + 1/4 récessifs (3:1)","color":"green"},
  {"type":"warning","content":"⚠️ Piège BAC : Ne pas oublier que les gamètes sont équiprobables (50% chacun) chez l'hétérozygote !"},
  {"type":"tip","content":"✅ Règle d'or : Toujours écrire les génotypes en fraction \\dfrac{allèle}{allèle} pour vi
…[tronqué]
```

### [PASS] Dihybridisme indépendant — test-cross
- query : `On considère deux gènes indépendants chez la drosophile : couleur du corps (gris [g+] dominant / noir [g]) et longueur des ailes (longues [v…`
- has_ui : True
- has_table : True (cells=8)
- has_dfrac : True
- inline_violations : ∅
- elapsed : 21.5s

**Réponse LLM (extrait 2.5k char) :**

```
# Test-cross chez la drosophile — Gènes indépendants

Très bien Audit ! Je vais te montrer l'interprétation chromosomique complète du test-cross pour deux gènes indépendants. C'est une question classique du BAC (25% de l'épreuve SVT).

<ui>{"actions":[{"type":"whiteboard","action":"show_board","payload":{"title":"Interprétation chromosomique du test-cross","lines":[
  {"type":"title","content":"Test-cross : F1 double hétérozygote × double homozygote récessif"},
  {"type":"subtitle","content":"Parents : F1 × P2 (testeur)"},
  {"type":"math","content":"\\text{Phénotypes : }\\;[g^+,vg^+]\\;\\times\\;[g,vg]"},
  {"type":"math","content":"\\text{Génotypes : }\\;\\dfrac{g^+}{g}\\,\\dfrac{vg^+}{vg}\\;\\times\\;\\dfrac{g}{g}\\,\\dfrac{vg}{vg}"},
  {"type":"separator","content":""},
  {"type":"subtitle","content":"Gamètes formés"},
  {"type":"box","content":"F1 (double hétérozygote) produit 4 types de gamètes équiprobables (gènes indépendants)","color":"blue"},
  {"type":"math","content":"\\dfrac{g^+}{}\\,\\dfrac{vg^+}{}\\;(25\\,\\%)"},
  {"type":"math","content":"\\dfrac{g^+}{}\\,\\dfrac{vg}{}\\;(25\\,\\%)"},
  {"type":"math","content":"\\dfrac{g}{}\\,\\dfrac{vg^+}{}\\;(25\\,\\%)"},
  {"type":"math","content":"\\dfrac{g}{}\\,\\dfrac{vg}{}\\;(25\\,\\%)"},
  {"type":"box","content":"P2 (testeur) produit 1 seul type de gamète : \\;\\dfrac{g}{}\\,\\dfrac{vg}{}\\;(100\\,\\%)","color":"blue"},
  {"type":"separator","content":""},
  {"type":"subtitle","content":"Échiquier de croisement (test-cross)"},
  {"type":"table","content":"","headers":[
    "♀ \\\\ ♂",
    "\\dfrac{g}{}\\,\\dfrac{vg}{}\\;(100\\,\\%)"
  ],"rows":[
    ["\\dfrac{g^+}{}\\,\\dfrac{vg^+}{}\\;(25\\,\\%)",
     "\\dfrac{g^+}{g}\\,\\dfrac{vg^+}{vg}\\;[g^+,vg^+]"],
    ["\\dfrac{g^+}{}\\,\\dfrac{vg}{}\\;(25\\,\\%)",
     "\\dfrac{g^+}{g}\\,\\dfrac{vg}{vg}\\;[g^+,vg]"],
    ["\\dfrac{g}{}\\,\\dfrac{vg^+}{}\\;(25\\,\\%)",
     "\\dfrac{g}{g}\\,\\dfrac{vg^+}{vg}\\;[g,vg^+]"],
    ["\\dfrac{g}{}\\,\\dfrac{vg}{}\\;(25\\,\\%)",
     "\\dfrac{g}{g}\\,\\dfrac{vg}{vg}\\;[g,vg]"]
  ]},
  {"type":"separator","content":""},
  {"type":"box","content":"Résultats du test-cross : [g⁺,vg⁺] : 1/4 = 25 %  |  [g⁺,vg] : 1/4 = 25 %  |  [g,vg⁺] : 1/4 = 25 %  |  [g,vg] : 1/4 = 25 %","color":"green"},
  {"type":"separator","content":""},
  {"type":"subtitle","content":"📝 À NOTER"},
  {"type":"text","content":"• Test-cross = croisement d'un individu avec un double homozygote récessif"},
  {"type":"text","content":"• Pour gènes indé
…[tronqué]
```

### [PASS] Dihybridisme gènes liés (linkage)
- query : `Chez la drosophile, le gène de la couleur du corps et le gène de la longueur des ailes sont LIÉS sur le même chromosome, à une distance de 1…`
- has_ui : True
- has_table : True (cells=20)
- has_dfrac : True
- inline_violations : ∅
- elapsed : 21.7s

**Réponse LLM (extrait 2.5k char) :**

```
Bonjour Audit ! Excellente question sur les gènes liés, un classique du BAC SVT (25% de l'examen). On va détailler ça pas à pas.

Voici l'interprétation chromosomique complète pour ce test-cross avec gènes liés.

<ui>{"actions":[{"type":"whiteboard","action":"show_board","payload":{"title":"Interprétation chromosomique du test-cross (gènes liés)","lines":[
  {"type":"subtitle","content":"Données de l'énoncé"},
  {"type":"text","content":"Distance entre les deux gènes : $d = 17\\,\\text{cM}$ (centiMorgans)"},
  {"type":"text","content":"Test-cross : croisement d'un individu double hétérozygote avec un individu double récessif."},
  {"type":"separator","content":""},
  {"type":"subtitle","content":"1. Génotypes des parents"},
  {"type":"math","content":"\\text{Parent 1 (double hétérozygote) : }\\;\\dfrac{C\\;L}{c\\;l}\\;\\text{(phénotype [C,L])}"},
  {"type":"math","content":"\\text{Parent 2 (double récessif) : }\\;\\dfrac{c\\;l}{c\\;l}\\;\\text{(phénotype [c,l])}"},
  {"type":"separator","content":""},
  {"type":"subtitle","content":"2. Types et proportions des gamètes du Parent 1"},
  {"type":"text","content":"La distance de 17 cM signifie que le taux de recombinaison est de 17 %."},
  {"type":"text","content":"Donc :"},
  {"type":"math","content":"\\text{Gamètes parentaux (non recombinés) : }\\;\\dfrac{C\\;L}{}\\;\\text{et}\\;\\dfrac{c\\;l}{}\\;\\text{— chacun }\\dfrac{100-17}{2}=41,5\\,\\%"},
  {"type":"math","content":"\\text{Gamètes recombinés : }\\;\\dfrac{C\\;l}{}\\;\\text{et}\\;\\dfrac{c\\;L}{}\\;\\text{— chacun }\\dfrac{17}{2}=8,5\\,\\%"},
  {"type":"separator","content":""},
  {"type":"subtitle","content":"3. Gamètes du Parent 2 (double récessif)"},
  {"type":"math","content":"\\text{Un seul type : }\\;\\dfrac{c\\;l}{}\\;\\text{(100 %)}"},
  {"type":"separator","content":""},
  {"type":"subtitle","content":"4. Résultats du test-cross (descendance)"},
  {"type":"table","content":"","headers":["Gamètes Parent 1","Gamète Parent 2","Génotype F1","Phénotype F1","% attendu"],
   "rows":[
     ["$\\dfrac{C\\;L}{}$ (parental)","$\\dfrac{c\\;l}{}$","$\\dfrac{C\\;L}{c\\;l}$","[C,L]","41,5 %"],
     ["$\\dfrac{c\\;l}{}$ (parental)","$\\dfrac{c\\;l}{}$","$\\dfrac{c\\;l}{c\\;l}$","[c,l]","41,5 %"],
     ["$\\dfrac{C\\;l}{}$ (recombiné)","$\\dfrac{c\\;l}{}$","$\\dfrac{C\\;l}{c\\;l}$","[C,l]","8,5 %"],
     ["$\\dfrac{c\\;L}{}$ (recombiné)","$\\dfrac{c\\;l}{}$","$\\dfrac{c\\;L}{c\\;l}$","[c,L]","8,5 %"]
   ]},
  {"type":"box","content":"📝 À RETENIR : Total paren
…[tronqué]
```
