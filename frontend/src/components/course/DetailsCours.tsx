import { useEffect, useState } from 'react';
import { CheckCircle2, CircleDashed, CircleHelp, Clock3, Eye, MessageCircle, Play, Repeat2, X, XCircle } from 'lucide-react';
import type { CourseCatalogCourse, StatutCompetence, TableauCours } from '../../services/api';

/**
 * Le panneau « Détails » d'un cours (21 novembre 2026), ouvert depuis sa carte dans la bibliothèque : ce que l'élève
 * en a vu, combien de fois il l'a lu, le temps passé, ses compétences (acquises, partielles, à revoir, restantes) et
 * ses lacunes avec la manière de les reprendre, le temps par jour sur deux semaines. Rien n'y est inventé : tout vient
 * de GET /course-player/tableau-de-bord (stats de lecture + suivi des acquis).
 */

export const STATUTS: { id: StatutCompetence; label: string; couleur: string; Icone: typeof CheckCircle2 }[] = [
  { id: 'acquis', label: 'Acquises', couleur: 'bg-emerald-400', Icone: CheckCircle2 },
  { id: 'partiel', label: 'Partielles', couleur: 'bg-amber-400', Icone: CircleHelp },
  { id: 'non_acquis', label: 'À revoir', couleur: 'bg-rose-400', Icone: XCircle },
  { id: 'non_evalue', label: 'Pas encore évaluées', couleur: 'bg-white/15', Icone: CircleDashed },
];

export const formatMinutes = (minutes: number) => {
  if (minutes < 1) return '0 min';
  if (minutes < 60) return `${Math.round(minutes)} min`;
  const h = Math.floor(minutes / 60);
  const m = Math.round(minutes % 60);
  return m ? `${h} h ${String(m).padStart(2, '0')}` : `${h} h`;
};

const ilYA = (iso: string | null) => {
  if (!iso) return '';
  const jours = Math.floor((Date.now() - new Date(iso).getTime()) / 86400000);
  if (jours <= 0) return "aujourd'hui";
  if (jours === 1) return 'hier';
  return `il y a ${jours} jours`;
};

/** La barre des compétences : un segment par statut, 2 px d'écart, bouts arrondis. */
export function BarreCompetences({ c, hauteur = 'h-1.5' }: { c: TableauCours['competences']; hauteur?: string }) {
  if (!c.total) return null;
  return (
    <span className={`flex ${hauteur} w-full gap-[2px] overflow-hidden rounded-full`}>
      {STATUTS.map(({ id, couleur, label }) => {
        const n = c[id];
        return n ? (
          <span key={id} className={`${couleur} h-full first:rounded-l-full last:rounded-r-full`} style={{ width: `${(n * 100) / c.total}%` }} title={`${label} : ${n}`} />
        ) : null;
      })}
    </span>
  );
}

function Tuile({ Icone, valeur, libelle, detail }: { Icone: typeof Eye; valeur: string; libelle: string; detail?: string }) {
  return (
    <div className="rounded-2xl border border-white/[0.07] bg-white/[0.035] p-3">
      <p className="flex items-center gap-1.5 text-[11px] font-bold text-white/45"><Icone className="h-3.5 w-3.5" /> {libelle}</p>
      <p className="mt-1 text-xl font-black text-white">{valeur}</p>
      {detail && <p className="mt-0.5 text-[11px] text-white/40">{detail}</p>}
    </div>
  );
}

function TempsParJour({ jours, barre }: { jours: { jour: string; minutes: number }[]; barre: string }) {
  const [survol, setSurvol] = useState<number | null>(null);
  const max = Math.max(1, ...jours.map((j) => j.minutes));
  const libelleJour = (iso: string) => new Date(`${iso}T12:00:00`).toLocaleDateString('fr-FR', { day: 'numeric', month: 'short' });
  return (
    <div>
      <div className="relative flex h-24 items-end gap-1 border-b border-white/10" onMouseLeave={() => setSurvol(null)}>
        <span className="absolute -top-4 left-0 text-[10px] text-white/30">max {formatMinutes(max)}</span>
        {jours.map((j, i) => (
          <button
            key={j.jour}
            type="button"
            onMouseEnter={() => setSurvol(i)}
            onFocus={() => setSurvol(i)}
            onClick={() => setSurvol(i)}
            className="relative flex h-full flex-1 items-end"
            aria-label={`${libelleJour(j.jour)} : ${formatMinutes(j.minutes)}`}
          >
            <span
              className={`block w-full rounded-t ${j.minutes ? barre : 'bg-white/[0.06]'} ${survol === i ? 'opacity-100' : 'opacity-80'}`}
              style={{ height: j.minutes ? `${Math.max(6, (j.minutes * 100) / max)}%` : '2px' }}
            />
            {survol === i && (
              <span className={`pointer-events-none absolute bottom-full z-10 mb-1 whitespace-nowrap rounded-md bg-white px-2 py-1 text-[11px] font-bold text-indigo-950 shadow-lg ${
                i < jours.length / 3 ? 'left-0' : i > (jours.length * 2) / 3 ? 'right-0' : 'left-1/2 -translate-x-1/2'
              }`}>
                {libelleJour(j.jour)} · {formatMinutes(j.minutes)}
              </span>
            )}
          </button>
        ))}
      </div>
      <div className="mt-1 flex justify-between text-[10px] text-white/35">
        <span>{libelleJour(jours[0].jour)}</span>
        <span>aujourd'hui</span>
      </div>
    </div>
  );
}

export default function DetailsCours({
  course, tableau, barre, badge, matiere, onClose, onOpen, onAskTutor,
}: {
  course: CourseCatalogCourse;
  tableau?: TableauCours;
  barre: string;
  badge: string;
  matiere: string;
  onClose: () => void;
  onOpen: () => void;
  onAskTutor: () => void;
}) {
  useEffect(() => {
    const touche = (e: KeyboardEvent) => { if (e.key === 'Escape') onClose(); };
    window.addEventListener('keydown', touche);
    return () => window.removeEventListener('keydown', touche);
  }, [onClose]);

  const st = tableau?.stats;
  const c = tableau?.competences;
  const vu = Math.max(tableau?.vu_pourcent || 0, course.progress_percent || 0);
  const lacunes = (c?.liste || [])
    .filter((x) => x.statut === 'non_acquis' || x.statut === 'partiel')
    .sort((a, b) => (a.statut === b.statut ? 0 : a.statut === 'non_acquis' ? -1 : 1));
  const restantes = (c?.liste || []).filter((x) => x.statut === 'non_evalue');
  const acquises = (c?.liste || []).filter((x) => x.statut === 'acquis');
  const pctAcquis = c?.total ? Math.round((c.acquis * 100) / c.total) : 0;
  const completed = course.progress_status === 'completed';
  const inProgress = course.progress_status === 'in_progress';

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 p-3 backdrop-blur-sm" onClick={onClose} role="dialog" aria-modal="true" aria-label={`Détails du cours ${course.title}`}>
      <div className="flex max-h-[92vh] w-full max-w-2xl flex-col overflow-hidden rounded-3xl border border-white/10 bg-[#0e0e26] shadow-2xl" onClick={(e) => e.stopPropagation()}>
        <header className="flex items-start gap-3 border-b border-white/[0.07] p-4">
          <div className="min-w-0 flex-1">
            <span className={`rounded-md px-2 py-0.5 text-[11px] font-black ${badge}`}>{matiere}</span>
            <h2 className="mt-1.5 text-lg font-black leading-6 text-white">{course.title}</h2>
          </div>
          <button onClick={onClose} className="rounded-xl p-2 text-white/50 hover:bg-white/10 hover:text-white" aria-label="Fermer">
            <X className="h-5 w-5" />
          </button>
        </header>

        <div className="flex-1 space-y-5 overflow-y-auto overflow-x-hidden p-4">
          <section className="grid grid-cols-2 gap-2 sm:grid-cols-4">
            <Tuile Icone={Eye} libelle="Vu" valeur={`${vu} %`} detail={`${tableau?.diapos || course.slide_count} diapositives`} />
            <Tuile
              Icone={Repeat2}
              libelle="Lectures terminées"
              valeur={`${st?.terminaisons || 0}`}
              detail={inProgress ? `lecture en cours : ${course.progress_percent} %` : completed ? 'dernière lecture finie' : 'pas encore lu en entier'}
            />
            <Tuile
              Icone={Clock3}
              libelle="Temps passé"
              valeur={formatMinutes(st?.minutes || 0)}
              detail={course.estimated_minutes ? `durée du cours : ${formatMinutes(course.estimated_minutes)}` : undefined}
            />
            <Tuile Icone={Play} libelle="Séances" valeur={`${st?.ouvertures || 0}`} detail={st?.derniere ? `dernière : ${ilYA(st.derniere)}` : 'jamais ouvert'} />
          </section>

          {c && c.total > 0 && (
            <section>
              <div className="flex items-baseline justify-between gap-2">
                <h3 className="text-sm font-black text-white">Compétences</h3>
                <p className="text-xs font-bold text-white/60">{c.acquis} acquises sur {c.total} · {pctAcquis} %</p>
              </div>
              <div className="mt-2"><BarreCompetences c={c} hauteur="h-3" /></div>
              <ul className="mt-2 flex flex-wrap gap-x-4 gap-y-1 text-[11px] text-white/60">
                {STATUTS.map(({ id, label, couleur, Icone }) => (
                  <li key={id} className="inline-flex items-center gap-1.5">
                    <span className={`h-2.5 w-2.5 rounded-sm ${couleur}`} /> <Icone className="h-3 w-3 text-white/45" /> {label} : <b className="text-white/85">{c[id]}</b>
                  </li>
                ))}
              </ul>

              {lacunes.length > 0 ? (
                <div className="mt-4">
                  <h4 className="text-xs font-black uppercase tracking-wider text-rose-200/80">Tes lacunes à reprendre</h4>
                  <ul className="mt-2 space-y-1.5">
                    {lacunes.slice(0, 4).map((x) => (
                      <li key={x.id} className="rounded-xl border border-white/[0.06] bg-white/[0.03] px-3 py-2">
                        <p className="flex items-start gap-2 text-sm font-bold text-white/90">
                          {x.statut === 'non_acquis'
                            ? <XCircle className="mt-0.5 h-4 w-4 shrink-0 text-rose-300" />
                            : <CircleHelp className="mt-0.5 h-4 w-4 shrink-0 text-amber-300" />}
                          <span>{x.label} <span className="font-semibold text-white/40">· {x.statut === 'non_acquis' ? 'à revoir' : 'partielle'}</span></span>
                        </p>
                        {x.reprendre_avec.length > 0 && (
                          <p className="ml-6 mt-0.5 text-[11px] text-white/45">À reprendre avec {x.reprendre_avec.join(' puis ')}.</p>
                        )}
                      </li>
                    ))}
                  </ul>
                  {lacunes.length > 4 && (
                    <details className="mt-1.5 rounded-xl border border-white/[0.06] bg-white/[0.02] px-3 py-2">
                      <summary className="cursor-pointer text-xs font-bold text-white/70">{lacunes.length - 4} autre{lacunes.length > 5 ? 's' : ''} lacune{lacunes.length > 5 ? 's' : ''}</summary>
                      <ul className="mt-2 space-y-1 text-xs text-white/60">
                        {lacunes.slice(4).map((x) => (
                          <li key={x.id} className="flex gap-2">
                            {x.statut === 'non_acquis' ? <XCircle className="mt-0.5 h-3 w-3 shrink-0 text-rose-300" /> : <CircleHelp className="mt-0.5 h-3 w-3 shrink-0 text-amber-300" />}
                            {x.label}
                          </li>
                        ))}
                      </ul>
                    </details>
                  )}
                </div>
              ) : (c.acquis > 0 && (
                <p className="mt-3 text-xs font-semibold text-emerald-200/80">Aucune lacune pour l'instant sur les compétences évaluées.</p>
              ))}

              {restantes.length > 0 && (
                <details className="mt-3 rounded-xl border border-white/[0.06] bg-white/[0.02] px-3 py-2">
                  <summary className="cursor-pointer text-xs font-bold text-white/70">Il te reste {restantes.length} compétence{restantes.length > 1 ? 's' : ''} à travailler</summary>
                  <ul className="mt-2 space-y-1 text-xs text-white/55">
                    {restantes.map((x) => <li key={x.id} className="flex gap-2"><CircleDashed className="mt-0.5 h-3 w-3 shrink-0" /> {x.label}</li>)}
                  </ul>
                </details>
              )}
              {acquises.length > 0 && (
                <details className="mt-2 rounded-xl border border-white/[0.06] bg-white/[0.02] px-3 py-2">
                  <summary className="cursor-pointer text-xs font-bold text-white/70">{acquises.length} compétence{acquises.length > 1 ? 's' : ''} acquise{acquises.length > 1 ? 's' : ''}</summary>
                  <ul className="mt-2 space-y-1 text-xs text-white/55">
                    {acquises.map((x) => <li key={x.id} className="flex gap-2"><CheckCircle2 className="mt-0.5 h-3 w-3 shrink-0 text-emerald-300" /> {x.label}</li>)}
                  </ul>
                </details>
              )}
            </section>
          )}

          {st && st.jours.length > 0 && (
            <section>
              <div className="mb-5 flex items-baseline justify-between">
                <h3 className="text-sm font-black text-white">Temps par jour</h3>
                <p className="text-[11px] text-white/40">14 derniers jours</p>
              </div>
              <TempsParJour jours={st.jours} barre={barre} />
            </section>
          )}
        </div>

        <footer className="flex gap-2 border-t border-white/[0.07] p-3">
          <button onClick={onOpen} className="inline-flex h-10 flex-1 items-center justify-center gap-1.5 rounded-xl bg-white text-sm font-black text-indigo-950 hover:bg-cyan-50">
            <Play className="h-4 w-4 fill-current" /> {inProgress ? 'Reprendre' : completed ? 'Revoir' : 'Commencer'}
          </button>
          <button onClick={onAskTutor} className="inline-flex h-10 items-center gap-1.5 rounded-xl border border-white/10 bg-white/[0.04] px-3 text-xs font-bold text-white/70 hover:bg-white/[0.08] hover:text-white">
            <MessageCircle className="h-4 w-4" /> Demander à Moalim
          </button>
        </footer>
      </div>
    </div>
  );
}
