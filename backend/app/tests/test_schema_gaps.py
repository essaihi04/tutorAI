"""La liste des schémas qui manquent doit être fiable et silencieuse.

Fiable : un vrai manque s'y retrouve. Silencieuse : elle n'interrompt jamais
une séance, et elle ne se remplit pas de « bonjour ».
"""

import json

import app.services.schema_gaps as gaps


def _isoler(tmp_path, monkeypatch):
    monkeypatch.setattr(gaps, "FICHIER", tmp_path / "schema_gaps.jsonl")
    monkeypatch.setattr(gaps, "_deja_notes", set())


def test_un_manque_reel_est_note(tmp_path, monkeypatch):
    _isoler(tmp_path, monkeypatch)

    assert gaps.noter_manque("structure de la cellule végétale, paroi et vacuole", None, 0)

    lignes = [json.loads(l) for l in gaps.FICHIER.read_text(encoding="utf-8").splitlines()]
    assert len(lignes) == 1
    assert "cellule" in lignes[0]["sujet"]
    assert lignes[0]["score"] == 0


def test_le_meme_sujet_ne_se_note_qu_une_fois(tmp_path, monkeypatch):
    """Un sujet revient à chaque tour d'une séance : la liste de courses ne
    doit pas devenir un journal de bord."""
    _isoler(tmp_path, monkeypatch)

    assert gaps.noter_manque("le cycle de l'eau et les nappes phréatiques")
    assert not gaps.noter_manque("Le cycle de l'eau et les nappes phreatiques !")

    assert len(gaps.FICHIER.read_text(encoding="utf-8").splitlines()) == 1


def test_le_bavardage_n_est_pas_un_manque(tmp_path, monkeypatch):
    _isoler(tmp_path, monkeypatch)

    assert not gaps.noter_manque("bonjour")
    assert not gaps.noter_manque("   ")
    assert not gaps.noter_manque("ok merci")
    assert not gaps.FICHIER.exists()


def test_une_ecriture_impossible_n_interrompt_pas_la_seance(tmp_path, monkeypatch):
    """Perdre une ligne de liste de courses est acceptable ; couper le cours
    au milieu d'une explication ne l'est pas."""
    _isoler(tmp_path, monkeypatch)

    def refuse(*args, **kwargs):
        raise OSError("disque plein")

    monkeypatch.setattr(gaps.Path, "open", refuse)

    assert gaps.noter_manque("la photosynthèse et les pigments chlorophylliens") is False


def test_les_manques_se_relisent_du_plus_recent(tmp_path, monkeypatch):
    _isoler(tmp_path, monkeypatch)
    gaps.noter_manque("premier sujet à dessiner un jour")
    gaps.noter_manque("second sujet à dessiner un jour")

    releve = gaps.manques()

    assert [m["sujet"][:6] for m in releve] == ["second", "premie"]
