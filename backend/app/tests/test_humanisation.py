"""Le miroir que le tuteur reçoit sur ses propres tours.

Les cas viennent d'un échange réel du 18 août 2026 : cinq réponses de suite
ouvertes par « مزيان بزاف زهير », la même question sur le pH du Water reposée
à sept minutes d'intervalle, et un pictogramme à chaque tour toujours au même
endroit. Ce sont ces trois-là que les tests tiennent.
"""
from app.services import humanisation
from app.websockets.session_handler import _StreamTagFilter


def _echange_repetitif() -> list[dict]:
    """Trois tours du tuteur bâtis sur le même moule."""
    return [
        {"role": "user", "content": "7"},
        {"role": "assistant", "content": (
            "مزيان بزاف زهير! جاوبتي صحيح، بي آش ديال الماء النقي كيساوي 7. "
            "دابا واش عرفتي شنو هي العلاقة بين بي آش و تركيز الأيونات؟"
        )},
        {"role": "user", "content": "8"},
        {"role": "assistant", "content": (
            "واخا زهير، مزيان بزاف! جاوبتي صحيح، بي آش ديال الصابون قريب ل 8. "
            "واش عندك فكرة على شحال كيساوي بي آش ديال الماء النقي؟"
        )},
        {"role": "user", "content": "ok"},
        {"role": "assistant", "content": (
            "مزيان بزاف زهير! جاوبتي صحيح، بي آش ديال الماء النقي كيساوي 7. "
            "واش عرفتي كيفاش كيتحسب بي آش من التركيز؟"
        )},
    ]


# ── Le miroir ─────────────────────────────────────────────────────


def test_le_miroir_se_tait_quand_il_n_a_rien_a_dire():
    """Premier tour d'une séance : aucun passé, donc aucune interdiction."""
    assert humanisation.bloc_memoire([]) == ""
    assert humanisation.bloc_memoire([{"role": "user", "content": "دوز الشيمي"}]) == ""


def test_l_ouverture_qui_revient_est_citee_au_modele():
    """Une consigne de style ne bat pas trois exemples ; une citation, si."""
    bloc = humanisation.bloc_memoire(_echange_repetitif())

    assert "MIROIR DE TES DERNIERS TOURS" in bloc
    assert "مزيان بزاف زهير" in bloc
    assert "INTERDIT" in bloc


def test_le_prenom_est_attrape_sans_avoir_a_le_translitterer():
    """Le profil dit « Zouhair », la réponse dit « زهير ».

    Aucune table de translittération ne fait ce pont de façon fiable. On ne
    cherche donc pas le prénom : on cherche ce qui se replace en tête de
    réponse tour après tour — et le prénom en fait partie, au même titre
    qu'un « مزيان » réflexe.
    """
    tics = humanisation.mots_d_ouverture_repetes(_echange_repetitif())

    assert "زهير" in tics
    assert "مزيان" in tics


def test_la_ponctuation_arabe_ne_reste_pas_collee_au_mot():
    """« صحيح، » et « صحيح » sont le même tic, pas deux mots différents."""
    tics = humanisation.mots_d_ouverture_repetes(_echange_repetitif())

    assert "صحيح" in tics
    assert not any("،" in mot for mot in tics)


def test_la_question_ouverte_est_la_derniere_posee():
    ouverte = humanisation.question_ouverte(_echange_repetitif())

    assert "كيفاش كيتحسب" in ouverte


def test_la_question_encore_ouverte_n_est_pas_donnee_pour_resolue():
    """Elle serait à la fois « déjà répondue » et « à laquelle il répond »."""
    posees = humanisation.questions_deja_posees(_echange_repetitif())
    ouverte = humanisation.question_ouverte(_echange_repetitif())

    assert ouverte
    assert ouverte not in posees
    assert any("العلاقة" in question for question in posees)


def test_le_miroir_rappelle_de_ne_rien_inventer():
    """Le tuteur avait félicité l'élève pour « بي آش 9 » — valeur absente de
    tout l'échange. Le garde-fou tient à la question ouverte."""
    bloc = humanisation.bloc_memoire(_echange_repetitif())

    assert "n'invente" in bloc


# ── Pictogrammes ──────────────────────────────────────────────────


def test_un_seul_pictogramme_survit_par_reponse():
    texte, restant = humanisation.limiter_emojis(
        "مزيان بزاف زهير! 🎉 جاوبتي صحيح. دابا نكملو ✍️ واش فهمتي؟ 🤔", 1
    )

    assert texte.count("🎉") == 1
    assert "✍" not in texte
    assert "🤔" not in texte
    assert restant == 0
    assert "جاوبتي صحيح" in texte


def test_une_rafale_collee_compte_pour_une_decoration():
    """« 🎉✨ » est UN geste, pas deux : le budget ne doit pas le couper."""
    texte, _ = humanisation.limiter_emojis("بدينا 🎉✨ الدرس", 1)

    assert texte.count("🎉") == 1
    assert texte.count("✨") == 1


def test_les_fleches_et_les_signes_ne_sont_pas_des_decorations():
    """« → » porte du sens dans une correction : il reste."""
    texte, _ = humanisation.limiter_emojis("acide → pH < 7 🎉 ✍️", 1)

    assert "→" in texte
    assert "<" in texte
    assert "✍" not in texte


def test_le_texte_sans_pictogramme_ressort_intact():
    texte, restant = humanisation.limiter_emojis("واخا، نكملو مع la formule.", 1)

    assert texte == "واخا، نكملو مع la formule."
    assert restant == 1


# ── L'accord entre ce qui se dit et ce qui s'écrit ────────────────

_TABLEAU = (
    '<ui>{"actions":[{"type":"whiteboard","action":"show_board","payload":'
    '{"title":"Le pH","lines":[{"type":"math","content":"pH = -\\\\log[H_3O^+]"}]}}]}</ui>'
)


def test_une_question_seule_ne_doit_rien_ecrire_au_tableau():
    """En coaching, `force_schema` est vrai à chaque tour : sans ce constat,
    une question de deux phrases finissait recopiée sur le tableau."""
    reponse = "واخا. دابا جرب تكتب la formule اللي كتربط بي آش بالتركيز. شنو غادي تكتب؟"

    assert humanisation.tour_purement_socratique(reponse)


def test_un_tour_qui_ecrit_n_est_pas_une_simple_question():
    """Le modèle a produit un tableau : l'exigence garde tout son sens."""
    reponse = "شوف اللوح، كتبت ليك la formule. واش واضحة؟ " + _TABLEAU

    assert not humanisation.tour_purement_socratique(reponse)


def test_une_explication_longue_n_est_pas_une_simple_question():
    """Un cours qui se termine par une question reste un cours."""
    reponse = "خلينا نبداو من الصفر. " * 30 + "واش فهمتي؟"

    assert not humanisation.tour_purement_socratique(reponse)


def test_une_affirmation_n_est_pas_une_question():
    reponse = "الليمون حمضي، والصابون قاعدي."

    assert not humanisation.tour_purement_socratique(reponse)


def test_un_tableau_jamais_annonce_est_signale():
    """La plainte telle quelle : des données au tableau que rien n'explique."""
    reponse = "واش عرفتي شنو هي العلاقة بين بي آش و التركيز؟ " + _TABLEAU

    assert humanisation.tableau_non_annonce(reponse)
    assert "MUET" in humanisation.defaut_d_accord(reponse)


def test_un_tableau_annonce_ne_declenche_rien():
    reponse = "شوف اللوح. هاد le log كيقلب القيمة، ملي التركيز كيزيد بي آش كينقص. " + _TABLEAU

    assert not humanisation.tableau_non_annonce(reponse)
    assert humanisation.defaut_d_accord(reponse) == ""


def test_un_tour_sans_tableau_n_a_rien_a_accorder():
    assert not humanisation.tableau_non_annonce("واخا، نكملو.")
    assert humanisation.defaut_d_accord("واخا، نكملو.") == ""


def test_le_texte_parle_exclut_le_contenu_du_tableau():
    """Ce que l'élève ENTEND ne contient rien du JSON d'affichage."""
    parle = humanisation.texte_parle("شوف اللوح. " + _TABLEAU)

    assert "show_board" not in parle
    assert "شوف اللوح" in parle


def test_le_budget_est_partage_par_tous_les_morceaux_du_flux():
    """La coupure entre deux tokens ne doit pas rouvrir un quota.

    Sans état partagé, chaque chunk gardait « son » pictogramme et la réponse
    complète en affichait autant qu'avant le filtre.
    """
    filtre = _StreamTagFilter()
    accumule = ""
    sortie = ""
    for token in ("واخا 🎉 ", "صحيح.\n", "دابا ✍️ نكملو.\n", "واش فهمتي؟ 🤔\n"):
        accumule += token
        sortie += filtre.feed(accumule)
    sortie += filtre.flush(accumule)

    assert sortie.count("🎉") == 1
    assert "✍" not in sortie
    assert "🤔" not in sortie
    assert "واش فهمتي؟" in sortie
