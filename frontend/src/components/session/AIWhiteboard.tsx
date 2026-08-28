import { memo, useMemo } from 'react';
import { getSchemaById } from './schemas';
import type { ScientificControlCommand, ScientificSimulationUpdate, ScientificVisualSpec } from './scientific/types';
import LiveBoard, { type LiveScript } from './LiveBoard';

// Types for drawing elements
interface DrawPoint {
  x: number;
  y: number;
}

interface DrawElement {
  id: string;
  type: 'line' | 'arrow' | 'rect' | 'circle' | 'text' | 'path' | 'mitochondria' | 'cell' | 'dna' | 'nucleus' | 'membrane';
  points?: DrawPoint[];
  x?: number;
  y?: number;
  width?: number;
  height?: number;
  radius?: number;
  text?: string;
  color: string;
  strokeWidth: number;
  fontSize?: number;
  fill?: string;
  label?: string;
  // 3D effect properties
  shadow?: boolean;
  gradient?: boolean;
  depth?: number;
  // Animation
  delay?: number;
}

interface DrawStep {
  elements: DrawElement[];
  narration?: string;
  title?: string;
  clear?: boolean;
}

interface BoardContent {
  title?: string;
  lines: Array<{
    type: 'title' | 'subtitle' | 'text' | 'math' | 'step' | 'separator' | 'box' | 'note' | 'table' | 'graph' | 'diagram' | 'qcm' | 'vrai_faux' | 'association' | 'scientific';
    content: string;
    color?: string;
    label?: string;
    scientific?: ScientificVisualSpec;
    // Interactive exercise data
    choices?: string[];
    correct?: number | number[] | boolean;
    explanation?: string;
    statements?: { text: string; correct: boolean; explanation?: string }[];
    pairs?: { left: string; right: string }[];
    // Table/graph/diagram data (pass-through)
    headers?: string[];
    rows?: string[][];
    curves?: any[];
    nodes?: any[];
    edges?: any[];
    [key: string]: any;
  }>;
}

interface AIWhiteboardProps {
  drawCommands: DrawStep[] | null;
  isVisible: boolean;
  onClose?: () => void;
  schemaId?: string | null;
  activeHighlights?: string[];
  boardContent?: BoardContent | null;
  liveScript?: LiveScript | null;
  /** Mode live plein écran : envoi d'une question de l'élève au professeur. */
  onStudentMessage?: (text: string) => void;
  /** Mode live plein écran : dernière réponse texte du professeur. */
  assistantReply?: string | null;
  /** Mode live plein écran : une requête est en cours (le prof réfléchit). */
  busy?: boolean;
  /** false = le tableau s'affiche sans voix (c'est le chat qui parle). */
  voiceEnabled?: boolean;
  /** true tant que la voix du chat parle — le tableau s'écrit à son rythme. */
  audioActive?: boolean;
  /** Le tableau passe en plein écran : la page doit replier sa barre latérale. */
  onFocusChange?: (focus: boolean) => void;
  /** Commande LLM pour la scène scientifique actuellement affichée. */
  scientificControl?: ScientificControlCommand | null;
  /** État compact d'une simulation de catalogue, à transmettre au tuteur. */
  onSimulationUpdate?: (update: ScientificSimulationUpdate) => void;
}

/**
 * Un tableau structuré, rejoué comme un professeur l'écrirait.
 *
 * Chaque ligne devient un pas du script : ce qui s'écrit à la craie devient un
 * `write`, ce qui se lit d'un bloc — tableau à double entrée, courbe, carte
 * mentale, QCM — devient un `bloc`, et une figure de moteur devient une
 * `figure` posée dans la zone de dessin.
 *
 * Un titre laisse respirer avant la suite, comme un professeur qui marque un
 * temps après avoir souligné son titre.
 */
function scriptDepuisTableau(board: BoardContent): LiveScript {
  const steps: LiveScript['steps'] = [];
  for (const line of board.lines || []) {
    if (!line || typeof line !== 'object') continue;
    const type = String(line.type || 'text').toLowerCase();

    if (type === 'scientific' && line.scientific) {
      steps.push({ action: 'figure', scientific: line.scientific, say: line.content || undefined });
      continue;
    }
    if (BOARD_BLOC_TYPES.has(type)) {
      steps.push({ action: 'bloc', line: line as any });
      continue;
    }
    if (typeof line.content !== 'string' || !line.content.trim()) continue;
    steps.push({ action: 'write', line: { type, content: line.content, color: line.color } });
    if (type === 'title' || type === 'subtitle') {
      steps.push({ action: 'pause', duration: 700 });
    }
  }
  return { title: board.title || 'Cours en direct', steps };
}

/**
 * Un croquis animé, rejoué comme un professeur le tracerait.
 *
 * Chaque étape pose ses éléments dans la zone de dessin ; son titre s'écrit à
 * gauche, et `clear` essuie la zone avant la suivante — un professeur ne
 * superpose pas son deuxième croquis sur le premier.
 */
function scriptDepuisCroquis(commandes: DrawStep[]): LiveScript {
  const steps: LiveScript['steps'] = [];
  commandes.forEach((etape, index) => {
    if (!etape || typeof etape !== 'object') return;
    if (etape.clear && index > 0) {
      steps.push({ action: 'erase', zone: 'draw' });
    }
    if (typeof etape.title === 'string' && etape.title.trim()) {
      steps.push({ action: 'write', line: { type: 'subtitle', content: etape.title.trim() } });
    }
    const elements = (etape.elements || []).filter(el => el && el.type);
    if (elements.length > 0) {
      steps.push({ action: 'draw', elements: elements as any });
    }
    if (typeof etape.narration === 'string' && etape.narration.trim()) {
      steps.push({ action: 'narrate', text: etape.narration.trim() });
    }
  });
  return { title: commandes[0]?.title || 'Croquis', steps };
}

/** Les lignes que la craie ne sait pas écrire : elles se posent d'un bloc. */
const BOARD_BLOC_TYPES = new Set([
  'table', 'graph', 'diagram', 'mindmap',
  'qcm', 'vrai_faux', 'association', 'illustration',
]);

/**
 * Un schéma de la BIBLIOTHÈQUE, posé dans la zone de dessin du tableau.
 *
 * Il s'affichait auparavant seul, sur un fond BLANC, avec sa propre barre
 * d'outils — au milieu d'une séance sombre, et sans la colonne de gauche où
 * le professeur écrit. L'élève voyait la figure sans un mot autour.
 */
function scriptDepuisSchema(schemaId: string, titre: string, surlignages?: string[]): LiveScript {
  const steps: LiveScript['steps'] = [
    { action: 'write', line: { type: 'title', content: titre } },
    { action: 'figure', schema_id: schemaId, highlights: surlignages },
  ];

  // ── Le professeur COMMENTE la planche qu'il vient d'accrocher ──
  //
  // Le script s'arrêtait sur ces deux pas : un titre, une figure, et une
  // colonne de gauche vide jusqu'à « Explication terminée ». L'élève recevait
  // une image sans un mot autour — celle-là même que le commentaire de cette
  // fonction promettait d'éviter.
  //
  // Les mots existaient pourtant déjà : chaque schéma porte ses annotations,
  // et chacune a un intitulé et une phrase qui l'explique. Personne ne les
  // lisait. Elles sont écrites à la craie l'une après l'autre, dans l'ordre du
  // schéma, donc dites à voix haute par le tableau — c'est exactement ce qu'un
  // professeur fait en désignant sa planche du doigt.
  //
  // La borne à six lignes n'est pas décorative : au-delà, la colonne défile et
  // l'élève ne voit plus la figure dont on lui parle.
  const annotations = (getSchemaById(schemaId)?.annotations || []).slice(0, 6);
  for (const annotation of annotations) {
    const intitule = (annotation.label || '').trim();
    const explication = (annotation.description || '').trim();
    if (!intitule && !explication) continue;
    steps.push({
      action: 'write',
      line: {
        type: 'text',
        content: intitule && explication ? `${intitule} : ${explication}` : intitule || explication,
      },
    });
  }

  return { title: titre, steps };
}

  function AIWhiteboardInner({ drawCommands, isVisible, onClose, schemaId, activeHighlights, boardContent, liveScript, onStudentMessage, assistantReply, busy, voiceEnabled, audioActive, onFocusChange, scientificControl, onSimulationUpdate }: AIWhiteboardProps) {
  console.log('[AIWhiteboard] Render:', {
    hasDrawCommands: !!(drawCommands && drawCommands.length > 0),
    hasSchemaId: !!schemaId,
    hasBoardContent: !!(boardContent && boardContent.lines?.length > 0),
    hasLiveScript: !!(liveScript && liveScript.steps?.length > 0),
    isVisible
  });
  const activeSchema = schemaId ? getSchemaById(schemaId) : undefined;

  // ── Le script ne se refabrique QUE si son contenu change ──
  //
  // Il était construit en plein rendu. `LiveBoard` redémarre son script dès
  // que l'objet reçu change d'identité — et cet objet en changeait à chaque
  // rendu, donc à chaque bascule de `audioActive` : la voix commence, le
  // tableau repart de zéro ; elle s'arrête, il repart encore. L'élève voyait
  // le titre s'écrire, puis se réécrire, deux ou trois fois par tour.
  //
  // `useMemo` rend l'identité stable tant que le contenu l'est. Les hooks
  // vivent au-dessus des aiguillages : ils doivent être appelés à chaque
  // rendu, quel que soit le tableau choisi ensuite.
  const scriptTableau = useMemo(
    () => (boardContent && boardContent.lines && boardContent.lines.length > 0
      ? scriptDepuisTableau(boardContent)
      : null),
    [boardContent],
  );
  // `activeHighlights` arrive souvent en tableau fraîchement construit : on se
  // lie à son CONTENU, pas à sa référence, sinon le mémo ne retient rien.
  const clesSurlignages = (activeHighlights || []).join('|');
  const scriptSchema = useMemo(
    () => (activeSchema
      ? scriptDepuisSchema(activeSchema.id, activeSchema.title, clesSurlignages ? clesSurlignages.split('|') : [])
      : null),
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [activeSchema?.id, activeSchema?.title, clesSurlignages],
  );
  const scriptCroquis = useMemo(
    () => (drawCommands && drawCommands.length > 0 ? scriptDepuisCroquis(drawCommands) : null),
    [drawCommands],
  );

  // ── Live mode (priorité maximale) : le professeur écrit/dessine en direct ──
  if (liveScript && liveScript.steps && liveScript.steps.length > 0) {
    return (
      <LiveBoard
        script={liveScript}
        isVisible={isVisible}
        onClose={onClose}
        onStudentMessage={onStudentMessage}
        assistantReply={assistantReply}
        busy={busy}
        voiceEnabled={voiceEnabled}
        audioActive={audioActive}
        onFocusChange={onFocusChange}
        scientificControl={scientificControl}
        onSimulationUpdate={onSimulationUpdate}
      />
    );
  }

  const hasActiveDrawCommands = drawCommands && drawCommands.length > 0;

  // ── UN SEUL TABLEAU ───────────────────────────────────────────
  //
  // Ce composant aiguillait vers quatre rendus : le cours structuré, le
  // schéma de la bibliothèque, le dessin au canvas, et le professeur en
  // direct. Quatre présentations pour une même chose — un tableau — et
  // l'élève devait deviner, à chaque affichage, où regarder et ce qu'il
  // pouvait faire. Le tableau structuré posait tout d'un bloc, sans un mot ;
  // le schéma s'ouvrait sur un fond BLANC au milieu d'une séance sombre.
  //
  // Il n'en reste qu'un. Le cours structuré et le schéma de la bibliothèque
  // sont CONVERTIS en script « prof en direct » : le texte s'écrit à gauche
  // au rythme de la parole, la figure se pose à droite. Rien n'est perdu en
  // route — les tableaux à double entrée, les QCM et les cartes mentales
  // que seul `MathBoard` savait rendre y sont posés par son propre rendu,
  // appelé depuis la colonne de gauche.
  if (!hasActiveDrawCommands && boardContent && boardContent.lines && boardContent.lines.length > 0) {
    return (
      <LiveBoard
        script={scriptTableau!}
        isVisible={isVisible}
        onClose={onClose}
        onStudentMessage={onStudentMessage}
        assistantReply={assistantReply}
        busy={busy}
        voiceEnabled={voiceEnabled}
        audioActive={audioActive}
        onFocusChange={onFocusChange}
        scientificControl={scientificControl}
        onSimulationUpdate={onSimulationUpdate}
      />
    );
  }

  if (!hasActiveDrawCommands && activeSchema) {
    return (
      <LiveBoard
        script={scriptSchema!}
        isVisible={isVisible}
        onClose={onClose}
        onStudentMessage={onStudentMessage}
        assistantReply={assistantReply}
        busy={busy}
        voiceEnabled={voiceEnabled}
        audioActive={audioActive}
        onFocusChange={onFocusChange}
        scientificControl={scientificControl}
        onSimulationUpdate={onSimulationUpdate}
      />
    );
  }

  // ── Le dessin, lui aussi, se rejoue en direct ──
  //
  // C'était le quatrième rendu : un CANVAS, avec ses dégradés radiaux, ses
  // ombres portées et ses cinq formes de SVT peintes à la main — une
  // imitation de photo au milieu d'une séance qui se donne à la craie. Et
  // rien à côté : pas de colonne où le professeur écrit, pas de figure, pas
  // de coin élève.
  //
  // Le croquis devient un script. Chaque étape trace ses éléments dans la
  // zone de dessin, son titre s'écrit à gauche, et `clear` essuie la zone
  // avant la suite. Les cinq formes de SVT ont suivi : `LiveBoard` les trace
  // maintenant à la craie, avec leur anatomie (double membrane, crêtes,
  // brins en opposition de phase, bicouche orientée).
  if (drawCommands && drawCommands.length > 0) {
    return (
      <LiveBoard
        script={scriptCroquis!}
        isVisible={isVisible}
        onClose={onClose}
        onStudentMessage={onStudentMessage}
        assistantReply={assistantReply}
        busy={busy}
        voiceEnabled={voiceEnabled}
        audioActive={audioActive}
        onFocusChange={onFocusChange}
        scientificControl={scientificControl}
        onSimulationUpdate={onSimulationUpdate}
      />
    );
  }

  return null;
}


const AIWhiteboard = memo(AIWhiteboardInner);
export default AIWhiteboard;
