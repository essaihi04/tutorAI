"""La question libre de l'élève : contexte complet, gestes bornés, exercice en image sans réponse finale."""
import asyncio
import json

from app.services import question_eleve as qe

CTX = {"title": "Le retard", "speech": "…", "ce_qui_se_voit": "M à 0,8 m, τ = 0,80 s", "moments": {"m_atteint": 0.8}, "reperes": {"retard_tau": "le retard τ"}}


def test_le_prompt_porte_la_question_et_la_figure():
    p = qe.prompt_question(CTX, {"texte": "علاش tau كيكبر ؟", "transcription": "", "image_texte": ""})
    assert "علاش tau" in p and "m_atteint" in p and "retard_tau" in p and "Ce que l'élève voit" in p and "jamais en chiffres" in p
    p2 = qe.prompt_question(CTX, {"texte": "", "transcription": "", "image_texte": "Exercice 2 : d = 1,02 m…"})
    assert "Texte lu sur l'image" in p2 and "ne donne pas la réponse finale" in p2.replace("\r", "").replace("\n", " ")


def test_la_reponse_est_nettoyee_et_les_gestes_bornes():
    r = qe.reponse_depuis(json.dumps({"parole": "**شوف**", "ecrit": "τ = SM / v", "gestes": [{"repere": "retard_tau"}, {"repere": "x"}, {"commande": "play_until", "parametres": {"moment": "m_atteint"}}]}), CTX)
    assert r["parole"] == "شوف" and r["gestes"] == [{"repere": "retard_tau"}, {"commande": "play_until", "parametres": {"moment": "m_atteint"}}]
    assert qe.reponse_depuis("rien", CTX) is None


def test_comprendre_sans_audio_ni_image_garde_le_texte():
    c = asyncio.run(qe.comprendre("  ma question ", None, None, "image/png"))
    assert c == {"texte": "ma question", "transcription": "", "image_texte": ""}
