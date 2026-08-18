/**
 * Déblocage du son — une fois pour toute l'application.
 *
 * Chrome (et Safari, plus strictement encore) refuse tout son tant que la page
 * n'a pas reçu de geste de l'élève. Or le professeur parle DE LUI-MÊME dès
 * l'ouverture d'une session : aucun clic n'a eu lieu sur la page de cours, et
 * la voix partait en silence — d'où la bannière « clique pour activer le son ».
 *
 * Le geste existe pourtant presque toujours : l'élève a cliqué pour se
 * connecter, puis sur sa leçon. C'est le MÊME document (l'application est une
 * SPA), donc l'autorisation est déjà acquise — il suffisait de la saisir au
 * moment où elle passe, pas d'attendre un clic supplémentaire sur l'écran de
 * cours. Ce service s'installe donc au démarrage de l'application, bien avant
 * la session, et garde l'`AudioContext` partagé « running » pour toute la
 * durée de la visite.
 *
 * Conséquence : dans le parcours normal (login → tableau de bord → leçon), la
 * bannière ne s'affiche plus jamais, et le son part tout seul dès le départ.
 * Elle ne reste utile que sur un accès direct à l'URL d'une session suivi d'un
 * rechargement, où réellement aucun geste n'a encore eu lieu.
 */

type Ecouteur = () => void;

/** Safari expose encore l'AudioContext sous son nom prefixe. */
type FenetreAudio = Window & { webkitAudioContext?: typeof AudioContext };

/** Activation « collante » du document : elle survit a la navigation SPA. */
type NavigateurActivation = Navigator & {
  userActivation?: { hasBeenActive: boolean; isActive: boolean };
};

// Les gestes qui accordent l'autorisation. `pointerdown` couvre souris et
// tactile sur les navigateurs récents ; les autres sont là pour les anciens.
const GESTES = ['pointerdown', 'mousedown', 'touchstart', 'keydown', 'click'] as const;

// WAV d'un seul échantillon muet. Safari n'accorde l'autorisation qu'à un
// `play()` lancé DANS le geste : ce son sans contenu suffit à l'obtenir.
const WAV_MUET =
  'data:audio/wav;base64,UklGRiQAAABXQVZFZm10IBAAAAABAAEAgD4AAAB9AAACABAAZGF0YQAAAAA=';

class AudioUnlock {
  private ctx: AudioContext | null = null;
  private installe = false;
  private gesteVu = false;
  private abonnes = new Set<Ecouteur>();

  /**
   * Écoute le premier geste de l'élève, où qu'il se produise dans
   * l'application. Idempotent : appelable depuis plusieurs points d'entrée.
   */
  installer() {
    if (this.installe || typeof window === 'undefined') return;
    this.installe = true;
    GESTES.forEach((g) =>
      window.addEventListener(g, this.surGeste, { capture: true, passive: true }),
    );
  }

  private surGeste = () => {
    this.gesteVu = true;
    if (!this.ctx || this.ctx.state !== 'running') {
      // Safari : l'autorisation ne s'obtient qu'ici, pendant le geste.
      try {
        const muet = new Audio(WAV_MUET);
        muet.volume = 0;
        void muet.play().catch(() => {});
      } catch {
        /* pas de son muet possible : le geste seul suffit sur Chrome */
      }
    }
    void this.ensureRunning().then(() => this.notifier());
  };

  private notifier() {
    // Copie : un abonné peut se désabonner depuis son propre rappel.
    [...this.abonnes].forEach((cb) => {
      try { cb(); } catch { /* un abonné fautif n'empêche pas les autres */ }
    });
  }

  /** L'AudioContext partagé de l'application (`null` si non pris en charge). */
  context(): AudioContext | null {
    if (this.ctx) return this.ctx;
    const Ctor = window.AudioContext || (window as FenetreAudio).webkitAudioContext;
    if (!Ctor) return null;
    this.ctx = new Ctor();
    return this.ctx;
  }

  /** Un geste a-t-il déjà eu lieu dans ce document ? */
  get activationPresente(): boolean {
    if (this.gesteVu) return true;
    // Chrome expose l'activation « collante » : elle survit à la navigation
    // interne de la SPA, donc au clic qui a ouvert la session.
    const ua = (navigator as NavigateurActivation).userActivation;
    return Boolean(ua && (ua.hasBeenActive || ua.isActive));
  }

  /** Le son peut-il sortir maintenant ? */
  get pret(): boolean {
    const ctx = this.ctx;
    if (ctx) return ctx.state === 'running';
    return this.activationPresente;
  }

  /**
   * Tente de remettre le contexte en marche. Renvoie `true` seulement si le
   * son peut RÉELLEMENT sortir — c'est cette réponse, et non l'absence de
   * geste, qui doit décider d'afficher la bannière.
   */
  async ensureRunning(): Promise<boolean> {
    const ctx = this.context();
    if (!ctx) return this.activationPresente;
    // Relu à travers une fonction : `resume()` change l'état sous les pieds du
    // compilateur, qui sinon le croit encore figé sur « suspended ».
    const etat = (): string => ctx.state;
    if (etat() === 'running') return true;
    try {
      await ctx.resume();
    } catch {
      /* refusé : le prochain geste réessaiera */
    }
    return etat() === 'running';
  }

  /** Prévient dès que le son est débloqué. Renvoie la fonction de retrait. */
  onUnlock(cb: Ecouteur): () => void {
    this.abonnes.add(cb);
    return () => this.abonnes.delete(cb);
  }

  /**
   * Attend le déblocage, au plus `timeoutMs`. Utilisé par les lecteurs qui
   * peuvent patienter un instant plutôt que d'abandonner leur fragment.
   */
  attendreDeblocage(timeoutMs = 5000): Promise<boolean> {
    if (this.pret) return Promise.resolve(true);
    return new Promise((resolve) => {
      let fini = false;
      const finir = (ok: boolean) => {
        if (fini) return;
        fini = true;
        retirer();
        clearTimeout(minuteur);
        resolve(ok);
      };
      const minuteur = setTimeout(() => finir(this.pret), timeoutMs);
      const retirer = this.onUnlock(() => { if (this.pret) finir(true); });
    });
  }
}

export const audioUnlock = new AudioUnlock();

// Installation immédiate : le module est importé au démarrage de
// l'application, donc l'écoute commence avant le premier écran.
audioUnlock.installer();
