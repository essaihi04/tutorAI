/**
 * Réaction immédiate du professeur.
 *
 * La vraie réponse demande 4 à 6 s (le LLM écrit, puis la voix se calcule
 * sur le GPU Kaggle) : un silence que personne ne prend pour une conversation.
 * Dès que l'élève envoie son message, le professeur dit donc une courte
 * phrase déjà enregistrée avec sa voix (« مزيان، سؤال زوين », « Voyons ta
 * réponse »), et la réponse s'enchaîne derrière elle.
 *
 * Les phrases, leurs textes et leurs fichiers sont décrits par
 * /media/audio/reactions/manifest.json (généré par
 * `python -m scripts.kaggle_tts reactions`). Sans manifeste, rien ne se passe.
 */

export type CategorieReaction = 'question' | 'reponse';
export type LangueReaction = 'mixed' | 'fr';

interface Reaction {
  id: string;
  cat: CategorieReaction;
  lang: LangueReaction;
  texte: string;
  url: string;
}

const MANIFESTE = '/media/audio/reactions/manifest.json';
let reactions: Reaction[] = [];
const sons = new Map<string, AudioBuffer>();
let chargement: Promise<void> | null = null;
const dernieres: string[] = [];

/** Charge et décode une fois toutes les réactions : à l'usage, zéro attente. */
export function prechargerReactions(ctx: AudioContext): Promise<void> {
  if (chargement) return chargement;
  chargement = (async () => {
    try {
      const r = await fetch(MANIFESTE, { cache: 'force-cache' });
      if (!r.ok) return;
      const donnees = await r.json();
      reactions = Array.isArray(donnees?.reactions) ? donnees.reactions : [];
      await Promise.all(reactions.map(async (reaction) => {
        try {
          const audio = await fetch(reaction.url, { cache: 'force-cache' });
          if (!audio.ok) return;
          sons.set(reaction.id, await ctx.decodeAudioData(await audio.arrayBuffer()));
        } catch { /* une réaction manquante n'empêche pas les autres */ }
      }));
    } catch {
      chargement = null;   // réessayer à la prochaine séance
    }
  })();
  return chargement;
}

const LETTRE_ARABE = /[؀-ۿ]/g;
const LETTRE_LATINE = /[A-Za-zÀ-ÿ]/g;
const INTERROGATION = /[?؟]|\b(comment|pourquoi|qu['’]est|c['’]est quoi|explique|expliquer|peux[- ]tu|je comprends pas|j['’]ai pas compris|quelle?s?|quand|combien)\b|كيفاش|علاش|شنو|اشنو|واش|فين|شحال|اشرح|شرح|ما فهمتش|مافهمتش|عاود/i;

/** Même règle que le backend (bloc_langue_du_tour) : l'alphabet arabe décide. */
export function langueDe(texte: string): LangueReaction {
  const arabe = (texte.match(LETTRE_ARABE) || []).length;
  const latin = (texte.match(LETTRE_LATINE) || []).length;
  return arabe > 0 && arabe >= latin * 0.5 ? 'mixed' : 'fr';
}

export function categorieDe(texte: string): CategorieReaction {
  return INTERROGATION.test(texte) ? 'question' : 'reponse';
}

/**
 * Choisit la réaction (son décodé + texte), sans redire l'une des trois
 * dernières. `null` si rien n'est prêt — la page reste alors silencieuse,
 * comme avant.
 */
export function choisirReaction(texteEleve: string): { texte: string; son: AudioBuffer } | null {
  const texte = (texteEleve || '').trim();
  if (!texte) return null;
  const cat = categorieDe(texte);
  const lang = langueDe(texte);
  const candidates = reactions.filter((r) => r.cat === cat && r.lang === lang && sons.has(r.id));
  if (!candidates.length) return null;
  const fraiches = candidates.filter((r) => !dernieres.includes(r.id));
  const pool = fraiches.length ? fraiches : candidates;
  const choisie = pool[Math.floor(Math.random() * pool.length)];
  dernieres.push(choisie.id);
  if (dernieres.length > 3) dernieres.shift();
  return { texte: choisie.texte, son: sons.get(choisie.id) as AudioBuffer };
}
