/**
 * Banc d'essai du lecteur de cours — mise en page seule.
 *
 * Le lecteur n'apparaît qu'au bout d'une session authentifiée sur une leçon
 * possédant un deck rédigé : impossible de regarder sa mise en page sans
 * rejouer tout le parcours. Cette page le monte seul, avec un deck factice et
 * un chat simulé à gauche, pour vérifier d'un coup d'œil ce que l'élève voit.
 */
import { useState } from 'react';
import CoursePlayer from '../components/course/CoursePlayer';
import type { CourseDeck } from '../components/course/types';
import energyManifestSource from '../../../backend/data/courses/svt_ch1_energy_course_v1.json?raw';
import muscleManifestSource from '../../../backend/data/courses/svt_ch1_muscle_course_v1.json?raw';

const ENERGY_MANIFEST = JSON.parse(energyManifestSource) as CourseDeck;
const MUSCLE_MANIFEST = JSON.parse(muscleManifestSource) as CourseDeck;

const DECK: CourseDeck = {
  id: 'deck-demo-glycolyse-v4',
  lesson_id: 'lesson-demo',
  title: "Consommation de la matière organique et libération de l'énergie",
  activities: [
    {
      id: 'act-1',
      title: 'Respiration ou fermentation — enquête expérimentale',
      slides: [
        {
          id: 'slide-1',
          slide_type: 'concept',
            title: 'Du glucose aux pyruvates',
            screen_content: {
            lead: 'Observe le trajet des six carbones dans le cytoplasme.',
            bullets: [
              'Lieu : cytoplasme',
              '1 glucose à 6 C → 2 pyruvates à 3 C',
              'Bilan net : 2 ATP et 2 NADH,H⁺',
            ],
            essential_text: 'La glycolyse est commune à la respiration et aux fermentations.',
            },
            visual: {
            kind: 'simulation',
            url: '/media/simulations/svt/ch1_consommation_matiere_organique/glycolyse/index.html',
            caption: 'Simulation — glycolyse dans la cellule, puis trajet des pyruvates vers la mitochondrie',
            },
            speech_text: {
            fr: 'La glycolyse se déroule dans le cytoplasme. Deux ATP sont investis pour activer le glucose à six carbones. La molécule se sépare ensuite en deux chaînes à trois carbones qui deviennent deux pyruvates ; quatre ATP et deux NADH,H⁺ sont formés. Le gain net est donc de deux ATP, sans consommation directe de dioxygène.',
            },
            question: {
            prompt: 'En regardant la chaîne, combien de carbones porte chaque pyruvate ?',
            options: ['3 carbones', '6 carbones', '36 carbones'],
            timeout_seconds: 14,
            },
          timing: { reading_seconds: 8 },
        },
        {
          id: 'slide-image',
          slide_type: 'image',
          title: 'La cuve à ondes',
          screen_content: { lead: 'Deux capteurs, un même front d’onde.' },
          visual: {
            kind: 'image',
            url: '/media/images/svt/ch1_consommation_matiere_organique/diagnostic/test_iode_amidon_reconstitution.png',
            caption: 'Reconstitution pédagogique d’un test à l’iode sur feuille panachée',
          },
          speech_text: { fr: 'Voici le montage : la source à gauche, deux capteurs alignés sur le trajet du front.' },
          // Enregistrement publié : le tableau doit le jouer tel quel plutôt
          // que de resynthétiser l'explication.
          audio: { fr: { url: '/media/audio/courses/svt_ch1_energy/mixed/energy_a00_s01_v1.wav' } },
          timing: { reading_seconds: 7 },
        },
        {
          id: 'slide-schema',
          slide_type: 'schema',
          title: 'La mitochondrie',
          screen_content: { lead: 'Double membrane, crêtes, matrice.' },
          visual: { kind: 'schema', schema_id: 'svt_croquis_mitochondrie', caption: 'Croquis au tableau' },
          speech_text: { fr: 'La membrane externe est lisse ; l’interne se replie en crêtes.' },
        },
        {
          id: 'slide-simu',
          slide_type: 'simulation',
          title: 'Respiration et fermentation',
          visual: {
            kind: 'simulation',
            url: '/media/simulations/svt/ch1_consommation_matiere_organique/labs/respiration-fermentation/index.html',
            caption: 'Laboratoire virtuel',
          },
          speech_text: { fr: 'Fais varier l’oxygène et regarde le bilan en ATP.' },
        },
        {
          id: 'slide-eval',
          slide_type: 'evaluation',
          title: 'Faire le point sur la glycolyse',
          screen_content: {
            lead: 'Avant la mitochondrie, vérifions ce qui vient d’être établi.',
            bullets: ['Le lieu', 'Le devenir des six carbones', 'Le bilan net'],
          },
          visual: { kind: 'none' },
          question: {
            type: 'qcm',
            prompt: 'La glycolyse produit quatre ATP, mais son gain net n’est que de deux. Pourquoi ?',
            options: [
              'Deux ATP ont été investis dans la phase d’activation du glucose',
              'Deux ATP sont détruits par la mitochondrie',
              'Deux ATP servent à fabriquer le NADH,H⁺',
            ],
            timeout_seconds: 20,
          },
          exercises: [
            {
              type: 'qcm',
              prompt: 'Pourquoi la glycolyse est-elle commune à la respiration ET aux fermentations ?',
              choices: [
                'Parce qu’elle ne consomme directement aucun dioxygène',
                'Parce qu’elle se déroule dans la matrice mitochondriale',
                'Parce qu’elle produit autant d’ATP que le cycle de Krebs',
              ],
              correct: 0,
              explanation: 'Aucune étape de la glycolyse n’utilise le dioxygène : elle se déroule à l’identique en aérobiose comme en anaérobiose.',
            },
            {
              type: 'association',
              prompt: 'Relie chaque élément au rôle qu’il joue dans la glycolyse.',
              pairs: [
                { left: 'Cytoplasme', right: 'Lieu de la glycolyse' },
                { left: 'Glucose (6 C)', right: 'Molécule dégradée au départ' },
                { left: '2 pyruvates (3 C)', right: 'Produits carbonés de la glycolyse' },
                { left: '2 NADH,H⁺', right: 'Transporteurs réduits formés' },
                { left: '2 ATP nets', right: 'Gain énergétique directement utilisable' },
              ],
              explanation: 'Les six carbones du glucose se retrouvent intégralement dans les deux pyruvates.',
            },
          ],
          speech_text: { fr: 'Deux questions t’attendent au tableau, puis un exercice où tu relies chaque élément à son rôle.' },
        },
        {
          id: 'slide-2',
          slide_type: 'synthesis',
          title: 'Ce qu’il faut retenir',
          screen_content: {
            essential_text: 'v = d / Δt',
            student_trace: 'La célérité se lit toujours sur deux points du même front.',
          },
          speech_text: { fr: 'La célérité, c’est la distance parcourue par le front divisée par la durée du trajet.' },
          timing: { reading_seconds: 6 },
        },
      ],
    },
  ],
};

export default function CoursePlayerAudit() {
  const [messages, setMessages] = useState<string[]>([]);
  const [chatVisible, setChatVisible] = useState(true);
  // Preview the authored slide through the real player, without changing the
  // published deck or requiring a student session.
  const scene = new URLSearchParams(window.location.search).get('scene');
  const previewId = scene === 'pyruvate' ? 'energy_a10_s01' : scene === 'glucose-journey' ? 'energy_a08_s02' : 'energy_a07_s02';
  const respiratorySlide = ENERGY_MANIFEST.activities.flatMap(activity => activity.slides)
    .find(slide => slide.id === previewId);
  const deck = scene === 'muscle' ? MUSCLE_MANIFEST : (scene === 'respiratory-chain' || scene === 'glucose-journey' || scene === 'pyruvate') && respiratorySlide
    ? { ...DECK, id: `${scene}-preview`, activities: [{
      id: scene, title: scene === 'pyruvate' ? 'Le carrefour du pyruvate' : scene === 'glucose-journey' ? 'Le voyage du glucose' : 'Chaîne respiratoire et phosphorylation oxydative',
      slides: [respiratorySlide],
    }] }
    : DECK;

  return (
    <div className="h-screen w-screen bg-[#0a0a18] text-white flex">
      {chatVisible && (
      <div className="w-[280px] shrink-0 border-r border-white/5 bg-[#0a0a18]/80 flex flex-col">
        <div className="flex-1 overflow-y-auto px-4 py-6 space-y-3">
          {messages.length === 0 && (
            <p className="text-white/30 text-sm">En attente du tuteur IA…</p>
          )}
          {messages.map((texte, i) => (
            <div key={i} className="rounded-2xl rounded-tl-md border border-white/10 bg-white/[0.07] px-4 py-3 text-sm leading-relaxed whitespace-pre-wrap">
              {texte}
            </div>
          ))}
        </div>
        <div className="border-t border-white/5 p-3 text-xs text-white/30">
          Champ de saisie (simulé)
        </div>
      </div>
      )}

      <div className="flex-1 min-w-0 p-2">
        <div className="h-full w-full overflow-hidden rounded-2xl border border-white/10">
          <CoursePlayer
            deck={deck}
            language="fr"
            onNarration={texte => setMessages(liste => [...liste, texte])}
            onStudentQuestion={texte => setMessages(liste => [...liste, `Élève : ${texte}`])}
            onFocusChange={focus => setChatVisible(!focus)}
          />
        </div>
      </div>
    </div>
  );
}
