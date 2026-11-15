"""Ramène dans le dossier local les fichiers poussés sur origin/main par des sessions cloud, sans pull ni reset.

Le `main` local est en retard et contient du travail non commité d'autres sessions : on ne touche ni à la branche, ni à
l'index, ni aux fichiers modifiés localement. Pour chaque fichier changé entre BASE et origin/main dans les dossiers
donnés :
  - si le fichier local est identique à sa version de BASE (personne n'y a touché ici) → il reçoit la version
    d'origin/main (fins de ligne du fichier local conservées) ; un fichier supprimé sur origin est supprimé ;
  - sinon → « CONFLIT », le fichier local n'est pas touché (à fusionner à la main).

  python scripts/recuperer_cloud.py BASE [dossier …] [--appliquer]

BASE : le commit d'origin/main que le dossier local reflète déjà (par exemple le SHA poussé juste avant de lancer les
sessions cloud). Sans --appliquer, la commande montre seulement ce qu'elle ferait.
Exemple : python scripts/recuperer_cloud.py 205f4700 frontend/public/media/simulations --appliquer
"""
import subprocess, sys, pathlib

def git(*a, ok=False):
    r = subprocess.run(['git', *a], capture_output=True)
    if r.returncode and not ok: sys.exit(r.stderr.decode('utf-8', 'replace'))
    return r

args = [a for a in sys.argv[1:] if not a.startswith('--')]
appliquer = '--appliquer' in sys.argv
if not args: sys.exit(__doc__)
base, dossiers = args[0], args[1:] or ['.']
git('fetch', '-q', 'origin')
norm = lambda b: b.replace(b'\r\n', b'\n')
noms = git('diff', '--name-status', '--no-renames', base, 'origin/main', '--', *dossiers).stdout.decode('utf-8').splitlines()
maj = conflits = 0
for ligne in noms:
    etat, chemin = ligne.split('\t', 1)
    p = pathlib.Path(chemin)
    avant = git('show', f'{base}:{chemin}', ok=True)
    avant = norm(avant.stdout) if avant.returncode == 0 else None
    local = norm(p.read_bytes()) if p.exists() else None
    # Intact ici si le fichier local est sa version de BASE, ou une version poussée depuis (récupération précédente).
    connues = [avant]
    for sha in git('log', '--format=%H', f'{base}..origin/main', '--', chemin).stdout.decode().split():
        v = git('show', f'{sha}:{chemin}', ok=True)
        connues.append(norm(v.stdout) if v.returncode == 0 else None)
    if local not in connues:
        nouveau = git('show', f'origin/main:{chemin}', ok=True)
        if nouveau.returncode == 0 and local == norm(nouveau.stdout):
            continue                                           # déjà à jour
        print('CONFLIT (modifié ici, non touché)', chemin); conflits += 1; continue
    if etat != 'D':
        actuel = git('show', f'origin/main:{chemin}', ok=True)
        if actuel.returncode == 0 and local == norm(actuel.stdout):
            continue                                           # déjà à jour
    if etat == 'D':
        print('supprimer', chemin)
        if appliquer and p.exists(): p.unlink()
    else:
        contenu = norm(git('show', f'origin/main:{chemin}').stdout)
        if p.exists() and b'\r\n' in p.read_bytes(): contenu = contenu.replace(b'\n', b'\r\n')
        print('mettre à jour' if p.exists() else 'créer', chemin)
        if appliquer:
            p.parent.mkdir(parents=True, exist_ok=True); p.write_bytes(contenu)
    maj += 1
print(f'{maj} fichier(s) {"mis à jour" if appliquer else "à mettre à jour"}, {conflits} conflit(s).'
      + ('' if appliquer else ' Relancer avec --appliquer pour écrire.'))
