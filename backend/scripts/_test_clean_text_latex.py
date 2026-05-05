"""Quick test for _clean_text_latex without requiring full app boot."""
import re

_TABULAR_RE = re.compile(
    r'\\begin\{tabular\}\{[^}]*\}(.*?)\\end\{tabular\}',
    re.DOTALL,
)

def _tabular_to_markdown(match):
    inner = match.group(1)
    rows = [r.strip() for r in re.split(r'\\\\', inner)]
    rows = [r.replace('\\hline', '').strip() for r in rows if r.replace('\\hline', '').strip()]
    if not rows:
        return ''
    md_rows = []
    for i, row in enumerate(rows):
        cells = [c.strip() for c in row.split('&')]
        md_rows.append('| ' + ' | '.join(cells) + ' |')
        if i == 0:
            md_rows.append('| ' + ' | '.join(['---'] * len(cells)) + ' |')
    return '\n' + '\n'.join(md_rows) + '\n'

def clean_text_latex(text):
    if not text:
        return text
    text = text.replace('\\newline', '\n')
    text = re.sub(r'\\textbf\{([^}]*)\}', r'**\1**', text)
    text = re.sub(r'\\textit\{([^}]*)\}', r'*\1*', text)
    text = re.sub(r'\\underline\{([^}]*)\}', r'\1', text)
    text = re.sub(r'\\emph\{([^}]*)\}', r'*\1*', text)
    text = _TABULAR_RE.sub(_tabular_to_markdown, text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text

# Test 1: the 2020-normale context
sample = (
    r"Les parties 1 et 2 sont indépendantes.\newline"
    r"\textbf{Partie 1 : Étude d'une solution aqueuse d'ammoniac}\newline"
    r" L'ammoniac $\mathrm{NH_3}$ est un gaz.\newline"
    r"\textbf{Données :}\newline"
    r" - $K_e = 10^{-14}$ ;\newline"
    r" - toutes les mesures à $25^\circ C$."
)
result = clean_text_latex(sample)
print("=== Test 1: context field ===")
print(result)
print()

# Test 2: tabular table
sample2 = (
    r"Choisir l'indicateur adéquat.\newline"
    r"\begin{tabular}{|c|c|c|c|}\hline Indicateur & hélianthine & rouge de méthyle & phénolphtaléine \\ \hline Zone & 3,1–4,4 & 4,2–6,2 & 8,2–10 \\ \hline\end{tabular}"
)
result2 = clean_text_latex(sample2)
print("=== Test 2: tabular table ===")
print(result2)
