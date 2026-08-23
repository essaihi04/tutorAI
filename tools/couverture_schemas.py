# -*- coding: utf-8 -*-
"""Ce que le programme demande, et ce que la bibliothèque sait montrer.

Le programme du BAC est FINI : on peut donc savoir, une fois pour toutes, ce
qui manque. Chaque notion ci-dessous est passée au rapprochement automatique,
exactement comme le fait une séance. Trois verdicts :

  ✓  un schéma répond, et c'est le bon ;
  ~  un schéma répond, mais faiblement — à vérifier, souvent des mots-clés
     trop génériques ;
  ✗  rien ne répond : la notion sera expliquée sans schéma.

Les ✗ sont écrits dans la liste des manques (`schema_gaps.jsonl`), au même
endroit que ceux relevés en séance. La liste se lit comme une liste de
courses, et elle doit se vider.

    python tools/couverture_schemas.py
    python tools/couverture_schemas.py --enregistrer   (alimente la liste)
"""
from __future__ import annotations

import io
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))

from app.services.schema_catalog import match_schema  # noqa: E402
from app.services.schema_gaps import noter_manque  # noqa: E402
from app.services.scientific_visual_router import route_scientific_visual  # noqa: E402

# Le programme 2BAC PC BIOF, notion par notion, dans les mots qu'un élève ou
# un intitulé de leçon emploie vraiment.
PROGRAMME: dict[str, list[str]] = {
    "SVT — matière organique et énergie": [
        "la glycolyse et la dégradation du glucose",
        "la respiration cellulaire et le cycle de Krebs",
        "la fermentation lactique et alcoolique",
        "ultrastructure de la mitochondrie",
        "la chaîne respiratoire et la phosphorylation oxydative",
        "le bilan énergétique de la respiration et de la fermentation",
        "structure du muscle strié squelettique et de la fibre musculaire",
        "le sarcomère, actine et myosine pendant la contraction",
        "l'ATP et l'ADP, molécule d'énergie de la cellule",
        "la cellule végétale, paroi et chloroplastes",
        "la photosynthèse et les pigments chlorophylliens",
    ],
    "SVT — information génétique": [
        "la structure de l'ADN en double hélice",
        "la réplication de l'ADN",
        "la transcription et la traduction des protéines",
        "le code génétique et les codons",
        "la mitose et ses phases",
        "la méiose et le brassage génétique",
        "le monohybridisme et l'échiquier de croisement",
        "le dihybridisme et les gènes liés",
        "l'hérédité humaine et l'arbre généalogique",
        "les mutations de l'ADN",
    ],
    "SVT — géodynamique interne": [
        "la zone de subduction, fosse et arc volcanique",
        "la dorsale océanique et l'accrétion",
        "le métamorphisme et les schistes bleus",
        "la chaîne de montagnes et la racine crustale",
        "la structure interne de la Terre et les discontinuités",
        "les séismes et la propagation des ondes sismiques",
        "le magmatisme et la granitisation",
        "l'isostasie et l'équilibre de la lithosphère",
    ],
    "SVT — environnement et santé": [
        "le traitement des eaux usées dans une STEP, DBO5 et DCO",
        "la pollution des nappes par les nitrates et pesticides",
        "le tri et la valorisation des déchets, compostage et biogaz",
        "l'effet de serre renforcé et le réchauffement climatique",
    ],
    "Physique — ondes": [
        "les ondes mécaniques progressives et le retard",
        "les ondes périodiques et la longueur d'onde",
        "la diffraction de la lumière par une fente",
        "les ondes lumineuses et l'indice de réfraction",
    ],
    "Physique — nucléaire": [
        "la radioactivité alpha, bêta et gamma",
        "la décroissance radioactive et la demi-vie",
        "la fission et la fusion nucléaires",
        "l'énergie de liaison et la courbe d'Aston",
    ],
    "Physique — électricité": [
        "le dipôle RC, charge et décharge du condensateur",
        "le dipôle RL et la bobine",
        "les oscillations libres du circuit RLC",
        "les oscillations forcées et la résonance",
        "la modulation et la démodulation d'amplitude AM",
    ],
    "Physique — mécanique": [
        "les lois de Newton et le bilan des forces",
        "la chute libre verticale d'un corps",
        "le mouvement d'un projectile dans le champ de pesanteur",
        "le mouvement circulaire uniforme",
        "le mouvement des satellites et les lois de Kepler",
        "le pendule élastique et l'oscillateur mécanique",
        "le travail et l'énergie mécanique",
    ],
    "Chimie — cinétique et suivi": [
        "les transformations lentes et rapides",
        "la vitesse de réaction et le temps de demi-réaction",
        "le suivi temporel d'une transformation chimique",
    ],
    "Chimie — solutions aqueuses": [
        "l'acide, la base et le pH d'une solution",
        "le dosage acide-base et l'équivalence",
        "la conductance et la conductivité d'une solution",
        "les couples acide-base et le pKa",
    ],
    "Chimie — électrochimie et organique": [
        "la pile électrochimique, anode et cathode",
        "l'électrolyse et le sens forcé de la transformation",
        "l'estérification et l'hydrolyse d'un ester",
        "la saponification et les savons",
        "les groupes fonctionnels en chimie organique",
    ],
    "Maths": [
        "les limites de fonctions et la continuité",
        "la dérivation et l'étude des variations",
        "les fonctions exponentielle et logarithme",
        "les suites numériques arithmétiques et géométriques",
        "le calcul intégral et les primitives",
        "les probabilités et la loi binomiale",
        "les nombres complexes et le plan complexe",
        "la géométrie dans l'espace, droites et plans",
        "les équations différentielles",
        "l'arithmétique, PGCD et congruences",
    ],
}

def main() -> None:
    enregistrer = "--enregistrer" in sys.argv
    couverts = blueprints = generiques = 0
    liste_manques: list[tuple[str, str]] = []

    for chapitre, notions in PROGRAMME.items():
        print(f"\n{chapitre}")
        print("-" * len(chapitre))
        for notion in notions:
            route = route_scientific_visual(notion)
            schema_id, score = match_schema(notion)
            if route["source"] == "schema":
                couverts += 1
                print(f"  ✓ {notion:<62} SVG {route['schema_id']} ({route['score']})")
            elif route["source"] == "blueprint":
                blueprints += 1
                liste_manques.append((chapitre, notion))
                print(f"  ⚙ {notion:<62} {route['engine']} · {route['blueprint_id']}")
                if enregistrer:
                    noter_manque(notion, schema_id, score)
            else:
                generiques += 1
                liste_manques.append((chapitre, notion))
                print(f"  ◇ {notion:<62} génération générale · {route['engine']}")
                if enregistrer:
                    noter_manque(notion, schema_id, score)

    total = couverts + blueprints + generiques
    print("\n" + "=" * 78)
    print(f"{total} notions — {couverts} SVG validés, {blueprints} blueprints BAC, {generiques} routages généraux")
    print(f"couverture statique : {round(100 * couverts / total)} % | capacité de génération : 100 %")

    if liste_manques:
        print("\nBACKLOG STATIQUE — notions générables mais pas encore figées en SVG validé :")
        chapitre_courant = ""
        for chapitre, notion in liste_manques:
            if chapitre != chapitre_courant:
                chapitre_courant = chapitre
                print(f"\n  {chapitre}")
            print(f"    · {notion}")
    if enregistrer:
        print("\n(les manques ont été ajoutés à backend/data/schema_gaps.jsonl)")


if __name__ == "__main__":
    main()
