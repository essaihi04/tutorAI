"""Images du tableau SANS télécharger la vidéo (disque presque plein) : ffmpeg lit le flux YouTube à chaque instant.
  python images_flux.py <id> <dossier> <pas_s> [debut_s fin_s]
Même sortie que explorer_cours.py images : <id>_<seconde>.jpg"""
import sys, subprocess, pathlib
DENO = "C:/Users/HP/AppData/Local/Microsoft/WinGet/Links/deno.exe"
YT = [sys.executable, "-m", "yt_dlp", "--js-runtimes", f"deno:{DENO}", "-q", "--no-warnings"]
vid, dossier, pas = sys.argv[1], pathlib.Path(sys.argv[2]), float(sys.argv[3])
dossier.mkdir(parents=True, exist_ok=True)
r = subprocess.run(YT + ["-f", "bv*[height<=480]/b[height<=480]", "--print", "%(duration)s", "-g",
                         "https://www.youtube.com/watch?v=" + vid], capture_output=True, text=True)
lignes = [l for l in r.stdout.splitlines() if l.strip()]
if len(lignes) < 2:
    sys.exit("flux introuvable : " + r.stderr[-400:])
duree, url = float(lignes[0]), lignes[1]
s = float(sys.argv[4]) if len(sys.argv) > 4 else 0.0
f = min(float(sys.argv[5]), duree) if len(sys.argv) > 5 else duree
n = 0
while s < f:
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{s:.0f}", "-i", url, "-frames:v", "1",
                    "-vf", "scale='min(960,iw)':-2", "-q:v", "5", str(dossier / f"{vid}_{int(s):05d}.jpg")], timeout=120)
    s += pas; n += 1
print(f"{vid} : {n} images (durée {duree:.0f} s)")
