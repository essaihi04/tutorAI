/**
 * Banc d'essai du professeur dans un laboratoire — sans session ni serveur.
 *
 * Le professeur animé ne vole dans une simulation qu'au bout d'une session
 * authentifiée : cette page monte un laboratoire au tableau et le personnage
 * seuls, et laisse envoyer à la main les commandes du tuteur (pointer un repère,
 * lancer, vérifier) pour voir le vol, le doigt tendu, l'appui, l'anneau à la
 * craie et les gestes de réaction (bravo, non de la tête).
 */
import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import AIAvatar, { type LabControlCommand } from '../components/session/AIAvatar';
import { SessionMediaDisplay } from '../components/session/MediaViewer';
import { PROFESSOR_POINT_HOLD_MS, PROFESSOR_REACH_MS, POINTING_COMMANDS } from '../services/professorFocus';
import type { ProfessorEmotionKind } from '../services/professorEmotion';

const LABOS = [
  { label: 'Ondes · capteurs et retard', url: '/media/simulations/physics/progressive/index.html?variant=progressive', id: 'physics_waves_advanced_lab' },
  { label: 'Ondes · corde', url: '/media/simulations/physics/progressive/index.html?variant=cord', id: 'physics_waves_advanced_lab' },
  { label: 'TP dipôle RC', url: '/media/simulations/physics/tp/rc/index.html', id: '' },
  { label: 'Chimie · électrochimie', url: '/media/simulations/chimie/labs/electrochimie/index.html', id: '' },
  { label: 'SVT · chimiosmose', url: '/media/simulations/svt/ch1_consommation_matiere_organique/chimiosmose/index.html', id: '' },
];

export default function ProfesseurLaboAudit() {
  const [labo, setLabo] = useState(LABOS[0]);
  const [labControl, setLabControl] = useState<LabControlCommand | null>(null);
  const [emotion, setEmotion] = useState<{ kind: ProfessorEmotionKind; key: number } | null>(null);
  const [reperes, setReperes] = useState<Record<string, string>>({});
  const [journal, setJournal] = useState<string[]>([]);
  const sequence = useRef(0);
  const queue = useRef<Record<string, unknown>[]>([]);
  const busy = useRef(false);

  // La file se vide une commande à la fois, comme dans LearningSession ; le relancement passe par une
  // référence, car la fonction ne peut pas se nommer elle-même avant d'être déclarée.
  const suivant = useRef<() => void>(() => {});
  const dispatch = useCallback(() => {
    if (busy.current) return;
    const next = queue.current.shift();
    if (!next) return;
    busy.current = true;
    const command = String(next.command ?? '');
    setLabControl({ sequence: ++sequence.current, command, message: next });
    const delai = POINTING_COMMANDS.has(command) ? Math.round(PROFESSOR_POINT_HOLD_MS * 0.7) : PROFESSOR_REACH_MS + 700;
    window.setTimeout(() => { busy.current = false; suivant.current(); }, delai);
  }, []);
  useEffect(() => { suivant.current = dispatch; }, [dispatch]);
  const envoyer = useCallback((command: string, parameters: Record<string, unknown> = {}) => {
    queue.current.push({ type: 'simulation_control', simulation_id: labo.id || undefined, command, parameters });
    dispatch();
  }, [dispatch, labo.id]);

  const onSimulationUpdate = useCallback((data: { type?: string; capabilities?: { reperes?: Record<string, string> }; current_state?: Record<string, unknown>; student_actions?: unknown[] }) => {
    if (data.type === 'simulation_manifest' && data.capabilities?.reperes) setReperes(data.capabilities.reperes);
    if (data.type === 'simulation_state') {
      const dernier = data.student_actions?.[data.student_actions.length - 1];
      const action = typeof dernier === 'string' ? dernier : String((dernier as { action?: string })?.action ?? '');
      setJournal(previous => [`${new Date().toLocaleTimeString()} · ${action || 'état'}${typeof data.current_state?.correct === 'boolean' ? ` · correct=${data.current_state.correct}` : ''}`, ...previous].slice(0, 8));
    }
  }, []);
  const media = useMemo(() => ({ type: 'simulation' as const, url: labo.url }), [labo.url]);

  return (
    <div className="min-h-screen bg-slate-900 text-slate-100 p-4 flex flex-col gap-3">
      <header className="flex flex-wrap items-center gap-3">
        <h1 className="text-lg font-semibold">Banc d'essai · le professeur dans un laboratoire</h1>
        <select className="bg-slate-800 rounded px-2 py-1" value={labo.url} onChange={e => { setReperes({}); setLabo(LABOS.find(l => l.url === e.target.value) ?? LABOS[0]); }}>
          {LABOS.map(l => <option key={l.url} value={l.url}>{l.label}</option>)}
        </select>
      </header>
      <div className="flex gap-3 flex-1 min-h-0">
        <aside className="w-72 shrink-0 flex flex-col gap-2 text-sm">
          <section className="bg-slate-800 rounded p-2 flex flex-col gap-1">
            <b>Commandes (le professeur appuie)</b>
            <div className="flex flex-wrap gap-1">
              {['start', 'fire_pulse', 'pause', 'step', 'check', 'reset', 'reveal_hint'].map(c =>
                <button key={c} className="px-2 py-1 rounded bg-emerald-700 hover:bg-emerald-600" onClick={() => envoyer(c)}>{c}</button>)}
            </div>
          </section>
          <section className="bg-slate-800 rounded p-2 flex flex-col gap-1">
            <b>Repères (le professeur montre du doigt)</b>
            {Object.keys(reperes).length === 0 && <span className="text-slate-400">En attente du manifeste du laboratoire…</span>}
            <div className="flex flex-wrap gap-1">
              {Object.entries(reperes).map(([id, label]) =>
                <button key={id} className="px-2 py-1 rounded bg-amber-700 hover:bg-amber-600" title={id} onClick={() => envoyer('highlight', { target: id })}>{label}</button>)}
            </div>
          </section>
          <section className="bg-slate-800 rounded p-2 flex flex-col gap-1">
            <b>Réactions</b>
            <div className="flex flex-wrap gap-1">
              {(['celebrate', 'wrong', 'encourage'] as ProfessorEmotionKind[]).map(k =>
                <button key={k} className="px-2 py-1 rounded bg-sky-700 hover:bg-sky-600" onClick={() => setEmotion({ kind: k, key: Date.now() })}>{k}</button>)}
            </div>
          </section>
          <section className="bg-slate-800 rounded p-2 flex flex-col gap-1 text-xs text-slate-300">
            <b className="text-sm text-slate-100">Journal du laboratoire</b>
            {journal.map((l, i) => <span key={i}>{l}</span>)}
          </section>
        </aside>
        <main className="flex-1 min-w-0 min-h-[520px]">
          <SessionMediaDisplay media={media} isVisible onSimulationUpdate={onSimulationUpdate} />
        </main>
      </div>
      <AIAvatar isSpeaking={false} isProcessing={false} labControl={labControl} emotion={emotion} />
    </div>
  );
}
