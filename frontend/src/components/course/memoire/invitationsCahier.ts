import type { ReactionPreparee } from '../types';

/**
 * Ce que le tuteur dit quand le cours s'arrête pour le cahier (14 novembre 2026, demande de l'utilisateur) : en
 * darija, il invite l'élève à écrire les notions dans son cahier, dit pourquoi (écrire à la main ancre la notion,
 * la fait passer en mémoire longue ; bien écrire, avec le schéma ; revenir le relire de temps en temps). Une phrase
 * différente à chaque fois : on ne redit pas l'une des dernières entendues (mémorisées dans le navigateur).
 *
 * Voix : pistes Bodi `/media/audio/reactions/cahier-N.mp3` quand elles existent (`AVEC_PISTE`, rempli après la
 * génération sur le serveur, dossier `/srv/corpus_v4/voix_lot/_cahier_invitations`) ; sinon la voix en direct dit
 * le texte. Règles de la voix : darija en lettres arabes, mots du programme en français, pas de chiffres ni de tachkil.
 */
const PHRASES: string[] = [
  'دابا نوقفو شوية. خرج le cahier ديالك وكتب هاد الأفكار بيدك، حيت اللي كتكتبو بيدك كيبقى فالراس كثر من اللي غير كتقراه.',
  'مزيان، وصلنا لوقت الكتابة. كتب هادشي فle cahier بخط نقي، باش يبقى le cahier organisé، وملي ترجع ليه من بعد، تفهمو بلا تعب.',
  'قبل ما نكملو، كتب هاد les notions فle cahier. الكتابة كتثبت المعلومة، وكتخليها تدوز من الذاكرة القصيرة للذاكرة الطويلة.',
  'دابا دورك. كتب هاد الأسطر فle cahier ديالك، وخلي شي بلاصة باش تزيد ملاحظاتك. ومن بعد، رجع ليهم من وقت لوقت.',
  'خود وقتك وكتب مزيان. اللي كنكتبوه بيدنا كنحفظوه كثر، وle cahier organisé غادي يعاونك بزاف فالمراجعة ديال الامتحان.',
  'واخا، دابا كتب هاد الملخص فle cahier. ما تكتبش بالزربة، ركز فكل كلمة، حيت هادي هي الطريقة باش تبقى عندك المعلومة.',
  'هادشي اللي شفنا مهم بزاف. كتبو فle cahier ديالك، ومن بعد شي أيام عاود قراه، هكا كيتثبت فالذاكرة ديالك.',
  'خلي الشاشة على جنب شوية، وكتب فle cahier هاد les notions و le schéma. ملي كترسم وكتكتب بيدك، الفهم ديالك كيولي أقوى.',
  'دابا الكتابة. كتب بالترتيب، العنوان، من بعد الأفكار، من بعد le schéma. le cahier organisé هو أحسن صاحب ليك نهار الامتحان.',
  'باش ما تنساش داكشي اللي خدينا، خاصنا نكتبوه. كتب فle cahier ديالك، ومن وقت لوقت رجع ليه وقراه، غير خمس دقايق كافيين.',
  'مزيان بزاف، دابا وقت le cahier. الكتابة ماشي غير نقل، هي طريقة باش الدماغ يخزن المعلومة ويلقاها ملي تحتاجها.',
  'قبل ما ندوزو للي من بعد، كتب هاد الأفكار ورسم le schéma فle cahier. ومن بعد، ملي تراجع، غادي تلقى كلشي واضح قدامك.',
];

/** Les phrases qui ont déjà leur piste Bodi (numéros à partir de 1) : les 12, générées le 14 novembre 2026. */
const AVEC_PISTE = new Set<number>([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]);

const CLE = 'moalim.invitationsCahier';
/** On ne redit pas l'une des N dernières : avec 12 phrases, l'élève en entend 8 autres avant qu'une revienne. */
const MEMOIRE = 8;

export const INVITATIONS_CAHIER = PHRASES;

export function invitationCahier(): ReactionPreparee {
  let recentes: number[] = [];
  try { recentes = JSON.parse(localStorage.getItem(CLE) || '[]'); } catch { /* navigateur sans stockage */ }
  const libres = PHRASES.map((_, i) => i).filter(i => !recentes.includes(i));
  const i = (libres.length ? libres : PHRASES.map((_, k) => k))[Math.floor(Math.random() * (libres.length || PHRASES.length))];
  try { localStorage.setItem(CLE, JSON.stringify([i, ...recentes].slice(0, MEMOIRE))); } catch { /* idem */ }
  const n = i + 1;
  return { parole: PHRASES[i], ecrit: '', audio: AVEC_PISTE.has(n) ? `/media/audio/reactions/cahier-${n}.mp3` : undefined };
}
