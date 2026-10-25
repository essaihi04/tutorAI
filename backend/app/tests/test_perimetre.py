"""Le périmètre du programme : fiche injectée, dépassements détectés et journalisés."""
import json

import pytest

from app.services.perimetre import _normaliser, bloc_prompt, charger, detecter, fiche, journaliser


def test_la_fiche_rc_se_charge_avec_sa_source():
    f = fiche("Physique", "dipole_RC")
    assert f is not None and "CDR-PC-2015" in f.source
    assert any("τ = RC" in n for n in f.notions)
    assert f.demonstrations_admises and f.methodes_autorisees


def test_un_chapitre_sans_fiche_n_injecte_rien():
    assert fiche("Physique", "chapitre_inconnu") is None
    assert bloc_prompt("Physique", "chapitre_inconnu") == ""
    assert bloc_prompt("Physique", None) == ""
    assert bloc_prompt("Philosophie", "dipole_RC") == ""


def test_le_bloc_prompt_dit_quoi_dire_a_la_place():
    bloc = bloc_prompt("Physique-Chimie", "dipole_RC")
    assert "[PÉRIMÈTRE DU PROGRAMME — Dipôle RC]" in bloc
    assert "N'emploie pas" in bloc and "filtre passe-bas / passe-haut →" in bloc
    assert "Ni, dans toute la matière : transformée de Laplace" in bloc
    assert "Admis sans démonstration" in bloc
    assert len(bloc) < 3500, "un bloc long se fait paraphraser au lieu d'être suivi"


def test_le_detecteur_releve_les_termes_hors_programme_avec_ou_sans_accents():
    texte = ("Pour résoudre, on applique la transformee de Laplace, ou on raisonne avec "
             "l'impédance Z du condensateur ; c'est un filtre passe-bas.")
    noms = {d.terme for d in detecter(texte, "Physique", "dipole_RC")}
    assert "transformée de Laplace" in noms and "impédance" in noms and "filtre passe-bas / passe-haut" in noms
    d = next(d for d in detecter(texte, "Physique", "dipole_RC") if d.terme == "impédance")
    assert "resistance R" in d.dire_plutot.replace("é", "e") and "impedance" in d.extrait


def test_une_reponse_au_programme_ne_declenche_rien():
    texte = ("À t = τ, la tension u_C atteint 63 % de E. La tangente à l'origine coupe l'asymptote u = E en "
             "t = τ = RC. L'énergie emmagasinée vaut ½·C·u_C².")
    assert detecter(texte, "Physique", "dipole_RC") == []


def test_les_termes_generiques_valent_meme_sans_fiche_de_chapitre():
    assert [d.terme for d in detecter("on passe par le lagrangien", "Physique", "chapitre_inconnu")] == ["lagrangien / hamiltonien"]
    assert detecter("on passe par le lagrangien", "SVT", None) == []


def test_le_journal_garde_une_ligne_par_tour_avec_depassement(tmp_path):
    chemin = tmp_path / "j.jsonl"
    journaliser([], subject="Physique", chapitre="dipole_RC", chemin=chemin)
    assert not chemin.exists(), "rien à noter, rien d'écrit"
    d = detecter("on utilise un phaseur", "Physique", "dipole_RC")
    journaliser(d, subject="Physique", chapitre="dipole_RC", student_id="0123456789", tour=4, chemin=chemin)
    ligne = json.loads(chemin.read_text(encoding="utf-8").splitlines()[0])
    assert ligne["eleve"] == "01234567" and ligne["tour"] == 4 and ligne["termes"][0]["terme"].startswith("nombres complexes")


def test_chaque_chapitre_du_programme_a_sa_fiche():
    import pathlib
    from app.services import prerequis
    racine = pathlib.Path(prerequis.CHEMIN).parent
    carte = charger()
    for fichier, matiere in (("physique.json", "Physique-Chimie"), ("mathematiques.json", "Mathématiques"), ("svt.json", "SVT")):
        programme = json.loads((racine / fichier).read_text(encoding="utf-8"))
        attendus = {ch["id"] for dom in programme["domains"] for ch in dom["chapters"]}
        fiches = set(carte[matiere]["fiches"])
        assert attendus <= fiches, (matiere, attendus - fiches)
        assert fiches <= attendus, (matiere, fiches - attendus)


def test_aucun_motif_hors_programme_ne_matche_le_programme_lui_meme():
    """Le contrôle le plus utile : un motif qui attrape un mot du programme
    ferait signaler des réponses justes. On confronte chaque motif aux notions
    et termes du programme de tous les chapitres de sa matière."""
    carte = charger()
    texte = lambda f: " ".join(list(f.notions) + list(f.termes_programme) + list(f.methodes_autorisees))
    for matiere, bloc in carte.items():
        # Les termes génériques valent pour toute la matière : aucun chapitre ne doit les employer.
        tout = _normaliser(" ".join(texte(f) for f in bloc["fiches"].values()))
        for t in bloc["generiques"]:
            hit = t.motif.search(tout)
            assert hit is None, (matiere, "générique", t.terme, tout[max(0, hit.start() - 30):hit.end() + 30])
        # Les termes d'un chapitre ne sont détectés que dans ce chapitre : « passe-bas » est
        # hors programme pour le RC et au programme de la modulation.
        for f in bloc["fiches"].values():
            propre = _normaliser(texte(f))
            for t in f.termes_hors_programme:
                hit = t.motif.search(propre)
                assert hit is None, (matiere, f.chapitre, t.terme, propre[max(0, hit.start() - 30):hit.end() + 30])


def test_chaque_bloc_prompt_reste_court():
    carte = charger()
    for matiere, bloc in carte.items():
        for chapitre in bloc["fiches"]:
            # ≈ 1 000 jetons : au-delà, le bloc se fait paraphraser au lieu d'être suivi.
            assert len(bloc_prompt(matiere, chapitre, carte)) < 4300, (matiere, chapitre)


def test_une_fiche_incomplete_est_refusee(tmp_path):
    mauvais = tmp_path / "p.json"
    mauvais.write_text(json.dumps({"matieres": {"Physique-Chimie": {"termes_hors_programme": [{"terme": "x"}], "chapitres": {}}}}), encoding="utf-8")
    with pytest.raises(ValueError):
        charger(mauvais)
