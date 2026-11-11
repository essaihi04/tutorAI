"""Sur le VPS : DeepSeek écrit la réaction du tuteur pour chaque élément de items.json (cf. preparer_reponses.py).

  mkdir -p /tmp/gen_rep ; copier ici simulation_reaction.py et reponse_eleve.py (backend/app/services), avec dans
  reponse_eleve.py « from simulation_reaction import » au lieu de « from app.services.simulation_reaction import »,
  puis : cd /opt/moalim/backend && set -a && . /etc/moalim/backend.env && set +a &&
         .venv/bin/python /tmp/gen_rep/gen_reponses_vps.py /tmp/gen_rep/items.json /tmp/gen_rep/sortie.json
  Six appels à la fois, trois essais par réaction ; une clé connue impose le verdict (le modèle explique seulement).
"""
import asyncio, json, sys
sys.path.insert(0, "/opt/moalim/backend"); sys.path.insert(0, "/tmp/gen_rep_derivation_etude_fonctions")
import reponse_eleve as re_
from app.services.llm_service import llm_service
items = json.load(open(sys.argv[1], encoding="utf-8"))
sem = asyncio.Semaphore(6)
SYS = "Tu es un professeur de mathématiques bienveillant et exigeant. Tu réponds uniquement en JSON valide."
async def un(it):
    async with sem:
        p = re_.prompt_reponse(it["diapo"], it["question"], it["reponse"], it["t"], it["verdict"])
        for _ in range(3):
            try:
                x = await llm_service.chat(messages=[{"role": "user", "content": p}], system_prompt=SYS, temperature=0.4, max_tokens=500)
            except Exception as e:
                print("erreur", e, file=sys.stderr); continue
            r = re_.reaction_reponse(x, it["verdict"])
            if r:
                it["reaction"] = r; return
async def main():
    await asyncio.gather(*(un(it) for it in items))
    json.dump(items, open(sys.argv[2], "w", encoding="utf-8"), ensure_ascii=False)
    print(sum(1 for i in items if "reaction" in i), "/", len(items))
asyncio.run(main())
