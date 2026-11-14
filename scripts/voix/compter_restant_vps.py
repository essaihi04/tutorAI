# Compte les pistes sans voix dans chaque dossier du lot (à lancer sur le VPS : scp puis python3). 14 novembre 2026.
import json,os,re,datetime
R="/srv/corpus_v4/voix_lot"; tot={}
def ajoute(cle,n,c):
    a=tot.setdefault(cle,[0,0]); a[0]+=n; a[1]+=c
for d in sorted(os.listdir(R)):
    D=os.path.join(R,d)
    if not os.path.isfile(os.path.join(D,"cours.json")): continue
    m=json.load(open(os.path.join(D,"cours.json"),encoding="utf-8"))
    t=[]
    for a in m.get("activities",[]):
        for s in a["slides"]:
            x=(s.get("speech_text") or {}).get("mixed","").strip()
            if x: t.append(("mixed",s["id"],x))
    for f,sub in (("pistes.json","reponses"),("demonstrations.json","demos")):
        p=os.path.join(D,f)
        if os.path.isfile(p): t+=[(sub,r["id"],r["parole"].strip()) for r in json.load(open(p,encoding="utf-8"))]
    groupe="cours en attente (att_)" if d.startswith("att_") else ("autres (_)" if d.startswith("_") else "cours en ligne")
    for sub,i,x in t:
        if not os.path.isfile(os.path.join(D,sub,i+".wav")):
            ajoute(groupe+" / "+("diapos" if sub=="mixed" else sub),1,len(x))
            ajoute("TOTAL",1,len(x))
for k,v in sorted(tot.items()): print(f"{k:45s} {v[0]:5d} pistes {v[1]:7d} car.")
# débit : pistes faites dans la dernière heure du log
L=open(R+"/voix_compte1.log",encoding="utf-8",errors="ignore").read().splitlines()
fa=[l for l in L if re.match(r"\s*\d+\s+[\d.]+ s\s+calcul",l)]
print("pistes faites depuis la relance :",len(fa))
