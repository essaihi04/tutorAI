/**
 * Émotions du professeur animé, déduites de ce que disent le tuteur et l'élève.
 *
 * Chaque émotion donne un geste du personnage et des émoticônes qui s'envolent de lui :
 * - `greet`     : coucou de la main, 👋 — un message qui commence par « Bonjour », « Salut », « Salam »…
 * - `goodbye`   : coucou de la main, 👋🌟 — « Au revoir », « À bientôt », « Bslama »…
 * - `celebrate` : bras levés, 🎉⭐✨👏 — « Bravo », « Excellent », « Mabrouk »…
 * - `love`      : mains sur le cœur, ❤️💖💕 — « Fier de toi », « Je t'adore », un ❤️ ; un « Merci » de l'élève.
 * - `encourage` : hochement de tête, 💪👍 — « Presque », « Réessaie », « Courage »…
 * - `laugh`     : rire (le corps saute, la moustache tremble), 😂🤣😄 — « Haha », « C'est drôle », « Mdr »…
 * - `surprise`  : sursaut, sourcils hauts, mains levées, 😮❗✨ — « Oh ! », « Incroyable », « Waouh »…
 * - `think`     : 🤔 — quand le tuteur réfléchit vraiment (traitement de plus de 1,5 s), pas aux mots.
 * - `wrong`     : tête qui dit non et index qui balance, 🤔💡 — une réponse fausse (exercice du tableau,
 *                 vérification d'un laboratoire, ou `<eval>faux</eval>` déclaré par le tuteur) ; jamais aux mots.
 */
export const PROFESSOR_EMOTIONS = {
  greet: { gesture: 'wave', emojis: ['👋', '😊'], count: 3 },
  goodbye: { gesture: 'wave', emojis: ['👋', '🌟'], count: 3 },
  celebrate: { gesture: 'cheer', emojis: ['🎉', '⭐', '✨', '👏'], count: 8 },
  love: { gesture: 'heart', emojis: ['❤️', '💖', '💕'], count: 7 },
  encourage: { gesture: 'nod', emojis: ['💪', '👍'], count: 4 },
  laugh: { gesture: 'laugh', emojis: ['😂', '🤣', '😄'], count: 6 },
  surprise: { gesture: 'startle', emojis: ['😮', '❗', '✨'], count: 4 },
  think: { gesture: null, emojis: ['🤔'], count: 1 },
  wrong: { gesture: 'shake', emojis: ['🤔', '💡'], count: 3 },
};

const APOSTROPHE = "['’]";
const TUTOR_RULES = [
  ['celebrate', new RegExp(`\\b(bravo|excellent|f[ée]licitations?|parfait|g[ée]nial|bien jou[ée]|tr[eè]s bien|exactement|c${APOSTROPHE}est (ça|exact|juste)|mabrou?k|tbarkallah|wa3er)\\b|🎉|👏|🥳`, 'i')],
  ['love', new RegExp(`\\b(je t${APOSTROPHE}adore|je vous adore|fi[eè]re? de (toi|vous)|je t${APOSTROPHE}aime|avec amour|de tout c(œ|oe)ur|mon (petit )?champion|ma (petite )?championne|tu es (formidable|brillante?|g[ée]niale?))\\b|❤|💖|💕|🥰|😍`, 'i')],
  ['laugh', new RegExp(`\\b(ha ?ha|hihi|h[ée]h[ée])|\\b(mdr|lol|c${APOSTROPHE}est dr[ôo]le|rigolo|une blague|je plaisante)\\b|😂|🤣|😄|😆`, 'i')],
  ['surprise', /\b(oh ?!|oh l[àa] l[àa]|incroyable|surprenant|[ée]tonnant|tiens ?!|waouh|wow|ouah|pas possible|quelle surprise)|😮|😲|🤯/i],
  ['encourage', new RegExp(`\\b(pas tout [àa] fait|presque|r[ée]essaie|essaie encore|encore un effort|ne t${APOSTROPHE}inqui[èe]te pas|t${APOSTROPHE}inqui[èe]te pas|pas grave|tu (y )?(peux|vas y arriver)|on continue|courage|tu progresses)\\b|💪|👍`, 'i')],
  ['goodbye', /\b(au revoir|[àa] bient[ôo]t|bonne (journ[ée]e|soir[ée]e|chance|continuation)|[àa] la prochaine|bslama|bye)\b/i],
  ['greet', /^\W*(bonjour|salut|bienvenue|bonsoir|coucou|hello|ahlan|salam|ssalam|marhba)\b|👋/i],
];
const STUDENT_RULES = [
  ['love', new RegExp(`\\b(merci|chokran|choukran|thanks|je t${APOSTROPHE}adore|je vous adore)\\b|❤|🥰`, 'i')],
  ['greet', /^\W*(bonjour|salut|bonsoir|coucou|hello|ahlan|salam|ssalam|marhba)\b/i],
  ['goodbye', /\b(au revoir|[àa] bient[ôo]t|bye|bslama)\b/i],
  ['laugh', /\b(ha ?ha|hihi)|\b(mdr|lol|ptdr)\b|😂|🤣|😄/i],
  ['surprise', /\b(wow|waouh|ouah|s[ée]rieux ?\?|pas possible)\b|😮|😲|🤯/i],
];

/** Événement émis quand l'élève répond à un exercice du tableau. */
export const REPONSE_ELEVE_EVENT = 'moalim:reponse-eleve';

/**
 * L'élève vient de répondre à un exercice (QCM, vrai/faux) ou de vérifier une
 * mesure dans un laboratoire : le professeur réagit — il applaudit une bonne
 * réponse, il fait non de la tête puis encourage après une erreur.
 * Les exercices vivent au fond du tableau ; un événement de fenêtre leur évite
 * de faire remonter une callback à travers tous les composants.
 * @param {boolean} juste
 */
export function signalerReponseEleve(juste) {
  if (typeof window === 'undefined') return;
  window.dispatchEvent(new CustomEvent(REPONSE_ELEVE_EVENT, { detail: { juste: !!juste } }));
}

/**
 * @param {string} text
 * @param {'ai' | 'student'} speaker
 * @returns {keyof typeof PROFESSOR_EMOTIONS | null}
 */
/** Réaction du professeur à une réponse jugée : bravo si juste, non de la tête sinon. */
export function emotionPourReponse(juste) { return juste ? 'celebrate' : 'wrong'; }

/**
 * Réaction déclarée par le tuteur dans sa balise <eval> (serveur → `professor_reaction`).
 * @param {string} evaluation  correct | partiel | faux | incertain | aucune
 * @returns {keyof typeof PROFESSOR_EMOTIONS | null}
 */
export function emotionPourEvaluation(evaluation) {
  const e = String(evaluation || '').toLowerCase();
  if (e === 'correct') return 'celebrate';
  if (e === 'faux') return 'wrong';
  if (e === 'partiel') return 'encourage';
  return null;
}

export function detectProfessorEmotion(text, speaker = 'ai') {
  const content = String(text || '');
  if (!content.trim()) return null;
  for (const [kind, rule] of speaker === 'student' ? STUDENT_RULES : TUTOR_RULES) {
    if (rule.test(content)) return kind;
  }
  return null;
}
