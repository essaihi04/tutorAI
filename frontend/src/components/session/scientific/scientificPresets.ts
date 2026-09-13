import type {
  CytoscapeEdgeSpec,
  CytoscapeNodeSpec,
  CytoscapeVisualSpec,
  JSXGraphElementSpec,
  JSXGraphVisualSpec,
  RoughSVGElementSpec,
  RoughSVGHotspotPanelSpec,
  RoughSVGHotspotSpec,
  RoughSVGVisualSpec,
  ScientificDetailSpec,
  ScientificPoint,
  ScientificPresetId,
  ScientificVisualSpec,
} from './types';
import { initialVesicleState, vesicleResult } from './vesicleExperimentModel';
import { RESPIRATORY_MAX_STEP } from './respiratoryChainModel';
import { energyBalance, energyNumber } from './energyBalanceModel';

export interface ScientificPresetVariant {
  id: string;
  label: string;
}

export interface ScientificPresetMeta {
  id: ScientificPresetId;
  title: string;
  variants: ScientificPresetVariant[];
  defaultVariant: string;
  maxStep: number;
  frameMs: number;
}

export const SCIENTIFIC_PRESETS: Record<ScientificPresetId, ScientificPresetMeta> = {
  phys_ch1_propagation_onde: {
    id: 'phys_ch1_propagation_onde',
    title: 'Propagation, retard et superposition d’une onde',
    defaultVariant: 'propagation',
    variants: [
      { id: 'propagation', label: 'Propagation' },
      { id: 'retard', label: 'Retard entre deux points' },
      { id: 'superposition', label: 'Superposition' },
    ],
    maxStep: 40,
    frameMs: 140,
  },
  phys_ch1_types_ondes: {
    id: 'phys_ch1_types_ondes',
    title: 'Ondes transversales et longitudinales',
    defaultVariant: 'comparaison',
    variants: [
      { id: 'comparaison', label: 'Comparer' },
      { id: 'transversale', label: 'Onde transversale' },
      { id: 'longitudinale', label: 'Onde longitudinale' },
    ],
    maxStep: 40,
    frameMs: 140,
  },
  phys_ch1_celerite_corde: {
    id: 'phys_ch1_celerite_corde',
    title: 'Célérité d’une onde sur une corde',
    defaultVariant: 'forte_tension',
    variants: [
      { id: 'forte_tension', label: 'Tension plus forte' },
      { id: 'faible_tension', label: 'Tension plus faible' },
      { id: 'forte_masse_lineique', label: 'Masse linéique plus forte' },
    ],
    maxStep: 40,
    frameMs: 140,
  },
  chem_ch1_facteurs_cinetiques: {
    id: 'chem_ch1_facteurs_cinetiques',
    title: 'Facteurs cinétiques',
    defaultVariant: 'temperature',
    variants: [
      { id: 'temperature', label: 'Température' },
      { id: 'concentration', label: 'Concentration' },
      { id: 'catalyseur', label: 'Catalyseur' },
      { id: 'surface_contact', label: 'Surface de contact' },
    ],
    maxStep: 36,
    frameMs: 160,
  },
  chem_ch1_energie_activation: {
    id: 'chem_ch1_energie_activation',
    title: 'Énergie d’activation et catalyse',
    defaultVariant: 'comparaison',
    variants: [
      { id: 'comparaison', label: 'Comparer les deux voies' },
      { id: 'sans_catalyseur', label: 'Sans catalyseur' },
      { id: 'avec_catalyseur', label: 'Avec catalyseur' },
    ],
    maxStep: 36,
    frameMs: 160,
  },
  chem_ch1_oxydoreduction: {
    id: 'chem_ch1_oxydoreduction',
    title: 'Transfert d’électrons en oxydoréduction',
    defaultVariant: 'transfert_direct',
    variants: [
      { id: 'transfert_direct', label: 'Transfert direct' },
      { id: 'pile', label: 'Pile' },
      { id: 'electrolyse', label: 'Électrolyse' },
    ],
    maxStep: 7,
    frameMs: 720,
  },
  svt_ch1_respiration_mitochondriale: {
    id: 'svt_ch1_respiration_mitochondriale',
    title: 'Bilan de la respiration mitochondriale',
    defaultVariant: 'bilan',
    variants: [
      { id: 'bilan', label: 'Bilan complet' },
      { id: 'krebs', label: 'Cycle de Krebs' },
      { id: 'chaine_respiratoire', label: 'Chaîne respiratoire' },
    ],
    maxStep: 9,
    frameMs: 700,
  },
  svt_ch1_glissement_sarcomere: {
    id: 'svt_ch1_glissement_sarcomere',
    title: 'Glissement des filaments et raccourcissement du sarcomère',
    defaultVariant: 'contraction',
    variants: [
      { id: 'repos', label: 'Au repos' },
      { id: 'contraction', label: 'Pendant la contraction' },
      { id: 'comparaison', label: 'Comparer repos et contraction' },
    ],
    maxStep: 30,
    frameMs: 170,
  },
  svt_ch1_couplage_excitation_contraction: {
    id: 'svt_ch1_couplage_excitation_contraction',
    title: 'Couplage excitation–contraction–relaxation',
    defaultVariant: 'cycle_complet',
    variants: [
      { id: 'cycle_complet', label: 'Cycle complet' },
      { id: 'liberation_calcium', label: 'Libération du Ca²⁺' },
      { id: 'contraction', label: 'Contraction' },
      { id: 'relaxation', label: 'Relaxation' },
    ],
    maxStep: 8,
    frameMs: 720,
  },
  svt_ch1_cycle_atp: {
    id: 'svt_ch1_cycle_atp',
    title: 'Cycle ATP–ADP',
    defaultVariant: 'cycle_complet',
    variants: [
      { id: 'cycle_complet', label: 'Cycle complet' },
      { id: 'hydrolyse', label: 'Hydrolyse' },
      { id: 'phosphorylation', label: 'Phosphorylation' },
      { id: 'couplage', label: 'Couplage énergétique' },
    ],
    maxStep: 5,
    frameMs: 850,
  },
  svt_ch1_levures_exao: {
    id: 'svt_ch1_levures_exao',
    title: 'Levures : respiration ou fermentation',
    defaultVariant: 'comparaison',
    variants: [
      { id: 'comparaison', label: 'Comparer' },
      { id: 'avec_oxygene', label: 'Avec O₂' },
      { id: 'sans_oxygene', label: 'Sans O₂' },
    ],
    maxStep: 24,
    frameMs: 180,
  },
  svt_ch1_glycolyse_etapes: {
    id: 'svt_ch1_glycolyse_etapes', title: 'Les étapes de la glycolyse',
    defaultVariant: 'scene', variants: [{ id: 'scene', label: 'Glycolyse' }], maxStep: 9, frameMs: 900,
  },
  svt_ch1_pyruvate_acetyl_coa: {
    id: 'svt_ch1_pyruvate_acetyl_coa', title: 'Voyage du pyruvate vers la matrice',
    defaultVariant: 'scene', variants: [{ id: 'scene', label: 'Pyruvate → acétyl-CoA' }], maxStep: 8, frameMs: 900,
  },
  svt_ch1_krebs_detaille: {
    id: 'svt_ch1_krebs_detaille', title: 'Cycle de Krebs dans la matrice',
    defaultVariant: 'scene', variants: [{ id: 'scene', label: 'Krebs' }], maxStep: 8, frameMs: 1150,
  },
  svt_ch1_echelle_redox: {
    id: 'svt_ch1_echelle_redox', title: 'Potentiels d’oxydoréduction',
    defaultVariant: 'scene', variants: [{ id: 'scene', label: 'Escalier des électrons' }], maxStep: 8, frameMs: 1000,
  },
  svt_ch1_ultrastructure_mitochondrie: {
    id: 'svt_ch1_ultrastructure_mitochondrie', title: 'Zoom sur les compartiments de la mitochondrie',
    defaultVariant: 'scene', variants: [{ id: 'scene', label: 'Compartiments essentiels' }], maxStep: 4, frameMs: 1100,
  },
  svt_ch1_flux_protons: {
    id: 'svt_ch1_flux_protons', title: 'Réduction du dioxygène et flux de protons',
    defaultVariant: 'scene', variants: [{ id: 'scene', label: 'Flux de protons' }], maxStep: 8, frameMs: 850,
  },
  svt_ch1_molecules_glucose_atp: {
    id: 'svt_ch1_molecules_glucose_atp', title: 'Structure du glucose et de l’ATP',
    defaultVariant: 'glucose', variants: [
      { id: 'glucose', label: 'Glucose' },
      { id: 'atp', label: 'ATP' },
      { id: 'scene', label: 'Glucose et ATP' },
    ], maxStep: 5, frameMs: 850,
  },
  svt_ch1_rendement_energetique: {
    id: 'svt_ch1_rendement_energetique', title: 'Bilan en ATP et rendement énergétique',
    defaultVariant: 'scene', variants: [
      { id: 'scene', label: 'Convention 38 ATP' },
      { id: 'navette_36', label: 'Convention 36 ATP · navette' },
    ], maxStep: 10, frameMs: 2200,
  },
  svt_ch1_schema_bilan_annote: {
    id: 'svt_ch1_schema_bilan_annote', title: 'Schéma-bilan de la respiration',
    defaultVariant: 'scene', variants: [{ id: 'scene', label: 'Schéma-bilan' }], maxStep: 21, frameMs: 1400,
  },
  svt_ch1_vesicules_atp_synthase: {
    id: 'svt_ch1_vesicules_atp_synthase', title: 'Rôle des sphères pédonculées',
    defaultVariant: 'scene', variants: [
      { id: 'scene', label: 'Préparation puis expérience' },
      { id: 'acide_externe', label: 'pHi 6 / pHe 4' },
      { id: 'equilibre', label: 'pHi 7 / pHe 7' },
      { id: 'acide_interne', label: 'pHi 6 / pHe 9' },
      { id: 'personnalisee', label: 'pH personnalisés' },
    ], maxStep: 8, frameMs: 850,
  },
  svt_ch1_isolement_cretes_ultrasons: {
    id: 'svt_ch1_isolement_cretes_ultrasons', title: 'Isolement des crêtes par ultrasons',
    defaultVariant: 'scene', variants: [{ id: 'scene', label: 'Sonication et vésicules retournées' }], maxStep: 3, frameMs: 1800,
  },
  svt_ch1_fermentations_photos: {
    id: 'svt_ch1_fermentations_photos', title: 'Fermentations lactique et alcoolique en photos',
    defaultVariant: 'scene', variants: [{ id: 'scene', label: 'Muscle et levure' }], maxStep: 3, frameMs: 1900,
  },
  svt_ch1_chimiosmose: {
    id: 'svt_ch1_chimiosmose',
    title: 'Chaîne respiratoire et phosphorylation oxydative',
    defaultVariant: 'nadh',
    variants: [{ id: 'nadh', label: 'NADH,H⁺' }, { id: 'fadh2', label: 'FADH₂' }, { id: 'scene', label: 'NADH,H⁺ (ancien cours)' }],
    maxStep: RESPIRATORY_MAX_STEP,
    frameMs: 1800,
  },
  svt_ch1_carte_metabolique: {
    id: 'svt_ch1_carte_metabolique',
    title: 'De la matière organique à l’ATP',
    defaultVariant: 'scene',
    variants: [{ id: 'scene', label: 'Devenir du pyruvate' }],
    maxStep: 10,
    frameMs: 850,
  },
  svt_ch1_myogrammes: {
    id: 'svt_ch1_myogrammes',
    title: 'Réponses mécaniques du muscle',
    defaultVariant: 'secousse',
    variants: [
      { id: 'secousse', label: 'Secousse' },
      { id: 'sommation', label: 'Sommation' },
      { id: 'tetanus_incomplet', label: 'Tétanos incomplet' },
      { id: 'tetanus_complet', label: 'Tétanos complet' },
    ],
    maxStep: 32,
    frameMs: 110,
  },
  svt_ch1_chaleurs_muscle: {
    id: 'svt_ch1_chaleurs_muscle',
    title: 'Secousse musculaire et dégagements de chaleur',
    defaultVariant: 'comparaison',
    variants: [
      { id: 'comparaison', label: 'Comparer avec et sans O₂' },
      { id: 'avec_oxygene', label: 'Récupération avec O₂' },
      { id: 'sans_oxygene', label: 'Récupération sans O₂' },
    ],
    maxStep: 36,
    frameMs: 130,
  },
  svt_ch1_cycle_actomyosine: {
    id: 'svt_ch1_cycle_actomyosine',
    title: 'Cycle des ponts actine–myosine',
    defaultVariant: 'cycle_complet',
    variants: [
      { id: 'cycle_complet', label: 'Cycle complet' },
      { id: 'fixation', label: '1. Fixation' },
      { id: 'pivotement', label: '2. Pivotement' },
      { id: 'detachement', label: '3. Détachement' },
      { id: 'reactivation', label: '4. Réactivation' },
    ],
    maxStep: 5,
    frameMs: 900,
  },
  svt_ch1_filieres_effort: {
    id: 'svt_ch1_filieres_effort',
    title: 'Régénération de l’ATP pendant l’effort',
    defaultVariant: 'vue_ensemble',
    variants: [
      { id: 'vue_ensemble', label: 'Vue d’ensemble' },
      { id: 'effort_bref', label: 'Effort bref' },
      { id: 'effort_intense', label: 'Effort intense' },
      { id: 'effort_prolonge', label: 'Effort prolongé' },
      { id: 'recuperation', label: 'Récupération' },
    ],
    maxStep: 7,
    frameMs: 760,
  },
};

const INACTIVE_NODE = '#334155';
const ACTIVE_NODE = '#0891b2';
const ACTIVE_END = '#f97316';
const INACTIVE_EDGE = '#64748b';
const ACTIVE_EDGE = '#22d3ee';

function revealedCount(length: number, step: number, maxStep: number): number {
  if (length <= 0) return 0;
  const safeStep = Math.max(0, Math.min(maxStep, Math.round(step)));
  return Math.max(1, Math.ceil((safeStep / maxStep) * length));
}

/** Une voie du carrefour : ce qui l'ouvre, puis ce qu'elle traverse. */
interface VoieCarrefour {
  etiquette: string;
  stations: StationRuban[];
}

/**
 * Le carrefour : un tronc, des voies paralleles, parfois une arrivee commune.
 * Trois colonnes seulement, parce qu'au-dela les cartes redeviennent illisibles
 * a la largeur reelle de la vignette.
 */
function carrefourSpec(
  title: string,
  tronc: StationRuban,
  voies: VoieCarrefour[],
  arrivee: StationRuban | null,
  step: number,
  maxStep: number,
): RoughSVGVisualSpec {
  const VIF = '#67e8f9';
  const OR = '#fde047';
  const COL_L = 270;
  const colonnes = [155, 480, 805];

  const ordre: StationRuban[] = [tronc];
  voies.forEach(voie => ordre.push(...voie.stations));
  if (arrivee) ordre.push(arrivee);
  const vues = revealedCount(ordre.length, step, maxStep);
  const visible = (station: StationRuban) => ordre.indexOf(station) < vues;
  const courant = ordre[Math.max(0, vues - 1)];

  const el: RoughSVGElementSpec[] = [];
  const zones: RoughSVGHotspotSpec[] = [];

  const poser = (station: StationRuban, cx: number, cy: number, largeur: number, hauteur: number) => {
    const actif = station === courant;
    el.push({
      id: `c-${station.id}`, type: 'rect', x: cx - largeur / 2, y: cy - hauteur / 2,
      width: largeur, height: hauteur,
      color: actif ? OR : VIF, fill: actif ? '#713f12' : '#0e7490', strokeWidth: actif ? 5 : 3,
    });
    const lignes = couperTexte(station.label, Math.floor(largeur / 11), 3);
    const depart = cy - ((lignes.length - 1) * 23) / 2 + 7;
    lignes.forEach((ligne, i) => el.push({
      id: `c-${station.id}-l${i}`, type: 'text', x: cx, y: depart + i * 23,
      text: ligne, color: '#ecfeff', fontSize: 19, align: 'middle',
    }));
    if (station.detail) zones.push({
      id: station.id, x: cx - largeur / 2, y: cy - hauteur / 2, width: largeur, height: hauteur,
      color: actif ? OR : VIF, label: station.label, value: station.detail.value, lines: station.detail.lines,
    });
  };

  poser(tronc, 480, 62, 380, 78);

  voies.forEach((voie, v) => {
    const cx = colonnes[v] || colonnes[colonnes.length - 1];
    if (voie.stations.some(visible)) {
      // La fleche s'arrete avant l'etiquette : sur la colonne du milieu elle
      // la traversait de part en part.
      el.push({ id: `v-${v}`, type: 'arrow', strokeWidth: 3, color: OR,
        points: [{ x: 480, y: 101 }, { x: cx, y: 142 }] });
      el.push({ id: `v-${v}-t`, type: 'text', x: cx, y: 170,
        text: couperTexte(voie.etiquette, 22, 1)[0], color: '#fcd34d', fontSize: 15, align: 'middle' });
    }
    voie.stations.forEach((station, k) => {
      if (!visible(station)) return;
      const cy = 232 + k * 118;
      poser(station, cx, cy, COL_L, 88);
      if (k > 0) el.push({ id: `v-${v}-f${k}`, type: 'arrow', strokeWidth: 3, color: VIF,
        points: [{ x: cx, y: cy - 76 }, { x: cx, y: cy - 48 }] });
    });
  });

  const profondeur = Math.max(...voies.map(voie => voie.stations.length));
  const basVoies = 232 + (profondeur - 1) * 118 + 44;

  if (arrivee && visible(arrivee)) {
    voies.forEach((_voie, v) => {
      const cx = colonnes[v] || colonnes[colonnes.length - 1];
      el.push({ id: `j-${v}`, type: 'arrow', strokeWidth: 3, color: OR, dashed: true,
        points: [{ x: cx, y: basVoies + 4 }, { x: 480, y: basVoies + 52 }] });
    });
    poser(arrivee, 480, basVoies + 96, 560, 78);
  }

  const bas = basVoies + (arrivee ? 140 : 10);
  return {
    engine: 'roughsvg', title, width: 960, height: bas + 168,
    elements: el,
    hotspots: zones,
    hotspotPanel: zones.length ? panneauQuestion(30, bas + 28, 400, 124) : undefined,
  };
}

/** Les libelles de transition, ranges par couple de stations successives. */
function transitionsSuivant(chemin: string[], table: Record<string, string>): string[] {
  return chemin.slice(0, -1).map((id, i) => table[`${id}>${chemin[i + 1]}`] || '');
}

/** Une station du ruban : son nom complet, son nom court, sa fiche. */
interface StationRuban {
  id: string;
  label: string;
  /** Nom court, celui qui tient dans la piste du bas. */
  court: string;
  detail?: ScientificDetailSpec;
}

/**
 * Le SVG ne coupe pas les lignes tout seul : on les coupe avant de les poser.
 * Au-dela du nombre de lignes permis, on tronque plutot que de deborder.
 */
function couperTexte(texte: string, maxCar: number, maxLignes: number): string[] {
  const lignes: string[] = [];
  let courante = '';
  for (const mot of texte.split(' ')) {
    const essai = courante ? `${courante} ${mot}` : mot;
    if (!courante || essai.length <= maxCar) {
      courante = essai;
      continue;
    }
    lignes.push(courante);
    courante = mot;
  }
  if (courante) lignes.push(courante);
  if (lignes.length <= maxLignes) return lignes;
  const gardees = lignes.slice(0, maxLignes);
  gardees[maxLignes - 1] = `${gardees[maxLignes - 1].slice(0, maxCar - 1)}…`;
  return gardees;
}

/**
 * Le ruban : une chaine longue ne tient pas en entier a une taille lisible.
 * On montre donc une fenetre de trois grandes cartes autour de l'etape
 * courante, et la chaine complete est rappelee en dessous sur une piste.
 * La transformation s'ecrit dans l'intervalle, la ou elle a lieu.
 */
function rubanSpec(
  title: string,
  stations: StationRuban[],
  transitions: string[],
  step: number,
  maxStep: number,
  /** Un cycle : la derniere station ramene a la premiere. */
  boucle = false,
): RoughSVGVisualSpec {
  const INK = '#e0f2fe';
  const VIF = '#67e8f9';
  const PALE = '#64748b';
  const OR = '#fde047';

  const total = stations.length;
  const courant = Math.max(0, Math.min(total - 1, revealedCount(total, step, maxStep) - 1));
  // La fenetre reste pleine aux deux bouts : un tiers de cadre vide en fin
  // de chaine donne l'impression que la figure est cassee.
  const debut = Math.max(0, Math.min(courant - 1, total - 3));
  const fenetre = boucle
    ? [(courant - 1 + total) % total, courant, (courant + 1) % total]
    : [debut, debut + 1, debut + 2];
  const centres = [160, 480, 800];
  const CARTE_L = 210;
  const CARTE_H = 118;
  const HAUT = 91;

  const el: RoughSVGElementSpec[] = [];

  fenetre.forEach((index, place) => {
    const station = stations[index];
    if (!station) return;
    const actif = index === courant;
    const cx = centres[place];
    el.push({
      id: `carte-${place}`, type: 'rect', x: cx - CARTE_L / 2, y: HAUT,
      width: CARTE_L, height: CARTE_H,
      color: actif ? VIF : PALE, fill: actif ? '#0e7490' : '#1e293b', strokeWidth: actif ? 5 : 3,
    });
    const lignes = couperTexte(station.label, 19, 3);
    const depart = 150 - ((lignes.length - 1) * 24) / 2 + 8;
    lignes.forEach((ligne, i) => el.push({
      id: `carte-${place}-l${i}`, type: 'text', x: cx, y: depart + i * 24,
      text: ligne, color: actif ? '#ecfeff' : '#cbd5e1', fontSize: 20, align: 'middle',
    }));
  });

  // Les fleches et, dans leur intervalle, ce qui se transforme.
  [0, 1].forEach(place => {
    const depuis = fenetre[place];
    const vers = fenetre[place + 1];
    if (!stations[depuis] || !stations[vers]) return;
    const x1 = centres[place] + CARTE_L / 2 + 4;
    const x2 = centres[place + 1] - CARTE_L / 2 - 4;
    el.push({ id: `fleche-${place}`, type: 'arrow', points: [{ x: x1, y: 150 }, { x: x2, y: 150 }], color: OR, strokeWidth: 3 });
    const texte = transitions[depuis] || '';
    couperTexte(texte, 15, 3).forEach((ligne, i) => el.push({
      id: `trans-${place}-${i}`, type: 'text', x: (x1 + x2) / 2, y: 184 + i * 20,
      text: ligne, color: '#fcd34d', fontSize: 15, align: 'middle',
    }));
  });

  // La piste : toute la chaine, en petit, pour savoir ou l'on en est.
  const PAR_RANG = 7;
  const rangs = Math.ceil(total / PAR_RANG);
  const largeurJeton = (900 - (PAR_RANG - 1) * 8) / PAR_RANG;
  stations.forEach((station, i) => {
    const rang = Math.floor(i / PAR_RANG);
    const colonne = i % PAR_RANG;
    const x = 30 + colonne * (largeurJeton + 8);
    const y = 258 + rang * 44;
    const passe = i <= courant;
    el.push({
      id: `jeton-${i}`, type: 'rect', x, y, width: largeurJeton, height: 34,
      color: i === courant ? OR : (passe ? VIF : PALE),
      fill: i === courant ? '#713f12' : (passe ? '#164e63' : '#0f172a'), strokeWidth: i === courant ? 3 : 2,
    });
    el.push({
      id: `jeton-t-${i}`, type: 'text', x: x + largeurJeton / 2, y: y + 22,
      text: couperTexte(station.court, 14, 1)[0], color: i === courant ? OR : (passe ? INK : '#94a3b8'),
      fontSize: 13, align: 'middle',
    });
  });

  if (boucle) {
    const finRang = 258 + (rangs - 1) * 44;
    el.push({ id: 'retour', type: 'arrow', strokeWidth: 3, color: OR, dashed: true,
      points: [{ x: 930, y: finRang + 44 }, { x: 930, y: finRang + 62 }, { x: 30, y: finRang + 62 }, { x: 30, y: finRang + 46 }] });
    el.push({ id: 'retour-t', type: 'text', x: 480, y: finRang + 80, text: 'et le cycle recommence', color: OR, fontSize: 16, align: 'middle' });
  }

  const basPiste = 258 + rangs * 44 + (boucle ? 44 : 0);
  el.push({
    id: 'compteur', type: 'text', x: 930, y: basPiste + 26,
    text: `étape ${courant + 1} sur ${total}`, color: PALE, fontSize: 16, align: 'end',
  });

  const zones: RoughSVGHotspotSpec[] = fenetre.flatMap((index, place) => {
    const station = stations[index];
    if (!station || !station.detail) return [];
    return [{
      id: `${station.id}-${index}`, x: centres[place] - CARTE_L / 2, y: HAUT, width: CARTE_L, height: CARTE_H,
      color: index === courant ? OR : VIF,
      label: station.label, value: station.detail.value, lines: station.detail.lines,
    }];
  });

  return {
    engine: 'roughsvg', title, width: 960, height: basPiste + 176,
    elements: el,
    hotspots: zones,
    hotspotPanel: zones.length ? panneauQuestion(30, basPiste + 40, 400, 124) : undefined,
  };
}

function processSpec(
  title: string,
  layout: CytoscapeVisualSpec['layout'],
  rawNodes: Array<[string, string]>,
  rawEdges: Array<[string, string, string?]>,
  activePath: string[],
  step: number,
  maxStep: number,
): CytoscapeVisualSpec {
  const count = revealedCount(activePath.length, step, maxStep);
  const activeNodes = new Set(activePath.slice(0, count));
  const activePairs = new Set(
    activePath.slice(0, Math.max(0, count - 1)).map((id, index) => `${id}>${activePath[index + 1]}`),
  );
  const nodes: CytoscapeNodeSpec[] = rawNodes.map(([id, label]) => ({
    id,
    label,
    active: activeNodes.has(id),
    color: activeNodes.has(id)
      ? (id === activePath[Math.min(count - 1, activePath.length - 1)] ? ACTIVE_END : ACTIVE_NODE)
      : INACTIVE_NODE,
  }));
  const edges: CytoscapeEdgeSpec[] = rawEdges.map(([from, to, label]) => {
    const active = activePairs.has(`${from}>${to}`);
    return { from, to, label, active, color: active ? ACTIVE_EDGE : INACTIVE_EDGE };
  });
  return { engine: 'cytoscape', title, layout, nodes, edges };
}

function pointsToSegments(
  id: string,
  points: ScientificPoint[],
  color: string,
  label: string,
  step: number,
  maxStep: number,
  labelPoint?: ScientificPoint,
): JSXGraphElementSpec[] {
  const visible = Math.min(points.length, revealedCount(points.length, step, maxStep));
  const shown = points.slice(0, visible);
  const segments: JSXGraphElementSpec[] = shown.slice(1).map((point, index) => ({
    id: `${id}-${index}`,
    type: 'segment',
    points: [shown[index], point],
    color,
  }));
  const last = shown[shown.length - 1];
  if (last && visible === points.length) {
    segments.push({ id: `${id}-label`, type: 'text', points: [labelPoint || last], label, color });
  }
  return segments;
}

function samples(fn: (x: number) => number, from = 0, to = 12, count = 49): ScientificPoint[] {
  return Array.from({ length: count }, (_, index) => {
    const x = from + ((to - from) * index) / (count - 1);
    return { x, y: fn(x) };
  });
}

function fullSegments(
  id: string,
  points: ScientificPoint[],
  color: string,
  label?: string,
): JSXGraphElementSpec[] {
  const segments: JSXGraphElementSpec[] = points.slice(1).map((point, index) => ({
    id: `${id}-${index}`,
    type: 'segment',
    points: [points[index], point],
    color,
  }));
  if (label && points.length) {
    segments.push({
      id: `${id}-label`,
      type: 'text',
      points: [points[Math.max(0, points.length - 6)]],
      label,
      color,
    });
  }
  return segments;
}

function pulse(x: number, center: number, amplitude = 2.7): number {
  return amplitude * Math.exp(-Math.pow((x - center) / 0.62, 2));
}

function propagationOndeSpec(variant: string, step: number, maxStep: number): JSXGraphVisualSpec {
  const progress = Math.max(0, Math.min(1, step / maxStep));
  if (variant === 'superposition') {
    const left = 1 + 10 * progress;
    const right = 11 - 10 * progress;
    const first = samples(x => pulse(x, left, 1.55), 0, 12, 73);
    const second = samples(x => pulse(x, right, 1.55), 0, 12, 73);
    const resultant = samples(x => pulse(x, left, 1.55) + pulse(x, right, 1.55), 0, 12, 73);
    return {
      engine: 'jsxgraph',
      title: 'Les perturbations se superposent puis poursuivent leur propagation',
      boundingBox: [-0.7, 4.2, 13.6, -1.3],
      axis: true,
      xLabel: 'x (m)',
      yLabel: 'élongation (m)',
      elements: [
        ...fullSegments('pulse-gauche', first, '#64748b'),
        ...fullSegments('pulse-droite', second, '#64748b'),
        ...fullSegments('resultante', resultant, 'cyan'),
        { id: 'resultante-label', type: 'text', points: [{ x: 6, y: 3.55 }], color: 'cyan', label: 'résultante' },
      ],
    };
  }

  const center = 1 + 10 * progress;
  const profile = samples(x => pulse(x, center), 0, 12, 73);
  const elements: JSXGraphElementSpec[] = [
    ...fullSegments('onde', profile, 'cyan'),
    { id: 'perturbation-label', type: 'text', points: [{ x: center, y: 3.0 }], color: 'cyan', label: 'perturbation' },
    { id: 'sens', type: 'arrow', points: [{ x: 1, y: 3.45 }, { x: 11.4, y: 3.45 }], color: 'green', label: 'sens de propagation' },
  ];
  if (variant === 'retard') {
    const reachedA = center >= 2;
    const reachedB = center >= 9;
    elements.push(
      { id: 'a', type: 'point', points: [{ x: 2, y: 0 }], color: reachedA ? 'orange' : 'white', label: 'A' },
      { id: 'b', type: 'point', points: [{ x: 9, y: 0 }], color: reachedB ? 'orange' : 'white', label: 'B' },
      { id: 'ab', type: 'segment', points: [{ x: 2, y: -0.55 }, { x: 9, y: -0.55 }], color: 'orange', label: 'd = AB' },
      { id: 'tau', type: 'text', points: [{ x: 5.5, y: -1.0 }], color: 'yellow', label: 'τ = d / v' },
    );
  }
  return {
    engine: 'jsxgraph',
    title: variant === 'retard' ? 'Le même signal atteint B après A' : 'Une perturbation se propage sans transport de matière',
    boundingBox: [-0.7, 4.2, 13.6, -1.3],
    axis: true,
    xLabel: 'x (m)',
    yLabel: 'élongation (m)',
    elements,
  };
}

function typesOndesSpec(variant: string, step: number, maxStep: number): JSXGraphVisualSpec {
  const progress = Math.max(0, Math.min(1, step / maxStep));
  const center = 1 + 10 * progress;
  const elements: JSXGraphElementSpec[] = [];
  if (variant !== 'longitudinale') {
    const transverse = samples(x => 2.25 + pulse(x, center, 1.15), 0, 12, 49);
    elements.push(
      ...fullSegments('transverse', transverse, 'cyan'),
      ...transverse.filter((_, index) => index % 4 === 0).map((point, index) => ({
        id: `grain-t-${index}`, type: 'point' as const, points: [point], color: 'cyan',
      })),
      { id: 'label-t', type: 'text', points: [{ x: 6, y: 3.85 }], color: 'cyan', label: 'transversale : déplacement ⟂ propagation' },
      { id: 'arrow-t', type: 'arrow', points: [{ x: 1, y: 1.55 }, { x: 11, y: 1.55 }], color: 'green' },
    );
  }
  if (variant !== 'transversale') {
    const particles = Array.from({ length: 25 }, (_, index) => {
      const restX = index * 0.5;
      const displacement = 0.38 * Math.exp(-Math.pow((restX - center) / 0.9, 2));
      return { x: restX + displacement, y: -1.65 };
    });
    elements.push(
      ...particles.map((point, index) => ({
        id: `grain-l-${index}`, type: 'point' as const, points: [point], color: 'orange',
      })),
      { id: 'label-l', type: 'text', points: [{ x: 6, y: -0.75 }], color: 'orange', label: 'longitudinale : déplacement ∥ propagation' },
      { id: 'arrow-l', type: 'arrow', points: [{ x: 1, y: -2.45 }, { x: 11, y: -2.45 }], color: 'green' },
    );
  }
  return {
    engine: 'jsxgraph',
    title: 'La matière oscille localement ; seule la perturbation se propage',
    boundingBox: [-0.8, 4.5, 13.8, -3.1],
    axis: false,
    elements,
  };
}

function celeriteCordeSpec(variant: string, step: number, maxStep: number): JSXGraphVisualSpec {
  const progress = Math.max(0, Math.min(1, step / maxStep));
  const speedFactors: Record<string, number> = {
    forte_tension: 1.35,
    faible_tension: 0.72,
    forte_masse_lineique: 0.62,
  };
  const descriptions: Record<string, string> = {
    forte_tension: 'T plus grande → v plus grande',
    faible_tension: 'T plus faible → v plus faible',
    forte_masse_lineique: 'μ plus grande → v plus faible',
  };
  const referenceCenter = 1 + 8 * progress;
  const changedCenter = Math.min(11.2, 1 + 8 * (speedFactors[variant] || 1) * progress);
  const reference = samples(x => 2.15 + pulse(x, referenceCenter, 0.9), 0, 12, 61);
  const changed = samples(x => -1.35 + pulse(x, changedCenter, 0.9), 0, 12, 61);
  return {
    engine: 'jsxgraph',
    title: 'Même durée : la distance parcourue révèle la célérité',
    boundingBox: [-0.8, 4.1, 14.8, -3.0],
    axis: false,
    elements: [
      ...fullSegments('corde-reference', reference, 'blue'),
      ...fullSegments('corde-modifiee', changed, 'orange'),
      { id: 'ref-label', type: 'text', points: [{ x: 12.6, y: 2.15 }], color: 'blue', label: 'référence' },
      { id: 'changed-label', type: 'text', points: [{ x: 12.6, y: -1.35 }], color: 'orange', label: descriptions[variant] || 'condition modifiée' },
      { id: 'law', type: 'text', points: [{ x: 6, y: -2.45 }], color: 'yellow', label: 'v = √(T / μ)' },
    ],
  };
}

function facteursCinetiquesSpec(variant: string, step: number, maxStep: number): JSXGraphVisualSpec {
  const factorLabels: Record<string, string> = {
    temperature: 'température plus élevée',
    concentration: 'concentration plus élevée',
    catalyseur: 'avec catalyseur',
    surface_contact: 'surface de contact plus grande',
  };
  const fastRates: Record<string, number> = {
    temperature: 0.52,
    concentration: 0.43,
    catalyseur: 0.68,
    surface_contact: 0.47,
  };
  const reference = samples(t => 10 * (1 - Math.exp(-0.23 * t)), 0, 12, 73);
  const accelerated = samples(t => 10 * (1 - Math.exp(-(fastRates[variant] || 0.5) * t)), 0, 12, 73);
  const time = 12 * Math.max(0, Math.min(1, step / maxStep));
  const refY = 10 * (1 - Math.exp(-0.23 * time));
  const fastY = 10 * (1 - Math.exp(-(fastRates[variant] || 0.5) * time));
  return {
    engine: 'jsxgraph',
    title: 'Le facteur modifie la vitesse, pas l’état final',
    boundingBox: [-0.8, 11.8, 14.5, -1.5],
    axis: true,
    grid: true,
    xLabel: 'temps (min)',
    yLabel: 'avancement (mmol)',
    elements: [
      ...pointsToSegments('reference', reference, 'blue', 'référence', step, maxStep, { x: 10.8, y: 8.8 }),
      ...pointsToSegments('acceleree', accelerated, 'orange', factorLabels[variant] || 'facteur augmenté', step, maxStep, { x: 8.6, y: 10.7 }),
      { id: 'plateau', type: 'segment', points: [{ x: 0, y: 10 }, { x: 12, y: 10 }], color: 'green', dashed: true, label: 'même état final' },
      // Les deux points avancent sur les courbes : leurs noms sont déjà
      // écrits à des positions fixes au bout des courbes. Ne pas rattacher de
      // texte aux marqueurs mobiles évite doublons, déplacement et clignotement.
      { id: 'ref-now', type: 'point', points: [{ x: time, y: refY }], color: 'blue' },
      { id: 'fast-now', type: 'point', points: [{ x: time, y: fastY }], color: 'orange' },
    ],
  };
}

function energieActivationSpec(variant: string, step: number, maxStep: number): JSXGraphVisualSpec {
  const progress = Math.max(0, Math.min(1, step / maxStep));
  const sansCatalyseur = (x: number) => 2 - 0.1 * x + 5.2 * Math.pow(Math.sin(Math.PI * x / 10), 2);
  const avecCatalyseur = (x: number) => 2 - 0.1 * x + 2.7 * Math.pow(Math.sin(Math.PI * x / 10), 2);
  const showWithout = variant !== 'avec_catalyseur';
  const showWith = variant !== 'sans_catalyseur';
  const movingFn = variant === 'sans_catalyseur' ? sansCatalyseur : avecCatalyseur;
  const x = 10 * progress;
  const elements: JSXGraphElementSpec[] = [
    { id: 'reactifs', type: 'text', points: [{ x: 0.7, y: 1.55 }], color: 'white', label: 'Réactifs' },
    { id: 'produits', type: 'text', points: [{ x: 9.3, y: 0.55 }], color: 'white', label: 'Produits' },
    { id: 'delta-r', type: 'segment', points: [{ x: 0, y: 2 }, { x: 1.2, y: 2 }], color: 'white' },
    { id: 'delta-p', type: 'segment', points: [{ x: 8.8, y: 1 }, { x: 10, y: 1 }], color: 'white' },
  ];
  if (showWithout) {
    elements.push(...fullSegments('sans-cat', samples(sansCatalyseur, 0, 10, 73), 'red'));
  }
  if (showWith) {
    elements.push(...fullSegments('avec-cat', samples(avecCatalyseur, 0, 10, 73), 'green'));
  }
  elements.push(
    { id: 'ea', type: 'segment', points: [{ x: 5, y: 2 }, { x: 5, y: variant === 'avec_catalyseur' ? avecCatalyseur(5) : sansCatalyseur(5) }], color: 'yellow', label: 'Ea' },
    { id: 'progress', type: 'point', points: [{ x, y: movingFn(x) }], color: 'orange', label: 'système' },
    { id: 'message', type: 'text', points: [{ x: 5, y: -0.35 }], color: 'cyan', label: 'Le catalyseur abaisse Ea sans changer ΔrH ni l’état final' },
  );
  return {
    engine: 'jsxgraph',
    title: 'Deux chemins réactionnels, mêmes réactifs et produits',
    boundingBox: [-0.8, 8.3, 11.8, -1.0],
    axis: true,
    xLabel: 'coordonnée réactionnelle',
    yLabel: 'énergie relative',
    elements,
  };
}

function oxydoreductionSpec(variant: string, step: number, maxStep: number): RoughSVGVisualSpec {
  const chemins: Record<string, string[]> = {
    transfert_direct: ['reducteur', 'electrons', 'oxydant', 'produits'],
    pile: ['anode', 'electrons', 'circuit', 'cathode', 'reduction'],
    electrolyse: ['generateur', 'anode', 'oxydation', 'electrons', 'cathode', 'reduction'],
  };
  const table: Record<string, StationRuban> = {
    reducteur: { id: 'reducteur', label: 'Réducteur', court: 'Réducteur',
      detail: { value: 'il donne les e⁻', lines: ['son nombre d’oxydation augmente', 'c’est donc lui qui est oxydé'] } },
    electrons: { id: 'electrons', label: 'Électrons', court: 'e⁻',
      detail: { value: 'jamais libres en solution', lines: ['ils passent directement d’une espèce à l’autre'] } },
    oxydant: { id: 'oxydant', label: 'Oxydant', court: 'Oxydant',
      detail: { value: 'il capte les e⁻', lines: ['son nombre d’oxydation diminue', 'c’est donc lui qui est réduit'] } },
    produits: { id: 'produits', label: 'Produits redox', court: 'Produits',
      detail: { value: 'les deux couples ont échangé', lines: ['oxydation et réduction sont simultanées'] } },
    anode: { id: 'anode', label: 'Anode', court: 'Anode',
      detail: { value: 'siège de l’oxydation', lines: ['pôle − dans une pile', 'pôle + dans une électrolyse'] } },
    circuit: { id: 'circuit', label: 'Circuit extérieur', court: 'Circuit',
      detail: { value: 'le courant électrique', lines: ['les e⁻ y circulent, en sens inverse du courant'] } },
    cathode: { id: 'cathode', label: 'Cathode', court: 'Cathode',
      detail: { value: 'siège de la réduction', lines: ['l’électrode où arrivent les électrons'] } },
    reduction: { id: 'reduction', label: 'Espèce réduite', court: 'Réduite',
      detail: { value: 'elle a capté les e⁻', lines: ['c’est le produit de la cathode'] } },
    generateur: { id: 'generateur', label: 'Générateur', court: 'Générateur',
      detail: { value: 'il impose le sens', lines: ['l’électrolyse est une transformation forcée'] } },
    oxydation: { id: 'oxydation', label: 'Espèce oxydée', court: 'Oxydée',
      detail: { value: 'elle a cédé ses e⁻', lines: ['c’est le produit de l’anode'] } },
  };
  const libelles: Record<string, string> = {
    'reducteur>electrons': 'oxydation', 'electrons>oxydant': 'transfert direct',
    'oxydant>produits': 'réduction', 'anode>electrons': 'e⁻ libérés',
    'electrons>circuit': 'courant', 'circuit>cathode': 'e⁻ reçus',
    'cathode>reduction': 'réduction', 'generateur>anode': 'impose le sens',
    'anode>oxydation': 'oxydation forcée', 'oxydation>electrons': 'e⁻ arrachés',
    'electrons>cathode': 'vers la cathode',
  };
  const chemin = chemins[variant] || chemins.transfert_direct;
  return rubanSpec(
    variant === 'pile' ? 'Pile : réaction spontanée et courant électrique'
      : variant === 'electrolyse' ? 'Électrolyse : transformation imposée par le générateur'
        : 'Oxydation et réduction sont simultanées',
    chemin.map(id => table[id]),
    transitionsSuivant(chemin, libelles),
    step, maxStep,
  );
}

function levuresSpec(variant: string, step: number, maxStep: number): JSXGraphVisualSpec {
  const avecOxygene = [
    { id: 'o2-aero', label: 'O₂ avec O₂', color: 'cyan', points: samples(x => 18 - 0.8 * x), labelPoint: { x: 6.5, y: 13.6 } },
    { id: 'co2-aero', label: 'CO₂ avec O₂', color: 'green', points: samples(x => 2 + 0.75 * x), labelPoint: { x: 8.2, y: 9.2 } },
    { id: 'eth-aero', label: 'Éthanol avec O₂', color: 'purple', points: samples(() => 0.8), labelPoint: { x: 4.3, y: 1.55 } },
  ];
  const sansOxygene = [
    { id: 'o2-ana', label: 'O₂ sans O₂', color: 'blue', points: samples(() => 0.5), labelPoint: { x: 11.2, y: 1.5 } },
    { id: 'co2-ana', label: 'CO₂ sans O₂', color: 'orange', points: samples(x => 2 + 0.45 * x), labelPoint: { x: 5.6, y: 5.3 } },
    { id: 'eth-ana', label: 'Éthanol sans O₂', color: 'red', points: samples(x => 0.8 + 0.62 * x), labelPoint: { x: 11.2, y: 8.5 } },
  ];
  const selected = variant === 'avec_oxygene'
    ? avecOxygene
    : variant === 'sans_oxygene'
      ? sansOxygene
      : [...avecOxygene, ...sansOxygene];
  return {
    engine: 'jsxgraph',
    title: 'Évolution relative des substances chez les levures',
    boundingBox: [-0.7, 21, 15.8, -1.8],
    axis: true,
    grid: true,
    xLabel: 'Temps (min)',
    yLabel: 'Valeur relative (u.a.)',
    elements: selected.flatMap(series => pointsToSegments(
      series.id, series.points, series.color, series.label, step, maxStep, series.labelPoint,
    )),
  };
}

function twitch(t: number, onset: number): number {
  const z = t - onset;
  return z <= 0 ? 0 : 8.2 * z * Math.exp(-1.75 * z);
}

function myogramPoints(variant: string): ScientificPoint[] {
  const onsets = variant === 'secousse' ? [1]
    : variant === 'sommation' ? [1, 2.1]
      : variant === 'tetanus_incomplet' ? [1, 1.85, 2.7, 3.55, 4.4, 5.25, 6.1]
        : Array.from({ length: 25 }, (_, index) => 1 + index * 0.24);
  return samples(
    time => Math.min(7.3, onsets.reduce((force, onset) => force + twitch(time, onset), 0)),
    0, 8, 97,
  );
}

function myogramSpec(variant: string, step: number, maxStep: number): JSXGraphVisualSpec {
  const label = SCIENTIFIC_PRESETS.svt_ch1_myogrammes.variants.find(v => v.id === variant)?.label || 'Myogramme';
  return {
    engine: 'jsxgraph',
    title: label,
    boundingBox: [-0.5, 8.5, 9, -0.8],
    axis: true,
    grid: true,
    xLabel: 'Temps (u.a.)',
    yLabel: 'Tension musculaire (u.a.)',
    elements: [
      ...pointsToSegments('myogramme', myogramPoints(variant), 'orange', label, step, maxStep),
      ...(variant === 'secousse' ? [
        { id: 'stimulus', type: 'arrow' as const, points: [{ x: 0.75, y: -0.55 }, { x: 0.75, y: 0 }], color: 'yellow' },
        { id: 'latence', type: 'text' as const, points: [{ x: 0.8, y: 0.65 }], label: 'Latence', color: 'yellow' },
        { id: 'contraction', type: 'text' as const, points: [{ x: 1.5, y: 2.7 }], label: 'Contraction', color: 'orange' },
        { id: 'relachement', type: 'text' as const, points: [{ x: 4, y: 1.5 }], label: 'Relâchement', color: 'cyan' },
      ] : []),
    ],
  };
}

function muscleHeatSpec(variant: string, step: number, maxStep: number): JSXGraphVisualSpec {
  const twitchCurve = samples(t => 5.5 * Math.exp(-Math.pow((t - 2.1) / 0.68, 2)), 0, 8, 81);
  const initialHeat = samples(t => 2.7 * Math.exp(-Math.pow((t - 2.6) / 1.0, 2)), 0, 8, 81);
  const delayedWithOxygen = samples(t => 1.7 * Math.exp(-Math.pow((t - 5.8) / 1.25, 2)), 0, 8, 81);
  const delayedWithoutOxygen = samples(t => 0.25 * Math.exp(-Math.pow((t - 5.8) / 1.25, 2)), 0, 8, 81);
  const elements = [
    ...pointsToSegments('secousse', twitchCurve, 'orange', 'Tension musculaire', step, maxStep),
    ...pointsToSegments('initiale', initialHeat, 'red', 'Chaleur initiale', step, maxStep),
  ];
  if (variant !== 'sans_oxygene') {
    elements.push(...pointsToSegments('retardee-o2', delayedWithOxygen, 'cyan', 'Chaleur retardée avec O₂', step, maxStep));
  }
  if (variant !== 'avec_oxygene') {
    elements.push(...pointsToSegments('retardee-sans-o2', delayedWithoutOxygen, 'purple', 'Chaleur retardée sans O₂', step, maxStep));
  }
  return {
    engine: 'jsxgraph',
    title: 'La chaleur retardée dépend des réactions oxydatives de récupération',
    boundingBox: [-0.5, 6.5, 8.7, -0.8],
    axis: true,
    grid: true,
    xLabel: 'Temps (u.a.)',
    yLabel: 'Valeur relative (u.a.)',
    elements,
  };
}

function atpSpec(variant: string, step: number, maxStep: number): RoughSVGVisualSpec {
  const chemins: Record<string, string[]> = {
    hydrolyse: ['atp', 'travail', 'adp'],
    regeneration: ['adp', 'nutriments', 'atp'],
    cycle_complet: ['nutriments', 'adp', 'atp', 'travail'],
  };
  const table: Record<string, StationRuban> = {
    nutriments: { id: 'nutriments', label: 'Énergie des nutriments', court: 'Nutriments',
      detail: { value: '2860 kJ par mole de glucose', lines: ['dont 40,5 % seulement passent dans l’ATP'] } },
    adp: { id: 'adp', label: 'ADP + Pi', court: 'ADP + Pi',
      detail: { value: 'la forme déchargée', lines: ['la respiration la recharge en continu'] } },
    atp: { id: 'atp', label: 'ATP', court: 'ATP',
      detail: { value: 'la monnaie de la cellule', lines: ['le stock ne tient que quelques secondes', 'il est refait aussitôt que dépensé'] } },
    travail: { id: 'travail', label: 'Travail cellulaire', court: 'Travail',
      detail: { value: 'contraction, transport, synthèses', lines: ['toutes payées par l’hydrolyse de l’ATP'] } },
  };
  const libelles: Record<string, string> = {
    'nutriments>adp': 'énergie libérée', 'adp>atp': 'phosphorylation',
    'atp>travail': 'hydrolyse', 'travail>nutriments': 'il faut recharger',
    'atp>adp': 'ATP → ADP + Pi', 'travail>adp': 'après transfert', 'adp>nutriments': 'recharge',
  };
  const chemin = chemins[variant] || chemins.cycle_complet;
  const boucle = chemin === chemins.cycle_complet;
  const suite = boucle ? [...chemin, chemin[0]] : chemin;
  return rubanSpec(
    'L’ATP transfère l’énergie aux activités cellulaires',
    chemin.map(id => table[id]),
    transitionsSuivant(suite, libelles),
    step, maxStep, boucle,
  );
}

function glycolyseEtapesSpec(_variant: string, step: number, maxStep: number): RoughSVGVisualSpec {
  return rubanSpec(
    'Glycolyse : 2 ATP nets et 2 NADH,H⁺ par glucose',
    [
      { id: 'glucose', label: 'Glucose 6C', court: 'Glucose',
        detail: { value: '6 carbones', lines: ['le point de départ, dans le cytoplasme'] } },
      { id: 'g6p', label: 'Glucose-6-phosphate', court: 'G6P',
        detail: { value: '1er ATP dépensé', lines: ['le phosphate piège le glucose dans la cellule'] } },
      { id: 'f6p', label: 'Fructose-6-phosphate', court: 'F6P',
        detail: { value: 'simple isomérisation', lines: ['même formule brute, autre structure'] } },
      { id: 'f16bp', label: 'Fructose-1,6-bisphosphate', court: 'F1,6BP',
        detail: { value: '2 ATP dépensés en tout', lines: ['fin de la phase d’investissement', 'la cellule paie avant de gagner'] } },
      { id: 'trioses', label: '2 trioses phosphate 3C', court: '2 × 3C',
        detail: { value: '6C → 2 × 3C', lines: ['tout ce qui suit compte double'] } },
      { id: 'bpg', label: '2 bisphosphoglycérates', court: '2 × BPG',
        detail: { value: '2 NADH,H⁺ formés', lines: ['ils partiront vers la chaîne respiratoire'] } },
      { id: 'pg3', label: '2 phosphoglycérates 3', court: '2 × 3PG',
        detail: { value: '2 ATP produits', lines: ['la cellule commence à être remboursée'] } },
      { id: 'pg2', label: '2 phosphoglycérates 2', court: '2 × 2PG',
        detail: { value: 'le phosphate se déplace', lines: ['préparation de la dernière étape'] } },
      { id: 'pep', label: '2 phosphoénolpyruvates', court: '2 × PEP',
        detail: { value: 'liaison très instable', lines: ['c’est elle qui rendra le dernier ATP'] } },
      { id: 'pyruvate', label: '2 pyruvates 3C', court: 'Pyruvate',
        detail: { value: 'bilan : 2 ATP nets', lines: ['4 ATP produits moins 2 investis', 'et 2 NADH,H⁺'] } },
    ],
    [
      '1 · ATP → ADP', '2 · isomérisation', '3 · ATP → ADP', '4–5 · scission',
      '6 · 2 NAD⁺ → 2 NADH', '7 · 2 ADP → 2 ATP', '8 · mutase', '9 · − 2 H₂O', '10 · 2 ADP → 2 ATP',
    ],
    step, maxStep,
  );
}

function krebsDetailleSpec(_variant: string, step: number, maxStep: number): CytoscapeVisualSpec {
  const nodes: Array<[string, string]> = [
    ['acetyl', 'Acétyl-CoA 2C'], ['citrate', 'Citrate 6C'], ['isocitrate', 'Isocitrate 6C'],
    ['c5', 'α-cétoglutarate 5C'], ['succinyl', 'Succinyl-CoA 4C'], ['succinate', 'Succinate 4C'],
    ['fumarate', 'Fumarate 4C'], ['malate', 'Malate 4C'], ['oxaloacetate', 'Oxaloacétate 4C'],
    ['bilan', 'Par tour : 2 CO₂ · 3 NADH,H⁺ · 1 FADH₂ · 1 GTP ≈ ATP'],
  ];
  const edges: Array<[string, string, string?]> = [
    ['acetyl', 'citrate', '+ oxaloacétate + H₂O ; sortie CoA-SH'], ['citrate', 'isocitrate', 'isomérisation'],
    ['isocitrate', 'c5', 'NAD⁺ → NADH,H⁺ ; sortie CO₂'], ['c5', 'succinyl', 'NAD⁺ + CoA-SH → NADH,H⁺ ; sortie CO₂'],
    ['succinyl', 'succinate', 'GDP + Pi → GTP ; sortie CoA-SH'], ['succinate', 'fumarate', 'FAD → FADH₂'],
    ['fumarate', 'malate', '+ H₂O'], ['malate', 'oxaloacetate', 'NAD⁺ → NADH,H⁺'],
    ['oxaloacetate', 'citrate', 'nouveau tour'], ['oxaloacetate', 'bilan', 'bilan d’un tour'],
  ];
  return processSpec('Cycle de Krebs dans la matrice', 'circle', nodes, edges,
    ['acetyl', 'citrate', 'isocitrate', 'c5', 'succinyl', 'succinate', 'fumarate', 'malate', 'oxaloacetate', 'bilan'], step, maxStep);
}

/**
 * L'encart de réponse des planches interrogeables. Même invite partout :
 * l'élève apprend le geste une fois et le rejoue sur toutes les figures.
 */
function panneauQuestion(x: number, y: number, width: number, height: number): RoughSVGHotspotPanelSpec {
  return { x, y, width, height, hint: 'Clique sur un « ? » pour le détail' };
}

/**
 * L'escalier des électrons. La chaîne respiratoire n'est pas un nuage de
 * points dans un repère : c'est une descente. La HAUTEUR d'une marche est
 * l'énergie libérée, proportionnelle au ΔE°′ réel (360, 210 puis 570 mV) ;
 * trois marches, trois complexes qui pompent des H⁺. Les millivolts restent
 * en légende sous chaque palier, sans axe ni grille.
 */
function echelleRedoxSpec(_variant: string, step: number, _maxStep: number): RoughSVGVisualSpec {
  const INK = '#e0f2fe';
  const MEMBRANE = '#fbbf24';
  const PROTON = '#c084fc';
  const ELECTRON = '#fde047';
  const PUMP_OFF = '#64748b';
  const PUMP_ON = '#f472b6';
  const OXY = '#22d3ee';
  const WATER = '#86efac';
  const current = Math.max(0, Math.min(8, Math.round(step)));

  const landings = [
    { x0: 90, x1: 270, y: 105, name: 'NADH,H⁺', mv: 'E°′ = −320 mV' },
    { x0: 330, x1: 500, y: 209, name: 'Q / QH₂', mv: 'E°′ = +40 mV' },
    { x0: 560, x1: 700, y: 270, name: 'cyt c', mv: 'E°′ = +250 mV' },
    { x0: 760, x1: 900, y: 435, name: 'O₂, accepteur final', mv: 'E°′ = +820 mV' },
  ];
  // Une pompe par marche : le complexe se lit à l'endroit exact de la chute.
  const pumps = [
    { x: 300, y: 157, label: 'Complexe I', from: 2 },
    { x: 530, y: 240, label: 'Complexe III', from: 4 },
    { x: 730, y: 352, label: 'Complexe IV', from: 6 },
  ];
  const spots = [
    { x: 130, y: 105 }, { x: 250, y: 105 }, { x: 300, y: 157 }, { x: 420, y: 209 },
    { x: 530, y: 240 }, { x: 640, y: 270 }, { x: 730, y: 352 }, { x: 820, y: 435 },
    { x: 820, y: 435 },
  ];

  const stairs: ScientificPoint[] = landings.flatMap(l => [{ x: l.x0, y: l.y }, { x: l.x1, y: l.y }]);

  // Décor : même longueur et même ordre à chaque étape, sinon les traits
  // crayonnés se retirent au sort d'une image à l'autre et la figure tremble.
  const el: RoughSVGElementSpec[] = [
    { id: 'espace-txt', type: 'text', x: 470, y: 28, text: 'Espace intermembranaire : les H⁺ s’y entassent', color: PROTON, fontSize: 18, align: 'middle' },
    { id: 'escalier', type: 'polyline', points: stairs, color: MEMBRANE, strokeWidth: 6 },
    { id: 'matrice-txt', type: 'text', x: 120, y: 470, text: 'Matrice', color: '#7dd3fc', fontSize: 19, align: 'start' },
  ];

  landings.forEach((l, i) => {
    const mid = (l.x0 + l.x1) / 2;
    el.push(
      { id: `pal-n-${i}`, type: 'text', x: mid, y: l.y + 30, text: l.name, color: i === 3 ? OXY : INK, fontSize: 21, align: 'middle' },
      { id: `pal-mv-${i}`, type: 'text', x: mid, y: l.y + 52, text: l.mv, color: '#94a3b8', fontSize: 15, align: 'middle' },
    );
  });

  pumps.forEach((p, i) => {
    const on = current >= p.from;
    el.push(
      { id: `pompe-${i}`, type: 'rect', x: p.x - 32, y: p.y - 23, width: 64, height: 46, color: on ? PUMP_ON : PUMP_OFF, fill: on ? '#500724' : '#1e293b', strokeWidth: 4 },
      { id: `pompe-t-${i}`, type: 'text', x: p.x + 42, y: p.y + 6, text: p.label, color: on ? PUMP_ON : PUMP_OFF, fontSize: 17, align: 'start' },
    );
  });

  // Ce que la chute produit : des H⁺ montés dans l'espace intermembranaire.
  pumps.forEach((p, i) => {
    if (current < p.from) return;
    el.push({ id: `h-fleche-${i}`, type: 'arrow', points: [{ x: p.x, y: p.y - 28 }, { x: p.x, y: 80 }], color: PROTON, strokeWidth: 3, dashed: true });
    for (let k = 0; k < 3; k += 1) {
      el.push({ id: `h-${i}-${k}`, type: 'circle', x: p.x - 30 + k * 30, y: 58, radius: 9, color: PROTON, fill: '#3b0764', strokeWidth: 2 });
    }
  });

  const spot = spots[current];
  el.push(
    { id: 'e-corps', type: 'circle', x: spot.x, y: spot.y - 18, radius: 15, color: '#78350f', fill: ELECTRON, strokeWidth: 3 },
    { id: 'e-oeil-g', type: 'circle', x: spot.x - 5, y: spot.y - 22, radius: 2, color: '#78350f', fill: '#78350f', strokeWidth: 1 },
    { id: 'e-oeil-d', type: 'circle', x: spot.x + 5, y: spot.y - 22, radius: 2, color: '#78350f', fill: '#78350f', strokeWidth: 1 },
    { id: 'e-txt', type: 'text', x: spot.x, y: spot.y - 42, text: 'e⁻', color: ELECTRON, fontSize: 20, align: 'middle' },
  );

  if (current >= 7) {
    el.push(
      { id: 'eau', type: 'ellipse', x: 922, y: 396, radiusX: 27, radiusY: 21, color: WATER, fill: '#064e3b', strokeWidth: 3 },
      { id: 'eau-t', type: 'text', x: 922, y: 403, text: 'H₂O', color: WATER, fontSize: 17, align: 'middle' },
    );
  }
  if (current >= 8) {
    el.push({ id: 'bilan', type: 'text', x: 340, y: 500, text: 'Marche haute = beaucoup d’énergie libérée', color: ELECTRON, fontSize: 20, align: 'middle' });
  }

  const recits = [
    'Un électron riche en énergie arrive du NADH,H⁺ : il est tout en haut de l’escalier.',
    'Sur un palier il ne perd rien : c’est en tombant, pas en avançant, qu’il libère de l’énergie.',
    'Première marche : la chute traverse le complexe I, qui pompe des H⁺ vers l’espace intermembranaire.',
    'L’électron se pose sur le transporteur Q, un cran plus bas en énergie.',
    'Deuxième marche, la plus courte : le complexe III libère moins d’énergie.',
    'Palier du cytochrome c : l’électron attend la dernière chute.',
    'Troisième marche, la plus haute : le complexe IV libère le plus d’énergie de toute la chaîne.',
    'En bas, le dioxygène récupère l’électron : il devient de l’eau. C’est l’accepteur final.',
    'Bilan : la hauteur d’une marche est l’énergie libérée, et elle sert à entasser les H⁺ en haut.',
  ];

  return {
    engine: 'roughsvg',
    title: 'L’escalier des électrons : du NADH au dioxygène',
    width: 960,
    height: 540,
    description: recits[current],
    elements: el,
    // Chaque marche se laisse interroger : le ΔE°′ n'encombre pas le dessin,
    // il attend la question. La zone couvre la chute ET son complexe.
    hotspots: [
      { id: 'marche-1', x: 256, y: 98, width: 88, height: 118, color: PUMP_ON,
        label: 'Marche 1 — complexe I', value: 'ΔE°′ = + 360 mV',
        lines: ['NADH,H⁺ (−320 mV) → Q (+40 mV)', 'de quoi pomper des H⁺'] },
      { id: 'marche-2', x: 486, y: 202, width: 88, height: 76, color: PUMP_ON,
        label: 'Marche 2 — complexe III', value: 'ΔE°′ = + 210 mV',
        lines: ['Q (+40 mV) → cyt c (+250 mV)', 'la plus courte des trois'] },
      { id: 'marche-3', x: 686, y: 263, width: 88, height: 180, color: PUMP_ON,
        label: 'Marche 3 — complexe IV', value: 'ΔE°′ = + 570 mV',
        lines: ['cyt c (+250 mV) → O₂ (+820 mV)', 'la plus haute : le plus d’énergie'] },
    ],
    hotspotPanel: panneauQuestion(58, 292, 352, 124),
    legend: [
      { color: ELECTRON, label: 'électron' },
      { color: MEMBRANE, label: 'membrane interne' },
      { color: PUMP_ON, label: 'complexe qui pompe' },
      { color: PROTON, label: 'H⁺' },
    ],
  };
}

function ultrastructureMitochondrieSpec(_variant: string, step: number, _maxStep: number): RoughSVGVisualSpec {
  const INK = '#e0f2fe';
  const OUTER = '#22d3ee';
  const INNER = '#fbbf24';
  const SPACE = '#c084fc';
  const MATRIX = '#0c4a6e';
  const FOCUS = '#fde047';
  const safeStep = Math.max(0, Math.min(4, Math.round(step)));

  const el: RoughSVGElementSpec[] = [
    // Coupe principale, volontairement grande et limitée aux compartiments utiles.
    { id: 'outer', type: 'ellipse', x: 330, y: 270, radiusX: 285, radiusY: 170, color: OUTER, fill: '#082f49', strokeWidth: 4 },
    { id: 'inner', type: 'ellipse', x: 330, y: 270, radiusX: 255, radiusY: 140, color: INNER, fill: MATRIX, strokeWidth: 4 },
  ];

  const crests: ScientificPoint[][] = [];
  for (let i = 0; i < 5; i += 1) {
    const x = 145 + i * 82;
    const points = [
      { x, y: 137 }, { x: x + 38, y: 202 }, { x, y: 270 },
      { x: x + 38, y: 338 }, { x, y: 403 },
    ];
    crests.push(points);
    el.push({ id: `crest-${i}`, type: 'polyline', color: INNER, strokeWidth: 4, points });
  }

  // Repères courts : aucune donnée chiffrée dans l'image.
  el.push(
    { type: 'arrow', color: OUTER, strokeWidth: 2, points: [{ x: 78, y: 78 }, { x: 125, y: 116 }] },
    { type: 'text', x: 70, y: 64, text: 'Membrane externe', color: INK, fontSize: 18, align: 'start' },
    { type: 'arrow', color: INNER, strokeWidth: 2, points: [{ x: 98, y: 466 }, { x: 155, y: 395 }] },
    { type: 'text', x: 72, y: 492, text: 'Membrane interne + crêtes', color: INK, fontSize: 18, align: 'start' },
    { type: 'arrow', color: SPACE, strokeWidth: 2, points: [{ x: 520, y: 76 }, { x: 555, y: 132 }] },
    { type: 'text', x: 450, y: 60, text: 'Espace intermembranaire', color: INK, fontSize: 18, align: 'start' },
    { type: 'arrow', color: '#38bdf8', strokeWidth: 2, points: [{ x: 525, y: 466 }, { x: 470, y: 360 }] },
    { type: 'text', x: 510, y: 492, text: 'Matrice', color: INK, fontSize: 18, align: 'start' },
  );

  const anchors = [
    { x: 600, y: 205, label: 'Vue d’ensemble' },
    { x: 595, y: 188, label: 'Membrane externe' },
    { x: 485, y: 270, label: 'Membrane interne et crêtes' },
    { x: 570, y: 150, label: 'Espace intermembranaire' },
    { x: 455, y: 335, label: 'Matrice' },
  ];
  const focus = anchors[safeStep];

  if (safeStep === 1) {
    el.push({ type: 'ellipse', x: 330, y: 270, radiusX: 285, radiusY: 170, color: FOCUS, strokeWidth: 7 });
  } else if (safeStep === 2) {
    el.push({ type: 'ellipse', x: 330, y: 270, radiusX: 255, radiusY: 140, color: FOCUS, strokeWidth: 7 });
    el.push({ type: 'polyline', color: FOCUS, strokeWidth: 7, points: crests[4] });
  } else if (safeStep === 3) {
    el.push({ type: 'ellipse', x: 330, y: 270, radiusX: 270, radiusY: 155, color: FOCUS, strokeWidth: 7, dashed: true });
  } else if (safeStep === 4) {
    el.push({ type: 'ellipse', x: 330, y: 270, radiusX: 205, radiusY: 105, color: FOCUS, strokeWidth: 6, dashed: true });
  }

  // Loupe pédagogique : son contenu change à chaque étape, sans ajouter de texte documentaire.
  el.push(
    { type: 'arrow', color: FOCUS, strokeWidth: 3, dashed: true, points: [{ x: focus.x, y: focus.y }, { x: 676, y: 242 }] },
    { type: 'circle', x: 810, y: 260, radius: 132, color: FOCUS, fill: '#06202e', strokeWidth: 5 },
  );

  if (safeStep === 0) {
    el.push(
      { type: 'ellipse', x: 810, y: 255, radiusX: 92, radiusY: 54, color: OUTER, fill: '#082f49', strokeWidth: 4 },
      { type: 'ellipse', x: 810, y: 255, radiusX: 76, radiusY: 39, color: INNER, fill: MATRIX, strokeWidth: 4 },
      { type: 'polyline', color: INNER, strokeWidth: 4, points: [{ x: 775, y: 219 }, { x: 798, y: 255 }, { x: 775, y: 291 }] },
      { type: 'polyline', color: INNER, strokeWidth: 4, points: [{ x: 820, y: 217 }, { x: 844, y: 255 }, { x: 820, y: 293 }] },
    );
  } else if (safeStep === 1) {
    el.push(
      { type: 'polyline', color: FOCUS, strokeWidth: 8, points: [{ x: 710, y: 235 }, { x: 760, y: 205 }, { x: 815, y: 202 }, { x: 870, y: 220 }, { x: 910, y: 250 }] },
      { type: 'polyline', color: OUTER, strokeWidth: 3, points: [{ x: 710, y: 257 }, { x: 760, y: 227 }, { x: 815, y: 224 }, { x: 870, y: 242 }, { x: 910, y: 272 }] },
    );
  } else if (safeStep === 2) {
    el.push(
      { type: 'polyline', color: INNER, strokeWidth: 9, points: [{ x: 716, y: 190 }, { x: 770, y: 255 }, { x: 730, y: 327 }] },
      { type: 'polyline', color: INNER, strokeWidth: 9, points: [{ x: 792, y: 185 }, { x: 850, y: 255 }, { x: 804, y: 330 }] },
      { type: 'polyline', color: INNER, strokeWidth: 9, points: [{ x: 862, y: 198 }, { x: 902, y: 255 }, { x: 870, y: 315 }] },
    );
  } else if (safeStep === 3) {
    el.push(
      { type: 'polyline', color: OUTER, strokeWidth: 7, points: [{ x: 715, y: 215 }, { x: 810, y: 190 }, { x: 905, y: 215 }] },
      { type: 'polyline', color: INNER, strokeWidth: 7, points: [{ x: 720, y: 298 }, { x: 810, y: 273 }, { x: 900, y: 298 }] },
      { type: 'text', x: 810, y: 248, text: 'espace', color: SPACE, fontSize: 22, align: 'middle' },
    );
  } else {
    el.push(
      { type: 'ellipse', x: 810, y: 260, radiusX: 103, radiusY: 78, color: '#38bdf8', fill: MATRIX, strokeWidth: 4 },
      { type: 'circle', x: 770, y: 240, radius: 9, color: INK, fill: '#38bdf8' },
      { type: 'circle', x: 825, y: 225, radius: 9, color: INK, fill: '#38bdf8' },
      { type: 'circle', x: 850, y: 280, radius: 9, color: INK, fill: '#38bdf8' },
      { type: 'circle', x: 785, y: 295, radius: 9, color: INK, fill: '#38bdf8' },
    );
  }

  el.push(
    { type: 'text', x: 810, y: 430, text: safeStep === 0 ? 'Vue d’ensemble' : `Zoom ${safeStep}/4`, color: FOCUS, fontSize: 19, align: 'middle' },
    { type: 'text', x: 810, y: 458, text: focus.label, color: INK, fontSize: 20, align: 'middle' },
  );

  return {
    engine: 'roughsvg',
    title: 'Zoom sur la mitochondrie',
    width: 960,
    height: 530,
    description: 'Coupe agrandie et zoom progressif sur les compartiments essentiels de la mitochondrie.',
    elements: el,
  };
}

function pyruvateAcetylCoaSpec(_variant: string, step: number, _maxStep: number): RoughSVGVisualSpec {
  const current = Math.max(0, Math.min(8, Math.round(step)));
  const elements: RoughSVGElementSpec[] = [
    { id: 'zone-cyto', type: 'text', x: 105, y: 45, text: 'Cytoplasme', color: '#67e8f9', fontSize: 24, align: 'middle' },
    { id: 'mito-title', type: 'text', x: 625, y: 40, text: 'Mitochondrie', color: '#fef08a', fontSize: 26, align: 'middle' },
    { id: 'outer', type: 'ellipse', x: 620, y: 240, radiusX: 270, radiusY: 185, color: '#e2e8f0', fill: '#102a2a', strokeWidth: 4 },
    { id: 'inner', type: 'ellipse', x: 620, y: 240, radiusX: 235, radiusY: 150, color: '#94a3b8', strokeWidth: 3 },
    { id: 'crest-1', type: 'polyline', points: [{ x: 485, y: 115 }, { x: 520, y: 155 }, { x: 555, y: 120 }, { x: 585, y: 155 }], color: '#94a3b8', strokeWidth: 3 },
    { id: 'crest-2', type: 'polyline', points: [{ x: 690, y: 115 }, { x: 720, y: 160 }, { x: 755, y: 125 }, { x: 785, y: 165 }], color: '#94a3b8', strokeWidth: 3 },
    { id: 'crest-3', type: 'polyline', points: [{ x: 680, y: 365 }, { x: 715, y: 325 }, { x: 750, y: 365 }, { x: 785, y: 325 }], color: '#94a3b8', strokeWidth: 3 },
    { id: 'matrix-label', type: 'text', x: 625, y: 92, text: 'Matrice', color: '#86efac', fontSize: 20, align: 'middle' },
  ];
  const carbon = (id: string, x: number, y: number, count: number, color: string, label: string): RoughSVGElementSpec[] => {
    const result: RoughSVGElementSpec[] = [];
    for (let i = 0; i < count; i += 1) {
      result.push({ id: `${id}-c${i}`, type: 'circle', x: x + i * 38, y, radius: 17, color, fill: '#0f172a' });
      result.push({ id: `${id}-t${i}`, type: 'text', x: x + i * 38, y: y + 6, text: 'C', color: 'white', fontSize: 16, align: 'middle' });
    }
    result.push({ id: `${id}-label`, type: 'text', x: x + (count - 1) * 19, y: y + 47, text: label, color, fontSize: 18, align: 'middle' });
    return result;
  };
  const messages = [
    '1 · La glycolyse fournit un pyruvate à 3 carbones dans le cytoplasme.',
    '2 · Le pyruvate se dirige vers la mitochondrie.',
    '3 · Il franchit les membranes grâce à des protéines de transport.',
    '4 · Le pyruvate atteint la matrice mitochondriale.',
    '5 · Décarboxylation : un carbone quitte la molécule sous forme de CO₂.',
    '6 · Oxydation : NAD⁺ capte des électrons et devient NADH,H⁺.',
    '7 · La coenzyme A se fixe au groupement acétyle à 2 carbones.',
    '8 · L’acétyl-CoA est prêt à alimenter le cycle de Krebs.',
    'Bilan par pyruvate : 1 acétyl-CoA + 1 CO₂ + 1 NADH,H⁺.',
  ];

  if (current === 0) elements.push(...carbon('pyr-cyto', 115, 230, 3, '#fb7185', 'Pyruvate · 3C'));
  if (current === 1) {
    elements.push({ id: 'travel-1', type: 'arrow', points: [{ x: 215, y: 230 }, { x: 330, y: 230 }], color: '#fb7185', strokeWidth: 4 });
    elements.push(...carbon('pyr-outer', 270, 230, 3, '#fb7185', 'Pyruvate · 3C'));
  }
  if (current === 2) {
    elements.push({ id: 'transport', type: 'rect', x: 345, y: 190, width: 65, height: 82, color: '#22d3ee', fill: '#164e63' });
    elements.push({ id: 'transport-label', type: 'text', x: 377, y: 180, text: 'transporteur', color: '#67e8f9', fontSize: 16, align: 'middle' });
    elements.push({ id: 'travel-2', type: 'arrow', points: [{ x: 290, y: 230 }, { x: 450, y: 230 }], color: '#fb7185', strokeWidth: 4 });
    elements.push(...carbon('pyr-cross', 395, 230, 3, '#fb7185', 'Pyruvate · 3C'));
  }
  if (current === 3) elements.push(...carbon('pyr-matrix', 480, 230, 3, '#fb7185', 'Pyruvate dans la matrice'));
  if (current >= 4) {
    elements.push(...carbon('acetyl-2c', 500, 230, 2, '#fbbf24', current >= 6 ? 'Acétyl-CoA · 2C' : 'Résidu à 2C'));
    elements.push({ id: 'co2-arrow', type: 'arrow', points: [{ x: 560, y: 205 }, { x: 625, y: 145 }], color: '#f97316', strokeWidth: 3 });
    elements.push({ id: 'co2', type: 'circle', x: 650, y: 125, radius: 28, color: '#f97316', fill: '#7c2d12' });
    elements.push({ id: 'co2-label', type: 'text', x: 650, y: 132, text: 'CO₂', color: 'white', fontSize: 18, align: 'middle' });
  }
  if (current >= 5) {
    elements.push({ id: 'nad', type: 'text', x: 500, y: 340, text: 'NAD⁺', color: '#c084fc', fontSize: 20, align: 'middle' });
    elements.push({ id: 'nad-arrow', type: 'arrow', points: [{ x: 540, y: 334 }, { x: 650, y: 334 }], color: '#c084fc', strokeWidth: 3 });
    elements.push({ id: 'nadh', type: 'text', x: 720, y: 340, text: 'NADH,H⁺', color: '#e9d5ff', fontSize: 20, align: 'middle' });
  }
  if (current >= 6) {
    elements.push({ id: 'coa', type: 'text', x: 455, y: 170, text: 'CoA', color: '#22c55e', fontSize: 21, align: 'middle' });
    elements.push({ id: 'coa-arrow', type: 'arrow', points: [{ x: 470, y: 180 }, { x: 505, y: 207 }], color: '#22c55e', strokeWidth: 3 });
  }
  if (current >= 7) {
    elements.push({ id: 'to-krebs', type: 'arrow', points: [{ x: 610, y: 250 }, { x: 745, y: 250 }], color: '#22c55e', strokeWidth: 4 });
    elements.push({ id: 'krebs-ring', type: 'circle', x: 790, y: 250, radius: 54, color: '#22c55e', dashed: true });
    elements.push({ id: 'krebs-label', type: 'text', x: 790, y: 245, text: 'Cycle de', color: '#bbf7d0', fontSize: 18, align: 'middle' });
    elements.push({ id: 'krebs-label-2', type: 'text', x: 790, y: 270, text: 'Krebs', color: '#bbf7d0', fontSize: 20, align: 'middle' });
  }
  elements.push({ id: 'message', type: 'text', x: 450, y: 455, text: messages[current], color: '#f8fafc', fontSize: 20, align: 'middle' });
  return {
    engine: 'roughsvg', title: 'Du pyruvate cytoplasmique à l’acétyl-CoA matriciel', width: 900, height: 480,
    description: 'Le pyruvate traverse les membranes mitochondriales puis subit une décarboxylation oxydative dans la matrice avant le cycle de Krebs.',
    elements,
    legend: [{ color: '#fb7185', label: 'Pyruvate · 3C' }, { color: '#fbbf24', label: 'Acétyle · 2C' }, { color: '#22c55e', label: 'CoA / Krebs' }],
  };
}

function fluxProtonsSpec(_variant: string, step: number, _maxStep: number): RoughSVGVisualSpec {
  // Repere dessine a la main plutot que confie a JSXGraph : une cinetique de
  // 330 s contre 60 unites ne tient pas dans le rapport du conteneur, et le
  // moteur etirait alors l'axe des abscisses jusqu'a faire cogner son nom
  // contre ses propres graduations.
  const AXE = '#94a3b8', INK = '#e0f2fe', ORANGE = '#fb923c', GOLD = '#fde047';
  const px = (t: number) => 150 + t * (750 / 330);
  const py = (h: number) => 430 - h * (340 / 62);
  const courbe: Array<[number, number]> = [
    [0, 10], [20, 10], [40, 10], [55, 32], [66, 58],
    [90, 50], [130, 40], [180, 32], [240, 25], [330, 18],
  ];
  const total = courbe.length - 1;
  const shown = step >= 5 ? total : Math.max(1, Math.ceil((step / 5) * total));

  const el: RoughSVGElementSpec[] = [
    { type: 'arrow', points: [{ x: 150, y: 430 }, { x: 920, y: 430 }], color: AXE, strokeWidth: 2 },
    { type: 'arrow', points: [{ x: 150, y: 430 }, { x: 150, y: 76 }], color: AXE, strokeWidth: 2 },
    // Nom ET unite sur chaque axe : un axe anonyme est faux au bac.
    { type: 'text', x: 535, y: 470, text: 'temps (s)', color: INK, fontSize: 19, align: 'middle' },
    { type: 'text', x: 150, y: 62, text: '[H⁺] (10⁻⁹ mol/L)', color: INK, fontSize: 19, align: 'start' },
  ];
  [0, 100, 200, 300].forEach(t => {
    el.push({ type: 'line', points: [{ x: px(t), y: 430 }, { x: px(t), y: 438 }], color: AXE, strokeWidth: 2 });
    el.push({ type: 'text', x: px(t), y: 458, text: String(t), color: '#cbd5e1', fontSize: 16, align: 'middle' });
  });
  [10, 20, 30, 40, 50, 60].forEach(h => {
    el.push({ type: 'line', points: [{ x: 142, y: py(h) }, { x: 150, y: py(h) }], color: AXE, strokeWidth: 2 });
    el.push({ type: 'text', x: 132, y: py(h) + 6, text: String(h), color: '#cbd5e1', fontSize: 16, align: 'end' });
  });

  el.push({ type: 'line', dashed: true, color: GOLD, strokeWidth: 2,
    points: [{ x: px(40), y: 430 }, { x: px(40), y: 104 }] });
  el.push({ type: 'text', x: px(40) + 10, y: 96, text: 'pulse de O₂', color: GOLD, fontSize: 18, align: 'start' });

  el.push({ type: 'polyline', color: ORANGE, strokeWidth: 4,
    points: courbe.slice(0, shown + 1).map(([t, h]) => ({ x: px(t), y: py(h) })) });

  // Les trois commentaires ne s'ecrivent plus par-dessus la courbe : ils sont
  // devenus des zones a interroger, et la narration passe sous la figure.
  const recits = [
    'Concentration en protons du milieu, mesurée en continu.',
    'Avant l’injection, la mesure ne bouge pas.',
    'Toujours rien : sans dioxygène, la chaîne n’a pas d’accepteur final.',
    'Injection du dioxygène à t = 40 s.',
    'La concentration s’envole : les H⁺ quittent la matrice.',
    'Le pic est atteint.',
    'Montée rapide : la chaîne respiratoire pompe les H⁺ vers l’extérieur.',
    'Décroissance lente : les H⁺ regagnent la matrice par l’ATP synthase.',
    'Sans dioxygène, aucun flux : le pulse est bien la cause de tout.',
  ];
  const recit = recits[Math.max(0, Math.min(recits.length - 1, Math.round(step)))];

  return { engine: 'roughsvg', title: 'Flux de protons après un pulse de dioxygène', width: 960, height: 500,
    description: recit, elements: el,
    hotspots: [
      { id: 'avant', x: 152, y: 340, width: 76, height: 70, color: '#4ade80',
        label: 'Avant l’injection', value: '[H⁺] stable', lines: ['sans O₂, la chaîne est à l’arrêt'] },
      { id: 'pulse', x: 220, y: 118, width: 42, height: 312, color: GOLD,
        label: 'Pulse de dioxygène', value: 't = 40 s', lines: ['c’est la seule chose qui change'] },
      { id: 'montee', x: 264, y: 130, width: 62, height: 260, color: ORANGE,
        label: 'Montée rapide', value: '≈ +48 unités en 25 s', lines: ['les H⁺ sortent de la matrice'] },
      { id: 'descente', x: 340, y: 140, width: 170, height: 130, color: '#67e8f9',
        label: 'Décroissance lente', value: 'retour vers l’état initial', lines: ['les H⁺ rentrent par l’ATP synthase'] },
    ],
    hotspotPanel: panneauQuestion(570, 96, 360, 124) };
}

function moleculesGlucoseAtpSpec(variant: string, step: number, _maxStep: number): RoughSVGVisualSpec {
  const phosphate = (x: number, text: string): RoughSVGElementSpec[] => [
    { type: 'circle', x, y: 210, radius: 34, color: '#22d3ee', fill: '#0c4a6e' },
    { type: 'text', x, y: 218, text, color: '#e0f2fe', fontSize: 22, align: 'middle' },
  ];
  if (variant === 'glucose') {
    const glucose: RoughSVGElementSpec[] = [
      { type: 'text', x: 450, y: 45, text: 'Glucose : le substrat de départ', color: '#fef08a', fontSize: 29, align: 'middle' },
      { type: 'polygon', points: [{ x: 270, y: 145 }, { x: 370, y: 90 }, { x: 470, y: 145 }, { x: 470, y: 265 }, { x: 370, y: 320 }, { x: 270, y: 265 }], color: '#22c55e', fill: '#14532d' },
      { type: 'text', x: 370, y: 215, text: 'Glucose', color: 'white', fontSize: 31, align: 'middle' },
      { type: 'text', x: 370, y: 360, text: 'C₆H₁₂O₆ · molécule à 6 carbones', color: '#bbf7d0', fontSize: 21, align: 'middle' },
      { type: 'circle', x: 295, y: 145, radius: 17, color: '#86efac', fill: '#166534' },
      { type: 'text', x: 295, y: 152, text: '1', color: 'white', fontSize: 16, align: 'middle' },
      { type: 'circle', x: 445, y: 145, radius: 17, color: '#86efac', fill: '#166534' },
      { type: 'text', x: 445, y: 152, text: '6', color: 'white', fontSize: 16, align: 'middle' },
      { type: 'arrow', points: [{ x: 535, y: 180 }, { x: 650, y: 180 }], color: '#fbbf24', strokeWidth: 4 },
      { type: 'circle', x: 705, y: 180, radius: 37, color: '#22d3ee', fill: '#0c4a6e' },
      { type: 'text', x: 705, y: 188, text: 'P', color: 'white', fontSize: 25, align: 'middle' },
      { type: 'text', x: 450, y: 415, text: 'Première réaction : glucose + ATP → glucose-6-phosphate + ADP', color: '#fef08a', fontSize: 22, align: 'middle' },
    ];
    const n = [1, 3, 4, 7, 10, glucose.length][Math.max(0, Math.min(5, Math.round(step)))] || glucose.length;
    const zones: RoughSVGHotspotSpec[] = [];
    if (n >= 3) zones.push({ id: 'hexose', x: 268, y: 88, width: 204, height: 234, color: '#22c55e',
      label: 'Glucose', value: 'C₆H₁₂O₆', lines: ['six carbones : toute l’énergie du repas', 'il entre dans la glycolyse'] });
    if (n >= 10) zones.push({ id: 'phosphate', x: 666, y: 141, width: 78, height: 78, color: '#22d3ee',
      label: 'Phosphate fourni par l’ATP', value: 'glucose-6-phosphate', lines: ['il active la molécule', 'et la piège dans la cellule'] });
    return { engine: 'roughsvg', title: 'Glucose : substrat à six carbones de la glycolyse', width: 900, height: 470, description: 'Le glucose reçoit un phosphate fourni par l’ATP au début de la glycolyse.', elements: glucose.slice(0, n),
      hotspots: zones, hotspotPanel: zones.length ? panneauQuestion(36, 92, 216, 124) : undefined };
  }
  if (variant === 'atp') {
    const atp: RoughSVGElementSpec[] = [
      { type: 'text', x: 450, y: 45, text: 'ATP : donneur d’énergie et de phosphate', color: '#fef08a', fontSize: 29, align: 'middle' },
      { type: 'rect', x: 90, y: 145, width: 130, height: 120, color: '#c084fc', fill: '#581c87' },
      { type: 'text', x: 155, y: 212, text: 'Adénine', color: 'white', fontSize: 21, align: 'middle' },
      { type: 'polygon', points: [{ x: 250, y: 150 }, { x: 335, y: 175 }, { x: 315, y: 265 }, { x: 235, y: 265 }, { x: 215, y: 185 }], color: '#fbbf24', fill: '#78350f' },
      { type: 'text', x: 275, y: 218, text: 'Ribose', color: 'white', fontSize: 20, align: 'middle' },
      ...phosphate(410, 'P'), ...phosphate(520, 'P'), ...phosphate(630, 'P'),
      { type: 'arrow', points: [{ x: 630, y: 165 }, { x: 630, y: 95 }], color: '#fb7185', strokeWidth: 4 },
      { type: 'text', x: 630, y: 75, text: 'phosphate terminal transférable', color: '#fb7185', fontSize: 18, align: 'middle' },
      { type: 'arrow', points: [{ x: 690, y: 210 }, { x: 795, y: 210 }], color: '#22d3ee', strokeWidth: 4 },
      { type: 'text', x: 745, y: 185, text: 'hydrolyse', color: '#bae6fd', fontSize: 17, align: 'middle' },
      { type: 'text', x: 805, y: 220, text: 'ADP + Pi', color: 'white', fontSize: 23, align: 'middle' },
      { type: 'text', x: 450, y: 340, text: 'ATP + H₂O → ADP + Pi + énergie utilisable', color: '#fef08a', fontSize: 24, align: 'middle' },
    ];
    const n = [1, 3, 5, 11, 15, atp.length][Math.max(0, Math.min(5, Math.round(step)))] || atp.length;
    const zones: RoughSVGHotspotSpec[] = [];
    if (n >= 5) zones.push({ id: 'fixe', x: 86, y: 141, width: 253, height: 128, color: '#c084fc',
      label: 'Adénine + ribose', value: 'la partie fixe', lines: ['elle identifie la molécule', 'mais ne porte pas l’énergie'] });
    if (n >= 11) zones.push({ id: 'terminal', x: 592, y: 168, width: 78, height: 86, color: '#fb7185',
      label: 'Phosphate terminal', value: 'liaison riche en énergie', lines: ['c’est celui que l’ATP cède', 'la glycolyse en consomme 2 par glucose'] });
    return { engine: 'roughsvg', title: 'ATP : intermédiaire énergétique et donneur de phosphate', width: 900,
      height: zones.length ? 500 : 450, description: 'L’ATP cède un phosphate et devient ADP pendant la phase d’investissement de la glycolyse.', elements: atp.slice(0, n),
      hotspots: zones, hotspotPanel: zones.length ? panneauQuestion(40, 366, 350, 124) : undefined };
  }
  const all: RoughSVGElementSpec[] = [
    { type: 'polygon', points: [{ x: 80, y: 120 }, { x: 155, y: 80 }, { x: 230, y: 120 }, { x: 230, y: 210 }, { x: 155, y: 250 }, { x: 80, y: 210 }], color: '#22c55e', fill: '#14532d' },
    { type: 'text', x: 155, y: 170, text: 'Glucose', color: 'white', fontSize: 26, align: 'middle' },
    { type: 'text', x: 155, y: 285, text: 'C₆H₁₂O₆ · hexose cyclique', color: '#bbf7d0', fontSize: 18, align: 'middle' },
    { type: 'rect', x: 330, y: 145, width: 105, height: 120, color: '#c084fc', fill: '#581c87' },
    { type: 'text', x: 382, y: 210, text: 'Adénine', color: 'white', fontSize: 19, align: 'middle' },
    { type: 'polygon', points: [{ x: 465, y: 150 }, { x: 535, y: 175 }, { x: 520, y: 250 }, { x: 450, y: 250 }, { x: 430, y: 185 }], color: '#fbbf24', fill: '#78350f' },
    { type: 'text', x: 485, y: 215, text: 'Ribose', color: 'white', fontSize: 18, align: 'middle' },
    ...phosphate(600, 'P'), ...phosphate(690, 'P'), ...phosphate(780, 'P'),
    { type: 'arrow', points: [{ x: 748, y: 150 }, { x: 748, y: 95 }], color: '#fb7185', strokeWidth: 4 },
    { type: 'text', x: 748, y: 72, text: 'liaison riche en énergie', color: '#fb7185', fontSize: 17, align: 'middle' },
    { type: 'text', x: 595, y: 330, text: 'ATP + H₂O ⇄ ADP + Pi + énergie', color: '#fef08a', fontSize: 25, align: 'middle' },
    { type: 'text', x: 595, y: 370, text: 'hydrolyse exoénergétique · phosphorylation endoénergétique', color: '#bae6fd', fontSize: 16, align: 'middle' },
  ];
  const countByStep = [3, 5, 9, 13, 15, all.length][Math.max(0, Math.min(5, Math.round(step)))] || all.length;
  const zones: RoughSVGHotspotSpec[] = [];
  if (countByStep >= 3) zones.push({ id: 'glc', x: 76, y: 76, width: 158, height: 178, color: '#22c55e',
    label: 'Glucose', value: 'la réserve', lines: ['il stocke beaucoup d’énergie', 'mais la cellule ne la dépense pas ainsi'] });
  if (countByStep >= 9) zones.push({ id: 'base', x: 326, y: 141, width: 113, height: 128, color: '#c084fc',
    label: 'Adénine + ribose', value: 'la partie fixe', lines: ['elle ne porte pas l’énergie'] });
  if (countByStep >= 13) zones.push({ id: 'phos', x: 560, y: 168, width: 262, height: 86, color: '#22d3ee',
    label: 'Les trois phosphates', value: 'ATP → ADP + Pi', lines: ['la dernière liaison est riche en énergie', 'c’est elle que la cellule dépense'] });
  return { engine: 'roughsvg', title: 'Le glucose stocke l’énergie ; l’ATP la transfère', width: 900, height: 430, elements: all.slice(0, countByStep),
    hotspots: zones, hotspotPanel: zones.length ? panneauQuestion(36, 300, 310, 118) : undefined };
}

function rendementEnergetiqueSpec(variant: string, step: number, _maxStep: number): RoughSVGVisualSpec {
  // Repli statique compact : le lecteur React offre les cinq vues contextuelles.
  const b = energyBalance(variant);
  const elements: RoughSVGElementSpec[] = step < 9 ? [
    { type: 'text', x: 450, y: 45, text: 'ATP par glucose · convention du cours', color: '#bae6fd', fontSize: 25, align: 'middle' },
    ...['Glycolyse', 'Matrice', 'Chaîne'].flatMap((label, i): RoughSVGElementSpec[] => [
      { type: 'text', x: 150 + i * 300, y: 135, text: label, color: '#e2e8f0', fontSize: 25, align: 'middle' },
      { type: 'text', x: 150 + i * 300, y: 205, text: `${i === 2 ? b.chainATP : 2} ATP`, color: '#6ee7ad', fontSize: 32, align: 'middle' },
      { type: 'arrow', points: [{ x: 150 + i * 300, y: 240 }, { x: 450, y: 300 }], color: '#7dd3fc' },
    ]),
    { type: 'text', x: 450, y: 350, text: `${b.totalATP} ATP`, color: '#6ee7ad', fontSize: 40, align: 'middle' },
  ] : [
    { type: 'text', x: 450, y: 40, text: 'Même départ : 2 860 kJ/mol de glucose', color: '#bae6fd', fontSize: 25, align: 'middle' },
    ...[{ label: 'Respiration', y: 120, percent: b.respirationPercent }, { label: 'Fermentation', y: 260, percent: b.fermentationPercent }]
      .flatMap((row, i): RoughSVGElementSpec[] => [
        { type: 'text', x: 55, y: row.y - 20, text: row.label, color: '#e2e8f0', fontSize: 25 },
        { type: 'rect', x: 55, y: row.y, width: 600, height: 55, color: '#64748b', fill: '#334155' },
        { type: 'rect', x: 55, y: row.y, width: 600 * row.percent / 100, height: 55, color: '#6ee7ad', fill: '#6ee7ad' },
        { type: 'text', x: 690, y: row.y + 37, text: `${energyNumber(row.percent, i === 0 ? 1 : 2)} %`, color: '#6ee7ad', fontSize: 30 },
      ]),
  ];
  return { engine: 'roughsvg', title: 'Bilan visuel de l’énergie', width: 900, height: 400, elements,
    legend: step >= 9 ? [{ color: '#6ee7ad', label: 'Énergie en ATP' }, { color: '#64748b', label: 'Chaleur / énergie restante' }] : undefined };
}

function schemaBilanAnnoteSpec(_variant: string, step: number, _maxStep: number): RoughSVGVisualSpec {
  const labels = [
    '1 Glucose C₆H₁₂O₆', '2 Deux pyruvates', '3 2 ADP + 2 Pi → 2 ATP', '4 Glycolyse',
    '5–7 2 R′ → 2 R′H₂ · déshydrogénation', '8 Hyaloplasme', '9 Espace intermembranaire',
    '10 Matrice', '11 Pyruvates dans la matrice', '12 Décarboxylation · 6 CO₂',
    '13–15 10 R′ → 10 R′H₂', '16 2 ADP + 2 Pi → 2 ATP', '17 Membrane interne',
    '18 12 R′H₂ + 6 O₂', '19 12 R′ + 6 H₂O', '20 Sphère pédonculée',
    '21 Mitochondrie · 34 ATP',
  ];
  const shown = step >= 21 ? labels.length : Math.max(0, Math.min(labels.length, Math.round(step)));
  const elements: RoughSVGElementSpec[] = [
    { type: 'rect', x: 40, y: 35, width: 820, height: 100, color: '#38bdf8' },
    { type: 'text', x: 55, y: 60, text: 'HYALOPLASME', color: '#7dd3fc', fontSize: 18 },
    { type: 'ellipse', x: 60, y: 155, radiusX: 390, radiusY: 115, color: '#f59e0b' },
    { type: 'ellipse', x: 90, y: 175, radiusX: 350, radiusY: 90, color: '#fb7185' },
    { type: 'text', x: 450, y: 190, text: 'MITOCHONDRIE', color: '#fdba74', fontSize: 18, align: 'middle' },
    { type: 'arrow', points: [{ x: 200, y: 95 }, { x: 200, y: 225 }], color: '#22d3ee' },
    { type: 'arrow', points: [{ x: 400, y: 230 }, { x: 650, y: 230 }], color: '#22c55e' },
  ];
  labels.slice(0, shown).forEach((text, i) => elements.push({
    type: 'text', x: 55 + (i % 3) * 275, y: 310 + Math.floor(i / 3) * 30,
    text, color: i === shown - 1 ? '#fef08a' : '#e2e8f0', fontSize: 14,
  }));
  if (shown === 0) labels.forEach((_, i) => elements.push({ type: 'text', x: 85 + (i % 7) * 110, y: 335 + Math.floor(i / 7) * 35, text: String(i + 1), color: '#fef08a', fontSize: 18 }));
  return { engine: 'roughsvg', title: step === 0 ? 'Repères à identifier' : 'Correction progressive du schéma-bilan', width: 900, height: 520, elements };
}

function vesiculesAtpSynthaseSpec(variant: string, step: number, _maxStep: number): RoughSVGVisualSpec {
  // Repli statique du même montage pour les consommateurs sans contrôles React.
  const parameters = initialVesicleState({ engine: 'preset', presetId: 'svt_ch1_vesicules_atp_synthase', variant, step });
  const result = vesicleResult(parameters);
  const elements: RoughSVGElementSpec[] = [
    { type: 'text', x: 450, y: 45, text: 'Une vésicule, plusieurs gradients de pH', color: '#bae6fd', fontSize: 24, align: 'middle' },
    { type: 'rect', x: 80, y: 80, width: 310, height: 310, color: '#cbd5e1' },
    { type: 'text', x: 235, y: 115, text: `Solution tampon · pHe ${parameters.pHe}`, color: '#67e8f9', fontSize: 22, align: 'middle' },
    { type: 'circle', x: 235, y: 265, radius: 80, color: '#c4b5fd' },
    { type: 'circle', x: 235, y: 265, radius: 72, color: '#8b7bb4' },
    { type: 'text', x: 235, y: 270, text: `pHi ${parameters.pHi}`, color: '#fde68a', fontSize: 25, align: 'middle' },
    { type: 'text', x: 465, y: 155, text: result.atpSynthesis ? 'ATP synthétisé' : 'Pas d’ATP synthétisé', color: result.atpSynthesis ? '#86efac' : '#fda4af', fontSize: 26 },
    { type: 'text', x: 465, y: 210, text: `ΔpH = pHe − pHi = ${result.deltaPH}`, color: '#fde68a', fontSize: 23 },
    { type: 'text', x: 465, y: 265, text: 'Sphères vers l’extérieur', color: '#93c5fd', fontSize: 22 },
    { type: 'text', x: 465, y: 320, text: 'ADP + Pi disponibles', color: '#bbf7d0', fontSize: 22 },
    { type: 'text', x: 450, y: 445, text: 'Modèle qualitatif : membrane et ATP synthase intactes', color: '#cbd5e1', fontSize: 20, align: 'middle' },
  ];
  for (let k = 0; k < 12; k++) {
    const angle = k * Math.PI / 6;
    elements.push({ type: 'line', points: [{ x: 235 + 80 * Math.cos(angle), y: 265 + 80 * Math.sin(angle) }, { x: 235 + 96 * Math.cos(angle), y: 265 + 96 * Math.sin(angle) }], color: '#93c5fd' });
    elements.push({ type: 'circle', x: 235 + 100 * Math.cos(angle), y: 265 + 100 * Math.sin(angle), radius: 5, color: '#93c5fd', fill: '#93c5fd' });
  }
  return { engine: 'roughsvg', title: 'Vésicule retournée — expérience de pH', width: 900, height: 480, elements };
}

function chimiosmoseSpec(variant: string, step: number, maxStep: number): RoughSVGVisualSpec {
  const isFadh2 = variant === 'fadh2';
  return rubanSpec(
    'Chaîne respiratoire de la membrane interne mitochondriale',
    [
      { id: 'donor', label: isFadh2 ? 'FADH₂' : 'NADH,H⁺', court: isFadh2 ? 'FADH₂' : 'NADH,H⁺',
        detail: { value: 'une paire d’électrons', lines: [isFadh2 ? 'Convention scolaire : 2 ATP' : 'Convention scolaire : 3 ATP'] } },
      { id: 'entry', label: isFadh2 ? 'Complexe II' : 'Complexe I', court: isFadh2 ? 'CII · 0 H⁺' : 'CI · 4 H⁺',
        detail: { value: isFadh2 ? '0 H⁺ pompé' : '4 H⁺ pompés', lines: [isFadh2 ? 'le FADH₂ lié à CII contourne CI' : 'entrée des électrons du NADH'] } },
      { id: 'q', label: 'Coenzyme Q', court: 'Q',
        detail: { value: 'le passeur mobile', lines: ['reçoit les électrons de CI ou CII'] } },
      { id: 'ciii', label: 'Complexe III', court: 'CIII · 4 H⁺',
        detail: { value: '4 H⁺ pompés', lines: ['il transmet les électrons au cytochrome c'] } },
      { id: 'cytc', label: 'Cytochrome c', court: 'cyt c',
        detail: { value: 'le second passeur', lines: ['il circule sur la face externe de la membrane'] } },
      { id: 'civ', label: 'Complexe IV', court: 'CIV · 2 H⁺',
        detail: { value: '2 H⁺ pompés', lines: ['c’est lui qui réduit le dioxygène'] } },
      { id: 'o2', label: '½ O₂ + 2 H⁺', court: 'O₂',
        detail: { value: 'accepteur final', lines: ['sans lui, toute la chaîne se bloque'] } },
      { id: 'h2o', label: 'H₂O', court: 'H₂O',
        detail: { value: 'l’eau métabolique', lines: ['le dioxygène respiré finit en eau'] } },
      { id: 'gradient', label: 'Gradient de H⁺', court: 'gradient H⁺',
        detail: { value: 'H⁺ concentrés dans l’espace intermembranaire', lines: ['pH plus bas dans l’espace ; plus haut dans la matrice', 'après arrêt du pompage, le retour des H⁺ réduit le gradient'] } },
      { id: 'atpsynthase', label: 'ATP synthase', court: 'ATP synthase',
        detail: { value: 'F₁ côté matrice', lines: ['le retour des H⁺ entraîne le rotor', 'la sphère pédonculée catalyse ADP + Pi → ATP'] } },
      { id: 'atp', label: 'ATP', court: 'ATP',
        detail: { value: isFadh2 ? 'FADH₂ → 2 ATP' : 'NADH,H⁺ → 3 ATP', lines: ['Bilan selon la convention scolaire'] } },
    ],
    [
      '2 e⁻ cédés', isFadh2 ? 'aucun H⁺ pompé' : '4 H⁺ pompés', 'les e⁻ passent', '4 H⁺ pompés',
      'les e⁻ passent', '2 H⁺ pompés', '½ O₂ + 2 H⁺', 'pendant ce temps',
      'les H⁺ reviennent', 'ADP + Pi → ATP',
    ],
    step, maxStep,
  );
}

function metabolicSpec(_variant: string, step: number, maxStep: number): RoughSVGVisualSpec {
  return carrefourSpec(
    'Trois devenirs du pyruvate, une même nécessité : régénérer le NAD⁺',
    { id: 'pyruvate', label: '2 pyruvates, issus de la glycolyse', court: 'Pyruvate',
      detail: { value: 'le carrefour', lines: ['la suite dépend de la présence de dioxygène'] } },
    [
      {
        etiquette: 'avec O₂',
        stations: [
          { id: 'respiration', label: 'Respiration mitochondriale', court: 'Respiration',
            detail: { value: '36 à 38 ATP', lines: ['le glucose est dégradé jusqu’au CO₂ et à l’eau'] } },
          { id: 'nad_resp', label: 'NAD⁺ régénéré', court: 'NAD⁺',
            detail: { value: 'par la chaîne respiratoire', lines: ['le NADH y dépose ses électrons'] } },
        ],
      },
      {
        etiquette: 'sans O₂ · lactique',
        stations: [
          { id: 'lactate', label: '2 acides lactiques', court: 'Lactate',
            detail: { value: '2 ATP seulement', lines: ['le carbone reste piégé dans une molécule à 3C'] } },
          { id: 'nad_lac', label: 'NAD⁺ régénéré', court: 'NAD⁺',
            detail: { value: 'par la réduction du pyruvate', lines: ['c’est le seul intérêt de la fermentation'] } },
        ],
      },
      {
        etiquette: 'sans O₂ · alcoolique',
        stations: [
          { id: 'ethanol', label: '2 éthanols + 2 CO₂', court: 'Éthanol',
            detail: { value: '2 ATP seulement', lines: ['fermentation alcoolique de la levure'] } },
          { id: 'nad_eth', label: 'NAD⁺ régénéré', court: 'NAD⁺',
            detail: { value: 'par la réduction de l’acétaldéhyde', lines: ['même logique que la voie lactique'] } },
        ],
      },
    ],
    { id: 'conclusion', label: 'Sans NAD⁺ régénéré, la glycolyse s’arrête', court: 'Conclusion',
      detail: { value: 'le NAD⁺ est le vrai enjeu', lines: ['les trois voies n’existent que pour lui'] } },
    step, maxStep,
  );
}

function respirationMitochondrialeSpec(variant: string, step: number, maxStep: number): RoughSVGVisualSpec {
  const chemins: Record<string, string[]> = {
    krebs: ['pyruvate', 'acetyl', 'krebs', 'co2', 'coenzymes'],
    chaine_respiratoire: ['coenzymes', 'chaine', 'o2', 'h2o', 'gradient', 'atp'],
    bilan: ['glucose', 'glycolyse', 'pyruvate', 'acetyl', 'krebs', 'coenzymes', 'chaine', 'gradient', 'atp'],
  };
  const table: Record<string, StationRuban> = {
    glucose: { id: 'glucose', label: 'Glucose', court: 'Glucose',
      detail: { value: '2860 kJ par mole', lines: ['toute l’énergie du repas est là'] } },
    glycolyse: { id: 'glycolyse', label: 'Glycolyse', court: 'Glycolyse',
      detail: { value: 'dans le cytosol', lines: ['2 ATP nets et 2 NADH,H⁺', 'elle n’a pas besoin de dioxygène'] } },
    pyruvate: { id: 'pyruvate', label: 'Pyruvate', court: 'Pyruvate',
      detail: { value: 'le carrefour', lines: ['avec O₂ il entre dans la mitochondrie'] } },
    acetyl: { id: 'acetyl', label: 'Acétyl-CoA', court: 'Acétyl-CoA',
      detail: { value: '3C → 2C + 1 CO₂', lines: ['décarboxylation, dans la matrice'] } },
    krebs: { id: 'krebs', label: 'Cycle de Krebs', court: 'Krebs',
      detail: { value: 'dans la matrice', lines: ['par tour : 2 CO₂, 3 NADH,H⁺, 1 FADH₂'] } },
    co2: { id: 'co2', label: 'CO₂ rejeté', court: 'CO₂',
      detail: { value: '6 CO₂ par glucose', lines: ['tout le carbone du glucose finit là'] } },
    coenzymes: { id: 'coenzymes', label: 'NADH,H⁺ et FADH₂', court: 'Coenzymes',
      detail: { value: 'les porteurs d’électrons', lines: ['ils transportent l’énergie vers les crêtes'] } },
    chaine: { id: 'chaine', label: 'Chaîne respiratoire', court: 'Chaîne',
      detail: { value: 'sur les crêtes', lines: ['c’est là que se fabrique l’essentiel de l’ATP'] } },
    o2: { id: 'o2', label: 'Dioxygène', court: 'O₂',
      detail: { value: 'accepteur final', lines: ['sans lui, toute la chaîne se bloque'] } },
    h2o: { id: 'h2o', label: 'H₂O', court: 'H₂O',
      detail: { value: 'l’eau métabolique', lines: ['le dioxygène respiré finit en eau'] } },
    gradient: { id: 'gradient', label: 'Gradient de H⁺', court: 'gradient H⁺',
      detail: { value: 'l’énergie mise en réserve', lines: ['il fait tourner l’ATP synthase'] } },
    atp: { id: 'atp', label: 'ATP et chaleur', court: 'ATP',
      detail: { value: '36 à 38 ATP', lines: ['le reste part en chaleur : rendement 40,5 %'] } },
  };
  const libelles: Record<string, string> = {
    'glucose>glycolyse': 'oxydation partielle', 'glycolyse>pyruvate': 'dans le cytosol',
    'pyruvate>acetyl': 'entrée en matrice', 'acetyl>krebs': 'il rejoint le cycle',
    'krebs>co2': 'décarboxylations', 'krebs>coenzymes': 'électrons + H⁺',
    'co2>coenzymes': 'et aussi', 'coenzymes>chaine': 'vers les crêtes',
    'chaine>o2': 'les e⁻ arrivent', 'o2>h2o': 'réduction', 'h2o>gradient': 'pendant ce temps',
    'chaine>gradient': 'H⁺ pompés', 'gradient>atp': 'ATP synthase',
  };
  const chemin = chemins[variant] || chemins.bilan;
  return rubanSpec(
    'Matrice : Krebs · membrane interne et crêtes : chaîne respiratoire',
    chemin.map(id => table[id]),
    transitionsSuivant(chemin, libelles),
    step, maxStep,
  );
}

function sarcomereElements(prefix: string, contraction: number, y: number): JSXGraphElementSpec[] {
  const leftZ = 0.9 + 1.0 * contraction;
  const rightZ = 11.1 - 1.0 * contraction;
  const leftActinEnd = leftZ + 4.1;
  const rightActinEnd = rightZ - 4.1;
  return [
    { id: `${prefix}-z-left`, type: 'segment', points: [{ x: leftZ, y: y - 0.85 }, { x: leftZ, y: y + 0.85 }], color: 'white', label: 'Z' },
    { id: `${prefix}-z-right`, type: 'segment', points: [{ x: rightZ, y: y - 0.85 }, { x: rightZ, y: y + 0.85 }], color: 'white', label: 'Z' },
    { id: `${prefix}-actin-left-up`, type: 'segment', points: [{ x: leftZ, y: y + 0.42 }, { x: leftActinEnd, y: y + 0.42 }], color: 'cyan' },
    { id: `${prefix}-actin-left-down`, type: 'segment', points: [{ x: leftZ, y: y - 0.42 }, { x: leftActinEnd, y: y - 0.42 }], color: 'cyan' },
    { id: `${prefix}-actin-right-up`, type: 'segment', points: [{ x: rightActinEnd, y: y + 0.42 }, { x: rightZ, y: y + 0.42 }], color: 'cyan' },
    { id: `${prefix}-actin-right-down`, type: 'segment', points: [{ x: rightActinEnd, y: y - 0.42 }, { x: rightZ, y: y - 0.42 }], color: 'cyan' },
    { id: `${prefix}-myosin`, type: 'segment', points: [{ x: 4.1, y }, { x: 7.9, y }], color: 'orange', label: 'Myosine' },
    { id: `${prefix}-band-a`, type: 'segment', points: [{ x: 4.1, y: y - 1.05 }, { x: 7.9, y: y - 1.05 }], color: 'orange', label: 'A' },
    { id: `${prefix}-band-i`, type: 'segment', points: [{ x: leftZ, y: y - 1.05 }, { x: 4.1, y: y - 1.05 }], color: 'cyan', label: '½ I' },
    ...(contraction < 0.9 ? [{ id: `${prefix}-zone-h`, type: 'segment' as const, points: [{ x: leftActinEnd, y: y + 0.8 }, { x: rightActinEnd, y: y + 0.8 }], color: 'yellow', label: 'H' }] : []),
    { id: `${prefix}-left-slide`, type: 'arrow', points: [{ x: 3.4, y: y + 1.15 }, { x: 5.1, y: y + 1.15 }], color: 'green' },
    { id: `${prefix}-right-slide`, type: 'arrow', points: [{ x: 8.6, y: y + 1.15 }, { x: 6.9, y: y + 1.15 }], color: 'green' },
  ];
}

function glissementSarcomereSpec(variant: string, step: number, maxStep: number): JSXGraphVisualSpec {
  const progress = Math.max(0, Math.min(1, step / maxStep));
  const elements: JSXGraphElementSpec[] = variant === 'comparaison'
    ? [
        ...sarcomereElements('repos', 0, 2.2),
        { id: 'repos-label', type: 'text' as const, points: [{ x: 6, y: 3.75 }], color: 'white', label: 'repos' },
        ...sarcomereElements('contracte', progress, -2.0),
        { id: 'contracte-label', type: 'text' as const, points: [{ x: 6, y: -3.55 }], color: 'yellow', label: 'contraction' },
      ]
    : sarcomereElements('sarcomere', variant === 'repos' ? 0 : progress, 0);
  elements.push({
    id: 'conclusion', type: 'text', points: [{ x: 6, y: variant === 'comparaison' ? -4.1 : -1.8 }],
    color: 'cyan', label: 'Les filaments ne raccourcissent pas : leur chevauchement augmente',
  });
  return {
    engine: 'jsxgraph',
    title: 'Les stries Z se rapprochent tandis que la bande A reste constante',
    boundingBox: [-0.7, variant === 'comparaison' ? 4.7 : 2.8, 12.8, variant === 'comparaison' ? -4.8 : -2.4],
    axis: false,
    elements,
  };
}

function couplageExcitationContractionSpec(variant: string, step: number, maxStep: number): RoughSVGVisualSpec {
  const chemins: Record<string, string[]> = {
    liberation_calcium: ['message', 'tubule', 'reticulum', 'calcium'],
    contraction: ['calcium', 'troponine', 'ponts', 'glissement', 'contraction'],
    relaxation: ['fin_message', 'pompe', 'reticulum', 'sites_masques', 'relaxation'],
    cycle_complet: ['message', 'tubule', 'reticulum', 'calcium', 'troponine', 'ponts',
      'glissement', 'contraction', 'fin_message', 'pompe', 'sites_masques', 'relaxation'],
  };
  const table: Record<string, StationRuban> = {
    message: { id: 'message', label: 'Potentiel d’action', court: 'Message',
      detail: { value: 'le signal électrique de la fibre', lines: ['déclenché à la jonction neuromusculaire'] } },
    tubule: { id: 'tubule', label: 'Tubule T', court: 'Tubule T',
      detail: { value: 'il porte le signal au cœur', lines: ['sinon la fibre se contracterait en surface'] } },
    reticulum: { id: 'reticulum', label: 'Réticulum sarcoplasmique', court: 'Réticulum',
      detail: { value: 'la réserve de Ca²⁺', lines: ['il le libère, puis il le repompe'] } },
    calcium: { id: 'calcium', label: 'Ca²⁺ cytosolique', court: 'Ca²⁺',
      detail: { value: 'le messager', lines: ['il fait le lien entre l’électrique et le mécanique'] } },
    troponine: { id: 'troponine', label: 'Troponine', court: 'Troponine',
      detail: { value: 'elle fixe le Ca²⁺', lines: ['la tropomyosine se déplace', 'les sites de l’actine deviennent accessibles'] } },
    ponts: { id: 'ponts', label: 'Ponts actine–myosine', court: 'Ponts',
      detail: { value: 'l’ATP est indispensable', lines: ['c’est lui qui détache la tête de myosine'] } },
    glissement: { id: 'glissement', label: 'Glissement des filaments', court: 'Glissement',
      detail: { value: 'ils ne raccourcissent pas', lines: ['c’est leur chevauchement qui augmente'] } },
    contraction: { id: 'contraction', label: 'Contraction', court: 'Contraction',
      detail: { value: 'les stries Z se rapprochent', lines: ['la bande A garde sa longueur'] } },
    fin_message: { id: 'fin_message', label: 'Fin du message', court: 'Fin signal',
      detail: { value: 'plus de potentiel d’action', lines: ['le réticulum cesse de libérer du Ca²⁺'] } },
    pompe: { id: 'pompe', label: 'Pompes à Ca²⁺', court: 'Pompes',
      detail: { value: 'elles consomment de l’ATP', lines: ['se relâcher coûte de l’énergie, aussi'] } },
    sites_masques: { id: 'sites_masques', label: 'Sites de l’actine masqués', court: 'Sites masqués',
      detail: { value: 'la tropomyosine recouvre', lines: ['plus aucun pont ne peut se former'] } },
    relaxation: { id: 'relaxation', label: 'Relaxation', court: 'Relaxation',
      detail: { value: 'le muscle se rallonge', lines: ['sous l’effet des forces extérieures'] } },
  };
  const libelles: Record<string, string> = {
    'message>tubule': 'il pénètre', 'tubule>reticulum': 'déclenche',
    'reticulum>calcium': 'libération', 'calcium>troponine': 'fixation',
    'troponine>ponts': 'sites exposés', 'ponts>glissement': 'cycles à ATP',
    'glissement>contraction': 'raccourcissement', 'contraction>fin_message': 'fin de l’excitation',
    'fin_message>pompe': 'recapture', 'pompe>reticulum': 'Ca²⁺ stocké',
    'pompe>sites_masques': 'Ca²⁺ retiré', 'reticulum>sites_masques': 'plus de Ca²⁺',
    'sites_masques>relaxation': 'plus de ponts',
  };
  const chemin = chemins[variant] || chemins.cycle_complet;
  return rubanSpec(
    'Le Ca²⁺ relie le message électrique au mouvement mécanique',
    chemin.map(id => table[id]),
    transitionsSuivant(chemin, libelles),
    step, maxStep,
  );
}

function actomyosineSpec(variant: string, step: number, maxStep: number): RoughSVGVisualSpec {
  const cycle = ['ca', 'fixation', 'pivotement', 'detachement', 'reactivation'];
  const chemins: Record<string, string[]> = {
    fixation: ['ca', 'fixation'], pivotement: ['fixation', 'pivotement'],
    detachement: ['pivotement', 'detachement'], reactivation: ['detachement', 'reactivation'],
    cycle_complet: cycle,
  };
  const table: Record<string, StationRuban> = {
    ca: { id: 'ca', label: 'Ca²⁺ : sites exposés', court: 'Ca²⁺',
      detail: { value: 'le feu vert', lines: ['sans Ca²⁺, aucun pont ne peut se former'] } },
    fixation: { id: 'fixation', label: 'Tête de myosine fixée', court: 'Fixation',
      detail: { value: 'le pont se forme', lines: ['la tête portait déjà ADP et Pi'] } },
    pivotement: { id: 'pivotement', label: 'Pivotement de la tête', court: 'Pivotement',
      detail: { value: 'le filament glisse', lines: ['Pi puis ADP sont libérés'] } },
    detachement: { id: 'detachement', label: 'ATP fixé : détachement', court: 'Détachement',
      detail: { value: '1 ATP fixé', lines: ['sans ATP la tête reste collée', 'c’est la rigidité cadavérique'] } },
    reactivation: { id: 'reactivation', label: 'Tête réarmée', court: 'Réactivation',
      detail: { value: 'ATP hydrolysé', lines: ['la tête est prête pour un nouveau cycle'] } },
  };
  const libelles: Record<string, string> = {
    'ca>fixation': 'formation du pont', 'fixation>pivotement': 'Pi puis ADP libérés',
    'pivotement>detachement': 'fixation d’ATP', 'detachement>reactivation': 'hydrolyse de l’ATP',
    'reactivation>ca': 'si le Ca²⁺ est encore là',
  };
  const chemin = chemins[variant] || cycle;
  const boucle = chemin === cycle;
  const suite = boucle ? [...chemin, chemin[0]] : chemin;
  return rubanSpec(
    'Le Ca²⁺ autorise le cycle ; l’ATP détache puis réactive la myosine',
    chemin.map(id => table[id]),
    transitionsSuivant(suite, libelles),
    step, maxStep, boucle,
  );
}

function filieresSpec(_variant: string, step: number, maxStep: number): RoughSVGVisualSpec {
  return carrefourSpec(
    'Les filières régénèrent le même ATP à des vitesses et capacités différentes',
    { id: 'besoin', label: 'Le muscle a besoin d’ATP', court: 'Besoin',
      detail: { value: '2 à 3 secondes de stock', lines: ['il faut le régénérer sans arrêt'] } },
    [
      {
        etiquette: 'effort bref',
        stations: [
          { id: 'pc', label: 'Phosphocréatine', court: 'Phosphocréatine',
            detail: { value: 'dominante au début d’un effort maximal', lines: ['très rapide, réserves limitées ; sans O₂ direct'] } },
        ],
      },
      {
        etiquette: 'effort intense',
        stations: [
          { id: 'glycolyse', label: 'Glycolyse anaérobie', court: 'Glycolyse',
            detail: { value: 'forte contribution aux efforts intenses', lines: ['production rapide d’ATP', 'avec formation de lactate'] } },
          { id: 'lactate', label: 'Lactate', court: 'Lactate',
            detail: { value: 'produit même en présence d’O₂', lines: ['il peut être réutilisé comme combustible'] } },
        ],
      },
      {
        etiquette: 'effort prolongé',
        stations: [
          { id: 'respiration', label: 'Respiration mitochondriale', court: 'Respiration',
            detail: { value: 'soutient les efforts durables', lines: ['contribution progressive ; nécessite O₂'] } },
        ],
      },
    ],
    { id: 'atp', label: 'ATP régénéré · contraction musculaire', court: 'ATP',
      detail: { value: 'le même ATP dans les trois cas', lines: ['les trois filières contribuent simultanément'] } },
    step, maxStep,
  );
}

export function normalizePresetVariant(meta: ScientificPresetMeta, variant?: string): string {
  return meta.variants.some(item => item.id === variant) ? variant as string : meta.defaultVariant;
}

export function resolveScientificPreset(
  presetId: ScientificPresetId,
  variant: string,
  step: number,
): ScientificVisualSpec {
  const meta = SCIENTIFIC_PRESETS[presetId];
  const safeVariant = normalizePresetVariant(meta, variant);
  switch (presetId) {
    case 'phys_ch1_propagation_onde': return propagationOndeSpec(safeVariant, step, meta.maxStep);
    case 'phys_ch1_types_ondes': return typesOndesSpec(safeVariant, step, meta.maxStep);
    case 'phys_ch1_celerite_corde': return celeriteCordeSpec(safeVariant, step, meta.maxStep);
    case 'chem_ch1_facteurs_cinetiques': return facteursCinetiquesSpec(safeVariant, step, meta.maxStep);
    case 'chem_ch1_energie_activation': return energieActivationSpec(safeVariant, step, meta.maxStep);
    case 'chem_ch1_oxydoreduction': return oxydoreductionSpec(safeVariant, step, meta.maxStep);
    case 'svt_ch1_respiration_mitochondriale': return respirationMitochondrialeSpec(safeVariant, step, meta.maxStep);
    case 'svt_ch1_glissement_sarcomere': return glissementSarcomereSpec(safeVariant, step, meta.maxStep);
    case 'svt_ch1_couplage_excitation_contraction': return couplageExcitationContractionSpec(safeVariant, step, meta.maxStep);
    case 'svt_ch1_cycle_atp': return atpSpec(safeVariant, step, meta.maxStep);
    case 'svt_ch1_levures_exao': return levuresSpec(safeVariant, step, meta.maxStep);
    case 'svt_ch1_glycolyse_etapes': return glycolyseEtapesSpec(safeVariant, step, meta.maxStep);
    case 'svt_ch1_pyruvate_acetyl_coa': return pyruvateAcetylCoaSpec(safeVariant, step, meta.maxStep);
    case 'svt_ch1_krebs_detaille': return krebsDetailleSpec(safeVariant, step, meta.maxStep);
    case 'svt_ch1_echelle_redox': return echelleRedoxSpec(safeVariant, step, meta.maxStep);
    case 'svt_ch1_ultrastructure_mitochondrie': return ultrastructureMitochondrieSpec(safeVariant, step, meta.maxStep);
    case 'svt_ch1_flux_protons': return fluxProtonsSpec(safeVariant, step, meta.maxStep);
    case 'svt_ch1_molecules_glucose_atp': return moleculesGlucoseAtpSpec(safeVariant, step, meta.maxStep);
    case 'svt_ch1_rendement_energetique': return rendementEnergetiqueSpec(safeVariant, step, meta.maxStep);
    case 'svt_ch1_schema_bilan_annote': return schemaBilanAnnoteSpec(safeVariant, step, meta.maxStep);
    case 'svt_ch1_vesicules_atp_synthase': return vesiculesAtpSynthaseSpec(safeVariant, step, meta.maxStep);
    // Le composant photo dédié assure le rendu ; ce schéma reste le repli statique accessible.
    case 'svt_ch1_isolement_cretes_ultrasons': return vesiculesAtpSynthaseSpec(safeVariant, step, meta.maxStep);
    // Le composant photo dédié assure le rendu ; la carte métabolique reste le repli statique.
    case 'svt_ch1_fermentations_photos': return metabolicSpec(safeVariant, step, meta.maxStep);
    case 'svt_ch1_chimiosmose': return chimiosmoseSpec(safeVariant, step, meta.maxStep);
    case 'svt_ch1_carte_metabolique': return metabolicSpec(safeVariant, step, meta.maxStep);
    case 'svt_ch1_myogrammes': return myogramSpec(safeVariant, step, meta.maxStep);
    case 'svt_ch1_chaleurs_muscle': return muscleHeatSpec(safeVariant, step, meta.maxStep);
    case 'svt_ch1_cycle_actomyosine': return actomyosineSpec(safeVariant, step, meta.maxStep);
    case 'svt_ch1_filieres_effort': return filieresSpec(safeVariant, step, meta.maxStep);
  }
}
