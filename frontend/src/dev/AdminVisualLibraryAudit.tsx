import AdminVisualLibrary from '../components/admin/AdminVisualLibrary';
import { getAllSchemas } from '../components/session/schemas';
import { SCIENTIFIC_PRESETS } from '../components/session/scientific/scientificPresets';
import type { AdminVisualLibraryItem, AdminVisualLibraryResponse } from '../services/api';


const subjectNames: Record<string, string> = {
  svt: 'SVT',
  physics: 'Physique',
  chemistry: 'Chimie',
  math: 'Mathématiques',
};

const schemaItems: AdminVisualLibraryItem[] = getAllSchemas().map(schema => ({
  id: `schema:${schema.id}`,
  catalog_id: schema.id,
  kind: 'schema',
  title: schema.title,
  description: 'Schéma SVG validé et versionné dans le projet.',
  subject: subjectNames[schema.subject],
  subject_key: schema.subject,
  chapter: '',
  lesson: '',
  lesson_id: '',
  concepts: schema.keywords,
  source: 'core',
  status: 'validated',
  editable: false,
  deletable: false,
  preview: { kind: 'schema', schema_id: schema.id },
}));

const presetItems: AdminVisualLibraryItem[] = Object.values(SCIENTIFIC_PRESETS).map(preset => ({
  id: `preset:${preset.id}`,
  catalog_id: preset.id,
  kind: 'preset',
  title: preset.title,
  description: 'Scène contrôlable avec lecture, étapes et variantes.',
  subject: 'SVT',
  subject_key: 'svt',
  chapter: 'Consommation de la matière organique',
  lesson: '',
  lesson_id: '',
  concepts: preset.variants.map(variant => variant.label),
  source: 'core',
  status: 'validated',
  editable: false,
  deletable: false,
  variants: preset.variants.map(variant => variant.id),
  preview: {
    kind: 'scientific',
    scientific: {
      engine: 'preset',
      presetId: preset.id,
      variant: preset.defaultVariant,
      autoplay: false,
      step: preset.maxStep,
    },
  },
}));

const lesson = {
  id: 'audit-physics-free-fall',
  title: 'Chute verticale libre',
  chapter_id: 'audit-mechanics',
  chapter_title: 'Mécanique',
  subject_id: 'physics',
  subject_name: 'Physique',
};

const auditItems: AdminVisualLibraryItem[] = [
  {
    id: 'file:audit-fermentation-image',
    kind: 'image',
    title: 'Comparaison respiration et fermentation',
    description: 'Image de cours locale utilisée pour auditer le classement par type.',
    subject: 'SVT',
    subject_key: 'svt',
    chapter: 'Consommation de la matière organique',
    lesson: 'Libération de l’énergie',
    lesson_id: '',
    concepts: ['respiration', 'fermentation'],
    source: 'filesystem',
    status: 'validated',
    editable: false,
    deletable: false,
    preview: {
      kind: 'image',
      url: '/media/images/svt/ch1_consommation_matiere_organique/lesson_1_liberation_energie/fermentation/comparaison_respiration_fermentation.svg',
    },
  },
  {
    id: 'resource:audit-free-fall',
    resource_id: 'audit-free-fall',
    kind: 'scientific',
    title: 'Chute libre — hauteur et vitesse',
    description: 'Scène Matter.js transparente, mesurable et réglable.',
    subject: 'Physique',
    subject_key: 'physics',
    chapter: 'Mécanique',
    lesson: lesson.title,
    lesson_id: lesson.id,
    concepts: ['chute libre', 'vitesse', 'pesanteur'],
    source: 'admin_llm',
    status: 'draft',
    editable: true,
    deletable: true,
    quality: { score: 100, issues: [], acceptable: true },
    preview: {
      kind: 'scientific',
      scientific: {
        engine: 'matter',
        title: 'Chute libre',
        width: 600,
        height: 320,
        gravity: { x: 0, y: 1 },
        autoplay: true,
        scale: 100,
        bodies: [
          { id: 'sol', shape: 'rectangle', x: 300, y: 305, width: 580, height: 20, isStatic: true, label: 'Sol' },
          { id: 'balle', shape: 'circle', x: 300, y: 55, radius: 20, label: 'Balle', color: 'orange', frictionAir: 0 },
        ],
        measures: [
          { body: 'balle', quantity: 'height', label: 'Hauteur', unit: 'm', decimals: 2, origin: 295 },
          { body: 'balle', quantity: 'speed', label: 'Vitesse', unit: 'm/s', decimals: 2 },
          { quantity: 'time', label: 'Temps', unit: 's', decimals: 2 },
        ],
        parameters: [
          { target: 'gravity', label: 'Pesanteur', min: 0.2, max: 1.6, step: 0.1, value: 1, unit: 'g' },
        ],
      },
    },
  },
  {
    id: 'file:/media/simulations/physics/advanced/mechanics/index.html',
    kind: 'simulation',
    title: 'Laboratoire de mécanique',
    description: 'Simulation HTML locale à rattacher à une leçon.',
    subject: 'Physique', subject_key: 'physics', chapter: 'Mécanique', lesson: '', lesson_id: '',
    concepts: ['mouvement', 'forces'], source: 'filesystem', status: 'validated', editable: false, deletable: false,
    preview: { kind: 'simulation', url: '/media/simulations/physics/advanced/mechanics/index.html' },
  },
];

const library: AdminVisualLibraryResponse = {
  items: [...schemaItems, ...presetItems, ...auditItems],
  lessons: [lesson],
  stats: {
    total: schemaItems.length + presetItems.length + auditItems.length,
    editable: 1,
    by_kind: {
      schema: schemaItems.length,
      preset: presetItems.length,
      image: 1,
      scientific: 1,
      simulation: 1,
    },
  },
  database_available: true,
};

export default function AdminVisualLibraryAudit() {
  return (
    <main className="min-h-screen bg-gray-50 p-4 sm:p-6">
      <div className="mx-auto max-w-[1800px]">
        <AdminVisualLibrary initialLibrary={library} />
      </div>
    </main>
  );
}
