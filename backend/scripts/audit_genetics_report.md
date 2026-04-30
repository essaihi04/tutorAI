# Audit Protocole Génétique BAC SVT BIOF — Rapport

_Généré le 2026-04-30 16:41:03_


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
- elapsed : 14.8s

**Réponse LLM (extrait 2.5k char) :**

```
# Interprétation chromosomique du croisement chez la Drosophile

Très bien ! On va faire ce croisement pas à pas. C'est un **monohybridisme** (1 seul gène, 2 allèles). Le mâle P1 est homozygote dominant [g+] et la femelle P2 est homozygote récessive [g].

<ui>{"actions":[{"type":"whiteboard","action":"show_board","payload":{"title":"Interprétation chromosomique du 1er croisement (P1 × P2)","lines":[
  {"type":"subtitle","content":"Parents : P1 × P2"},
  {"type":"math","content":"\\text{Phénotypes : }\\;[g^+]\\;\\times\\;[g]"},
  {"type":"math","content":"\\text{Génotypes : }\\;\\dfrac{g^+}{g^+}\\;\\times\\;\\dfrac{g}{g}"},
  {"type":"subtitle","content":"Gamètes (avec %)"},
  {"type":"math","content":"P1\\to\\;\\dfrac{g^+}{}\\;(100\\,\\%)"},
  {"type":"math","content":"P2\\to\\;\\dfrac{g}{}\\;(100\\,\\%)"},
  {"type":"subtitle","content":"Fécondation"},
  {"type":"table","content":"","headers":["♀ \\\\ ♂","\\\\dfrac{g}{}\\\\;(100\\\\,\\\\%)"],"rows":[["\\\\dfrac{g^+}{}\\\\;(100\\\\,\\\\%)","\\\\dfrac{g^+}{g}\\\\;[g^+]"]]},
  {"type":"box","content":"F1 : 100 % [g⁺] hétérozygotes","color":"green"}
]}}]}</ui>

<ui>{"actions":[{"type":"whiteboard","action":"show_board","payload":{"title":"Interprétation chromosomique du 2e croisement (F1 × F1)","lines":[
  {"type":"subtitle","content":"Parents : F1 × F1"},
  {"type":"math","content":"\\text{Phénotypes : }\\;[g^+]\\;\\times\\;[g^+]"},
  {"type":"math","content":"\\text{Génotypes : }\\;\\dfrac{g^+}{g}\\;\\times\\;\\dfrac{g^+}{g}"},
  {"type":"subtitle","content":"Gamètes (avec %)"},
  {"type":"math","content":"F1\\to\\;\\dfrac{g^+}{}\\;(50\\,\\%)"},
  {"type":"math","content":"F1\\to\\;\\dfrac{g}{}\\;(50\\,\\%)"},
  {"type":"subtitle","content":"Fécondation (Échiquier de croisement)"},
  {"type":"table","content":"","headers":["♀ \\\\ ♂","\\\\dfrac{g^+}{}\\\\;(50\\\\,\\\\%)","\\\\dfrac{g}{}\\\\;(50\\\\,\\\\%)"],"rows":[
    ["\\\\dfrac{g^+}{}\\\\;(50\\\\,\\\\%)","\\\\dfrac{g^+}{g^+}\\\\;[g^+]","\\\\dfrac{g^+}{g}\\\\;[g^+]"],
    ["\\\\dfrac{g}{}\\\\;(50\\\\,\\\\%)","\\\\dfrac{g^+}{g}\\\\;[g^+]","\\\\dfrac{g}{g}\\\\;[g]"]
  ]},
  {"type":"box","content":"Résultats F2 : [g⁺] : 3/4 = 75 %    [g] : 1/4 = 25 %","color":"green"}
]}}]}</ui>

## 📝 Résumé à noter dans ton cahier

**Résultats du croisement :**
- **F1** : 100% des individus sont [gris] hétérozygotes (g⁺/g)
- **F2** (F1×F1) : 3/4 [gris] (75%) et 1/4 [noir] (25%)

**⚠️ Piège BAC :** Ne confonds pas le phénotype [g⁺] avec le génotype g⁺/g⁺. Un individu [gris
…[tronqué]
```

### [PASS] Dihybridisme indépendant — test-cross
- query : `On considère deux gènes indépendants chez la drosophile : couleur du corps (gris [g+] dominant / noir [g]) et longueur des ailes (longues [v…`
- has_ui : True
- has_table : True (cells=8)
- has_dfrac : True
- inline_violations : ∅
- elapsed : 14.5s

**Réponse LLM (extrait 2.5k char) :**

```
# Test-cross chez la Drosophile : gènes indépendants

Très bien ! On va réaliser le test-cross d'un individu F1 double hétérozygote [g+, vg+] avec un double homozygote récessif [g, vg]. Les gènes sont indépendants (portés par des paires de chromosomes différentes).

<ui>{"actions":[{"type":"whiteboard","action":"show_board","payload":{"title":"Interprétation chromosomique du test-cross","lines":[
  {"type":"subtitle","content":"Parents : F1 × P2 (test-cross)"},
  {"type":"math","content":"\\text{Phénotypes : }\\;[g^+,vg^+]\\;\\times\\;[g,vg]"},
  {"type":"math","content":"\\text{Génotypes : }\\;\\dfrac{g^+}{g}\\,\\dfrac{vg^+}{vg}\\;\\times\\;\\dfrac{g}{g}\\,\\dfrac{vg}{vg}"},
  {"type":"separator","content":""},
  {"type":"subtitle","content":"Gamètes produits par chaque parent"},
  {"type":"text","content":"🔴 F1 double hétérozygote (4 types de gamètes équiprobables car gènes indépendants) :"},
  {"type":"math","content":"\\dfrac{g^+}{}\\,\\dfrac{vg^+}{}\\;(25\\,\\%)"},
  {"type":"math","content":"\\dfrac{g^+}{}\\,\\dfrac{vg}{}\\;(25\\,\\%)"},
  {"type":"math","content":"\\dfrac{g}{}\\,\\dfrac{vg^+}{}\\;(25\\,\\%)"},
  {"type":"math","content":"\\dfrac{g}{}\\,\\dfrac{vg}{}\\;(25\\,\\%)"},
  {"type":"separator","content":""},
  {"type":"text","content":"🔵 Double homozygote récessif (1 seul type de gamète) :"},
  {"type":"math","content":"\\dfrac{g}{}\\,\\dfrac{vg}{}\\;(100\\,\\%)"},
  {"type":"separator","content":""},
  {"type":"subtitle","content":"Échiquier de croisement (test-cross)"},
  {"type":"table","content":"","headers":["♀ \\ ♂","\\dfrac{g}{}\\,\\dfrac{vg}{}\\;(100\\,\\%)"],"rows":[
    ["\\dfrac{g^+}{}\\,\\dfrac{vg^+}{}\\;(25\\,\\%)","\\dfrac{g^+}{g}\\,\\dfrac{vg^+}{vg}\\;[g^+,vg^+]"],
    ["\\dfrac{g^+}{}\\,\\dfrac{vg}{}\\;(25\\,\\%)","\\dfrac{g^+}{g}\\,\\dfrac{vg}{vg}\\;[g^+,vg]"],
    ["\\dfrac{g}{}\\,\\dfrac{vg^+}{}\\;(25\\,\\%)","\\dfrac{g}{g}\\,\\dfrac{vg^+}{vg}\\;[g,vg^+]"],
    ["\\dfrac{g}{}\\,\\dfrac{vg}{}\\;(25\\,\\%)","\\dfrac{g}{g}\\,\\dfrac{vg}{vg}\\;[g,vg]"]
  ]},
  {"type":"separator","content":""},
  {"type":"box","content":"📊 Résultats du test-cross : 4 phénotypes équiprobables à 25 % chacun","color":"green"},
  {"type":"box","content":"[g⁺,vg⁺] : 1/4 = 25 %    [g⁺,vg] : 1/4 = 25 %\n[g,vg⁺] : 1/4 = 25 %    [g,vg] : 1/4 = 25 %","color":"orange"}
]}}]}</ui>

## Explication pédagogique

**Pourquoi 4 phénotypes équiprobables ?** Parce que les gènes sont **indépendants** (portés par 2 paires de chromosomes différentes). Lors de la m
…[tronqué]
```

### [PASS] Dihybridisme gènes liés (linkage)
- query : `Chez la drosophile, le gène de la couleur du corps et le gène de la longueur des ailes sont LIÉS sur le même chromosome, à une distance de 1…`
- has_ui : True
- has_table : True (cells=8)
- has_dfrac : True
- inline_violations : ∅
- elapsed : 14.6s

**Réponse LLM (extrait 2.5k char) :**

```
Bonjour Audit ! Excellente question sur un classique du BAC SVT PC. Les gènes liés avec distance de recombinaison, c'est un point qui tombe très souvent (25% de l'examen SVT, domaine 2).

Voici l'interprétation chromosomique complète pour ce test-cross. Note bien la structure : les gamètes parentaux sont majoritaires et les recombinés minoritaires, avec des pourcentages calculés à partir de la distance de 17 cM.

<ui>{"actions":[{"type":"whiteboard","action":"show_board","payload":{"title":"Interprétation chromosomique du test-cross (gènes liés, d = 17 cM)","lines":[
  {"type":"subtitle","content":"Parents : F1 double hétérozygote × double récessif"},
  {"type":"math","content":"\\text{Phénotypes : }\\;[J,L]\\;\\times\\;[v,r]"},
  {"type":"math","content":"\\text{Génotypes : }\\;\\dfrac{J\\;L}{v\\;r}\\;\\times\\;\\dfrac{v\\;r}{v\\;r}"},
  {"type":"separator","content":""},
  {"type":"subtitle","content":"Gamètes du F1 (d = 17 cM)"},
  {"type":"subtitle","content":"Gamètes parentaux (majoritaires) :"},
  {"type":"math","content":"\\dfrac{J\\;L}{}\\;\\;\\;\\dfrac{100-17}{2}=41,5\\,\\%"},
  {"type":"math","content":"\\dfrac{v\\;r}{}\\;\\;\\;\\dfrac{100-17}{2}=41,5\\,\\%"},
  {"type":"subtitle","content":"Gamètes recombinés (minoritaires) :"},
  {"type":"math","content":"\\dfrac{J\\;r}{}\\;\\;\\;\\dfrac{17}{2}=8,5\\,\\%"},
  {"type":"math","content":"\\dfrac{v\\;L}{}\\;\\;\\;\\dfrac{17}{2}=8,5\\,\\%"},
  {"type":"separator","content":""},
  {"type":"subtitle","content":"Gamètes du parent récessif (P2)"},
  {"type":"math","content":"\\dfrac{v\\;r}{}\\;\\;\\;100\\,\\%"},
  {"type":"separator","content":""},
  {"type":"subtitle","content":"Résultats du test-cross (F1 × P2)"},
  {"type":"table","content":"","headers":["♀ \\ ♂","\\dfrac{v\\;r}{}\\;(100\\,\\%)"],"rows":[
    ["\\dfrac{J\\;L}{}\\;(41,5\\,\\%)","\\dfrac{J\\;L}{v\\;r}\\;[J,L]\\;(41,5\\,\\%)"],
    ["\\dfrac{v\\;r}{}\\;(41,5\\,\\%)","\\dfrac{v\\;r}{v\\;r}\\;[v,r]\\;(41,5\\,\\%)"],
    ["\\dfrac{J\\;r}{}\\;(8,5\\,\\%)","\\dfrac{J\\;r}{v\\;r}\\;[J,r]\\;(8,5\\,\\%)"],
    ["\\dfrac{v\\;L}{}\\;(8,5\\,\\%)","\\dfrac{v\\;L}{v\\;r}\\;[v,L]\\;(8,5\\,\\%)"]
  ]},
  {"type":"box","content":"Résultats : [J,L] = 41,5 % ; [v,r] = 41,5 % ; [J,r] = 8,5 % ; [v,L] = 8,5 %","color":"green"}
]}}]}</ui>

**Explication orale :**

La distance de 17 cM signifie que le taux de recombinaison (crossing-over) entre ces deux gènes est de 17%. Donc, 17% des gamètes du F1 sont recombinés (8,5% pour chaque type) et 83% sont parentaux
…[tronqué]
```
