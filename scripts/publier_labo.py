"""Publie le labo virtuel 3D (Desktop/labo-2bac) sur le site : https://moalim.online/labo/

Les manips sont écrites et testées dans le dossier de travail `labo-2bac` (voir la skill
labo-virtuel-2bac). Ce script les copie dans `frontend/public/labo/`, que Vite recopie dans le
build et que nginx sert tel quel :

- `index.html` (préparation de NaOH) devient `solution-naoh.html` ; `/labo/` est une page
  d'accueil générée ici, qui liste les manips par matière ;
- le menu « 📚 Manips… » de chaque page pointait vers les liens claude.ai : il pointe désormais
  vers les pages du site et s'ouvre dans le même onglet, avec un retour au sommaire ;
- chaque page reçoit le squelette que claude.ai ajoutait (doctype, charset UTF-8, viewport) ;
- seules les pages HTML partent (les .py, .js de queue et .md restent dans le dossier de travail :
  les queues sont déjà assemblées dans les pages).

Usage :  python -I scripts/publier_labo.py [chemin du dossier labo-2bac]
Puis commit, push et déploiement habituels (deploy/deploy-ubuntu.sh sur le VPS).
"""
from __future__ import annotations

import html
import io
import re
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parents[1]
SOURCE = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.home() / "Desktop" / "labo-2bac"
CIBLE = RACINE / "frontend" / "public" / "labo"

# Fichier source → fichier publié. Les deux dernières sont des versions antérieures, sans menu.
PAGES = {
    "index.html": "solution-naoh.html",
    "chimie-dosage-acide-base.html": "chimie-dosage-acide-base.html",
    "svt-exao-levures.html": "svt-exao-levures.html",
    "svt-sol-retention.html": "svt-sol-retention.html",
    "svt-sol-chimie.html": "svt-sol-chimie.html",
    "physique-5-stations.html": "physique-5-stations.html",
    "labo-3-manips.html": "labo-3-manips.html",
}
ANCIENNES = {
    "physique-5-stations.html": ("Physique · 2ᵉ Bac PC BIOF", "Cinq stations de physique (première version)"),
    "labo-3-manips.html": ("Physique-Chimie · 2ᵉ Bac PC BIOF", "Trois manips de chimie (première version)"),
}

_LIGNE_LAB = re.compile(r'\{\s*g:\s*"([^"]*)",\s*t:\s*"([^"]*)",\s*n:\s*"([^"]*)",\s*u:\s*"([^"]*)"\s*\}')
_OUVERTURE = re.compile(
    r'const w = window\.open\(l\.u, "_blank", "noopener"\); if \(!w\) \{ try \{ window\.top\.location\.href = l\.u; \} '
    r'catch \(e\) \{ location\.href = l\.u; \} \}'
)


def squelette(page: str) -> str:
    """Les manips sont des fragments d'artefact : claude.ai les enveloppait d'un doctype et d'un charset.

    Servies telles quelles, le navigateur lit l'UTF-8 comme du Latin-1 (« PrÃ©parer ») et passe en
    mode quirks. On ajoute donc le même squelette en tête ; head et body restent implicites.
    """
    if page.lstrip().lower().startswith("<!doctype"):
        return page
    return ('<!doctype html>\n<html lang="fr"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">\n' + page)


def titre(page: str) -> str:
    m = re.search(r"<title>([^<]*)</title>", page)
    return m.group(1).strip() if m else ""


def lire(nom: str) -> str:
    return io.open(SOURCE / nom, encoding="utf-8").read()


def main() -> None:
    if not SOURCE.is_dir():
        sys.exit(f"Dossier introuvable : {SOURCE}")
    pages = {nom: lire(nom) for nom in PAGES if (SOURCE / nom).is_file()}
    manquantes = sorted(set(PAGES) - set(pages))
    if manquantes:
        print("absentes, ignorées :", ", ".join(manquantes))

    # Le menu identifie chaque manip par le titre exact de sa page : titre → fichier publié.
    publie_par_titre = {titre(src): PAGES[nom] for nom, src in pages.items() if "<!--labnav-->" in src}
    nav = lire("labs-nav.html")
    labs = _LIGNE_LAB.findall(nav)
    if not labs:
        sys.exit("labs-nav.html : tableau LABS introuvable")

    CIBLE.mkdir(parents=True, exist_ok=True)
    for ancien in CIBLE.glob("*.html"):
        ancien.unlink()

    for nom, src in pages.items():
        sortie = src
        if "<!--labnav-->" in sortie:
            # Liens claude.ai → pages du site, et un retour au sommaire en tête de liste.
            for g, t, n, u in labs:
                fichier = publie_par_titre.get(t)
                if not fichier:
                    sys.exit(f"Manip du menu sans page : « {t} »")
                sortie = sortie.replace(f'u: "{u}"', f'u: "{fichier}"')
            sortie, remplacements = _OUVERTURE.subn("location.href = l.u;", sortie)
            if remplacements != 1:
                sys.exit(f"{nom} : ouverture du menu non reconnue ({remplacements})")
            sortie = sortie.replace(
                'head.textContent = "📚 Manips…"; head.value = ""; if (cur < 0) head.selected = true; sel.append(head);',
                'head.textContent = "📚 Manips…"; head.value = ""; if (cur < 0) head.selected = true; sel.append(head);'
                ' const home = document.createElement("option"); home.value = "home"; home.textContent = "🏠 Toutes les manips"; sel.append(home);',
                1,
            )
            sortie = sortie.replace(
                "const l = LABS[+sel.value]; if (!l || +sel.value === cur) return;",
                'if (sel.value === "home") { location.href = "./"; return; } const l = LABS[+sel.value]; if (!l || +sel.value === cur) return;',
                1,
            )
            if "claude.ai/artifact" in sortie:
                sys.exit(f"{nom} : un lien claude.ai reste dans la page")
        sortie = squelette(sortie)
        io.open(CIBLE / PAGES[nom], "w", encoding="utf-8", newline="\n").write(sortie)
        print(f"{nom:32s} -> labo/{PAGES[nom]}  ({len(sortie) // 1024} Ko)")

    groupes: dict[str, list[tuple[str, str]]] = {}
    for g, t, n, _u in labs:
        groupes.setdefault(g, []).append((n, publie_par_titre[t]))
    io.open(CIBLE / "index.html", "w", encoding="utf-8", newline="\n").write(sommaire(groupes, pages))
    print("sommaire                         -> labo/index.html")


def sommaire(groupes: dict[str, list[tuple[str, str]]], pages: dict[str, str]) -> str:
    cartes = []
    for g, manips in groupes.items():
        items = "".join(
            f'<li><a href="{html.escape(f)}"><span class="nom">{html.escape(n)}</span><span class="go">Ouvrir ›</span></a></li>'
            for n, f in manips
        )
        cartes.append(f"<section><h2>{html.escape(g)}</h2><ul>{items}</ul></section>")
    anciennes = "".join(
        f'<li><a href="{html.escape(PAGES[nom])}"><span class="nom">{html.escape(lib)}</span><span class="go">Ouvrir ›</span></a></li>'
        for nom, (_g, lib) in ANCIENNES.items() if nom in pages
    )
    if anciennes:
        cartes.append(f'<section class="old"><h2>Premières versions</h2><ul>{anciennes}</ul></section>')
    return f"""<!doctype html>
<html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Labo virtuel 3D · 2ᵉ Bac PC BIOF — Moalim</title>
<meta name="description" content="Laboratoire virtuel 3D de physique-chimie et SVT pour le 2ᵉ Bac PC BIOF : manipulations libres, mesures, bilan.">
<link rel="icon" href="/favicon.svg">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:wght@400;700&family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,800&display=swap" rel="stylesheet">
<style>
:root{{--bg:#0b111a;--card:#121a27;--line:#24324a;--fg:#e8eef7;--mut:#9fb0c8;--accent:#ffc54d}}
*{{box-sizing:border-box}}body{{margin:0;min-height:100vh;background:radial-gradient(circle at 20% 0,#1a2740 0,var(--bg) 55%);color:var(--fg);font:16px/1.5 "Atkinson Hyperlegible",system-ui,sans-serif}}
main{{max-width:880px;margin:0 auto;padding:48px 16px 64px}}
.kicker{{color:var(--accent);font-size:13px;letter-spacing:.14em;text-transform:uppercase;font-weight:700}}
h1{{font:800 clamp(28px,5vw,44px)/1.1 "Bricolage Grotesque",system-ui,sans-serif;margin:.3em 0 .4em}}
.intro{{color:var(--mut);max-width:62ch;margin:0 0 32px}}
section{{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:18px 18px 8px;margin:0 0 18px}}
h2{{font:700 15px/1.3 "Bricolage Grotesque",system-ui,sans-serif;color:var(--accent);margin:0 0 10px;letter-spacing:.02em}}
ul{{list-style:none;margin:0;padding:0}}li{{border-top:1px solid var(--line)}}li:first-child{{border-top:0}}
a{{display:flex;justify-content:space-between;align-items:center;gap:16px;padding:14px 4px;color:var(--fg);text-decoration:none}}
a:hover .nom,a:focus-visible .nom{{color:var(--accent)}}a:focus-visible{{outline:2px solid var(--accent);outline-offset:2px;border-radius:8px}}
.go{{flex:none;color:var(--mut);font-size:14px}}
.old{{opacity:.75}}
footer{{color:var(--mut);font-size:14px;margin-top:28px}}footer a{{display:inline;padding:0;color:var(--accent)}}
</style></head>
<body><main>
<div class="kicker">Moalim · laboratoire virtuel</div>
<h1>Labo virtuel 3D — 2ᵉ Bac PC BIOF</h1>
<p class="intro">Manipulations libres sur une paillasse en 3D : on pèse, on verse, on mesure comme au lycée, on peut se tromper et recommencer. Chaque manip a un mode démonstration, un carnet qui explique chaque geste et un bilan qui compare ce que tu crois à ce qui est vraiment dans le récipient. À ouvrir sur ordinateur de préférence.</p>
{''.join(cartes)}
<footer>Retour au <a href="/">site Moalim</a>.</footer>
</main></body></html>
"""


if __name__ == "__main__":
    main()
