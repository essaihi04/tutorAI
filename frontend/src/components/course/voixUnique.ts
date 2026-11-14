/**
 * Une seule voix à la fois (règle utilisateur, 14 novembre 2026 — « j'ai cliqué sur la question, l'audio de
 * l'explication reste et s'ajoute à l'audio de la question ») : la voix entendue est toujours celle de l'écran qui
 * vient d'apparaître. Chaque lecteur audio du cours (piste de la diapo, voix du tuteur, voix du cycle de mémoire)
 * s'inscrit ici ; dès que l'un démarre, tous les autres se taisent, et chacun est prévenu (`coupe`) pour remettre
 * son état d'aplomb (la piste de la diapo se note « en pause » et reprendra quand l'écran se refermera).
 */
type Inscrit = { el: HTMLMediaElement; coupe?: () => void };
const inscrits = new Set<Inscrit>();

/** Inscrit un lecteur ; rend la fonction qui le désinscrit. */
export function inscrireVoix(el: HTMLMediaElement, coupe?: () => void): () => void {
  const moi: Inscrit = { el, coupe };
  const surPlay = () => {
    for (const autre of inscrits) {
      if (autre === moi || autre.el.paused) continue;
      autre.el.pause();
      autre.coupe?.();
    }
  };
  el.addEventListener('play', surPlay);
  inscrits.add(moi);
  return () => { el.removeEventListener('play', surPlay); inscrits.delete(moi); };
}

/** Fait taire tous les lecteurs inscrits (un écran se ferme, le cours s'arrête). */
export function taireTout(): void {
  for (const i of inscrits) if (!i.el.paused) { i.el.pause(); i.coupe?.(); }
}
