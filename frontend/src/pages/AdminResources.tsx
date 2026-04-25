import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuthStore } from '../stores/authStore';
import api from '../services/api';

type ResourceType = 'image' | 'video' | 'simulation' | 'exercise' | 'evaluation' | 'exam' | 'definition';

interface MicroTeachingItem {
  id: string;
  title: string;
}

interface LessonContent {
  micro_enseignements?: MicroTeachingItem[];
}

interface ChapterInfo {
  title_fr?: string;
}

interface LessonResource {
  id: string;
  lesson_id: string;
  section_title: string;
  resource_type: ResourceType;
  title: string;
  description: string;
  file_path: string | null;
  external_url: string | null;
  trigger_text: string | null;
  phase: string | null;
  difficulty_tier: string;
  concepts: string[];
  metadata: Record<string, any>;
  order_index: number;
}

interface Lesson {
  id: string;
  title_fr: string;
  chapter_id: string;
  content?: LessonContent;
  chapters?: ChapterInfo | ChapterInfo[] | null;
}

const SVT_ENERGY_MICRO_ENSEIGNEMENTS: MicroTeachingItem[] = [
    { id: 'svt_ch1_intro_generale', title: '1. Introduction générale' },
    { id: 'svt_ch1_atp_transporteurs', title: '2. ATP et transporteurs d’énergie' },
    { id: 'svt_ch1_glycolyse', title: '3. Glycolyse (première étape)' },
    { id: 'svt_ch1_structure_mitochondrie', title: '4. Structure de la mitochondrie' },
    { id: 'svt_ch1_cycle_krebs', title: '5. Cycle de Krebs' },
    { id: 'svt_ch1_chaine_respiratoire', title: '6. Chaîne respiratoire et phosphorylation oxydative' },
    { id: 'svt_ch1_bilan_energetique', title: '7. Bilan énergétique de la respiration' },
    { id: 'svt_ch1_fermentation', title: '8. Fermentation' },
    { id: 'svt_ch1_synthese', title: '9. Synthèse de l’unité' },
    { id: 'svt_ch2_structure_muscle', title: '10. Structure du muscle strié' },
    { id: 'svt_ch2_contraction_energie', title: '11. Relation contraction ↔ énergie' },
    { id: 'svt_ch2_phenomenes_thermiques', title: '12. Phénomènes thermiques' },
    { id: 'svt_ch2_exercice_bac', title: '13. Exercice type BAC' },
    { id: 'svt_transversal_respiration_fermentation', title: '14. Comparaison respiration vs fermentation' },
    { id: 'svt_transversal_mini_quiz', title: '15. Mini-quiz d’évaluation (FAQ)' },
  ];

const SVT_CH2_MICRO_ENSEIGNEMENTS: MicroTeachingItem[] = [
  { id: 'svt_ch2_intro_information_genetique', title: "1. Introduction et notion d'information génétique" },
  { id: 'svt_ch2_adn_support', title: "2. ADN : support moléculaire de l'information génétique" },
  { id: 'svt_ch2_replication', title: "3. Réplication de l'ADN" },
  { id: 'svt_ch2_gene_allele', title: '4. Gène, allèle et localisation chromosomique' },
  { id: 'svt_ch2_transcription', title: "5. Transcription de l'ADN en ARN" },
  { id: 'svt_ch2_code_genetique', title: '6. Code génétique et lecture des codons' },
  { id: 'svt_ch2_traduction', title: '7. Traduction et synthèse protéique' },
  { id: 'svt_ch2_cycle_cellulaire_mitose', title: '8. Cycle cellulaire et mitose' },
  { id: 'svt_ch2_caryotype', title: '9. Caryotype et organisation chromosomique' },
  { id: 'svt_ch2_meiose', title: '10. Méiose et brassage génétique' },
  { id: 'svt_ch2_fecondation', title: '11. Fécondation et restauration de la diploïdie' },
  { id: 'svt_ch2_monohybridisme', title: '12. Monohybridisme et lois statistiques de Mendel' },
  { id: 'svt_ch2_dihybridisme', title: '13. Dihybridisme, gènes liés et exceptions des lois statistiques' },
  { id: 'svt_ch2_mutations', title: "14. Mutations et conséquences sur l'expression du gène" },
  { id: 'svt_ch2_synthese', title: '15. Synthèse et évaluation du chapitre' },
];

const SVT_CH3_MICRO_ENSEIGNEMENTS: MicroTeachingItem[] = [
  { id: 'svt_ch3_intro_utilisation_matieres', title: '1. Introduction : utilisation des matières organiques et inorganiques' },
  { id: 'svt_ch3_ordures_menageres_nature', title: '2. Nature et classification des ordures ménagères' },
  { id: 'svt_ch3_ordures_menageres_impacts', title: "3. Impacts des ordures ménagères sur l'environnement" },
  { id: 'svt_ch3_pollution_air', title: "4. Pollution de l'air : smog, pluies acides et effet de serre" },
  { id: 'svt_ch3_pollution_eau_sol', title: "5. Pollution de l'eau et du sol" },
  { id: 'svt_ch3_traitement_reduction_dechets', title: '6. Traitement, tri et reduction des dechets' },
  { id: 'svt_ch3_matieres_radioactives', title: '7. Matières radioactives : origines, usages et risques' },
  { id: 'svt_ch3_energie_nucleaire', title: '8. Energie nucleaire, dechets radioactifs et prevention' },
  { id: 'svt_ch3_energies_renouvelables', title: '9. Energies renouvelables et developpement durable' },
  { id: 'svt_ch3_synthese', title: '10. Synthèse et évaluation du chapitre' },
];

const SVT_CH4_MICRO_ENSEIGNEMENTS: MicroTeachingItem[] = [
  { id: 'svt_ch4_intro_tectonique', title: '1. Introduction à la tectonique des plaques' },
  { id: 'svt_ch4_structure_terre', title: '2. Structure interne de la Terre et dynamique lithosphérique' },
  { id: 'svt_ch4_limites_plaques', title: '3. Types de limites des plaques' },
  { id: 'svt_ch4_subduction', title: '4. Subduction et ses indices géologiques' },
  { id: 'svt_ch4_collision', title: '5. Collision continentale et formation des reliefs' },
  { id: 'svt_ch4_metamorphisme', title: '6. Métamorphisme et roches associées' },
  { id: 'svt_ch4_chaines_montagnes', title: '7. Formation des chaînes de montagnes' },
  { id: 'svt_ch4_synthese', title: '8. Synthèse et évaluation du chapitre' },
];

const MICRO_ENSEIGNEMENT_FALLBACKS: Record<string, MicroTeachingItem[]> = {
  "consommation de la matiere organique et flux d'energie": SVT_ENERGY_MICRO_ENSEIGNEMENTS,
  "liberation de l'energie emmagasinee dans la matiere organique": SVT_ENERGY_MICRO_ENSEIGNEMENTS,
  "nature et mecanisme de l'expression du materiel genetique": SVT_CH2_MICRO_ENSEIGNEMENTS,
  'utilisation des matieres organiques et inorganiques': SVT_CH3_MICRO_ENSEIGNEMENTS,
  'les phenomenes geologiques et la tectonique des plaques': SVT_CH4_MICRO_ENSEIGNEMENTS,
};

function normalizeLessonTitle(title: string): string {
  return title
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .replace(/[’']/g, "'")
    .replace(/\s+/g, ' ')
    .trim()
    .toLowerCase();
}

function getLessonMicroEnseignements(lesson: Lesson | undefined): MicroTeachingItem[] {
  if (!lesson) return [];

  const fromContent = lesson.content?.micro_enseignements;
  if (Array.isArray(fromContent) && fromContent.length > 0) {
    return fromContent;
  }

  const normalizedTitle = normalizeLessonTitle(lesson.title_fr);
  const chapterTitle = Array.isArray(lesson.chapters)
    ? lesson.chapters[0]?.title_fr || ''
    : lesson.chapters?.title_fr || '';
  const normalizedChapterTitle = chapterTitle ? normalizeLessonTitle(chapterTitle) : '';

  if (MICRO_ENSEIGNEMENT_FALLBACKS[normalizedTitle]) {
    return MICRO_ENSEIGNEMENT_FALLBACKS[normalizedTitle];
  }

  if (normalizedChapterTitle && MICRO_ENSEIGNEMENT_FALLBACKS[normalizedChapterTitle]) {
    return MICRO_ENSEIGNEMENT_FALLBACKS[normalizedChapterTitle];
  }

  if (
    normalizedTitle.includes('energie') &&
    normalizedTitle.includes('matiere organique')
  ) {
    return SVT_ENERGY_MICRO_ENSEIGNEMENTS;
  }

  if (normalizedTitle.includes('expression') || normalizedChapterTitle.includes('expression')) {
    return SVT_CH2_MICRO_ENSEIGNEMENTS;
  }

  if (
    normalizedTitle.includes('matieres organiques') ||
    normalizedTitle.includes('photosynthese') ||
    normalizedTitle.includes('nutrition') ||
    normalizedChapterTitle.includes('matieres organiques')
  ) {
    return SVT_CH3_MICRO_ENSEIGNEMENTS;
  }

  if (
    normalizedTitle.includes('tectonique') ||
    normalizedTitle.includes('subduction') ||
    normalizedTitle.includes('montagnes') ||
    normalizedChapterTitle.includes('tectonique') ||
    normalizedChapterTitle.includes('montagnes')
  ) {
    return SVT_CH4_MICRO_ENSEIGNEMENTS;
  }

  return [];
}

export default function AdminResources() {
  const navigate = useNavigate();
  const { token } = useAuthStore();
  const [activeTab, setActiveTab] = useState<ResourceType>('image');
  const [resources, setResources] = useState<LessonResource[]>([]);
  const [lessons, setLessons] = useState<Lesson[]>([]);
  const [loading, setLoading] = useState(false);
  const [showForm, setShowForm] = useState(false);
  const [editingResource, setEditingResource] = useState<LessonResource | null>(null);
  const [resourceLessonFilter, setResourceLessonFilter] = useState('');

  const [formData, setFormData] = useState({
    lesson_id: '',
    micro_enseignement_id: '',
    section_title: '',
    resource_type: 'image' as ResourceType,
    title: '',
    description: '',
    file_path: '',
    external_url: '',
    trigger_text: '',
    phase: 'explanation',
    difficulty_tier: 'intermediate',
    concepts: '',
    metadata: '{}',
    order_index: 0
  });

  const [uploadFile, setUploadFile] = useState<File | null>(null);
  const selectedLesson = lessons.find((lesson) => lesson.id === formData.lesson_id);
  const availableMicroEnseignements = getLessonMicroEnseignements(selectedLesson);

  useEffect(() => {
    if (!token) {
      navigate('/login');
      return;
    }
    fetchLessons();
    fetchResources();
  }, [token, navigate]);

  useEffect(() => {
    fetchResources();
  }, [activeTab, resourceLessonFilter]);

  const fetchLessons = async () => {
    try {
      const response = await api.get('/admin/lessons');
      setLessons(response.data);
    } catch (error) {
      console.error('Error fetching lessons:', error);
    }
  };

  const fetchResources = async () => {
    setLoading(true);
    try {
      const queryParams = new URLSearchParams({ type: activeTab });
      if (resourceLessonFilter) {
        queryParams.set('lesson_id', resourceLessonFilter);
      }

      const response = await api.get(`/admin/resources?${queryParams.toString()}`);
      setResources(response.data);
    } catch (error) {
      console.error('Error fetching resources:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      let filePath = formData.file_path;

      if (uploadFile && (activeTab === 'image' || activeTab === 'video')) {
        const uploadFormData = new FormData();
        uploadFormData.append('file', uploadFile);
        uploadFormData.append('type', activeTab);
        uploadFormData.append('lesson_id', formData.lesson_id);

        const uploadResponse = await api.post('/admin/upload', uploadFormData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        });
        filePath = uploadResponse.data.file_path;
      }

      const payload = {
        ...formData,
        file_path: filePath,
        concepts: formData.concepts.split(',').map(c => c.trim()).filter(Boolean),
        metadata: {
          ...JSON.parse(formData.metadata || '{}'),
          ...(formData.micro_enseignement_id
            ? {
                micro_enseignement_id: formData.micro_enseignement_id,
                micro_enseignement_title: availableMicroEnseignements.find(
                  (item) => item.id === formData.micro_enseignement_id
                )?.title || '',
              }
            : {}),
        }
      };

      if (editingResource) {
        await api.put(`/admin/resources/${editingResource.id}`, payload);
      } else {
        await api.post('/admin/resources', payload);
      }

      fetchResources();
      resetForm();
      setShowForm(false);
    } catch (error) {
      console.error('Error saving resource:', error);
      alert('Erreur lors de l\'enregistrement');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id: string) => {
    if (!confirm('Supprimer cette ressource ?')) return;

    try {
      await api.delete(`/admin/resources/${id}`);
      fetchResources();
    } catch (error) {
      console.error('Error deleting resource:', error);
    }
  };

  const handleEdit = (resource: LessonResource) => {
    setEditingResource(resource);
    setFormData({
      lesson_id: resource.lesson_id,
      micro_enseignement_id: String(resource.metadata?.micro_enseignement_id || ''),
      section_title: resource.section_title,
      resource_type: resource.resource_type,
      title: resource.title,
      description: resource.description,
      file_path: resource.file_path || '',
      external_url: resource.external_url || '',
      trigger_text: resource.trigger_text || '',
      phase: resource.phase || 'explanation',
      difficulty_tier: resource.difficulty_tier,
      concepts: resource.concepts.join(', '),
      metadata: JSON.stringify(resource.metadata),
      order_index: resource.order_index
    });
    setShowForm(true);
  };

  const resetForm = () => {
    setFormData({
      lesson_id: '',
      micro_enseignement_id: '',
      section_title: '',
      resource_type: activeTab,
      title: '',
      description: '',
      file_path: '',
      external_url: '',
      trigger_text: '',
      phase: 'explanation',
      difficulty_tier: 'intermediate',
      concepts: '',
      metadata: '{}',
      order_index: 0
    });
    setEditingResource(null);
    setUploadFile(null);
  };

  const resourceTypes: { type: ResourceType; label: string; icon: string }[] = [
    { type: 'image', label: 'Images', icon: '📸' },
    { type: 'video', label: 'Vidéos', icon: '🎥' },
    { type: 'simulation', label: 'Simulations', icon: '🔬' },
    { type: 'exercise', label: 'Exercices', icon: '✏️' },
    { type: 'evaluation', label: 'Évaluations', icon: '📝' },
    { type: 'exam', label: 'Examens', icon: '📋' },
    { type: 'definition', label: 'Définitions', icon: '📖' }
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Gestion des ressources pédagogiques</h1>
          <button
            onClick={() => navigate('/dashboard')}
            className="px-4 py-2 text-gray-600 hover:text-gray-900"
          >
            ← Retour
          </button>
        </div>

        <div className="bg-white rounded-lg shadow-sm mb-6">
          <div className="flex border-b overflow-x-auto">
            {resourceTypes.map(({ type, label, icon }) => (
              <button
                key={type}
                onClick={() => {
                  setActiveTab(type);
                  setShowForm(false);
                  resetForm();
                }}
                className={`px-6 py-4 font-medium whitespace-nowrap ${
                  activeTab === type
                    ? 'border-b-2 border-blue-600 text-blue-600'
                    : 'text-gray-600 hover:text-gray-900'
                }`}
              >
                <span className="mr-2">{icon}</span>
                {label}
              </button>
            ))}
          </div>
        </div>

        <div className="mb-6">
          <div className="flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
            <button
              onClick={() => {
                setShowForm(!showForm);
                if (showForm) resetForm();
              }}
              className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-medium"
            >
              {showForm ? '✕ Annuler' : `+ Ajouter ${resourceTypes.find(r => r.type === activeTab)?.label}`}
            </button>

            <div className="w-full md:w-[420px]">
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Filtrer les ressources par cours
              </label>
              <select
                value={resourceLessonFilter}
                onChange={(e) => setResourceLessonFilter(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              >
                <option value="">Tous les cours</option>
                {lessons.map((lesson) => (
                  <option key={lesson.id} value={lesson.id}>
                    {lesson.title_fr}
                  </option>
                ))}
              </select>
            </div>
          </div>
        </div>

        {showForm && (
          <div className="bg-white rounded-lg shadow-sm p-6 mb-6">
            <h2 className="text-xl font-bold mb-4">
              {editingResource ? 'Modifier' : 'Ajouter'} une ressource
            </h2>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Leçon *
                  </label>
                  <select
                    value={formData.lesson_id}
                    onChange={(e) => setFormData({ ...formData, lesson_id: e.target.value, micro_enseignement_id: '' })}
                    required
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="">Sélectionner une leçon</option>
                    {lessons.map((lesson) => (
                      <option key={lesson.id} value={lesson.id}>
                        {lesson.title_fr}
                      </option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Micro-enseignement
                  </label>
                  <select
                    value={formData.micro_enseignement_id}
                    onChange={(e) => setFormData({ ...formData, micro_enseignement_id: e.target.value })}
                    disabled={!formData.lesson_id || availableMicroEnseignements.length === 0}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100 disabled:text-gray-500"
                  >
                    <option value="">
                      {availableMicroEnseignements.length > 0
                        ? 'Sélectionner un micro-enseignement'
                        : 'Aucun micro-enseignement disponible pour cette leçon'}
                    </option>
                    {availableMicroEnseignements.map((item) => (
                      <option key={item.id} value={item.id}>
                        {item.title}
                      </option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Section *
                  </label>
                  <input
                    type="text"
                    value={formData.section_title}
                    onChange={(e) => setFormData({ ...formData, section_title: e.target.value })}
                    required
                    placeholder="Ex: Introduction, La glycolyse..."
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Titre *
                  </label>
                  <input
                    type="text"
                    value={formData.title}
                    onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                    required
                    placeholder="Titre de la ressource"
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Phase pédagogique
                  </label>
                  <select
                    value={formData.phase}
                    onChange={(e) => setFormData({ ...formData, phase: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="activation">Activation</option>
                    <option value="exploration">Exploration</option>
                    <option value="explanation">Explication</option>
                    <option value="application">Application</option>
                    <option value="consolidation">Consolidation</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Niveau
                  </label>
                  <select
                    value={formData.difficulty_tier}
                    onChange={(e) => setFormData({ ...formData, difficulty_tier: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="beginner">Débutant</option>
                    <option value="intermediate">Intermédiaire</option>
                    <option value="advanced">Avancé</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Texte déclencheur
                  </label>
                  <input
                    type="text"
                    value={formData.trigger_text}
                    onChange={(e) => setFormData({ ...formData, trigger_text: e.target.value })}
                    placeholder="Ex: regarde ce schéma glycolyse"
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Description *
                </label>
                <textarea
                  value={formData.description}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                  required
                  rows={3}
                  placeholder="Description de la ressource"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Concepts (séparés par des virgules)
                </label>
                <input
                  type="text"
                  value={formData.concepts}
                  onChange={(e) => setFormData({ ...formData, concepts: e.target.value })}
                  placeholder="Ex: glycolyse, ATP, cytoplasme"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                />
              </div>

              {(activeTab === 'image' || activeTab === 'video') && (
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Fichier {activeTab === 'image' ? 'image' : 'vidéo'}
                  </label>
                  <input
                    type="file"
                    accept={activeTab === 'image' ? 'image/*' : 'video/*'}
                    onChange={(e) => setUploadFile(e.target.files?.[0] || null)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                  />
                  <p className="text-sm text-gray-500 mt-1">
                    Ou spécifiez un chemin manuel ci-dessous
                  </p>
                </div>
              )}

              {activeTab === 'simulation' && (
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    URL de la simulation
                  </label>
                  <input
                    type="text"
                    value={formData.file_path}
                    onChange={(e) => setFormData({ ...formData, file_path: e.target.value })}
                    placeholder="/media/simulations/svt/..."
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  />
                </div>
              )}

              {(activeTab === 'image' || activeTab === 'video') && (
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Chemin du fichier (manuel)
                  </label>
                  <input
                    type="text"
                    value={formData.file_path}
                    onChange={(e) => setFormData({ ...formData, file_path: e.target.value })}
                    placeholder="/media/images/svt/..."
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  />
                </div>
              )}

              {activeTab === 'exam' && (
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Chemin du fichier examen
                  </label>
                  <input
                    type="text"
                    value={formData.file_path}
                    onChange={(e) => setFormData({ ...formData, file_path: e.target.value })}
                    placeholder="/media/exams/svt/..."
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  />
                </div>
              )}

              <div className="flex gap-4">
                <button
                  type="submit"
                  disabled={loading}
                  className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400"
                >
                  {loading ? 'Enregistrement...' : editingResource ? 'Modifier' : 'Ajouter'}
                </button>
                <button
                  type="button"
                  onClick={() => {
                    setShowForm(false);
                    resetForm();
                  }}
                  className="px-6 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300"
                >
                  Annuler
                </button>
              </div>
            </form>
          </div>
        )}

        <div className="bg-white rounded-lg shadow-sm p-6">
          <h2 className="text-xl font-bold mb-4">
            {resourceTypes.find(r => r.type === activeTab)?.label} existantes
          </h2>

          {loading ? (
            <div className="text-center py-8 text-gray-500">Chargement...</div>
          ) : resources.length === 0 ? (
            <div className="text-center py-8 text-gray-500">
              {resourceLessonFilter
                ? 'Aucune ressource de ce type pour ce cours pour le moment'
                : 'Aucune ressource de ce type pour le moment'}
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {resources.map((resource) => (
                <div
                  key={resource.id}
                  className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow"
                >
                  <div className="flex justify-between items-start mb-2">
                    <h3 className="font-semibold text-gray-900">{resource.title}</h3>
                    <span className="text-xs px-2 py-1 bg-blue-100 text-blue-800 rounded">
                      {resource.difficulty_tier}
                    </span>
                  </div>
                  <p className="text-sm text-gray-600 mb-2">{resource.description}</p>
                  <div className="text-xs text-gray-500 space-y-1 mb-3">
                    <div>Section: {resource.section_title}</div>
                    {resource.metadata?.micro_enseignement_title && (
                      <div>Micro-enseignement: {String(resource.metadata.micro_enseignement_title)}</div>
                    )}
                    <div>Phase: {resource.phase}</div>
                    {resource.concepts.length > 0 && (
                      <div>Concepts: {resource.concepts.join(', ')}</div>
                    )}
                  </div>
                  <div className="flex gap-2">
                    <button
                      onClick={() => handleEdit(resource)}
                      className="flex-1 px-3 py-1 bg-blue-50 text-blue-600 rounded hover:bg-blue-100 text-sm"
                    >
                      Modifier
                    </button>
                    <button
                      onClick={() => handleDelete(resource.id)}
                      className="flex-1 px-3 py-1 bg-red-50 text-red-600 rounded hover:bg-red-100 text-sm"
                    >
                      Supprimer
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
