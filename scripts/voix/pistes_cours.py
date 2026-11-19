"""Toutes les pistes à dire d'un cours, avec où poser leur voix (11 novembre 2026).
Chaque piste : (dossier, id, texte, poser(url, duree_ms, hash, version)).
  mixed    : texte dit de chaque diapositive
  reponses : réactions préparées des questions des diapositives, des rappels, des exercices de blocs
  demos    : démonstrations (question, exercices des diapositives, exercice de bloc)"""


#: La fin d'un bloc ne joue plus que le cahier (user rule, 13 novembre 2026, CycleBloc.ETAPES_FIN_DE_BLOC) :
#: les reactions, demonstrations et enonces du « retrouver » et de l'exercice de bloc ne sont pas mis en voix.
#: Les remettre (True) quand l'etape de fin de cours les reprendra.
FIN_DE_BLOC_COMPLETE = False


def _poser_audio(obj):
    def f(url, ms, h, v):
        obj["audio"] = url
    return f


def _poser_diapo(s):
    def f(url, ms, h, v):
        s.setdefault("audio", {})["mixed"] = {"url": url, "duration_ms": ms, "version": v, "speech_hash": h,
                                              "status": "published"}
    return f


def _reactions(prefixe, reponses):
    for o, qr in (reponses or {}).items():
        for quoi, r in qr.items():
            if isinstance(r, dict) and (r.get("parole") or "").strip():
                yield ("reponses", f"{prefixe}_{o}_{quoi}", r["parole"].strip(), _poser_audio(r))


def _demo(ident, obj):
    d = obj.get("demonstration") if isinstance(obj, dict) else None
    if isinstance(d, dict) and (d.get("parole") or "").strip():
        yield ("demos", ident, d["parole"].strip(), _poser_audio(d))


def _enonce(ident, obj):
    """Le tuteur lit l'énoncé (12 novembre 2026) : texte `enonce_dit`, piste posée dans `enonce_audio`."""
    t = (obj.get("enonce_dit") or "").strip() if isinstance(obj, dict) else ""
    if t:
        def f(url, ms, h, v):
            obj["enonce_audio"] = url
        yield ("reponses", ident, t, f)


def _association(prefixe, obj):
    """Association (19 novembre 2026) : le retour dit de chaque paire (`retours["1-c"].dit`, `retours["1-*"].dit`) et le
    bilan (`bilan.dit`) ; piste posée dans leur `audio`. Ids : <diapo>__<cle>_assoc_<g>-<d> (« * » écrit « autre »)."""
    a = obj.get("association") if isinstance(obj, dict) else None
    if not isinstance(a, dict):
        return
    for k, r in (a.get("retours") or {}).items():
        if isinstance(r, dict) and (r.get("dit") or "").strip():
            yield ("reponses", f"{prefixe}_assoc_{k.replace('*', 'autre')}", r["dit"].strip(), _poser_audio(r))
    b = a.get("bilan")
    if isinstance(b, dict) and (b.get("dit") or "").strip():
        yield ("reponses", f"{prefixe}_assoc_bilan", b["dit"].strip(), _poser_audio(b))


def pistes(m):
    yield from _pistes(m)
    # énoncés des questions (mêmes chemins et ids que enonces.py)
    sys_path = __import__("sys").path
    import os
    sys_path.insert(0, os.path.dirname(__file__))
    from enonces import cibles
    for chemin, ident, o in cibles(m):
        if chemin[0] in ("bx", "br") and not FIN_DE_BLOC_COMPLETE:
            continue       # retrouver / exercice de bloc : pas joues pour le moment (13 novembre 2026)
        yield from _enonce(ident, o)


def _pistes(m):
    for a in m.get("activities") or []:
        for s in a["slides"]:
            t = (s.get("speech_text") or {}).get("mixed", "").strip()
            if t:
                yield ("mixed", s["id"], t, _poser_diapo(s))
            for cle, rep in ((s.get("concentration") or {}).get("reponses") or {}).items():
                yield from _reactions(f"{s['id']}__{cle}", rep)
            yield from _demo(f"{s['id']}__demo_q", s.get("question") or {})
            yield from _association(f"{s['id']}__q", s.get("question") or {})
            for i, e in enumerate(s.get("exercises") or []):
                yield from _demo(f"{s['id']}__demo_e{i}", e)
                yield from _association(f"{s['id']}__e{i}", e)
    for c in m.get("competences") or []:
        for r in c.get("rappels") or []:
            yield from _reactions(f"rappel_{r['id']}", r.get("reponses"))
    if not FIN_DE_BLOC_COMPLETE:
        return
    for se in m.get("seances") or []:
        for b in se.get("blocs") or []:
            ex = b.get("exercice") or {}
            yield from _reactions(f"bloc_{b['id']}__ex", ex.get("reponses"))
            for j, st in enumerate(ex.get("statements") or []):
                yield from _reactions(f"bloc_{b['id']}__exs{j}", st.get("reponses"))
            yield from _demo(f"bloc_{b['id']}__demo_ex", ex)
