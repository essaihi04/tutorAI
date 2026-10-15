"""Version 3 du cours phys_ch1_waves : diapositives simplifiées pour un élève de 2e Bac + script darija réécrit.

Suit le plan du cours marocain (Pr. El Kaouahi, moutamadris.ma) : expériences → définitions → types
d'ondes → le son → propriétés (dimensions, superposition, célérité, facteurs) → retard temporel.
Règles : une idée par diapositive, phrases courtes, la formule visible à l'écran quand on la dit,
le vocabulaire du Bac (perturbation, milieu, célérité, retard) toujours écrit pareil.
Le script darija vient de phys_ch1_waves_mixed_script_v3.json ; les visuels existants sont conservés."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "data" / "courses"
MANIFEST = ROOT / "phys_ch1_waves_course_v1.json"
SCRIPT = ROOT / "phys_ch1_waves_mixed_script_v3.json"

# Écran (lead + bullets courts, formule visible) et voix française simplifiée, par diapositive.
ECRANS: dict[str, dict] = {
    "waves_water_entry": {
        "lead": "Une goutte tombe sur l'eau calme : des rides s'éloignent du point d'impact.",
        "bullets": ["Où est la source ?", "Qu'est-ce qui se déplace vraiment : l'eau, ou la forme ?"],
        "fr": "Bienvenue dans le premier chapitre de physique : les ondes mécaniques progressives. On commence par une expérience simple : une goutte tombe sur de l'eau calme. Observe les rides qui s'éloignent du point d'impact. Où est la source ? Et qu'est-ce qui se déplace vraiment ?",
    },
    "waves_a00_s01": {
        "lead": "Une secousse à gauche d'une corde tendue.",
        "bullets": ["Le capteur A réagit d'abord, puis B.", "Qu'est-ce qui arrive jusqu'à B : un morceau de corde, ou la déformation ?"],
        "essential_text": "Question de départ, sans note.",
        "fr": "On tend une corde et on donne une secousse à son extrémité gauche. Le capteur A réagit d'abord, puis le capteur B un peu plus tard. Avant tout calcul, demande-toi ce qui arrive jusqu'à B : un morceau de corde, ou seulement la déformation ? Réponds sans crainte, cette question n'est pas notée.",
    },
    "waves_a00_s02": {
        "lead": "Comment un signal avance-t-il sans transporter la matière ?",
        "bullets": ["La perturbation avance le long de la corde.", "Chaque point de la corde bouge sur place, puis revient.", "Au programme : décrire, comparer deux dates, mesurer distance et retard."],
        "fr": "Voici la question du chapitre : comment un signal avance-t-il sans transporter la matière ? Sur le schéma, deux mouvements : la perturbation avance le long de la corde, mais chaque point de la corde bouge sur place puis revient. Pour répondre, on va décrire la perturbation, comparer deux dates, et mesurer une distance et un retard.",
    },
    "waves_cord_observe": {
        "lead": "Lance une seule impulsion et regarde le point orange.",
        "bullets": ["Où est-il avant ? Où est-il après ?", "A-t-il changé de place à la fin ?"],
        "fr": "Lance une seule impulsion dans la simulation. Regarde seulement le point orange. Où est-il avant le passage de la perturbation, et où est-il après ? A-t-il changé de place à la fin ?",
    },
    "waves_a01_s01": {
        "lead": "La perturbation se transmet de proche en proche.",
        "bullets": ["Un point bouge → il entraîne ses voisins.", "L'énergie avance ; la matière reste sur place.", "La bouée monte et descend, elle ne suit pas la vague."],
        "student_trace": "L'onde transporte de l'énergie, pas de la matière.",
        "fr": "Pourquoi la perturbation avance-t-elle ? À un instant t, un point du milieu bouge, et il entraîne ses voisins : la perturbation se transmet de proche en proche. L'énergie avance depuis la source, mais la matière revient à sa place. Comme une bouée sur l'eau : elle monte et descend, elle ne suit pas la vague. Donc l'onde transporte de l'énergie, pas de la matière.",
    },
    "waves_spring_observe": {
        "lead": "Un ressort : on serre quelques spires, puis on lâche.",
        "bullets": ["Suis la spire marquée.", "Compare : direction de propagation, direction du mouvement de la spire."],
        "fr": "Troisième expérience du cours : un long ressort. On serre quelques spires, puis on les lâche. Suis la spire marquée et compare deux directions : celle de la propagation, et celle du mouvement de la spire.",
    },
    "waves_a01_s02": {
        "lead": "Deux directions à comparer : mouvement local et propagation.",
        "bullets": ["Perpendiculaires → onde transversale (corde, eau, ondes S).", "Parallèles → onde longitudinale (ressort, son, ondes P)."],
        "student_trace": "Transversale ⟂ ; longitudinale ∥.",
        "fr": "Pour nommer le type d'onde, on compare deux directions. Sur la corde, la perturbation est verticale et la propagation horizontale : perpendiculaires, c'est une onde transversale. Dans le ressort, les spires bougent dans la direction de propagation : parallèles, c'est une onde longitudinale. Dans les séismes aussi : les ondes S sont transversales, les ondes P longitudinales.",
    },
    "waves_definitions": {
        "lead": "Les définitions à retenir.",
        "bullets": ["Perturbation : modification temporaire du milieu (position, vitesse…).", "Source S : là où naît la perturbation.", "Onde mécanique : propagation d'une perturbation dans un milieu matériel, sans transport de matière, avec transport d'énergie.", "Milieu élastique : il reprend sa forme après le passage de l'onde."],
        "student_trace": "Onde mécanique = perturbation + milieu matériel + énergie transportée.",
        "fr": "Écrivons les définitions. La perturbation est une modification temporaire d'une propriété mécanique du milieu, comme la position ou la vitesse. La source est l'endroit où naît la perturbation. Une onde mécanique est la propagation d'une perturbation dans un milieu matériel, sans transport de matière, mais avec transport d'énergie. Et le milieu doit être élastique : il reprend sa forme après le passage de l'onde.",
    },
    "waves_bell_model": {
        "lead": "Un réveil sous une cloche : avec de l'air, puis presque sans air.",
        "bullets": ["Le réveil vibre toujours.", "Le son arrive-t-il encore jusqu'à toi ?"],
        "fr": "Le son est-il aussi une onde mécanique ? On met un réveil qui sonne sous une cloche, puis on retire l'air avec une pompe. Compare le son avec de l'air, puis presque sans air. Attention : le réveil vibre toujours, mais le son arrive-t-il encore jusqu'à toi ?",
    },
    "waves_sound_trace": {
        "lead": "Sans air, le son disparaît : le son a besoin d'un milieu matériel.",
        "bullets": ["Le son ne se propage pas dans le vide.", "Donc le son est une onde mécanique.", "Un son résiduel peut passer par les supports du montage."],
        "fr": "Quand on retire l'air, le son faiblit jusqu'à disparaître, alors que la source vibre toujours. Conclusion : le son a besoin d'un milieu matériel et ne se propage pas dans le vide. Le son est donc une onde mécanique. S'il reste un son faible, il passe par les supports du montage.",
    },
    "waves_air_particles": {
        "lead": "La membrane du haut-parleur pousse l'air.",
        "bullets": ["Repère les compressions (air serré) et les dilatations (air étalé).", "La particule orange part-elle avec le son, ou va-et-vient-elle sur place ?"],
        "fr": "Regarde la membrane du haut-parleur et les particules d'air. Repère les endroits où l'air est serré, les compressions, et ceux où il est étalé, les dilatations. Suis la particule orange : part-elle avec le son, ou fait-elle un va-et-vient sur place ?",
    },
    "waves_air_summary": {
        "lead": "Dans l'air, le son est une onde longitudinale.",
        "bullets": ["Chaque particule bouge dans la direction de propagation.", "La flamme devant le haut-parleur bouge horizontalement.", "Le son se propage dans toutes les directions autour de la source."],
        "student_trace": "Son = compression-dilatation du milieu (solide, liquide, gaz).",
        "fr": "Dans l'air, chaque particule bouge dans la direction de propagation : le son est une onde longitudinale. C'est ce que montre la flamme d'une bougie devant un haut-parleur : elle bouge horizontalement. Attention, la courbe de pression n'est pas le trajet des molécules. Et le son se propage dans toutes les directions autour de la source.",
    },
    "waves_water_lab": {
        "lead": "La surface de l'eau vue du dessus.",
        "bullets": ["Autour de S, des cercles qui grandissent.", "Pourquoi des cercles ? Même vitesse dans toutes les directions."],
        "fr": "Revenons à la surface de l'eau, vue du dessus. Autour du point S apparaissent des cercles qui grandissent. Pourquoi des cercles ? Parce que dans un milieu homogène, l'onde avance à la même vitesse dans toutes les directions de la surface.",
    },
    "waves_dimensions": {
        "lead": "L'onde se propage dans toutes les directions qui lui sont offertes.",
        "bullets": ["Corde, ressort : 1 dimension (une ligne).", "Surface de l'eau : 2 dimensions (un plan).", "Son dans l'air : 3 dimensions (l'espace)."],
        "student_trace": "1D corde/ressort — 2D eau — 3D son.",
        "fr": "L'onde se propage dans toutes les directions qui lui sont offertes. Sur une corde ou un ressort, une seule direction : onde à une dimension. À la surface de l'eau, elle avance dans un plan : onde à deux dimensions. Le son dans l'air se propage dans tout l'espace : onde à trois dimensions.",
    },
    "waves_overlap_lab": {
        "lead": "Deux impulsions arrivent l'une vers l'autre.",
        "bullets": ["Regarde avant, pendant, après la rencontre.", "Essaie : mêmes sens, puis sens opposés.", "Mets en pause à t = 2,5 s."],
        "fr": "Deux impulsions arrivent des deux côtés de la même corde. Suis-les avant la rencontre, pendant, et après. Essaie deux cas : deux impulsions du même côté, puis de côtés opposés. Mets en pause à t égal deux virgule cinq secondes et observe.",
    },
    "waves_overlap_summary": {
        "lead": "Pendant la rencontre, les déplacements s'ajoutent.",
        "bullets": ["Même sens : la bosse grandit.", "Sens opposés : elles peuvent s'annuler un instant.", "Après : chaque impulsion continue sans changer."],
        "student_trace": "Superposition : les amplitudes s'ajoutent algébriquement, puis chaque onde repart intacte.",
        "fr": "Pendant la rencontre, les déplacements s'ajoutent algébriquement. Du même côté, la bosse grandit. De côtés opposés, elles peuvent s'annuler un instant. Mais après, chaque impulsion continue son chemin sans changer. C'est la superposition des ondes.",
    },
    "waves_tp_report": {
        "lead": "Remplis ton tableau d'observation.",
        "bullets": ["Pour chaque expérience : milieu, perturbation, direction locale, dimension.", "Justifie avec ce que tu as vu, pas avec une règle apprise."],
        "fr": "Remplis maintenant ton tableau. Pour chaque expérience, écris le milieu, la perturbation, la direction du mouvement local et la dimension. Justifie chaque réponse avec une observation précise, pas seulement avec une règle apprise par cœur.",
    },
    "waves_tp_correction": {
        "lead": "Correction du tableau.",
        "bullets": ["Corde : transversale, 1D.", "Ressort : longitudinale, 1D.", "Son dans l'air : longitudinale, 3D.", "Surface de l'eau : transversale, 2D."],
        "student_trace": "Le type d'onde se lit sur la direction du mouvement local par rapport à la propagation.",
        "fr": "Corrigeons ensemble. La corde : déformation transversale, propagation à une dimension. Le ressort : compression longitudinale, une dimension. Le son dans l'air : compression longitudinale, trois dimensions. La surface de l'eau : onde transversale, deux dimensions. Le classement repose toujours sur la direction du mouvement local par rapport à la propagation.",
    },
    "waves_front_speed": {
        "lead": "Deux photos de la même corde, à t₁ puis t₂.",
        "bullets": ["Repère le même sommet sur les deux photos.", "d = distance parcourue ; Δt = t₂ − t₁.", "v = d / Δt (d en m, Δt en s)."],
        "student_trace": "Dans un milieu homogène, la célérité v est constante.",
        "fr": "Passons à la mesure. Voici deux photos de la même corde, à t un puis t deux. Repère le même sommet sur les deux photos et mesure la distance d qu'il a parcourue. Calcule la durée entre les deux photos. La célérité vaut v égal d sur delta t, avec d en mètres et delta t en secondes. Dans un milieu homogène, cette célérité est constante.",
    },
    "waves_a02_s01": {
        "lead": "Deux capteurs A et B sur la corde.",
        "bullets": ["A détecte à tA, B détecte à tB.", "Retard : τ = tB − tA.", "Célérité : v = AB / τ."],
        "student_trace": "Convertir : ms → s, cm → m, avant d'appliquer v = d/τ.",
        "fr": "Deux capteurs, A et B. A détecte la perturbation à t A, et B à t B. Le retard tau est la différence t B moins t A. Si la distance entre les capteurs est d, la célérité vaut d divisé par tau. Le grand piège, ce sont les unités : les millisecondes en secondes, les centimètres en mètres.",
    },
    "waves_a02_s02": {
        "lead": "Exemple : AB = 80 cm et τ = 20 ms.",
        "bullets": ["80 cm = 0,80 m", "20 ms = 0,020 s", "v = 0,80 / 0,020 = 40 m/s"],
        "essential_text": "Au Bac : relation, conversions, calcul, unité.",
        "fr": "Exemple : AB vaut quatre-vingts centimètres et tau vaut vingt millisecondes. On convertit d'abord : zéro virgule quatre-vingts mètre, et zéro virgule zéro vingt seconde. Puis on divise : v égal quarante mètres par seconde. Au Bac, écris la relation, les conversions, le calcul, et enfin l'unité.",
    },
    "waves_medium_lab": {
        "lead": "Trois essais : change une seule chose à la fois.",
        "bullets": ["Plus de tension, même masse linéique.", "Plus de masse linéique, même tension.", "Seulement l'amplitude."],
        "fr": "La célérité change-t-elle ? Fais trois essais en ne changeant qu'une seule chose à la fois. Augmente la tension de la corde à masse linéique fixe. Puis augmente la masse linéique à tension fixe. Enfin, change seulement l'amplitude, et regarde ce qui agit sur la célérité.",
    },
    "waves_medium_summary": {
        "lead": "La célérité ne dépend que du milieu.",
        "bullets": ["Corde : v augmente avec la tension, diminue avec la masse linéique.", "Gaz : dépend de la température et du gaz.", "L'amplitude et la durée de la perturbation ne changent pas v."],
        "student_trace": "v dépend du milieu (tension, masse linéique, température), jamais de l'amplitude.",
        "fr": "Conclusion : la célérité ne dépend que du milieu. Sur une corde, elle augmente avec la tension et diminue avec la masse linéique. Dans un gaz, elle dépend de la température et du gaz. L'amplitude ou la durée de la perturbation ne changent pas la célérité.",
    },
    "waves_a03_s01": {
        "lead": "Mission : deux mesures de célérité.",
        "bullets": ["Place A et B, lance l'impulsion.", "Lis tA et tB, calcule τ et v, enregistre.", "Déplace un capteur et recommence."],
        "essential_text": "Deux mesures cohérentes valent mieux qu'une.",
        "fr": "Dans la simulation, reste sur la mission onde progressive. Place les deux capteurs, lance l'impulsion et enregistre la mesure. Puis déplace un capteur et recommence. Le laboratoire compare ta célérité à celle du modèle. L'objectif : deux mesures cohérentes, pas cliquer vite.",
    },
    "waves_a03_s02": {
        "lead": "Compare tes deux célérités.",
        "bullets": ["Même milieu, mêmes réglages → valeurs proches.", "Grand écart → erreur d'unité ou de lecture des dates.", "d et τ grandissent ensemble ; d/τ reste presque constant."],
        "student_trace": "Dans un milieu donné, la célérité est une caractéristique du milieu.",
        "fr": "Compare tes deux célérités. Elles doivent être proches si le milieu et les réglages n'ont pas changé. Un grand écart signale souvent une erreur d'unité ou de lecture des dates. Conclusion : d et tau grandissent ensemble, et leur quotient reste presque constant.",
    },
    "waves_source_delay": {
        "lead": "De la source S au point M.",
        "bullets": ["M reproduit le mouvement de S avec un retard τ.", "τ = SM / v", "yM(t) = yS(t − τ)"],
        "student_trace": "Le retard τ = SM/v ; M répète S avec ce retard.",
        "fr": "Revenons à la source. Toute perturbation créée en S atteint le point M après un retard tau, avec tau égal S M sur v. Autrement dit, M reproduit le mouvement de S, mais en retard de tau. On écrit : y de M à l'instant t égal y de S à l'instant t moins tau.",
    },
    "waves_a04_s01": {
        "lead": "Le même pic : à 1,5 s sur A, à 3,5 s sur B.",
        "bullets": ["Choisir deux événements identiques (ici les deux maxima).", "τ = 3,5 − 1,5 = 2,0 s", "AB = 6,0 m → v = 6,0 / 2,0 = 3,0 m/s"],
        "student_trace": "Le retard se mesure entre deux événements de même nature : début, maximum, passage par zéro.",
        "fr": "Sur deux enregistrements, on ne soustrait pas n'importe quelles abscisses. Il faut le même événement sur les deux signaux, ici les deux maxima de la même impulsion. Le retard vaut deux secondes. Avec six mètres entre les capteurs, la célérité vaut six divisé par deux, soit trois mètres par seconde.",
    },
    "waves_final_problem": {
        "lead": "Exercice type Bac : deux micros à 1,70 m, retard 5,0 ms.",
        "bullets": ["1. Quel type d'onde dans l'air ?", "2. Convertis le retard, calcule v.", "3. Retard pour 3,40 m dans les mêmes conditions ?"],
        "fr": "Un exercice complet, type Bac. Deux microphones distants d'un mètre soixante-dix détectent le même signal avec cinq millisecondes de retard. Un : quel type d'onde est le son dans l'air ? Deux : convertis le retard et calcule v. Trois : quel retard pour trois mètres quarante dans les mêmes conditions ? Essaie seul avant la correction.",
    },
    "waves_a04_s02": {
        "lead": "Bilan du chapitre.",
        "bullets": ["Onde mécanique : perturbation + milieu matériel ; énergie transportée, pas la matière.", "Transversale ou longitudinale ; 1D, 2D ou 3D.", "Célérité constante dans un milieu homogène, dépend du milieu.", "Retard : τ = d / v ; yM(t) = yS(t − τ)."],
        "student_trace": "Méthode Bac : repérer deux événements identiques, convertir, calculer, écrire l'unité.",
        "fr": "Résumons le chapitre. Une onde mécanique est la propagation d'une perturbation dans un milieu matériel : elle transporte de l'énergie, pas la matière. Elle peut être transversale ou longitudinale, à une, deux ou trois dimensions. Dans un milieu homogène, la célérité est constante et ne dépend que du milieu. Et le retard tau vaut d sur v. Voilà les outils dont tu as besoin à l'examen.",
    },
    "waves_selfassessment": {
        "lead": "Mon bilan : acquis, en cours, ou à renforcer ?",
        "fr": "Évalue-toi. Pour chaque compétence, choisis acquis, en cours, ou à renforcer, et donne un exemple qui justifie ton choix. Si un point reste difficile, le tuteur reprendra avec toi les observations ou les calculs.",
    },
    "waves_transition": {
        "lead": "Et si la source répète son mouvement régulièrement ?",
        "bullets": ["Une suite d'impulsions à intervalles égaux.", "C'est le chapitre suivant : les ondes progressives périodiques."],
        "fr": "Dernière question, pour le chapitre suivant : que se passe-t-il si la source répète son mouvement régulièrement, à intervalles égaux ? Ce sont les ondes mécaniques progressives périodiques, et c'est par là que commence le prochain cours. Merci pour ton attention, à bientôt.",
    },
}


def main() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    script = json.loads(SCRIPT.read_text(encoding="utf-8"))
    touched = 0
    for activity in manifest["activities"]:
        for slide in activity["slides"]:
            sid = slide["stable_id"]
            ecran = ECRANS[sid]
            screen = slide.setdefault("screen_content", {})
            screen["lead"] = ecran["lead"]
            for key in ("bullets", "essential_text", "student_trace"):
                if key in ecran:
                    screen[key] = ecran[key]
                else:
                    screen.pop(key, None)
            slide["speech_text"]["fr"] = ecran["fr"]
            slide["speech_text"]["mixed"] = script[sid]
            touched += 1
    manifest["version"] = 3
    manifest["catalog"]["summary"] = ("Expériences (corde, ressort, eau, son), définitions, types d'ondes, "
                                      "dimensions et superposition, célérité et retard — plan du cours de 2e Bac.")
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{touched} diapositives réécrites → {MANIFEST.name} (version 3)")


if __name__ == "__main__":
    main()
