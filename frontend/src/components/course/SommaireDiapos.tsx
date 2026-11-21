import { useEffect, useRef } from 'react';
import type { CourseActivity, CourseSlide } from './types';

/**
 * Le plan du cours, comme le mode « trieuse » de PowerPoint (demande de l'utilisateur, 21 novembre 2026 : « un bouton
 * qui affiche toutes les diapos avec le titre petit de chaque diapo, bien organisé, cliquer sur une et aller vite »).
 * Les diapositives sont groupées par partie du cours, numérotées dans l'ordre ; la diapo courante est encadrée, celles
 * déjà vues portent ✓. Un clic y va directement ; Échap, × ou le fond ferment sans rien changer.
 * Tient sur un téléphone en paysage (~724×350) : la grille défile verticalement, jamais en largeur.
 */
export type DiapoDuSommaire = { activity: CourseActivity; activityIndex: number; slide: CourseSlide };

type Props = {
  diapos: DiapoDuSommaire[];
  courante: number;
  vues: string[];
  onChoisir: (index: number) => void;
  onFermer: () => void;
};

export default function SommaireDiapos({ diapos, courante, vues, onChoisir, onFermer }: Props) {
  const couranteRef = useRef<HTMLButtonElement | null>(null);

  useEffect(() => {
    couranteRef.current?.scrollIntoView({ block: 'center' });
    couranteRef.current?.focus({ preventScroll: true });
    const touche = (e: KeyboardEvent) => { if (e.key === 'Escape') onFermer(); };
    window.addEventListener('keydown', touche);
    return () => window.removeEventListener('keydown', touche);
  }, [onFermer]);

  // groupes = parties du cours (activités), dans l'ordre ; l'index global de chaque diapo est gardé pour y aller
  const groupes: { titre: string; numero: number; items: { diapo: DiapoDuSommaire; index: number }[] }[] = [];
  diapos.forEach((diapo, index) => {
    const dernier = groupes[groupes.length - 1];
    if (dernier && dernier.numero === diapo.activityIndex) dernier.items.push({ diapo, index });
    else groupes.push({ titre: diapo.activity.title || `Partie ${diapo.activityIndex + 1}`, numero: diapo.activityIndex, items: [{ diapo, index }] });
  });
  const vuesSet = new Set(vues);

  return (
    <div data-sommaire-diapos role="dialog" aria-modal="true" aria-label="Toutes les diapositives"
      className="absolute inset-0 z-[140] flex flex-col bg-[#050b14]/95 backdrop-blur-sm"
      onClick={onFermer}>
      <div className="flex shrink-0 items-center gap-3 border-b border-white/10 px-4 py-2 court:py-1" onClick={e => e.stopPropagation()}>
        <h2 className="text-sm font-semibold text-white/90">Toutes les diapositives</h2>
        <span className="text-xs tabular-nums text-white/45">{courante + 1} / {diapos.length}</span>
        <button onClick={onFermer} title="Fermer (Échap)" aria-label="Fermer"
          className="ml-auto h-8 w-8 rounded-full text-lg leading-none text-white/80 hover:bg-white/10">×</button>
      </div>
      <div className="min-h-0 flex-1 overflow-y-auto overflow-x-hidden px-4 py-3 court:px-2 court:py-2">
        {groupes.map(g => (
          <section key={`${g.numero}-${g.items[0].index}`} className="mb-4 court:mb-2" onClick={e => e.stopPropagation()}>
            <h3 className="mb-2 truncate text-xs font-semibold uppercase tracking-wide text-cyan-200/80 court:mb-1">
              {g.numero + 1}. {g.titre}
            </h3>
            <div className="grid gap-2 [grid-template-columns:repeat(auto-fill,minmax(150px,1fr))] court:gap-1.5 court:[grid-template-columns:repeat(auto-fill,minmax(130px,1fr))]">
              {g.items.map(({ diapo, index }) => {
                const estCourante = index === courante;
                const vue = vuesSet.has(diapo.slide.id);
                const titre = diapo.slide.title?.trim() || `Diapositive ${index + 1}`;
                return (
                  <button key={diapo.slide.id} ref={estCourante ? couranteRef : undefined}
                    onClick={() => onChoisir(index)} title={titre} aria-current={estCourante ? 'true' : undefined}
                    className={`flex min-h-16 min-w-0 flex-col items-start gap-0.5 rounded-lg border px-2 py-1.5 text-left transition-colors court:min-h-0 court:py-1 ${
                      estCourante
                        ? 'border-cyan-400 bg-cyan-500/20 ring-1 ring-cyan-400'
                        : 'border-white/10 bg-white/[0.04] hover:border-white/30 hover:bg-white/10'}`}>
                    <span className="flex w-full items-center gap-1 text-[10px] tabular-nums text-white/45">
                      {index + 1}
                      {vue && !estCourante && <span className="text-emerald-300/80" aria-label="déjà vue">✓</span>}
                      {estCourante && <span className="ml-auto text-cyan-200">ici</span>}
                    </span>
                    <span className="line-clamp-2 w-full break-words text-xs leading-snug text-white/90">{titre}</span>
                  </button>
                );
              })}
            </div>
          </section>
        ))}
      </div>
    </div>
  );
}
