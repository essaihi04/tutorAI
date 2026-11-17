import json,sys
d=json.load(open(sys.argv[1])); out=[f"# {d.get('title',d.get('titre',''))} ({sys.argv[1].split('/')[-1][:-5]})\n"]
def txt(v):
    if isinstance(v,str): return v
    if isinstance(v,list): return '\n'.join('  - '+txt(x) for x in v)
    if isinstance(v,dict): return '; '.join(f"{k}: {txt(x)}" for k,x in v.items() if k not in('audio','mot','image','visual'))
    return str(v)
for a in d.get('activities',[]):
    out.append(f"\n## [{a.get('id')}] {a.get('title','')}\n")
    for s in a.get('slides',[]):
        out.append(f"\n### {s.get('id')} — {s.get('title','')}\nÉCRAN:")
        for k,v in (s.get('screen_content') or {}).items():
            if k in('image','visual','simulation'): continue
            out.append(f"  {k}: {txt(v)}")
        c=s.get('concentration') or {}
        if c.get('cahier'): out.append("CAHIER: "+txt(c['cahier']))
        if c.get('centre'): out.append("CENTRE: "+' | '.join(x.get('texte',str(x)) if isinstance(x,dict) else str(x) for x in c['centre']))
        st=s.get('speech_text') or {}
        out.append("VOIX: "+(st.get('fr') or st.get('mixed') or ''))
        q=s.get('question') or (s.get('screen_content') or {}).get('question')
        if isinstance(q,dict):
            out.append("QUESTION: "+q.get('prompt','')+' || '+' / '.join(map(str,q.get('options',[]))))
            dm=q.get('demonstration')
            if dm: out.append("DÉMO: "+' ⏎ '.join(l.get('texte','') for l in dm.get('lignes',[])))
open(sys.argv[2],'w').write('\n'.join(out))
