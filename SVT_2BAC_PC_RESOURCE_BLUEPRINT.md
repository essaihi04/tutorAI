# Blueprint Flexible des Ressources SVT 2Bac PC

## Structure commune par leçon
Pour chaque leçon, créer 4 ressources:
- **Simulation**
- **Image / Schéma**
- **Exercice guidé**
- **Évaluation formative**

## Adaptation pédagogique commune
Utiliser ce bloc dans tous les prompts:

```text
Contraintes pédagogiques:
- Respecter le programme officiel marocain SVT 2Bac PC.
- Si l'élève est débutant absolu, expliquer avec vocabulaire simple, définir chaque terme et avancer pas à pas.
- Si l'élève est de niveau moyen, garder un équilibre entre simplicité et rigueur scientifique.
- Si l'élève est avancé, ajouter une couche d'analyse, de comparaison et de raisonnement.
- Toujours prévoir une version très accessible pour un élève qui commence à zéro.
- Ne pas surcharger visuellement ou conceptuellement la première version.
```

---

## Chapitre 1 - Consommation de la matière organique et flux d'énergie

### Leçon 1.1 - Libération de l'énergie emmagasinée

- **Simulation à créer**
  - respiration avec et sans O2
  - comparaison ATP
  - distinction glycolyse / respiration / fermentation

**Prompt simulation**
```text
Crée une simulation interactive HTML standalone pour la leçon "Libération de l'énergie emmagasinée" en SVT 2Bac PC Maroc.
Objectifs: comprendre le rôle de l'ATP, distinguer glycolyse, respiration cellulaire et fermentation, comparer la production d'énergie avec et sans dioxygène.
Fonctionnalités: choisir présence ou absence de O2, observer le lieu cellulaire, observer la quantité d'ATP produite, comparer respiration et fermentation, afficher un retour visuel clair.
La simulation doit communiquer avec l'IA via postMessage avec simulation_id="respiration_energie".
Contraintes pédagogiques: version très simple pour débutant, version structurée pour niveau moyen, version détaillée avec rendement énergétique pour avancé.
```

- **Image à créer**
  - glucose au départ
  - glycolyse dans le cytoplasme
  - chemin avec O2 et chemin sans O2

**Prompt image**
```text
Crée un schéma pédagogique haute qualité pour la leçon "Libération de l'énergie emmagasinée" en SVT 2Bac PC Maroc.
Le schéma doit montrer: glucose, glycolyse, avec O2 vers mitochondrie et respiration cellulaire, sans O2 vers fermentation, comparaison de la quantité d'ATP.
Faire une version débutant très simple, une version standard claire, et une version avancée avec pyruvate, NADH et chaîne respiratoire.
Style: fond propre, lisibilité maximale, couleurs cohérentes.
```

- **Exercice à créer**
  - comparaison respiration / fermentation
  - compléter tableau ATP

**Prompt exercice**
```text
Crée un exercice progressif pour la leçon "Libération de l'énergie emmagasinée" en SVT 2Bac PC.
Inclure: un niveau débutant pour associer chaque voie métabolique à son nombre d'ATP, un niveau moyen pour compléter un tableau respiration vs fermentation, un niveau avancé pour expliquer pourquoi l'absence d'O2 réduit le rendement énergétique.
Ajouter un corrigé détaillé, des indices et les erreurs fréquentes.
```

- **Évaluation à créer**
  - 3 QCM
  - 2 vrai/faux justifiés
  - 1 question courte

**Prompt évaluation**
```text
Crée une évaluation formative courte pour la leçon "Libération de l'énergie emmagasinée" en SVT 2Bac PC.
Inclure 3 QCM, 2 questions vrai/faux avec justification, 1 question courte comparant respiration et fermentation, puis un corrigé commenté.
Prévoir une variante débutant, standard et avancée.
```

### Leçon 1.2 - Rôle du muscle strié squelettique

- **Simulation à créer**
  - effort court / moyen / long
  - source d'énergie dominante
  - fatigue musculaire

**Prompt simulation**
```text
Crée une simulation interactive HTML standalone pour la leçon "Rôle du muscle strié squelettique" en SVT 2Bac PC Maroc.
Objectifs: visualiser la structure fonctionnelle du muscle, comprendre le glissement actine-myosine, comparer les sources d'énergie selon la durée et l'intensité de l'effort.
Fonctionnalités: sélectionner type d'effort, observer la source énergétique dominante, observer la fatigue, afficher une animation simple du sarcomère.
Communication IA via postMessage avec simulation_id="muscle_energie".
```

**Prompt image**
```text
Crée un schéma pédagogique de la structure du muscle strié squelettique pour SVT 2Bac PC.
Le schéma doit montrer: muscle, faisceau, fibre musculaire, myofibrille, sarcomère, actine, myosine.
Faire une version très simple pour débutant, une version standard avec légendes, et une version avancée avec raccourcissement du sarcomère.
```

**Prompt exercice**
```text
Crée un exercice progressif sur le rôle du muscle strié squelettique.
Inclure un exercice de classement des niveaux d'organisation du muscle, un exercice liant type d'effort et source d'énergie, et une question sur la fatigue musculaire.
Ajouter corrigé détaillé et version simplifiée pour débutants.
```

**Prompt évaluation**
```text
Crée une évaluation formative sur la structure du muscle et les sources d'énergie musculaire.
Inclure 4 questions courtes, 1 mini-tableau à compléter, et 1 question d'application: sprint vs marathon, avec corrigé commenté.
```

---

## Chapitre 2 - Information génétique et reproduction

### Leçon 2.1 - Notion de l'information génétique

- **Simulation à créer**
  - ADN, complémentarité, réplication, mitose simple

**Prompt simulation**
```text
Crée une simulation interactive HTML standalone pour la leçon "Notion de l'information génétique" en SVT 2Bac PC Maroc.
Objectifs: comprendre la structure de l'ADN, visualiser la réplication semi-conservative, observer les grandes phases de la mitose.
Fonctionnalités: visualiser une double hélice simplifiée, séparer les deux brins, ajouter les nucléotides complémentaires, lancer une animation simple de mitose.
Communication IA via postMessage avec simulation_id="adn_replication_mitose".
```

**Prompt image**
```text
Crée une image pédagogique pour la leçon "Notion de l'information génétique".
L'image doit montrer: nucléotide, double hélice ADN, chromosome, chromatides sœurs, relation ADN vers chromosome.
Prévoir version débutant, standard et avancée.
```

**Prompt exercice**
```text
Crée un exercice progressif sur la structure de l'ADN et la mitose.
Inclure: reconnaître les bases complémentaires, compléter une portion d'ADN, remettre dans l'ordre les phases principales de la mitose, avec corrigé détaillé.
```

**Prompt évaluation**
```text
Crée une évaluation formative sur ADN, réplication et mitose.
Inclure 3 QCM, 2 questions de définition, 1 question de comparaison chromosome/chromatide, et un corrigé avec explication des erreurs fréquentes.
```

### Leçon 2.2 - Expression du matériel génétique

- **Simulation à créer**
  - transcription puis traduction

**Prompt simulation**
```text
Crée une simulation interactive HTML standalone pour la leçon "Expression du matériel génétique" en SVT 2Bac PC Maroc.
Objectifs: comprendre la transcription de l'ADN en ARNm, comprendre la traduction de l'ARNm en protéine, distinguer clairement les deux étapes.
Fonctionnalités: sélectionner une petite séquence d'ADN, générer ARNm complémentaire, afficher les codons, traduire en chaîne d'acides aminés simplifiée.
Communication IA via postMessage avec simulation_id="expression_genetique".
```

**Prompt image**
```text
Crée un schéma pédagogique de l'expression du matériel génétique.
Le schéma doit montrer: ADN dans le noyau, transcription, ARNm, ribosome, traduction, protéine finale.
Utiliser des couleurs distinctes et une lisibilité maximale.
```

**Prompt exercice**
```text
Crée un exercice progressif sur transcription et traduction.
Inclure: identifier si une étape est transcription ou traduction, compléter un ARNm simple à partir d'un brin ADN, associer codon et acide aminé dans une version simplifiée, avec corrigé détaillé.
```

**Prompt évaluation**
```text
Crée une évaluation formative sur l'expression du matériel génétique.
Inclure 4 questions courtes, 1 exercice de distinction transcription/traduction, 1 mini question de synthèse sur le rôle du ribosome, avec corrigé progressif.
```

### Leçon 2.3 - Transfert lors de la reproduction

- **Simulation à créer**
  - méiose et brassage génétique

**Prompt simulation**
```text
Crée une simulation interactive HTML standalone pour la leçon "Transfert lors de la reproduction" en SVT 2Bac PC Maroc.
Objectifs: visualiser la méiose, comprendre le passage de 2n à n, comprendre le brassage génétique.
Fonctionnalités: montrer les deux divisions méiotiques, afficher le nombre de cellules finales, illustrer simplement le crossing-over, comparer mitose et méiose.
Communication IA via postMessage avec simulation_id="meiose_brassage".
```

**Prompt image**
```text
Crée un schéma comparatif mitose / méiose pour SVT 2Bac PC.
Le schéma doit montrer: nombre de divisions, nombre de cellules obtenues, ploïdie finale, identité génétique ou diversité, emplacement du brassage génétique.
```

**Prompt exercice**
```text
Crée un exercice progressif sur la méiose et le brassage génétique.
Inclure: tableau mitose vs méiose à compléter, question sur l'origine de la diversité génétique, question guidée sur le crossing-over, avec corrigé détaillé.
```

**Prompt évaluation**
```text
Crée une évaluation formative sur la méiose et le brassage génétique.
Inclure 3 QCM, 2 questions vrai/faux avec justification, 1 question courte sur la diversité génétique, avec corrigé commenté.
```

---

## Chapitre 3 - Utilisation des matières organiques et inorganiques

### Leçon 3.1 - Ordures ménagères

**Prompt simulation**
```text
Crée une simulation interactive HTML standalone pour la leçon "Ordures ménagères" en SVT 2Bac PC Maroc.
Objectifs: classifier les déchets, comprendre les filières de traitement, relier tri et impact environnemental.
Fonctionnalités: glisser chaque déchet vers la bonne catégorie, afficher le traitement adapté, donner un score pédagogique.
Communication IA via postMessage avec simulation_id="tri_dechets".
```

**Prompt image**
```text
Crée une image pédagogique sur les ordures ménagères montrant: déchets organiques, plastiques, verre, métal, papier, parcours du tri au traitement.
```

**Prompt exercice**
```text
Crée un exercice progressif sur le tri des déchets ménagers avec classement, justification, action simple pour réduire les déchets, et corrigé détaillé.
```

**Prompt évaluation**
```text
Crée une évaluation formative sur les ordures ménagères et leur traitement avec 5 questions courtes, 1 situation-problème de tri et un corrigé simple.
```

### Leçon 3.2 - Pollution des milieux

**Prompt simulation**
```text
Crée une simulation interactive HTML standalone pour la leçon "Pollution des milieux" en SVT 2Bac PC Maroc.
Objectifs: identifier les sources de pollution, observer leurs effets sur l'air, l'eau et le sol, proposer des solutions de prévention.
Fonctionnalités: choisir une source de pollution, observer l'impact sur un milieu, tester une solution corrective, comparer avant/après.
Communication IA via postMessage avec simulation_id="pollution_milieux".
```

**Prompt image**
```text
Crée un schéma pédagogique sur la pollution des milieux naturels montrant pollution de l'air, de l'eau et du sol, sources principales, conséquences et prévention.
```

**Prompt exercice**
```text
Crée un exercice progressif sur la pollution des milieux avec association source/conséquence, mesure de prévention adaptée et corrigé détaillé.
```

**Prompt évaluation**
```text
Crée une évaluation formative sur la pollution des milieux naturels avec QCM simple, question de classement, question d'application locale et corrigé clair.
```

### Leçon 3.3 - Matières radioactives

**Prompt simulation**
```text
Crée une simulation interactive HTML standalone pour la leçon "Matières radioactives et énergie nucléaire" en SVT 2Bac PC Maroc.
Objectifs: comprendre la radioactivité, distinguer usages médicaux, énergétiques et risques, analyser avantages et limites de l'énergie nucléaire.
Fonctionnalités: choisir un contexte, observer bénéfices et risques, ajuster le niveau de sécurité et voir l'effet.
Communication IA via postMessage avec simulation_id="radioactivite_nucleaire".
```

**Prompt image**
```text
Crée une image pédagogique sur les matières radioactives et l'énergie nucléaire montrant source radioactive, centrale simplifiée, usage médical, déchets radioactifs, risques et sécurité.
```

**Prompt exercice**
```text
Crée un exercice progressif sur la radioactivité et l'énergie nucléaire avec association usage/avantage, risque/précaution, courte question argumentative et corrigé détaillé.
```

**Prompt évaluation**
```text
Crée une évaluation formative sur les matières radioactives avec 4 questions courtes, 1 vrai/faux justifié, 1 mini débat encadré, et un corrigé structuré.
```

---

## Chapitre 4 - Phénomènes géologiques et chaînes de montagnes

### Leçon 4.1 - Chaînes de montagnes et tectonique

**Prompt simulation**
```text
Crée une simulation interactive HTML standalone pour la leçon "Chaînes de montagnes et tectonique" en SVT 2Bac PC Maroc.
Objectifs: comprendre le mouvement des plaques, distinguer subduction, collision et obduction, relier ces phénomènes à la formation des chaînes de montagnes.
Fonctionnalités: déplacer des plaques, choisir convergence ou subduction, observer formation du relief, afficher des légendes claires.
Communication IA via postMessage avec simulation_id="tectonique_montagnes".
```

**Prompt image**
```text
Crée un schéma pédagogique sur la formation des chaînes de montagnes en relation avec la tectonique des plaques montrant plaques lithosphériques, convergence, subduction, collision et reliefs.
```

**Prompt exercice**
```text
Crée un exercice progressif sur la tectonique et les chaînes de montagnes avec reconnaissance des mouvements de plaques, lien phénomène/relief, explication simple et corrigé détaillé.
```

**Prompt évaluation**
```text
Crée une évaluation formative sur les chaînes de montagnes et la tectonique avec 3 QCM, 2 questions courtes, 1 lecture de schéma tectonique simple et corrigé commenté.
```

### Leçon 4.2 - Métamorphisme

**Prompt simulation**
```text
Crée une simulation interactive HTML standalone pour la leçon "Métamorphisme" en SVT 2Bac PC Maroc.
Objectifs: comprendre le rôle de la pression et de la température, observer la transformation d'une roche sans fusion complète, relier métamorphisme et tectonique.
Fonctionnalités: ajuster pression et température, observer le changement de roche, afficher un type de métamorphisme simplifié.
Communication IA via postMessage avec simulation_id="metamorphisme".
```

**Prompt image**
```text
Crée un schéma pédagogique sur le métamorphisme montrant roche initiale, augmentation de pression/température, transformation minéralogique et contexte tectonique associé.
```

**Prompt exercice**
```text
Crée un exercice progressif sur le métamorphisme avec identification des facteurs, distinction métamorphisme/fusion, lien tectonique/transformation rocheuse et corrigé détaillé.
```

**Prompt évaluation**
```text
Crée une évaluation formative sur le métamorphisme avec 4 questions courtes, 1 distinction métamorphisme/magmatisme, 1 lien avec tectonique des plaques et corrigé progressif.
```

### Leçon 4.3 - Granitisation

**Prompt simulation**
```text
Crée une simulation interactive HTML standalone pour la leçon "Granitisation" en SVT 2Bac PC Maroc.
Objectifs: comprendre la formation du granite, relier granitisation, épaississement crustal et contexte tectonique, distinguer granite et roches métamorphiques.
Fonctionnalités: augmenter épaississement crustal, température et profondeur, observer fusion partielle simplifiée, afficher formation du granite.
Communication IA via postMessage avec simulation_id="granitisation".
```

**Prompt image**
```text
Crée un schéma pédagogique sur la granitisation montrant collision continentale, épaississement crustal, élévation de température, fusion partielle et mise en place du granite.
```

**Prompt exercice**
```text
Crée un exercice progressif sur la granitisation avec remise en ordre des étapes, lien collision/température/granite, distinction granite/roche métamorphique et corrigé détaillé.
```

**Prompt évaluation**
```text
Crée une évaluation formative sur la granitisation avec 3 QCM, 2 questions courtes, 1 petite synthèse et un corrigé commenté.
```

---

## Utilisation pratique par l'agent IA
- **Début de leçon**: lancer d'abord image simple ou schéma d'accroche
- **Phase exploration**: lancer la simulation
- **Phase explication**: utiliser schéma structuré
- **Phase application**: donner l'exercice progressif
- **Phase consolidation**: lancer l'évaluation formative

## Priorité de production
Créer d'abord ces ressources:
1. Leçon 1.1
2. Leçon 2.1
3. Leçon 2.2
4. Leçon 2.3
5. Leçon 4.1

Ces leçons ont le plus grand impact pédagogique et d'examen.
