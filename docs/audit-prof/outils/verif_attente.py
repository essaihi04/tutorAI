import json,sys
def walk(o,path,out):
    if isinstance(o,dict):
        dm=o.get('demonstration')
        if isinstance(dm,dict):
            par=dm.get('parole','')
            for l in dm.get('lignes',[]):
                if l.get('mot') and l['mot'] not in par: out.append(('demo',path,l['mot'][:40]))
        for k,v in o.items(): walk(v,path+'/'+k,out)
    elif isinstance(o,list):
        for i,v in enumerate(o): walk(v,f'{path}[{i}]',out)
for f in sys.argv[1:]:
    d=json.load(open(f)); out=[]; walk(d,'',out)
    sl=[s for a in d['activities'] for s in a['slides']]; ids=[s['id'] for s in sl]
    for s in sl:
        sp=(s.get('speech_text') or {}).get('mixed','')
        c=s.get('concentration') or {}
        for p in (c.get('pointage') or [])+(c.get('centre') or []):
            if isinstance(p,dict) and p.get('mot') and p['mot'] not in sp: out.append(('voix',s['id'],p['mot'][:40]))
    bl=[i for se in d['seances'] for b in se['blocs'] for i in b['slide_ids']]
    miss=set(ids)-set(bl); dup=len(bl)-len(set(bl)); extra=set(bl)-set(ids)
    comp={c['id'] for c in d.get('competences',[])}
    badc={x for s in sl for x in s.get('competence_ids',[]) if comp and x not in comp}
    noaud=sum(1 for s in sl if not ((s.get('audio') or {}).get('mixed')))
    print(f.split('/')[-1], 'diapos',len(sl),'mots_absents',len(out),'hors_bloc',sorted(miss),'doublons',dup,'inconnues',sorted(extra),'compet_inconnues',sorted(badc),'diapos_sans_voix',noaud)
    for x in out[:5]: print('   ',x)
