/**
 * Banc d'essai (dev seulement, /dev/memoire) des écrans de la mémoire longue, sans serveur : rappel de début de séance,
 * fin de bloc (cahier → retrouver → exercice), fin de séance et bannière de l'accueil. Les appels au serveur sont
 * simulés ; chaque événement noté s'affiche en bas.
 */
import { useState } from 'react';
import RappelDebutSeance from '../components/course/memoire/RappelDebutSeance';
import CycleBloc from '../components/course/memoire/CycleBloc';
import FinDeSeance from '../components/course/memoire/FinDeSeance';
import BanniereRappels from '../components/course/memoire/BanniereRappels';
import type { BlocCours, RappelsDuJour, SeanceCours } from '../components/course/memoire/api';

const notes: unknown[] = [];
let ecouteur: (() => void) | null = null;
const original = window.fetch.bind(window);
window.fetch = async (entree: RequestInfo | URL, init?: RequestInit) => {
  const url = typeof entree === 'string' ? entree : entree instanceof URL ? entree.href : entree.url;
  const json = (x: unknown) => new Response(JSON.stringify(x), { status: 200, headers: { 'Content-Type': 'application/json' } });
  if (url.includes('/memoire/evenement')) {
    const e = JSON.parse(String(init?.body || '{}'));
    notes.push(e); ecouteur?.();
    return json(e.evenement === 'rappel' ? { ok: true, marche: e.correct ? 2 : 0, prochaine: new Date(Date.now() + (e.correct ? 7 : 1) * 86400000).toISOString().slice(0, 10) } : { ok: true });
  }
  if (url.includes('/memoire/accueil')) return json({ badge: 3, dus: { 'physique-chimie': 3 }, heure: 18, heure_habituelle: 21, ignorees: 0, preferences: { heure: null, coupees: false },
    notification: { matiere: 'physique-chimie', nom_matiere: 'physique-chimie', nombre: 3, minutes: 3, texte: "3 rappels de physique-chimie t'attendent (3 min)", niveau: 'banniere', nouvelle: true } });
  if (url.includes('/memoire/rappels/')) return json(RAPPELS);
  if (url.includes('/memoire/preferences')) return json({ ok: true });
  if (url.includes('/answer-reaction')) {
    const b = JSON.parse(String(init?.body || '{}'));
    const ok = /Δt|d\s*\/|perturbation/i.test(b.reponse || '');
    await new Promise(r => setTimeout(r, 600));
    return json({ correct: ok, parole: '', ecrit: ok ? 'Juste : c’est la relation du cadre.' : 'Pas encore : pense à la distance et à la durée.' });
  }
  return original(entree, init);
};

const RAPPELS: RappelsDuJour = {
  matiere: 'physique-chimie', nom_matiere: 'physique-chimie', minutes: 3,
  questions: [
    { cours_id: 'phys_ch1_waves_exemple', cours_titre: 'Ondes mécaniques progressives', competence_id: 'C1', competence: 'Reconnaître une onde mécanique progressive', marche: 1, due: '2026-11-10', en_avance: false, jours_de_retard: 1,
      question: { id: 'r1', type: 'qcm', prompt: 'Une onde mécanique progressive transporte…', options: ['de la matière', 'de l’énergie, sans transport de matière', 'de la matière et de l’énergie'], correct: 1 } },
    { cours_id: 'phys_ch1_waves_exemple', cours_titre: 'Ondes mécaniques progressives', competence_id: 'C4', competence: 'Calculer la célérité', marche: 0, due: '2026-11-11', en_avance: false, jours_de_retard: 0,
      question: { id: 'r2', type: 'libre', prompt: 'Écris la relation qui donne la célérité v d’une onde.', attendu: 'v = d / Δt' } },
    { cours_id: 'chem_ch1_kinetics', cours_titre: 'Cinétique', competence_id: 'C2', competence: 'Facteurs cinétiques', marche: 2, due: '2026-11-11', en_avance: false, jours_de_retard: 0,
      question: { id: 'r3', type: 'vrai_faux', prompt: 'Augmenter la température ralentit une réaction.', correct: false } },
  ],
};

const BLOC: BlocCours = {
  id: 'b2', titre: 'La célérité', slide_ids: ['x'],
  cahier: [{ texte: 'Célérité : v = d / Δt (m·s⁻¹)' }, { texte: 'd : distance parcourue (m), Δt : durée (s)' }, { texte: 'La célérité dépend du milieu.' }],
  retrouver: { prompt: 'Cahier fermé : écris la relation de la célérité et l’unité de chaque grandeur.', attendu: 'v = d / Δt ; v en m·s⁻¹, d en m, Δt en s', competence_id: 'C4' },
  exercice: { type: 'qcm', prompt: 'Une onde parcourt 6 m en 2 s. Sa célérité vaut :', options: ['12 m·s⁻¹', '3 m·s⁻¹', '0,33 m·s⁻¹'], correct: 1 },
};
const SEANCES: SeanceCours[] = [
  { id: 's1', titre: 'Qu’est-ce qu’une onde ?', blocs: [BLOC, BLOC, BLOC] },
  { id: 's2', titre: 'Le retard et la célérité', blocs: [BLOC, BLOC, BLOC] },
];

export default function MemoireAudit() {
  const [vue, setVue] = useState<'rappel' | 'bloc' | 'fin' | 'pause' | 'accueil'>('rappel');
  const [, maj] = useState(0);
  const [cle, setCle] = useState(0);
  ecouteur = () => maj(x => x + 1);
  return (
    <div className="min-h-screen bg-slate-950 p-4 text-white">
      <div className="mb-3 flex flex-wrap gap-2 text-sm">
        {(['rappel', 'bloc', 'fin', 'pause', 'accueil'] as const).map(v => (
          <button key={v} onClick={() => { setVue(v); setCle(k => k + 1); }} className={`rounded px-3 py-1 ${vue === v ? 'bg-cyan-500 text-black' : 'bg-white/10'}`}>{v}</button>
        ))}
      </div>
      <div key={cle} className="mx-auto h-[620px] max-w-3xl">
        {vue === 'rappel' && <RappelDebutSeance rappels={RAPPELS} onFini={() => setVue('bloc')} />}
        {vue === 'bloc' && <CycleBloc bloc={BLOC} place={{ coursId: 'phys_ch1_waves_exemple', seanceId: 's1', seance: 0, nbSeances: 2, bloc: 2, nbBlocs: 3 }} onFini={() => setVue('fin')} />}
        {vue === 'fin' && <FinDeSeance coursId="phys_ch1_waves_exemple" seance={0} seances={SEANCES} debutMs={Date.now() - 27 * 60000} onPause={() => setVue('accueil')} onContinuer={() => setVue('rappel')} />}
        {vue === 'pause' && <FinDeSeance coursId="phys_ch1_waves_exemple" seance={0} seances={SEANCES} raison="saturation" onPause={() => setVue('accueil')} />}
        {vue === 'accueil' && <div className="p-4"><BanniereRappels /></div>}
      </div>
      <pre className="mx-auto mt-4 max-h-56 max-w-3xl overflow-auto rounded bg-black/40 p-2 text-xs text-white/60">{notes.map(n => JSON.stringify(n)).join('\n')}</pre>
    </div>
  );
}
