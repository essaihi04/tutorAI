"""Le contrat du script « prof en direct », tenu par l'exemple du prompt.

Un modèle imite l'EXEMPLE avant de lire la consigne. Celui du
``UI_CONTROL_PROMPT`` est donc la vraie spécification du format : si ses
``write`` n'ont pas de ``say``, le modèle n'en mettra pas non plus, et le
tableau écrira des lignes que personne n'explique.

Ce que le tableau fait de ces deux champs (``LiveBoard.tsx``) :

  ① la ligne s'écrit sous les yeux de l'élève et elle est LUE à voix haute,
     en français, mot pour mot — l'écriture avance au rythme de la parole ;
  ② puis le ``say`` explique ce qui vient d'être écrit, la ligne complète
     sous les yeux.

Demandé le 20 août 2026 : « une phrase écrite doit d'abord être dite et
expliquée par le prof, ensuite on écrit une autre information ».
"""
import json

from app.services.llm_service import UI_CONTROL_PROMPT


def _exemple_show_live() -> dict:
    """Le script de démonstration, extrait du prompt et décodé."""
    lignes = UI_CONTROL_PROMPT.split("\n")
    debut = next(
        i for i, l in enumerate(lignes)
        if l.startswith('<ui>{"actions":[{"type":"whiteboard","action":"show_live"')
    )
    fin = next(i for i in range(debut, len(lignes)) if lignes[i].startswith("]}}]}</ui>"))
    bloc = "\n".join(lignes[debut:fin + 1])
    return json.loads(bloc[len("<ui>"):-len("</ui>")])


def _steps() -> list[dict]:
    return _exemple_show_live()["actions"][0]["payload"]["steps"]


def test_l_exemple_du_prompt_est_un_json_valide():
    """Un exemple cassé apprend au modèle à produire du JSON cassé."""
    assert len(_steps()) > 5


def test_chaque_ligne_ecrite_est_expliquee():
    """Sans `say`, l'élève recopie une ligne dont personne ne dit le sens."""
    ecrits = [s for s in _steps() if s.get("action") == "write"]

    assert ecrits, "l'exemple n'écrit rien"
    for step in ecrits:
        dit = (step.get("say") or "").strip()
        assert dit, f"write sans say : {step['line']['content']}"


def test_l_explication_ne_redit_pas_la_ligne():
    """Le tableau LIT déjà la ligne. Un `say` qui la répète la fait entendre
    deux fois, et n'explique toujours rien."""
    for step in _steps():
        if step.get("action") != "write":
            continue
        ecrit = step["line"]["content"].strip().lower()
        dit = (step.get("say") or "").strip().lower()
        assert dit != ecrit, f"say identique à la ligne : {ecrit}"


def test_les_lignes_ecrites_restent_courtes():
    """Un tableau n'est pas un PDF : la phrase complète est à l'oral."""
    for step in _steps():
        if step.get("action") != "write":
            continue
        contenu = step["line"]["content"]
        # Les formules LaTeX ne se comptent pas en mots.
        if "\\" in contenu or "$" in contenu:
            continue
        assert len(contenu.split()) <= 8, contenu
