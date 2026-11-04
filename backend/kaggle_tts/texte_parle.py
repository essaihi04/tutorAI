"""Texte des cours -> texte « parlé » donné au modèle de voix, écrit comme les transcriptions du corpus d'entraînement
(regles_transcription.md) : le modèle n'a appris que des phrases écrites comme le prof les dit.
Le texte affiché dans le cours ne change pas ; seule la lecture change.
- formules : CO₂ -> C O deux, C6H12O6 -> C six H douze O six, Ca²⁺ -> Ca deux plus, NADH,H⁺ -> NADH H plus ;
- nombres en lettres : en français à côté d'un mot français (« x plus un », « f de un »), en darija entre deux mots
  arabes (« مختلف على واحد ») ; glucose-6-phosphate -> glucose six phosphate ;
- chiffres romains des complexes : complexe I/II/III/IV -> un/deux/trois/quatre ;
- arrêts : découpage après « : » et « ; » (0,35 s) et aux virgules des phrases longues (0,22 s).
Test : python texte_parle.py (affiche chaque phrase des cours qui change)."""
import re

FR = "zéro un deux trois quatre cinq six sept huit neuf dix onze douze treize quatorze quinze seize".split()
AR_N = "صفر واحد جوج ثلاثة ربعة خمسة ستة سبعة ثمنية تسعود عشرة".split()
AR_N[9] = "تسعة"
EXPOSANTS = str.maketrans("₀₁₂₃₄₅₆₇₈₉⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻", "01234567890123456789+-")
SIGLES = ("FADH", "NADH", "NADP", "NAD", "ATP", "ADP", "GTP")
FORMULE = re.compile(r"(?<![\w])([A-Z][A-Za-z0-9₀-₉⁰-⁹²³¹]*[0-9₀-₉⁰-⁹²³¹][A-Za-z0-9₀-₉⁰-⁹²³¹]*)([+⁺⁻-]?)(?![\w])")
ARABE = re.compile("[؀-ۿ]")
LATIN = re.compile("[A-Za-zÀ-ÿ]")


def _formule(mt):
    f, morceaux = mt.group(1).translate(EXPOSANTS), []
    for sg in SIGLES:
        if f.startswith(sg):
            morceaux.append(sg); f = f[len(sg):]; break
    for t in re.findall(r"[A-Z][a-z]?|[0-9]+", f):
        morceaux.append(FR[int(t)] if t.isdigit() and int(t) < len(FR) else t)
    return " ".join(morceaux) + {"+": " plus", "-": " moins"}.get(mt.group(2).translate(EXPOSANTS), "")


def _nombre(p, mt):
    n = int(mt.group(0))
    if n >= len(FR):
        return mt.group(0)
    avant = re.findall(r"[^\s\d]+", p[:mt.start()])[-1:] or [""]
    apres = re.findall(r"[^\s\d]+", p[mt.end():])[:1] or [""]
    # darija seulement entre deux mots arabes, et jamais dans une phrase de maths (variable x, f, g… : le prof dit les nombres en français)
    maths = re.search(r"(?<![\w'])[a-zA-Z](?![\w'])|\b(?:égale?|sur|plus|moins|limite)\b", p)
    if n < len(AR_N) and ARABE.search(avant[0][-1:]) and ARABE.search(apres[0][:1]) and not maths:
        return AR_N[n]
    return FR[n]


def parle(p):
    p = re.sub(r"NADH\s*,\s*H\s*(?:[+⁺]|plus\b)", "NADH H plus", p)
    p = re.sub(r"\b([A-Z][a-z]?)([+⁺⁻])(?!\w)", lambda mt: mt.group(1) + (" plus" if mt.group(2) in "+⁺" else " moins"), p)   # H⁺ -> H plus
    p = FORMULE.sub(_formule, p)
    p = re.sub(r"\b(NADP|NAD)\s*[+⁺]", r"\1 plus", p)
    p = re.sub(r"(?<=[A-Za-z])-([0-9]{1,2})-(?=[A-Za-z])", r" \1 ", p)          # glucose-6-phosphate
    p = re.sub(r"(?<!\w)(?<![0-9][,.])[0-9]{1,2}(?!\w)(?![,.][0-9])", lambda mt: _nombre(p, mt), p)   # pas les décimaux (1,70)
    p = re.sub(r"\b(complexe)\s+I\b", r"\1 un", p)
    return re.sub(r"\b(IV|III|II)\b", lambda mt: {"II": "deux", "III": "trois", "IV": "quatre"}[mt.group(1)], p)


COUPE = re.compile(r"\s*([:;؛])\s+|\s*([,،])\s+")
# expressions du prof suivies d'une virgule : on s'arrête après, même si le morceau est court
EXPRESSION = re.compile(r"^(?:و|ف)?(?:إذن|اذن|يعني|بمعنى|دابا|أولا|ثانيا|من بعد|ومن بعد|بالتالي|برافو|donc|alors|ensuite|"
                        r"maintenant|bon|bravo|attention|d'abord|c'est-à-dire|autrement dit)\s*[,،]$", re.I)


def segments(p):
    """Phrase -> [(morceau, pause après en s)] ; on ne coupe jamais un morceau de moins de 10 caractères."""
    out, cur, pos, longue = [], "", 0, len(p) > 90
    for mt in COUPE.finditer(p):
        cur = (cur + " " + p[pos:mt.end()].strip()).strip(); pos = mt.end()
        fort = bool(mt.group(1))
        if len(p) - pos >= 15 and EXPRESSION.match(cur):
            out.append((cur, 0.28)); cur = ""
        elif len(cur) >= 10 and len(p) - pos >= 15 and (fort or (longue and len(cur) >= 25)):
            out.append((cur, 0.35 if fort else 0.22)); cur = ""
    cur = (cur + " " + p[pos:].strip()).strip()
    if cur:
        out.append((cur, 0.0))
    return out


if __name__ == "__main__":
    import sys, json, glob
    sys.stdout.reconfigure(encoding="utf-8")
    sys.path.insert(0, r"C:/Users/HP/Desktop/ai-tutor-bac/backend")
    from scripts.generate_course_audio import load_manifest, manifest_slides
    FIN = re.compile(r"(?<=[.!?؟…])\s+")
    n = 0
    for f in sorted(glob.glob(r"C:/Users/HP/Desktop/ai-tutor-bac/backend/data/courses/*_course_v1.json")):
        _, m = load_manifest(json.load(open(f, encoding="utf-8"))["stable_id"])
        for s in manifest_slides(m):
            for ph in FIN.split(((s.get("speech_text") or {}).get(sys.argv[1] if len(sys.argv) > 1 else "mixed") or "").strip()):
                q = parle(ph)
                if q != ph:
                    n += 1; print("-", ph, "\n+", q, "\n")
    print(n, "phrases changées")
