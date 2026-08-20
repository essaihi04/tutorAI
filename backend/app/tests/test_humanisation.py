"""Le miroir que le tuteur reçoit sur ses propres tours.

Les cas viennent d'un échange réel du 18 août 2026 : cinq réponses de suite
ouvertes par « مزيان بزاف زهير », la même question sur le pH du Water reposée
à sept minutes d'intervalle, et un pictogramme à chaque tour toujours au même
endroit. Ce sont ces trois-là que les tests tiennent.
"""
from app.services import humanisation, tag_decoder
from app.services.tts_service import clean_for_tts
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


# ── Les commandes ne sont ni lues ni entendues ────────────────────
#
# Séance du 19 août : l'élève a lu « شوف هاد الصورة باش تفهم مزيان الفرق.
# OUVRIR_IMAGE دابا ڭولي ليا… » dans sa bulle de chat. Le mot-clé n'était
# retiré qu'au point de sortie NON streamé — or le chat est streamé, et la
# voix partage le même texte.

_TOUR_AVEC_COMMANDE = "شوف هاد الصورة باش تفهم مزيان الفرق.\nOUVRIR_IMAGE\nدابا ڭولي ليا، واش فهمتي؟"


def test_le_flux_du_chat_ne_laisse_pas_passer_une_commande():
    filtre = _StreamTagFilter()
    accumule = ""
    sortie = ""
    for token in ("شوف هاد الصورة.\n", "OUVRIR_IMAGE\n", "دابا ڭولي ليا، واش فهمتي؟\n"):
        accumule += token
        sortie += filtre.feed(accumule)
    sortie += filtre.flush(accumule)

    assert "OUVRIR_IMAGE" not in sortie
    assert "شوف هاد الصورة" in sortie
    assert "واش فهمتي؟" in sortie


def test_la_voix_ne_prononce_pas_la_commande():
    """C'était le plus grave : le tuteur DISAIT « OUVRIR IMAGE » à haute voix."""
    dit = clean_for_tts(_TOUR_AVEC_COMMANDE)

    assert "OUVRIR_IMAGE" not in dit
    assert "OUVRIR" not in dit
    assert "شوف هاد الصورة" in dit


def test_une_commande_collee_en_pleine_phrase_disparait_aussi():
    """À la répétition du 19 août, le mot-clé s'est retrouvé au milieu du
    paragraphe, plus sur sa propre ligne."""
    colle = "شوف هاد الصورة. OUVRIR_IMAGE دابا ڭولي ليا."

    assert "OUVRIR_IMAGE" not in tag_decoder.retirer_commandes(colle)
    assert "OUVRIR_IMAGE" not in clean_for_tts(colle)


def test_la_commande_la_plus_longue_ne_survit_pas_a_une_coupure():
    """La queue retenue en fin de flux doit couvrir le plus long mot-clé."""
    assert tag_decoder.LONGUEUR_MOT_CLE_MAX >= len("OUVRIR_SIMULATION")


def test_une_commande_composee_ne_laisse_pas_de_moignon():
    """« FERMER_EXERCICE » doit partir en entier, pas se réduire à
    « FERMER_ » parce que « EXERCICE: » aurait été traité d'abord."""
    propre = tag_decoder.retirer_commandes("واخا FERMER_EXERCICE صافي")

    assert "FERMER" not in propre
    assert "EXERCICE" not in propre
    assert "واخا" in propre and "صافي" in propre


def test_le_texte_ordinaire_traverse_sans_dommage():
    phrase = "الـ méiose كتعطي أربع خلايا، كل وحدة فيها la moitié ديال les chromosomes."

    assert tag_decoder.retirer_commandes(phrase) == phrase


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
    reponse = "بي آش كينقص ملي التركيز كيزيد. " + _TABLEAU

    assert humanisation.tableau_non_annonce(reponse)
    assert "MUET" in humanisation.defaut_d_accord(reponse)


def test_un_tableau_annonce_ne_declenche_rien():
    reponse = "شوف اللوح. هاد le log كيقلب القيمة، ملي التركيز كيزيد بي آش كينقص. " + _TABLEAU

    assert not humanisation.tableau_non_annonce(reponse)
    assert humanisation.defaut_d_accord(reponse) == ""


# ── La question dont la réponse est déjà à l'écran ────────────────
#
# Le tour de la capture d'écran du 19 août 2026 : le chat demande la
# différence entre un gène et un allèle, le tableau l'écrit, et le bouton de
# réponse la rend toute rédigée.

_TABLEAU_GENETIQUE = (
    '<ui>{"actions":[{"type":"whiteboard","action":"show_board","payload":'
    '{"title":"Génétique","lines":['
    '{"type":"box","content":"Un gène = segment d\'ADN qui code pour un caractère héréditaire"},'
    '{"type":"box","content":"Un allèle = version différente d\'un même gène"}]}}]}</ui>'
)
_QUESTION_GENETIQUE = (
    "قبل ما نبداو، عندي سؤال صغير: واش عرفتي الفرق بين un gène و un allèle؟ "
)


def test_le_tableau_qui_repond_a_la_question_posee_est_repere():
    reponse = _QUESTION_GENETIQUE + _TABLEAU_GENETIQUE

    assert humanisation.tableau_qui_donne_la_reponse(reponse)
    assert "RETIRÉ" in humanisation.defaut_d_accord(reponse)


def test_le_bloc_suggestions_ne_masque_plus_le_point_d_interrogation():
    """Le prompt EXIGE des <suggestions> après chaque question.

    Tant qu'elles comptaient comme de la prose, la réponse ne « finissait »
    plus sur « ؟ » et aucun garde-fou ne se déclenchait — donc jamais en
    production, où le bloc est toujours là.
    """
    reponse = (
        _QUESTION_GENETIQUE
        + _TABLEAU_GENETIQUE
        + '<suggestions>[{"label":"Je ne sais pas","prompt":"Je ne sais pas"}]</suggestions>'
    )

    assert humanisation.tableau_qui_donne_la_reponse(reponse)
    assert humanisation.tour_purement_socratique(_QUESTION_GENETIQUE + "<mode>libre</mode>")


def test_un_controle_de_comprehension_garde_son_recapitulatif():
    """« واش فهمتي؟ » ne cache aucune réponse : le tableau récapitule."""
    reponse = (
        "la mitose كتعطي جوج cellules identiques. واش فهمتي؟ " + _TABLEAU_GENETIQUE
    )

    assert not humanisation.tableau_qui_donne_la_reponse(reponse)


def test_une_question_sur_ce_qui_est_affiche_garde_son_tableau():
    """Quand l'oral ANNONCE le tableau, l'afficher est le sujet même."""
    reponse = "شوف اللوح. واش عرفتي شنو كيمثل هاد le schéma؟ " + _TABLEAU_GENETIQUE

    assert not humanisation.tableau_qui_donne_la_reponse(reponse)


def test_un_script_en_direct_n_est_jamais_retenu():
    """Un show_live EST le cours ; ses `ask` font partie du déroulé."""
    reponse = (
        "واش عرفتي الفرق بين un gène و un allèle؟ "
        '<ui>{"actions":[{"type":"whiteboard","action":"show_live","payload":{"steps":[]}}]}</ui>'
    )

    assert not humanisation.tableau_qui_donne_la_reponse(reponse)


def test_une_explication_suivie_de_son_tableau_reste_intacte():
    """Au-delà d'une question courte, le tour porte un cours."""
    reponse = "خلينا نشوفو هاد الحاجة بشوية. " * 20 + "شنو كتلاحظ؟ " + _TABLEAU_GENETIQUE

    assert not humanisation.tableau_qui_donne_la_reponse(reponse)


def test_le_bouton_qui_recopie_le_tableau_est_repere():
    reponse = _QUESTION_GENETIQUE + _TABLEAU_GENETIQUE

    assert humanisation.suggestion_donne_la_reponse(
        "Un gène = segment d'ADN, un allèle = une version", reponse
    )
    assert not humanisation.suggestion_donne_la_reponse("Je ne sais pas", reponse)
    assert not humanisation.suggestion_donne_la_reponse("Le gène est le lieu", reponse)


def test_retenir_le_tableau_laisse_passer_le_reste():
    """Les commandes en clair et le mode ne dépendent pas du tableau."""
    reponse = _QUESTION_GENETIQUE + "OUVRIR_IMAGE " + _TABLEAU_GENETIQUE + "<mode>cours</mode>"
    reste = humanisation.sans_les_affichages(reponse)

    assert "show_board" not in reste
    assert "OUVRIR_IMAGE" in reste
    assert "<mode>cours</mode>" in reste


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


def test_le_mot_question_dans_l_amorce_n_exempte_rien():
    """« J'ai une question pour toi : … » n'est pas un contrôle de
    compréhension. Chercher les marqueurs partout, plutôt que dans la seule
    phrase interrogative, aurait laissé passer le tour de la capture traduit
    en français."""
    reponse = (
        "J'ai une petite question pour toi. "
        "Quelle est la différence entre un gène et un allèle ? " + _TABLEAU_GENETIQUE
    )

    assert humanisation.tableau_qui_donne_la_reponse(reponse)


# ── L'interrogatoire : trois « non » et toujours pas de cours ──────
#
# Séance du 20 août 2026. « Fais-moi un cours complet sur le math » →
# « واش عرفتي شنو هي la fonction exponentielle؟ » → non → « واش عرفتي كيفاش
# كتحسب la dérivée؟ » → non → « واش واضح؟ » → non. Huit tours, zéro ligne de
# cours : le tuteur descendait d'un prérequis à l'autre.


def _eleve_qui_ne_sait_pas() -> list[dict]:
    return [
        {"role": "user", "content": "Fais-moi un cours complet sur le math"},
        {"role": "assistant", "content": "واش عرفتي شنو هي la fonction exponentielle؟"},
        {"role": "user", "content": "nn"},
        {"role": "assistant", "content": "واش عرفتي كيفاش كتحسب la dérivée؟"},
        {"role": "user", "content": "non ma3aeftch"},
        {"role": "assistant", "content": "واش واضح هاد المثال؟"},
        {"role": "user", "content": "non"},
    ]


def test_les_refus_de_suite_sont_comptes():
    assert humanisation.aveux_consecutifs(_eleve_qui_ne_sait_pas()) == 3


def test_une_reponse_courte_mais_pleine_n_est_pas_un_refus():
    """« 7 » et « 1 » répondent : ils ne signalent aucun blocage."""
    echange = [
        {"role": "user", "content": "1"},
        {"role": "assistant", "content": "واش عرفتي؟"},
        {"role": "user", "content": "7"},
    ]

    assert humanisation.aveux_consecutifs(echange) == 0


def test_un_seul_refus_ne_declenche_pas_l_alarme():
    """Un « non » isolé est le cours normal : on explique et on avance."""
    echange = [
        {"role": "user", "content": "واخا"},
        {"role": "assistant", "content": "واش عرفتي؟"},
        {"role": "user", "content": "non"},
    ]

    assert humanisation.aveux_consecutifs(echange) == 1
    assert "ARRÊTE D'INTERROGER" not in humanisation.bloc_memoire(echange)


def test_le_miroir_ordonne_d_enseigner_apres_deux_refus():
    bloc = humanisation.bloc_memoire(_eleve_qui_ne_sait_pas())

    assert "ARRÊTE D'INTERROGER" in bloc
    assert "3 fois DE SUITE" in bloc


def test_repondre_sans_regarder_le_tableau_est_un_aveu():
    """« جاوبني بلا ما تشوف اللوح » : la réponse EST au tableau, et le tuteur
    le dit lui-même. L'ancienne lecture y voyait une annonce et laissait
    passer le tableau."""
    reponse = (
        "واش عرفتي شنو هي la fonction exponentielle؟ جاوبني بلا ما تشوف اللوح. "
        + _TABLEAU_GENETIQUE
    )

    assert humanisation.tableau_qui_donne_la_reponse(reponse)


def test_une_consigne_courte_ne_fait_pas_oublier_la_question():
    """« …؟ جاوبني بلا ما تفكر بزاف. » attend toujours une réponse."""
    reponse = "واش عرفتي الفرق بين un gène و un allèle؟ جاوبني بلا ما تفكر بزاف."

    assert humanisation.tour_purement_socratique(reponse)
    assert humanisation.tableau_qui_donne_la_reponse(reponse + _TABLEAU_GENETIQUE)


def test_une_phrase_finale_longue_referme_bien_le_tour():
    """Une question suivie d'un vrai paragraphe n'attend plus rien."""
    reponse = (
        "واش عرفتي هادشي؟ صافي، غادي نشرح ليك دابا كيفاش كتخدم هاد la méthode "
        "من الأول للآخر، خطوة بخطوة، بلا ما نقفزو على حتى مرحلة."
    )

    assert not humanisation.tour_purement_socratique(reponse)


# ── La promesse de tableau ────────────────────────────────────────
#
# Séance du 20 août 2026 : sept réponses annoncent « شوف le tableau، كتبت
# ليك… », aucune ne porte de bloc <ui>, et l'élève finit par écrire « rien
# n'est affiché ».

_PROMESSE = (
    "شوف le tableau، كتبت ليك الفرق بين les trois. "
    "دابا، واش واضحة؟ ولا بغيتي نعطيك شي حاجة أخرى؟"
)


def test_annoncer_un_tableau_sans_lenvoyer_est_detecte():
    assert humanisation.promesse_de_tableau_non_tenue(_PROMESSE)


def test_la_meme_annonce_avec_le_tableau_ne_declenche_rien():
    assert not humanisation.promesse_de_tableau_non_tenue(_PROMESSE + _TABLEAU_GENETIQUE)


def test_parler_du_tableau_de_variation_nest_pas_une_promesse():
    """Le mot « tableau » seul ne promet rien — il faut l'annonce."""
    reponse = "نديرو le tableau de variation ديال la fonction، وغادي نشوفو le signe."

    assert not humanisation.promesse_de_tableau_non_tenue(reponse)


def test_lecran_vide_signale_par_leleve_est_reconnu():
    for message in ("rien n est afficher", "ma kayn walo", "ماكاين والو", "je ne vois rien"):
        assert humanisation.signale_un_ecran_vide(message), message
    assert not humanisation.signale_un_ecran_vide("واخا، فهمت")


# ── Les questions ─────────────────────────────────────────────────


def test_deux_questions_dans_un_tour_valent_un_rappel():
    rappel = humanisation.defaut_d_accord(_PROMESSE + _TABLEAU_GENETIQUE)

    assert "UNE seule" in rappel
    assert "porte de sortie" in rappel


def test_le_controle_de_comprehension_rabache_est_compte():
    tour = "شرحت ليك la secousse. دابا، واش واضح؟"
    echange = [
        {"role": "assistant", "content": tour},
        {"role": "user", "content": "ok"},
        {"role": "assistant", "content": tour},
    ]

    assert humanisation.controles_consecutifs(echange) == 2
    assert "signature de fin de message" in humanisation.bloc_memoire(echange)


def test_une_question_de_contenu_nest_pas_un_controle():
    echange = [
        {"role": "assistant", "content": "شنو كيوقع لـ la contraction إلى ما كانش relâchement؟"},
        {"role": "assistant", "content": "شنو هي la période de latence؟"},
    ]

    assert humanisation.controles_consecutifs(echange) == 0
