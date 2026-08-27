/**
 * Qui a la parole : le tableau, ou le chat ?
 *
 * Deux voix cohabitent dans une séance et ne se connaissent pas :
 *  • celle du TABLEAU (`boardVoice`), qui lit ligne à ligne ce qui s'écrit ;
 *  • celle du CHAT (flux `audio_chunk` / PCM du serveur), qui lit la réponse
 *    du professeur.
 *
 * Le tableau attendait le silence AVANT de démarrer, mais rien ne l'empêchait
 * ensuite : la synthèse du chat arrive plusieurs secondes plus tard, et les
 * deux voix se superposaient — la même leçon, dite deux fois autrement. Une
 * seule règle désormais : **tant que le tableau parle, il a la parole**, et
 * l'audio du chat est écarté pour ce tour.
 *
 * Le tableau ne prend la parole qu'au moment où un son sort RÉELLEMENT de ses
 * haut-parleurs. Si la voix serveur est indisponible, il écrit en silence et
 * laisse le chat parler : l'élève n'est jamais privé des deux.
 */

type Listener = (tableauParle: boolean) => void;

class VoiceFloor {
  /** Nombre de prises en cours (script + réplique courante). */
  private prises = 0;
  private listeners = new Set<Listener>();

  /**
   * Le tableau prend la parole. La fonction rendue la relâche — elle est
   * idempotente : l'appeler deux fois ne libère pas la parole d'un autre.
   */
  acquire(): () => void {
    this.prises += 1;
    if (this.prises === 1) this.emit();
    let relache = false;
    return () => {
      if (relache) return;
      relache = true;
      this.prises = Math.max(0, this.prises - 1);
      if (this.prises === 0) this.emit();
    };
  }

  /** Le tableau parle-t-il en ce moment ? */
  get tableauParle(): boolean {
    return this.prises > 0;
  }

  subscribe(fn: Listener): () => void {
    this.listeners.add(fn);
    return () => { this.listeners.delete(fn); };
  }

  /** Filet de sécurité : fin de séance, démontage de la page. */
  reset(): void {
    if (this.prises === 0) return;
    this.prises = 0;
    this.emit();
  }

  private emit(): void {
    const valeur = this.prises > 0;
    this.listeners.forEach((l) => { try { l(valeur); } catch { /* noop */ } });
  }
}

export const voiceFloor = new VoiceFloor();
