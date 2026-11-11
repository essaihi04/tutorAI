"""Claude modèle principal du tuteur, DeepSeek en secours (11 novembre 2026)."""
import asyncio
from types import SimpleNamespace

from app.services import llm_service as L


def test_messages_claude_alterne_et_commence_par_user():
    systeme, tours = L._messages_claude(
        [{"role": "assistant", "content": "salut"}, {"role": "system", "content": "règle"},
         {"role": "user", "content": "a"}, {"role": "user", "content": "b"},
         {"role": "assistant", "content": "c"}, {"role": "user", "content": ""}],
        "prompt",
    )
    assert systeme == "prompt\n\nrègle"
    assert tours == [{"role": "user", "content": "a\n\nb"}, {"role": "assistant", "content": "c"}]


class _Faux:
    def __init__(self, reponse=None, erreur=None):
        self.appels = []

        async def create(**kw):
            self.appels.append(kw)
            if erreur:
                raise erreur
            return reponse
        self.beta = SimpleNamespace(messages=SimpleNamespace(create=create))


def _service(monkeypatch, faux):
    s = L.LLMService()
    s._claude = faux

    async def deepseek(*a, **k):
        return "deepseek"

    async def rien(*a, **k):
        return None
    monkeypatch.setattr(s, "_chat_deepseek", deepseek)
    monkeypatch.setattr(L.token_tracker, "record_usage", rien)
    return s


def test_claude_repond(monkeypatch):
    r = SimpleNamespace(content=[SimpleNamespace(type="thinking", thinking=""), SimpleNamespace(type="text", text=" bonjour ")],
                        stop_reason="end_turn", usage=SimpleNamespace(input_tokens=3, output_tokens=2), model="claude-opus-5-5")
    faux = _Faux(reponse=r)
    s = _service(monkeypatch, faux)
    assert asyncio.run(s.chat([{"role": "user", "content": "x"}], "sys", temperature=0.4, max_tokens=500)) == "bonjour"
    kw = faux.appels[0]
    assert kw["model"] == s.claude_model and "temperature" not in kw
    assert kw["max_tokens"] > 500


def test_secours_deepseek_sur_erreur_ou_refus(monkeypatch):
    s = _service(monkeypatch, _Faux(erreur=RuntimeError("402")))
    assert asyncio.run(s.chat([{"role": "user", "content": "x"}], "sys")) == "deepseek"
    refus = SimpleNamespace(content=[], stop_reason="refusal", usage=None, model="m")
    s = _service(monkeypatch, _Faux(reponse=refus))
    assert asyncio.run(s.chat([{"role": "user", "content": "x"}], "sys")) == "deepseek"


def test_sans_cle_deepseek_seul(monkeypatch):
    s = _service(monkeypatch, None)
    assert asyncio.run(s.chat([{"role": "user", "content": "x"}], "sys")) == "deepseek"


def test_systeme_claude_met_le_fixe_en_cache_et_le_tour_a_la_fin():
    p = "[ROLE]\nprof\n\n[PROFIL_ETUDIANT]\nNom: Amine\n\n[PROTOCOLE_UI_UNIFIÉ]\nui\n\n[PROGRAMME OFFICIEL — PHYSIQUE]\nprog\n\n[REGLES_PHASE]\nphase"
    blocs = L._systeme_claude(p)
    assert [b.get("cache_control") is not None for b in blocs] == [True, True, False]
    assert "[ROLE]" in blocs[0]["text"] and "[PROTOCOLE_UI_UNIFIÉ]" in blocs[0]["text"] and "Amine" not in blocs[0]["text"]
    assert "[PROGRAMME OFFICIEL" in blocs[1]["text"]
    assert "Amine" in blocs[2]["text"] and "[REGLES_PHASE]" in blocs[2]["text"]
    assert L._systeme_claude("Tu es un professeur.") == [{"type": "text", "text": "Tu es un professeur."}]
