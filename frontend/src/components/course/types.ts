import type { ScientificVisualSpec } from '../session/scientific/types';
import type { QuestionMemoire, SeanceCours } from './memoire/api';
import type { FigureCahierData } from './FigureCahier';

export type CourseSlideType =
  | 'diagnostic'
  | 'situation'
  | 'concept'
  | 'image'
  | 'schema'
  | 'simulation'
  | 'exercise'
  | 'synthesis'
  | 'evaluation';

export interface CourseQuestion extends EnonceLu {
  type?: 'qcm' | 'prediction' | 'true_false' | 'select' | 'open' | 'ordering' | 'association';
  prompt?: string;
  options?: string[];
  timeout_seconds?: number;
  advance_on_timeout?: boolean;
  /** Index de la bonne option (mode concentration : correction immédiate et réaction préparée). */
  correct?: number;
  /** Calcul ou raisonnement : la démonstration écrite à la main au tableau, après la réaction. */
  demonstration?: Demonstration;
  /**
   * Question de PRÉDICTION (11 novembre 2026, mode concentration) : posée AVANT la voix d'explication ; la voix
   * et la simulation montrent ensuite la réponse, la question n'est pas reposée après. Une prédiction fausse
   * n'est pas une erreur de compétence (suivi des acquis : `type: 'prediction'`, hors score).
   */
  prediction?: boolean;
  /**
   * `type: 'association'` (19 novembre 2026, demande de l'utilisateur : « pour les questions d'association, ne pas les
   * transformer en QCM ; les mettre en association avec un feedback à chaque réponse, correcte ou fausse »). Une
   * question « Reliez… / Associez… / Recopiez les couples… » du national reste UNE association : l'élève relie lui-même
   * (glisser d'une colonne à l'autre, ou toucher deux éléments), chaque paire formée reçoit tout de suite son retour,
   * écrit et dit, puis le bilan des couples comme le barème les attend. Voir `AssociationDiapo`.
   */
  association?: AssociationQuestion;
  /** (20 novembre 2026) Codons de l'ARNm dont l'élève doit lire l'acide aminé : un extrait du tableau du code génétique
   *  s'affiche à côté de la question (`TableauCode`), comme le petit tableau donné dans le sujet. */
  tableau_code?: string[];
}

/** Un élément d'une colonne : `id` est l'étiquette du sujet (« 1 », « a »…), montrée devant le texte. */
export interface ElementAssociation { id: string; texte: string }

/** Le retour d'une paire formée : écrit sous les colonnes, dit par la voix (`audio` : la piste préparée, sinon `dit`). */
export interface RetourPaire {
  /** facultatif : sinon déduit de `couples` */
  juste?: boolean;
  texte: string;
  dit?: string;
  audio?: string;
}

export interface AssociationQuestion {
  /** la colonne de gauche, dans l'ordre du sujet */
  gauche: ElementAssociation[];
  /** la colonne de droite ; peut avoir des éléments de trop (l'intrus du sujet) */
  droite: ElementAssociation[];
  /** les bonnes paires : id de gauche → id de droite, ex. `{"1": "c", "2": "e"}` */
  couples: Record<string, string>;
  /**
   * Les retours, par paire `"<gauche>-<droite>"` (ex. `"1-c"`). Une paire fausse sans retour à elle prend celui de son
   * élément de gauche, `"<gauche>-*"` (ce qui ne va pas + un indice, jamais la réponse). Une paire juste sans retour : « Juste ».
   */
  retours?: Record<string, RetourPaire>;
  /** `false` : la colonne de droite garde l'ordre du sujet ; par défaut elle est battue (les étiquettes restent). */
  melanger?: boolean;
  /** Erreurs permises sur un même élément de gauche avant que la bonne paire soit donnée, avec son retour (défaut 2). */
  essais?: number;
  /** Le bilan dit et écrit à la fin, après la ligne des couples « (1 ; c) (2 ; e) … » écrite d'office. */
  bilan?: { texte?: string; dit?: string; audio?: string };
}

/**
 * Ce qui accompagne l'énoncé d'une question (12 novembre 2026), sur `question`, sur un exercice (et chacune de ses
 * affirmations), sur le « retrouver » et l'exercice d'un bloc, sur un rappel :
 *  - le tuteur LIT l'énoncé quand la question s'ouvre : `enonce_audio` (piste préparée, voix Bodi, même forme que les
 *    autres pistes `audio` : l'URL du son), sinon `enonce_dit` (le texte à dire, sans symboles : « lim de x carré… »)
 *    par la voix en direct, sinon l'énoncé écrit passé par la normalisation de la voix (serveur, `normalize_for_speech`) ;
 *  - `clavier` : les suggestions du clavier scientifique pour CETTE question (aides justes et pièges plausibles, jamais
 *    la formule complète ni la réponse) ; sans elles, le serveur les génère (`/course-player/clavier-suggestions`).
 */
export interface EnonceLu {
  enonce_audio?: string;
  enonce_dit?: string;
  clavier?: { aides?: string[]; pieges?: string[] };
}

/**
 * La démonstration manuscrite d'une question qui demande un calcul ou un raisonnement (user rule, 10 novembre 2026).
 * Une fois l'élève a répondu et entendu la réaction, le tableau des questions l'écrit ligne par ligne pendant que le
 * tuteur la dit ; chaque ligne apparaît quand la voix atteint son `mot` (extrait exact de `parole`, sa place dans le
 * texte × la durée de la piste, comme `concentration.centre`). `audio` : la piste de la voix du cours ; sans piste,
 * `parole` est dite par la voix en direct, par morceaux. Puis le carrousel passe seul à la question suivante.
 */
export interface Demonstration {
  /** Le texte dit (règles de la voix : darija simple, nombres et unités en mots, aucun symbole). */
  parole: string;
  /** Les lignes écrites comme le barème les lit : relation, substitution, résultat avec unité (`y_M` → M en indice). */
  lignes: LigneDemonstration[];
  /** La piste de `parole` (voix du cours), si elle est déjà calculée. */
  audio?: string;
  /**
   * `false` : la démonstration garde son tableau à part même quand la diapositive a une figure. Par défaut (18 novembre
   * 2026, simulations-au-tableau règle 17), une diapositive avec une simulation ou une image joue la démonstration SUR
   * la figure : la figure reste en grand, les lignes s'écrivent dans une colonne à côté.
   */
  sur_figure?: boolean;
}

/**
 * Une ligne de démonstration. `allume` (18 novembre 2026, règle 17) : ce que la ligne utilise sur la figure — l'id d'un
 * repère (`craie.repere`) ou d'un moment (`moments`) de la simulation, ou plusieurs. Quand la ligne s'écrit, le lecteur
 * envoie à la simulation `{ type: 'simulation_control', command: 'allume', parameters: { cible, ligne, texte } }`
 * (`cible` : une chaîne, ou la liste) ; avant la première ligne, `eteins` (rien d'allumé). Voir `CommandeAllumage`.
 */
export interface LigneDemonstration {
  texte: string;
  mot: string;
  allume?: string | string[];
}

/**
 * Les ordres d'allumage envoyés à l'iframe de la simulation pendant une démonstration jouée sur la figure (le message
 * est un `simulation_control` ordinaire). Le kit `shared/tableau/tableau.js` les comprend pour toute page qui déclare
 * `Tableau.protocole` : `allume` joue jusqu'au moment de ce nom (s'il existe et n'est pas passé) et allume le repère de
 * ce nom (une lueur qui reste, la dernière plus vive) ; `eteins` éteint tout. Une page qui veut mieux (tracer Δr entre
 * les deux fronts, compter les divisions une à une) met `allume`/`eteins` dans ses `commandes` et les exécute elle-même.
 */
export type CommandeAllumage =
  | { type: 'simulation_control'; command: 'allume'; parameters: { cible: string | string[]; ligne: number; texte: string } }
  | { type: 'simulation_control'; command: 'eteins'; parameters: Record<string, never> };

/** Réaction du tuteur préparée d'avance pour une réponse possible (texte dit, texte écrit, piste audio). */
export interface ReactionPreparee { parole: string; ecrit: string; audio?: string }

/**
 * Un exercice CLIQUABLE posé sur le tableau, à la fin d'une étape.
 *
 * `question` interroge à l'oral : le tableau pose l'énoncé, attend une
 * réponse, puis corrige et poursuit. C'est une vérification au passage, une
 * seule, et elle bloque le fil. Une fin d'étape demande autre chose : plusieurs
 * exercices posés ensemble, que l'élève manipule à son rythme et qui se
 * corrigent tout seuls sous ses doigts — QCM à choisir, paires à relier.
 *
 * Ils sont rendus par les mêmes blocs interactifs que le tableau du tuteur
 * (`boardLines`), donc la correction voyage avec l'énoncé : ces exercices
 * s'auto-corrigent dans le navigateur, ils ne notent pas.
 */
export interface CourseExercise extends EnonceLu {
  type: 'qcm' | 'vrai_faux' | 'association';
  /** L'énoncé. Pour une association, la consigne de mise en relation. */
  prompt: string;
  /** `qcm` : les propositions, et l'index de la bonne. */
  choices?: string[];
  correct?: number;
  /** `vrai_faux` : les affirmations à trancher une par une. */
  statements?: ({ text: string; correct: boolean; explanation?: string } & EnonceLu)[];
  /** `association` : les paires à reformer (la colonne de droite est battue). */
  pairs?: { left: string; right: string }[];
  /** `association` au contrat complet (colonnes avec étiquettes, éléments de trop, retour par paire) : voir `AssociationQuestion`. */
  association?: AssociationQuestion;
  /** Le mot de la fin, affiché une fois l'élève fixé. */
  explanation?: string;
  /** Calcul ou raisonnement : la démonstration manuscrite (pour un vrai/faux, après sa dernière affirmation). */
  demonstration?: Demonstration;
}

export interface CourseVisual {
  /**
   * `scientific` couvre les figures que personne n'a dessinées à l'avance :
   * géométrie et courbes (JSXGraph), chaînes et réseaux (Cytoscape), petite
   * mécanique 2D (Matter). Mêmes moteurs que le tableau du tuteur — une
   * diapositive n'a donc plus à choisir entre une image figée et rien.
   */
  kind?: 'none' | 'image' | 'schema' | 'simulation' | 'scientific' | 'examen';
  url?: string;
  /** `kind: 'examen'` : la page du sujet du national, telle qu'à l'examen (voir `PageExamen`). */
  examen?: PageExamen;
  schema_id?: string;
  scientific?: ScientificVisualSpec;
  caption?: string;
  alt?: string;
  required_interaction?: boolean;
  /**
   * `inline` place un croquis dans le fil du texte. C'est utile quand la
   * figure fait partie de l'explication et ne mérite pas un tableau séparé.
   */
  placement?: 'side' | 'inline';
}

/**
 * La page d'un sujet du national (18 novembre 2026, professeur règles 44-46) : le scan tel qu'à l'examen, en grand comme
 * une feuille (papier, ombre), recadré sur l'exercice, l'en-tête gardé au-dessus. Le tuteur le lit avant d'expliquer.
 * Les fractions sont comptées en hauteur de page (0 = le haut, 1 = le bas).
 */
export interface PageExamen {
  /** Le scan de la page : `/static/exams/<matière>/<année>-<session>/pages/sujet_pN.jpg`. */
  page: string;
  /** La zone de l'exercice sur cette page ; absente : toute la page. */
  recadrage?: { haut: number; bas: number };
  /** La suite de l'exercice sur les pages suivantes, dans l'ordre (ex. `{ page: '…/sujet_p4.jpg', haut: 0.10, bas: 0.147 }`). */
  suite?: { page: string; haut: number; bas: number }[];
  /**
   * La bande d'en-tête gardée visible au-dessus de la zone. Par défaut : l'en-tête officiel de la page elle-même
   * (`{ haut: 0, bas: 0.115 }`) ; `page` pour prendre celui d'une autre page (la première : `sujet_p1.jpg`, `bas: 0.25`) ;
   * `false` : pas de bande (la zone commence déjà en haut de page).
   */
  entete?: { page?: string; haut?: number; bas: number } | false;
  /** Ce qui est rogné à gauche et à droite (marges blanches du scan), en fraction de la largeur : 0.04 par défaut. */
  marge?: number;
  /**
   * Les phrases lues par le tuteur, dans l'ordre : chacune se surligne quand la voix atteint son `mot` (extrait exact
   * du texte parlé). `zone` : sa bande sur la page (fraction de hauteur ; `page` si ce n'est pas `page`, pour une phrase
   * de la `suite`) — surlignée au feutre jaune sur le scan ; sans `zone`, la phrase s'écrit sous la feuille. Tout
   * l'exercice reste visible (une feuille, ou deux côte à côte sur écran large) : la vue ne défile jamais.
   */
  phrases?: { texte: string; mot: string; zone?: { haut: number; bas: number; page?: string } }[];
  /** Source (exercice et questions) dans `exam.json` : « physique/2024-normale, exercice 2 ». Pour le cahier et le tuteur. */
  source?: string;
  /**
   * L'exercice REPRODUIT en code (19 novembre 2026, demande de l'utilisateur : « si l'exercice est divisé en deux pages,
   * c'est mieux de le lire et de le reproduire avec le code, comme un vrai examen avec en-tête et tout »). Quand il est
   * fourni, il remplace les morceaux de scan : une seule feuille de papier, l'en-tête de l'examen, puis tout l'exercice
   * (titre grisé, énoncé, questions, propositions, tableau, figure du sujet) écrit en police d'examen, à la plus grande
   * taille qui fait tout tenir (en deux colonnes sur écran large s'il le faut, jamais sous 15 px). Le texte vient de
   * l'`exam.json` du sujet, tel qu'écrit à l'examen. Chaque bloc qui a un `mot` se surligne quand la voix l'atteint.
   */
  reproduction?: ReproductionExamen;
}

/** L'exercice d'un sujet réécrit en code, comme sur la feuille d'examen. */
export interface ReproductionExamen {
  /**
   * L'en-tête écrit en code, comme celui du sujet : ses lignes (arabe ou français, dans l'ordre), le code du sujet
   * (« NS 28F ») et la page (« 3/6 »). Absent : la bande d'en-tête du scan (`entete` / `page` du visuel).
   */
  entete?: { lignes: string[]; code?: string; page?: string };
  blocs: BlocExamen[];
}

/** Un bloc de l'exercice reproduit. Le texte s'écrit en Unicode (t₁, r₂, v = √(g·h)), comme les cartes du tableau. */
export type BlocExamen =
  | { type: 'titre'; texte: string; mot?: string }
  | { type: 'texte'; texte: string; mot?: string }
  | { type: 'question'; numero: string; texte: string; points?: string; mot?: string }
  | { type: 'choix'; options: { lettre: string; texte: string }[]; mot?: string }
  | { type: 'tableau'; lignes: string[][]; mot?: string }
  /** une figure du sujet (`/static/exams/…/assets/fig….png`) ; `hauteur` en em (8 par défaut) */
  | { type: 'figure'; src: string; alt?: string; hauteur?: number; mot?: string };

export interface PublishedSlideAudio {
  url: string;
  duration_ms?: number | null;
  version?: number;
  speech_hash?: string;
  status?: string;
}

export interface CourseSlide {
  id: string;
  stable_id?: string;
  slide_type: CourseSlideType;
  title: string;
  screen_content?: {
    lead?: string;
    bullets?: string[];
    essential_text?: string;
    student_trace?: string;
    caption?: string;
    alt?: string;
    table?: {
      headers: string[];
      rows: string[][];
    };
  };
  visual?: CourseVisual;
  speech_text?: Record<string, string>;
  question?: CourseQuestion;
  /** Les exercices cliquables posés au tableau après la correction écrite. */
  exercises?: CourseExercise[];
  timing?: {
    auto_advance?: boolean;
    reading_seconds?: number;
    delay_after_feedback_ms?: number;
  };
  audio?: Record<string, PublishedSlideAudio>;
  order_index?: number;
  /** Mode concentration (`CourseFocusStage`) : ce que le tuteur 3D montre, et quand. */
  concentration?: SlideConcentration;
  /** Les compétences du cours que cette diapositive travaille (suivi des acquis). */
  competence_ids?: string[];
}

/** Une compétence du cours : l'unité du suivi des acquis (skill `suivi-des-acquis`). */
export interface CourseCompetence {
  id: string; label: string; slide_ids?: string[]; /** le nom dit par la voix (sans symbole) */ dit?: string;
  /** 3 à 4 questions de rappel espacé, sous des formes différentes (skill `suivi-des-acquis`, section 6). */
  rappels?: QuestionMemoire[];
}

/**
 * Le mode concentration : l'écrit est fermé, le tuteur 3D montre au rythme de la voix.
 * `mot` est un extrait exact du texte parlé ; sa place dans le texte donne l'instant.
 */
export interface SlideConcentration {
  /** Commande que le tuteur appuie dans la simulation quand la voix commence (start, fire_pulse). */
  demarrer?: string;
  /**
   * `repere` : repère dessiné dans la simulation ; `cible` : 'visuel', 'ligne:N' (tableau), 'centre:N' ;
   * `commande` : le tuteur appuie (relance la simulation au moment où la voix l'explique).
   */
  pointage?: { mot: string; repere?: string; cible?: string; commande?: string; parametres?: Record<string, unknown> }[];
  /** Formules ou mots-clés écrits au centre au moment où la voix les dit. */
  centre?: { texte: string; mot: string }[];
  /** La trace à recopier (bulle « À écrire dans le cahier »). */
  cahier?: string;
  /** Les dessins du cahier (courbe, schéma, croquis légendés), sous le texte : `FigureCahier.tsx`. */
  cahier_figures?: FigureCahierData[];
  /**
   * La comparaison que le tuteur fait LUI-MÊME après la voix, si l'élève n'a pas touché la simulation :
   * il change un réglage (M₂ plus loin, le fond plus bas…), rejoue et montre ce qui a changé.
   */
  variante?: { apres_s?: number; etapes: { commande?: string; parametres?: Record<string, unknown>; repere?: string }[] };
  /**
   * Le schéma à légender (15 novembre 2026), comme au bac : la simulation dit combien d'étiquettes sont à poser
   * (`legende_total`), bien posées et ses erreurs. Tant qu'il n'est pas fini, les questions attendent ; fini, il compte
   * pour les acquis et le tuteur le commente avec sa réaction préparée : `juste` (sans erreur), `partiel` (1 ou 2
   * erreurs), `faux` (plus), `aide` (l'élève n'a rien posé : le tuteur place les étiquettes).
   */
  legende?: { reactions?: Partial<Record<'juste' | 'partiel' | 'faux' | 'aide', ReactionPreparee>> };
  /**
   * Les réactions préparées, pour CHAQUE réponse possible : `reponses[cle][option]` avec `juste` (bonne option)
   * ou `1` (indice, 1er essai) et `2` (réponse et justification, 2e essai). `cle` : `q` (question de la
   * diapositive), `e{i}` (QCM de l'exercice i), `e{i}s{j}` (affirmation j d'un vrai/faux ; option 0 = Vrai).
   */
  reponses?: Record<string, Record<string, Partial<Record<'juste' | '1' | '2', ReactionPreparee>>>>;
  /**
   * La diapositive fait le bilan des acquis (fiche « ce qu'il faut retenir », carte du chapitre) : le lecteur lit le
   * bilan de l'élève (GET /course-player/acquis/{deck}), le donne à la simulation (`set_parameters {lacunes, acquis,
   * acquis_ids}`) et, la voix finie, le tuteur nomme ce qu'il reste à retravailler puis fige la page « lacunes ».
   */
  acquis?: boolean;
  /**
   * La question d'OBSERVATION (14 novembre 2026, skill professeur règle 29) : là où l'élève doit remarquer LUI-MÊME
   * quelque chose dans la simulation (une disparition, l'effet d'un curseur, une comparaison). Rare : une par diapositive
   * au plus, quelques-unes par cours.
   */
  observation?: QuestionObservation;
  /**
   * Rejouer la simulation APRÈS la réponse (18 novembre 2026, `parcours.js`) : la simulation s'arrête avant le moment
   * décisif, la question est posée, puis, la réponse donnée (juste, fausse après ses essais, ou passée), le tableau des
   * questions se replie et le tuteur fait `etapes` (en général `play_until` du moment du résultat) ; `duree_s` plus
   * tard (défaut 6), la démonstration ou la suite vient. Les moments `play_until` des étapes ne sont jamais joués avant.
   * Une liste : un rejeu par question (le premier vise par défaut la première question, les autres nomment la leur).
   */
  apres_reponse?: RejeuApresReponse | RejeuApresReponse[];
  /**
   * La diapositive est un RAPPEL de prérequis (18 novembre 2026) : sauté en avançant quand toutes les questions de la
   * (des) diapositive(s) diagnostic `si_reussi` ont été justes du premier coup ; « 🔁 Revoir le rappel » le rouvre.
   */
  rappel?: { si_reussi: string | string[] };
}

/** Un rejeu de la simulation après la réponse à UNE question (`concentration.apres_reponse`). */
export interface RejeuApresReponse {
  /** la question attendue : `q`, `e{i}`, `e{i}s{j}` (défaut, pour le premier rejeu : la première question de la diapositive) */
  question?: string;
  etapes: { commande?: string; parametres?: Record<string, unknown>; repere?: string }[];
  /** réglages envoyés à la simulation tant que la question est ouverte (ex. `{conclusions: false}`) */
  sim_avant?: Record<string, unknown>;
  /** le temps laissé pour regarder, en secondes (défaut 6) */
  duree_s?: number;
}

/**
 * La voix s'arrête juste après `apres_mot` (extrait exact du texte parlé de la langue jouée ; absent : à la fin de la
 * voix), le tuteur fait `gestes` dans la simulation, pose `enonce` (écrit + lu) et se tait : l'élève regarde. Sans
 * réponse, chaque `silence_s` apporte un indice (`indices`, le tuteur peut montrer un repère), puis les cartes `choix`.
 * L'élève répond au micro de réponse (maintenu, transcrit, jugé comme RÉPONSE à cette question) ou par une carte.
 * Chaque carte a son retour (`retours[i]`) ; deux erreurs → `solution`. Puis la voix du cours reprend où elle s'était arrêtée.
 */
export interface QuestionObservation {
  apres_mot?: string;
  /**
   * Réglages envoyés à la simulation (`set_parameters`, sans geste du tuteur) dès qu'elle est prête et jusqu'à la
   * réponse : une simulation qui ÉCRIT sa conclusion la tait (`{conclusions: false}`), sinon la réponse est sous les yeux.
   * `sim_apres` : envoyé quand la question se ferme (`{conclusions: true}`) — la conclusion s'écrit pendant que la voix confirme.
   */
  sim_avant?: Record<string, unknown>;
  sim_apres?: Record<string, unknown>;
  gestes?: { commande?: string; parametres?: Record<string, unknown>; repere?: string }[];
  /** La question écrite (courte, au présent : « Qu'est-ce qui a disparu ? »). */
  enonce: string;
  /** Sa piste préparée (voix Bodi), sinon `enonce_dit` (règles de la voix) par la voix en direct. */
  enonce_audio?: string;
  enonce_dit?: string;
  /** Silence d'observation avant chaque aide (s, défaut 8). */
  silence_s?: number;
  /** Indices progressifs (un ou deux) : du plus vague au plus précis, jamais la réponse. */
  indices?: { texte: string; dit?: string; audio?: string; repere?: string }[];
  /** Trois réponses possibles, ou ['Vrai', 'Faux'] (l'énoncé est alors l'affirmation). */
  choix: string[];
  bonne: number;
  /** Le retour de CHAQUE carte (même ordre que `choix`) : juste → ce qu'il fallait voir ; fausse → un indice. */
  retours?: ReactionPreparee[];
  /** Après la deuxième erreur : la réponse et ce qu'il fallait regarder. */
  solution?: ReactionPreparee;
}

export interface CourseActivity {
  id: string;
  stable_id?: string;
  title: string;
  phase?: string;
  duration_minutes?: number;
  objective_ids?: string[];
  order_index?: number;
  slides: CourseSlide[];
}

export interface CourseDeck {
  id: string;
  /** Identifiant stable du manifeste (le même en local et en base) : c'est lui que suit le suivi des acquis. */
  stable_id?: string;
  lesson_id: string;
  title: string;
  version?: number;
  language?: string;
  estimated_minutes?: number;
  source?: 'database' | 'manifest';
  activities: CourseActivity[];
  competences?: CourseCompetence[];
  /** Séances de 3 blocs (explication → cahier → retrouver → exercice) : `components/course/memoire`. Sans séances, le cours marche comme avant. */
  seances?: SeanceCours[];
  /** `concentration` : le cours se joue en mode concentration, avec le tuteur 3D du cours (cours refaits). */
  mode?: 'tableau' | 'concentration';
}

export interface CourseProgressSnapshot {
  current_activity_id?: string | null;
  current_slide_id?: string | null;
  audio_position_ms?: number;
  completed_slide_ids?: string[];
  status?: 'not_started' | 'in_progress' | 'completed';
}
