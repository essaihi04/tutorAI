export const meta = {
  name: 'corrections-physique-s1-ch6-8',
  description: 'Corriger les manques confirmés de la physique S1 (ch6-ch8) et relire toutes leurs démonstrations selon les skills (copies en attente)',
  phases: [{ title: 'Corrections' }],
}
const S = '/tmp/claude-0/-home-user-tutorAI/37504a6f-3914-5276-9f3c-7fce56aca424/scratchpad'
const R = '/home/user/tutorAI'
const COMMUN = `
Projet Moalim : tuteur IA pour le 2e bac marocain, filière sciences physiques (PC) BIOF. Les cours sont des JSON joués au tableau (mode concentration) : diapos (activities[].slides[]) avec écran (screen_content), voix (speech_text.mixed, darija + termes français), concentration (centre, pointage, cahier, reponses…), questions et exercices avec leur demonstration {parole, lignes:[{texte, mot}], audio}, séances et blocs (seances[].blocs[] : slide_ids, cahier, retrouver, exercice), competences.

À LIRE D'ABORD (en entier, c'est la demande expresse de l'utilisateur : « prendre en considération les skills de démonstration au fond ») :
- ${R}/.agents/skills/professeur/SKILL.md — les règles 37 (démonstration jusqu'au bout, AVEC son volet « Physics-chemistry » et « Shown one line at a time »), 38 (condition, « car », unités, conventions dessinées, phrases du bac — paragraphe physique-chimie), 10 (rédaction du barème), 17 (voix), 26, 27, 33 (une chose à la fois), 34.
- ${R}/.agents/skills/cours-concentration/SKILL.md — le format des données, les puces sur la démonstration (« written on its own board », « handwritten demonstration », « Every board fits on ONE screen »), l'étape 9b, la section Physique (pièges et hors cadre), « Formulas in the written text ».
- ${R}/.agents/skills/voix-du-cours/SKILL.md — pour toute nouvelle « parole » ou voix : darija simple, termes du programme, nombres et symboles DITS en mots, pas de tachkil.
- ${R}/docs/audit-rythme/BRIEF.md, section « Où écrire ».

OÙ ÉCRIRE (d'autres sessions travaillent sur le dépôt) :
- Ne modifie JAMAIS un cours en ligne (${R}/backend/data/courses/<deck>.json). La copie en attente ${R}/backend/data/courses/en_attente/<deck>.json EXISTE déjà (démonstrations déjà reprises ce matin) : PARS DE CETTE COPIE, ne perds rien de ce qu'elle contient.
- Écris avec json.dumps(d, ensure_ascii=False, indent=2), fins de ligne LF, en relisant le fichier juste avant d'écrire.
- Toute « parole » ou speech_text.mixed modifiée ou nouvelle : retire son « audio ». Ne touche pas aux voix inchangées. Chaque « mot » (lignes de démonstration, pointage, centre) est un extrait EXACT de sa parole/voix.
- Pas de nouvelle simulation ; une nouvelle diapo réutilise une vue existante du chapitre si elle convient, sinon sans visuel (signale-le). Une nouvelle diapo va dans un bloc, reçoit ses competence_ids et, si elle porte une question, ses réactions préparées (concentration.reponses : juste / faux 1 / faux 2 avec parole et ecrit, sans audio) et sa démonstration si elle demande un calcul. Règle 27 : on ne demande que ce qui est enseigné.
- Ne modifie rien d'autre dans le dépôt, ne commite pas, ne pousse pas.

DÉMONSTRATIONS « AU FOND » (règles 33, 37, 38, 10 et cours-concentration 9b) — dernière étape obligatoire, sur TOUTES les démonstrations du cours après tes corrections (question.demonstration, exercices et leurs statements, seances[].blocs[].exercice.demonstration, preuves et exemples travaillés écrits sur une diapo — centre, bullets, student_trace — et au cahier, réactions qui corrigent) :
- elle part des données de l'énoncé et nomme la loi utilisée avec ses conditions (« onde non amortie », « milieu homogène », convention récepteur, loi d'additivité des tensions) ;
- toute relation garde la ligne d'où elle vient (τ = SM/v car v = d/Δt…) ; aucune relation « parachutée » ;
- une étape par ligne : relation littérale, puis chaque conversion d'unité sur sa ligne, puis la substitution numérique, puis le résultat avec unité et chiffres significatifs ; rien de tête ;
- équation différentielle : établie depuis la loi jusqu'à la forme canonique avec la constante nommée ; solution : vérifiée par remplacement (dérivée écrite, termes qui s'annulent), puis condition initiale, puis identification des constantes ; valeurs particulières (e⁻¹ ≈ 0,37, 1 − e⁻¹ ≈ 0,63, N₀/2ⁿ, 5τ) calculées, pas annoncées ;
- elle va jusqu'au bout : la dernière ligne répond exactement à la question (valeur + unité, ou phrase de conclusion du bac) et à « correct » ;
- plus de ~8 lignes : deux démonstrations/tableaux (la méthode, puis le calcul), jamais moins d'étapes ; sur une diapo, une preuve en plusieurs étapes a une entrée centre (ou pointage) par ligne, chacune sur son mot ;
- la parole dit chaque ligne dans l'ordre ; audio retiré si changée. Vérifie chaque calcul en python.
Une démonstration déjà complète reste telle quelle.

VÉRIFICATION avant de finir : json valide ; script : chaque « mot » de demonstration.lignes est dans sa parole, chaque pointage/centre « mot » dans speech_text.mixed ; chaque slide dans exactement un bloc ; chaque competence_id existe ; lance aussi python3 -I ${S}/verif_attente.py <fichier> (0 mot absent, 0 hors bloc).
`
const CH = [
  ['ch6', 'Dipôle RC', 'phys_ch6_dipole_RC', "Doute à trancher si tu peux : rc_e8_national e0 et le bloc rc_s2_b3 donnent Q_max = 12 µC et E = 1,2 V alors que le sujet national 2023 R aurait q_max = 120 µC ; vérifie la cohérence interne de l'énoncé, ne change « correct » que si l'énoncé lui-même est incohérent."],
  ['ch7', 'Dipôle RL', 'phys_ch7_dipole_RL', ''],
  ['ch8', 'Oscillations libres d’un circuit RLC série', 'phys_ch8_circuit_RLC', ''],
]
phase('Corrections')
const res = await parallel(CH.map(([k, titre, deck, extra]) => () => agent(COMMUN + `
TA TÂCHE : le cours de physique « ${titre} » (copie en attente ${R}/backend/data/courses/en_attente/${deck}.json).
${extra}
1. CORRIGER LES MANQUES CONFIRMÉS. Lis l'audit ${S}/audit-phys/${k}.md (aussi dans ${R}/docs/audit-prof/physique.md). Corrige : tous les manques confirmés de priorité haute et moyenne ; ceux de priorité basse quand c'est un simple ajout écrit ; les éléments « présents seulement à l'oral » (les écrire à l'écran ou au cahier) ; toutes les « démonstrations qui sautent des étapes » ; les notations à ajouter que l'audit recommande. Ne fais PAS : les manques chez un seul professeur (sauf exigés par le cadre, dis-le), rien de hors cadre (${R}/docs/audit-programme-officiel/physique.md, fiche backend/data/curriculum/cadre_reference_2bac_pc.json). Si l'audit signale une erreur dans le cours, corrige-la si tu en es sûr.
   Comment : d'abord par les champs ÉCRITS existants (screen_content, centre, cahier, student_trace, bilan, blocs[].cahier) — condition de validité, « car… », unité, convention, phrase du bac, schéma décrit au cahier (cahier_figures si le format le permet, sinon texte). Une notion absente qui ne tient pas dans une diapo existante → nouvelle diapo au bon endroit (règles 26, 33, 34), avec voix, cahier, bloc, compétence ; ne pas alourdir : regroupe. Ne change une voix existante que si l'écran dit désormais autre chose.
2. DÉMONSTRATIONS « AU FOND » : la passe décrite plus haut, sur tout le cours.
3. RAPPORT : écris ${S}/corr/phys-${k}.md (Markdown, français simple, compact) :
   ## ${titre}
   ### Manques corrigés (tableau : constat | ce qui a été fait | diapo(s))
   ### Non corrigés et pourquoi
   ### Démonstrations (relues, réécrites, 3 exemples avant → après en une ligne chacun)
   ### Voix à enregistrer (id)
   ### Vérifications faites (résultats)
   Réponds à la fin en 5 lignes : manques corrigés, diapos nouvelles, démonstrations réécrites, pistes voix, ce qui reste à décider.
`, { label: 'phys:' + k, phase: 'Corrections' })))
return res