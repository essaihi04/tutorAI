/**
 * Le tableau explique-t-il en ce moment ?
 *
 * Le professeur ne passait en « parle » que lorsque la voix du chat jouait. Pendant un cours au tableau,
 * la voix est celle du tableau, et quand la voix serveur est indisponible il écrit en silence : le
 * professeur restait alors bras ballants, « Prêt à t'aider », pendant toute l'explication. Le tableau
 * signale donc son script en cours (lecture, ni terminée ni en attente d'une réponse), avec ou sans voix,
 * et le professeur explique avec ses mains tout ce temps-là.
 */
class BoardExplaining {
  constructor() {
    this.holders = 0;
    /** @type {Set<(explaining: boolean) => void>} */
    this.listeners = new Set();
  }

  /** Le tableau commence à expliquer ; la fonction rendue l'arrête (idempotente). */
  /** @returns {() => void} */
  begin() {
    this.holders += 1;
    if (this.holders === 1) this.emit();
    let released = false;
    return () => {
      if (released) return;
      released = true;
      this.holders = Math.max(0, this.holders - 1);
      if (this.holders === 0) this.emit();
    };
  }

  get active() {
    return this.holders > 0;
  }

  /** @param {(explaining: boolean) => void} fn */
  subscribe(fn) {
    this.listeners.add(fn);
    return () => { this.listeners.delete(fn); };
  }

  emit() {
    const value = this.holders > 0;
    this.listeners.forEach(listener => { try { listener(value); } catch { /* un abonné fautif n'arrête pas les autres */ } });
  }
}

export const boardExplaining = new BoardExplaining();
