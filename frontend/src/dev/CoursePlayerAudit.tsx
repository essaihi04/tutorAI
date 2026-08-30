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

const DECK: CourseDeck = {
  id: 'deck-demo',
  lesson_id: 'lesson-demo',
  title: 'Les ondes mécaniques progressives',
  activities: [
    {
      id: 'act-1',
      title: 'Découvrir la propagation',
      slides: [
        {
          id: 'slide-1',
          slide_type: 'concept',
          title: 'Qu’est-ce qu’une onde ?',
          screen_content: {
            lead: 'Une perturbation qui se déplace, sans transport de matière.',
            essential_text: 'Une onde transporte de l’énergie, pas de la matière.',
            bullets: [
              'La corde monte et redescend : elle ne part pas avec l’onde.',
              'La célérité dépend du milieu, pas de l’amplitude.',
            ],
            student_trace: 'Une onde transporte de l’énergie, jamais de la matière.',
          },
          speech_text: {
            fr: 'Regarde cette corde. Quand je secoue une extrémité, une bosse part vers l’autre bout. Mais la corde, elle, ne voyage pas : chaque point monte puis redescend sur place.',
          },
          question: {
            prompt: 'Que transporte une onde mécanique ?',
            options: ['De la matière', 'De l’énergie', 'Les deux'],
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
            deck={DECK}
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
