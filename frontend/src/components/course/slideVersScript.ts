/**
 * Une diapositive de cours devient un script de tableau.
 *
 * Le lecteur de cours redessinait sa propre surface : un cadre, du texte posé,
 * une image. Le tableau en direct, lui, sait déjà écrire à la craie au rythme
 * de la voix, dessiner, poser une figure, zoomer sur un détail, se mettre en
 * plein écran et attendre une réponse. Plutôt que de refaire tout cela une
 * seconde fois, on traduit : chaque diapositive est rendue par `LiveBoard`.
 *
 * ── L'ordre des étapes ──
 *
 * Le professeur pose d'abord sa figure — l'élève doit voir de quoi on parle
 * avant d'entendre parler. Il écrit ensuite son titre puis ses lignes, chacune
 * lue à mesure qu'elle s'écrit (c'est le comportement par défaut d'un `write`
 * sans `say`). Il explique enfin, à voix nue, devant un tableau déjà rempli —
 * c'est le `speech_text` de la diapositive. Et si elle porte une question, il
 * la pose et il ATTEND.
 *
 * ── La voix ──
 *
 * L'explication porte l'enregistrement PUBLIÉ de la diapositive quand il y en
 * a un (`slide.audio`) : c'est la voix qu'un auteur a écoutée et validée, et
 * la resynthétiser au moment de la lecture serait plus lent et moins fidèle.
 * Les lignes écrites, elles, sont dites par le tableau lui-même — elles sont
 * courtes, et leur synthèse est mise en cache côté serveur. Sans
 * enregistrement, tout retombe sur la voix du tableau.
 */
import type { LiveScript, LiveStep } from '../session/LiveBoard';
import type { CourseSlide } from './types';

/** La langue de ce qui est DIT autour du tableau (l'écrit reste en français). */
export type LangueSeance = 'fr' | 'ar' | 'mixed';

function textePourLaLangue(
  champ: Record<string, string> | undefined,
  langue: LangueSeance,
): string {
  if (!champ) return '';
  return (champ[langue] || champ.mixed || champ.fr || Object.values(champ)[0] || '').trim();
}

export function slideVersScript(slide: CourseSlide, langue: LangueSeance): LiveScript {
  const steps: LiveStep[] = [];
  const contenu = slide.screen_content || {};
  const visuel = slide.visual;

  // ── 1. La figure, d'abord ──
  if (visuel) {
    if (visuel.kind === 'schema' && visuel.schema_id) {
      steps.push({ action: 'figure', schema_id: visuel.schema_id, say: visuel.caption });
    } else if (visuel.kind === 'scientific' && visuel.scientific) {
      steps.push({ action: 'figure', scientific: visuel.scientific, say: visuel.caption });
    } else if (visuel.kind === 'image' && visuel.url) {
      steps.push({
        action: 'figure',
        image: { url: visuel.url, alt: visuel.alt || contenu.alt, caption: visuel.caption || contenu.caption },
        say: visuel.caption,
      });
    } else if (visuel.kind === 'simulation' && visuel.url) {
      steps.push({
        action: 'figure',
        simulation: { url: visuel.url, caption: visuel.caption || contenu.caption },
        say: visuel.caption,
      });
    }
  }

  // ── 2. Ce qui s'écrit ──
  const ecrire = (type: string, contenuLigne?: string | null) => {
    const propre = (contenuLigne || '').trim();
    if (propre) steps.push({ action: 'write', line: { type, content: propre } });
  };

  ecrire('title', slide.title);
  ecrire('subtitle', contenu.lead);
  // Le texte essentiel ne se réécrit pas s'il répète le chapeau : deux lignes
  // identiques à la craie, c'est une faute de tableau, pas une insistance.
  if ((contenu.essential_text || '').trim() !== (contenu.lead || '').trim()) {
    ecrire('text', contenu.essential_text);
  }
  (contenu.bullets || []).forEach(puce => ecrire('step', puce));
  if (contenu.student_trace) {
    steps.push({ action: 'write', line: { type: 'box', content: contenu.student_trace, color: 'green' } });
  }

  // ── 3. L'explication, devant le tableau écrit ──
  const parole = textePourLaLangue(slide.speech_text, langue);
  if (parole) {
    const pistes = slide.audio || {};
    const piste = pistes[langue] || pistes.mixed || pistes.fr || Object.values(pistes)[0];
    steps.push({ action: 'narrate', text: parole, audio_url: piste?.url });
  }

  // ── 4. La question, s'il y en a une : il la pose et il attend ──
  const question = slide.question;
  const enonce = (question?.prompt || '').trim();
  if (enonce) {
    steps.push({
      action: 'ask',
      text: enonce,
      options: (question?.options || []).filter(option => !!option?.trim()).slice(0, 4),
    });
  }

  // Une diapositive sans rien à écrire ni à dire laisserait un tableau vide et
  // un moteur qui se croit fini avant d'avoir commencé.
  if (steps.length === 0) {
    steps.push({ action: 'write', line: { type: 'title', content: slide.title || '…' } });
  }

  return { title: slide.title, steps };
}
