import { useCallback, useEffect, useState } from 'react';
import RappelDebutSeance from './RappelDebutSeance';
import { changerPreferences, lireAccueil, noter, type Accueil } from './api';

/**
 * Les rappels sur l'écran d'accueil de l'élève (skill `suivi-des-acquis`, section 8) : seulement quand quelque chose
 * est dû pour CET élève. Le badge est toujours là s'il y a du dû ; la bannière (« 3 rappels de physique-chimie
 * t'attendent (3 min) ») vient à son heure habituelle, une fois par jour au plus, et se fait discrète après plusieurs
 * ignorées (décidé par le serveur, `memoire_longue.accueil`). Un geste ouvre le rappel ; un geste change l'heure ou
 * coupe les notifications. `?rappel=<matière>` dans l'adresse ouvre directement le rappel (lien d'une notification).
 */
const HEURES = [7, 12, 14, 17, 18, 19, 20, 21, 22];

export default function BanniereRappels() {
  const [a, setA] = useState<Accueil | null>(null);
  const [ouvert, setOuvert] = useState<string | null>(null);
  const [reglage, setReglage] = useState(false);

  const charger = useCallback(() => { lireAccueil().then(setA).catch(() => setA(null)); }, []);
  useEffect(() => {
    charger();
    const m = new URLSearchParams(window.location.search).get('rappel');
    if (m) { setOuvert(m); void noter({ evenement: 'notification', action: 'ouverte', matiere: m }); }
  }, [charger]);

  const ouvrir = (matiere: string) => { setOuvert(matiere); void noter({ evenement: 'notification', action: 'ouverte', matiere }); };
  const regler = async (p: { heure: number | null; coupees: boolean }) => {
    setReglage(false);
    setA(x => (x ? { ...x, preferences: p, heure: p.heure ?? x.heure, notification: p.coupees ? null : x.notification } : x));
    await changerPreferences(p).catch(() => null);
    charger();
  };

  const premiereMatiere = a ? Object.entries(a.dus).sort((x, y) => y[1] - x[1])[0]?.[0] : undefined;

  return (
    <>
      {a && a.badge > 0 && (a.notification?.niveau === 'banniere' ? (
        <section className="relative overflow-hidden rounded-[22px] border border-amber-300/25 bg-gradient-to-r from-amber-500/15 via-amber-400/10 to-transparent p-4 sm:p-5">
          <div className="flex flex-wrap items-center gap-3">
            <span className="relative text-2xl">🔁<span className="absolute -right-2 -top-1 rounded-full bg-amber-400 px-1.5 text-[11px] font-black text-slate-950">{a.badge}</span></span>
            <div className="mr-auto min-w-0">
              <p className="text-base font-bold text-white">{a.notification.texte.charAt(0).toUpperCase() + a.notification.texte.slice(1)}</p>
              <p className="text-xs text-white/55">Ce que tu retrouves aujourd’hui, tu le gardes pour le bac.</p>
            </div>
            <button type="button" onClick={() => ouvrir(a.notification!.matiere)}
              className="rounded-full bg-amber-300 px-5 py-2.5 text-sm font-black text-slate-950 shadow-lg hover:bg-amber-200">
              Commencer
            </button>
            <button type="button" onClick={() => setReglage(r => !r)} title="Changer l’heure ou couper les rappels"
              className="rounded-full px-2 py-1 text-xs text-white/45 hover:text-white/80">⏰ {a.heure} h</button>
          </div>
          {reglage && <Reglage a={a} onChoix={regler} />}
        </section>
      ) : premiereMatiere && (
        <div className="flex items-center gap-2">
          <button type="button" onClick={() => ouvrir(premiereMatiere)}
            className="inline-flex items-center gap-2 rounded-full border border-amber-300/25 bg-amber-300/10 px-3 py-1.5 text-xs font-bold text-amber-100 hover:bg-amber-300/20">
            🔁 {a.badge} rappel{a.badge > 1 ? 's' : ''} · {Math.max(1, Math.ceil(a.badge * 0.7))} min
          </button>
          <button type="button" onClick={() => setReglage(r => !r)} className="text-xs text-white/35 hover:text-white/70">
            {a.preferences.coupees ? '🔕 coupés' : `⏰ ${a.heure} h`}
          </button>
          {reglage && <Reglage a={a} onChoix={regler} />}
        </div>
      ))}

      {ouvert && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/85 p-3 backdrop-blur-sm sm:p-6">
          <div className="relative mt-8 h-[min(85vh,720px)] w-full max-w-2xl">
            <button type="button" onClick={() => { setOuvert(null); charger(); }} aria-label="Fermer"
              className="absolute -top-9 right-0 z-10 rounded-full px-3 py-1 text-sm text-white/50 hover:text-white">Plus tard ✕</button>
            <RappelDebutSeance matiere={ouvert} libelleFin="Fini ✓" onFini={() => { setOuvert(null); charger(); }} />
          </div>
        </div>
      )}
    </>
  );
}

function Reglage({ a, onChoix }: { a: Accueil; onChoix: (p: { heure: number | null; coupees: boolean }) => void }) {
  return (
    <div className="mt-3 flex flex-wrap items-center gap-1.5 text-xs" style={{ fontFamily: 'system-ui, sans-serif' }}>
      <span className="mr-1 text-white/45">Me le rappeler à</span>
      {HEURES.map(h => (
        <button key={h} type="button" onClick={() => onChoix({ heure: h, coupees: false })}
          className={`rounded-full px-2.5 py-1 ${a.heure === h && !a.preferences.coupees ? 'bg-amber-300 text-slate-950' : 'bg-white/10 text-white/70 hover:bg-white/20'}`}>{h} h</button>
      ))}
      {a.heure_habituelle !== null && a.preferences.heure !== null && (
        <button type="button" onClick={() => onChoix({ heure: null, coupees: false })} className="rounded-full bg-white/10 px-2.5 py-1 text-white/70 hover:bg-white/20">
          mon heure habituelle ({a.heure_habituelle} h)
        </button>
      )}
      {a.preferences.coupees
        ? <button type="button" onClick={() => onChoix({ heure: a.preferences.heure, coupees: false })} className="rounded-full bg-white/10 px-2.5 py-1 text-white/70 hover:bg-white/20">🔔 Réactiver</button>
        : <button type="button" onClick={() => onChoix({ heure: a.preferences.heure, coupees: true })} className="rounded-full bg-white/10 px-2.5 py-1 text-white/70 hover:bg-white/20">🔕 Couper</button>}
    </div>
  );
}
