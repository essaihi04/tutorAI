"""node --check de chaque <script> inline d'une page HTML (et des .js) : python check_js.py <fichiers…>"""
import re, subprocess, sys, tempfile, os
sys.stdout.reconfigure(encoding='utf-8'); ko = 0
for p in sys.argv[1:]:
    if p.endswith('.js'):
        blocs = [open(p, encoding='utf-8').read()]
    else:
        blocs = re.findall(r'<script>(.*?)</script>', open(p, encoding='utf-8').read(), re.S)
    for i, b in enumerate(blocs):
        fd, t = tempfile.mkstemp(suffix='.js'); os.write(fd, b.encode('utf-8')); os.close(fd)
        r = subprocess.run(['node', '--check', t], capture_output=True, text=True); os.unlink(t)
        if r.returncode: ko += 1; print('ERREUR', p, i, r.stderr[-600:])
    print('ok' if not ko else '', os.path.basename(p))
sys.exit(1 if ko else 0)
