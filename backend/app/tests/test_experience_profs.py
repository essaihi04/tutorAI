"""L'expérience des profs : fiche chargée, vérifiée contre le programme, servie au bon moment."""
import json

from app.services import experience_profs, perimetre
from app.services.experience_profs import bloc_explication, bloc_pieges, bloc_resolution, detecter, fiche
from app.services.skill_professeur import SkillProfesseur, retirer_balise_eval


def test_la_fiche_des_ondes_se_charge():
    f = fiche("Physique-Chimie", "ondes_mecaniques")
    assert f is not None and f.nom == "Ondes mécaniques progressives"
    assert {c.id for c in f.cas_types} >= {"oscillogramme", "echo", "deux_milieux", "photo"}
    assert len(f.pieges) >= 10 and f.valeurs_reperes


def test_un_chapitre_sans_fiche_ne_recoit_rien():
    assert fiche("Physique", "chapitre_inconnu") is None
    assert fiche("Physique", None) is None
    assert bloc_explication(None) == bloc_resolution(None) == bloc_pieges(None) == ""


def test_les_chapitres_existent_dans_le_perimetre():
    """Une fiche d'expérience sans périmètre n'aurait rien pour la borner."""
    carte_perimetre = perimetre.charger()
    for matiere, chapitres in experience_profs.charger().items():
        for chapitre in chapitres:
            assert chapitre in carte_perimetre[matiere]["fiches"], chapitre


def test_rien_de_hors_programme_n_est_enseigne():
    """Ce que le périmètre interdit n'apparaît que dans la liste des exclus."""
    brut = json.loads(experience_profs.CHEMIN.read_text(encoding="utf-8"))
    carte_perimetre = perimetre.charger()
    for matiere, bloc in brut["matieres"].items():
        for chapitre, f in bloc["chapitres"].items():
            enseigne = dict(f)
            enseigne.pop("exclus_hors_programme", None)
            enseigne.pop("a_ne_pas_dire", None)
            texte = perimetre._normaliser(json.dumps(enseigne, ensure_ascii=False))
            p = carte_perimetre[matiere]["fiches"][chapitre]
            for terme in list(p.termes_hors_programme) + list(carte_perimetre[matiere]["generiques"]):
                assert not terme.motif.search(texte), f"{chapitre} : « {terme.terme} » est hors programme"
            for interdit in ("superposition", "sismique", "epicentre", "module d'elasticite", "√(t/μ)"):
                assert interdit not in texte, f"{chapitre} : « {interdit} » ne doit pas être enseigné"


def test_les_blocs_restent_courts():
    f = fiche("Physique", "ondes_mecaniques")
    for bloc in (bloc_explication(f), bloc_resolution(f), bloc_pieges(f)):
        assert 0 < len(bloc) < 3500, "un bloc long se fait paraphraser au lieu d'être suivi"


def test_l_explication_dit_ce_qu_il_ne_faut_pas_dire():
    bloc = bloc_explication(fiche("Physique", "ondes_mecaniques"))
    assert "Ne dis pas" in bloc and "densité" in bloc
    assert "Hors de ce cours" in bloc and "superposition" in bloc


def test_le_detecteur_releve_les_approximations_de_profs():
    texte = ("Le son va plus vite dans l'acier parce que c'est plus dense donc plus rapide. "
             "La longueur d'onde de cette perturbation vaut 3 cm.")
    noms = {d.terme for d in detecter(texte, "Physique", "ondes_mecaniques")}
    assert "plus le milieu est dense, plus l'onde est rapide" in noms
    assert "longueur d'onde d'une perturbation isolée" in noms


def test_le_detecteur_laisse_passer_le_discours_juste():
    texte = ("La célérité dépend de la nature du milieu : solide > liquide > gaz. "
             "La longueur de la perturbation vaut L = v·θ. Dans l'air, environ 340 m/s vers 20 °C.")
    assert detecter(texte, "Physique", "ondes_mecaniques") == []


# ── Servie au bon moment par le skill ──────────────────────────────

def _skill_ondes(**kw):
    skill = SkillProfesseur(**kw)
    skill.proposer_experience(fiche("Physique", "ondes_mecaniques"))
    return skill


def test_l_explication_recoit_les_insistances_et_la_definition_en_trois_questions():
    consigne = _skill_ondes(tours=3).consigne("c'est quoi une onde mécanique ?", "explanation")
    assert "ce qu'ils répètent" in consigne and "Quoi ? Où ?" in consigne


def test_les_pieges_n_arrivent_qu_apres_une_erreur():
    skill = _skill_ondes(tours=2, question_en_attente=True)
    assert "Erreurs que les profs voient souvent" not in skill.consigne("v = 34 m/s", "application")
    skill.lire_reponse("<eval>faux</eval> Pas tout à fait. Que vaut une division ?",
                       retirer_balise_eval("<eval>faux</eval> Pas tout à fait. Que vaut une division ?"))
    consigne = skill.consigne("2 ms", "application")
    assert "Erreurs que les profs voient souvent" in consigne and "début avec début" in consigne


def test_la_resolution_recoit_les_cas_types_et_le_bareme():
    skill = _skill_ondes(tours=4)
    skill.consigne("donne-moi un exercice", "application")
    skill.lire_reponse("<eval>aucune</eval> Voici l'exercice. De quoi parle-t-il ?", "Voici l'exercice. De quoi parle-t-il ?")
    skill.consigne("d'un sonar", "application")
    skill.lire_reponse("<eval>aucune</eval> Bien. Quelles sont les données ?", "Bien. Quelles sont les données ?")
    consigne = skill.consigne("la profondeur et 30 ms", "application")
    assert "Cas types du chapitre" in consigne and "réfléchi" in consigne
    assert "barème" in consigne and "Valeurs repères" in consigne


def test_sans_fiche_le_skill_reste_general():
    consigne = SkillProfesseur(tours=3).consigne("c'est quoi une onde ?", "explanation")
    assert "Quoi ? Où ?" in consigne and "ce qu'ils répètent" not in consigne


# ── Deuxième analyse : commentaires d'élèves et phrases marquées (7 novembre 2026) ─────────

def test_une_question_libre_recoit_la_reponse_juste_a_une_question_proche_d_eleve():
    skill = _skill_ondes(tours=5)
    consigne = skill.consigne("pourquoi on double la distance pour l'écho et pas le temps ?", "application")
    assert "Des élèves ont déjà posé une question proche" in consigne and "2d = v·τ" in consigne


def test_une_demande_sans_rapport_ne_recoit_aucune_question_d_eleve():
    assert experience_profs.bloc_questions(fiche("Physique", "ondes_mecaniques"), "bonjour, on commence ?") == ""


def test_la_methode_complete_ne_vient_que_pour_le_cas_evoque():
    f = fiche("Physique", "ondes_mecaniques")
    vise = bloc_resolution(f, "une caméra filme 25 images par seconde")
    assert "nombre d'INTERVALLES" in vise and "t_M = t₀ + SM/v" not in vise
    assert len(bloc_resolution(f)) < 3500


def test_le_detecteur_releve_une_dimension_definie_par_le_mouvement_du_point():
    noms = {d.terme for d in detecter("C'est une onde à deux dimensions car le point bouge en x et en y.",
                                      "Physique", "ondes_mecaniques")}
    assert "deux dimensions parce que le point bouge en x et en y" in noms
