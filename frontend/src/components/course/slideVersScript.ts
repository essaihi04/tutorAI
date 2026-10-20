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
 * Le professeur pose d'abord la figure et le contexte nécessaires. Si la
 * diapositive interroge l'élève, il pose ENSUITE la question et attend sa
 * réponse avant d'écrire ou de dire la correction. Cette règle évite qu'une
 * explication révèle la réponse juste avant l'interrogation.
 *
 * ── La voix ──
 *
 * L'explication porte l'enregistrement PUBLIÉ de la diapositive quand il y en
 * a un (`slide.audio`) : c'est la voix qu'un auteur a écoutée et validée, et
 * la resynthétiser au moment de la lecture serait plus lent et moins fidèle.
 * Avec un enregistrement, la parole COMMENCE AVEC L'ÉCRITURE, dès le titre :
 * le professeur parle pendant qu'il écrit, et tout le tableau s'écrit en
 * silence sous sa voix. La question de la diapositive vient alors À LA FIN,
 * une fois la parole terminée : elle vérifie ce qui vient d'être expliqué.
 * (Toutes les diapositives publiées portent une question ; la placer avant
 * la parole, c'était faire attendre la voix sur chaque diapositive.)
 * Sans enregistrement, chaque ligne est dite par le tableau en l'écrivant,
 * la question précède la correction, et l'explication vient à la fin.
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
  const parole = textePourLaLangue(slide.speech_text, langue);
  const pistes = slide.audio || {};
  const piste = pistes[langue] || pistes.mixed || pistes.fr || Object.values(pistes)[0];
  const paroleEnregistree = !!(parole && piste?.url);
  const enonce = (slide.question?.prompt || '').trim();
  const poserLaQuestion = () => {
    if (!enonce) return;
    steps.push({
      action: 'ask',
      text: enonce,
      options: (slide.question?.options || []).filter(option => !!option?.trim()).slice(0, 4),
    });
  };
  const contenu = slide.screen_content || {};
  const visuel = slide.visual;

  const figureLaterale = visuel && visuel.placement !== 'inline';
  const figureDansLeTexte = visuel && visuel.placement === 'inline';

  // La parole enregistrée part dès le début, figure comprise : sa légende n'est
  // alors pas dite par le tableau (elle couperait la voix du professeur).
  if (paroleEnregistree) {
    steps.push({ action: 'narrate', text: parole, audio_url: piste?.url, background: true });
  }
  const legende = (texte?: string) => (paroleEnregistree ? undefined : texte);

  // ── 1. La figure latérale, d'abord ──
  if (figureLaterale) {
    if (visuel.kind === 'schema' && visuel.schema_id) {
      steps.push({ action: 'figure', schema_id: visuel.schema_id, say: legende(visuel.caption) });
    } else if (visuel.kind === 'scientific' && visuel.scientific) {
      steps.push({ action: 'figure', scientific: visuel.scientific, say: legende(visuel.caption) });
    } else if (visuel.kind === 'image' && visuel.url) {
      steps.push({
        action: 'figure',
        image: { url: visuel.url, alt: visuel.alt || contenu.alt, caption: visuel.caption || contenu.caption },
        say: legende(visuel.caption),
      });
    } else if (visuel.kind === 'simulation' && visuel.url) {
      steps.push({
        action: 'figure',
        simulation: { url: visuel.url, caption: visuel.caption || contenu.caption },
        say: legende(visuel.caption),
      });
    }
  }

  // ── 2. Ce qui s'écrit — sous la parole enregistrée, s'il y en a une ──
  const ecrire = (type: string, contenuLigne?: string | null) => {
    const propre = (contenuLigne || '').trim();
    if (propre) steps.push({ action: 'write', line: { type, content: propre } });
  };

  ecrire('title', slide.title);
  if (figureDansLeTexte && visuel.kind === 'schema' && visuel.schema_id) {
    steps.push({
      action: 'bloc',
      line: {
        type: 'schema',
        content: visuel.caption || '',
        schema_id: visuel.schema_id,
      },
    });
  }
  ecrire('subtitle', contenu.lead);

  // ── 3. Sans enregistrement, la question vient AVANT la correction ──
  if (!paroleEnregistree) poserLaQuestion();

  // ── 4. Correction écrite, seulement après la réponse de l'élève ──
  // Le texte essentiel ne se réécrit pas s'il répète le chapeau : deux lignes
  // identiques à la craie, c'est une faute de tableau, pas une insistance.
  if ((contenu.essential_text || '').trim() !== (contenu.lead || '').trim()) {
    ecrire('text', contenu.essential_text);
  }
  (contenu.bullets || []).forEach(puce => ecrire('step', puce));
  if (contenu.table?.headers?.length && contenu.table.rows?.length) {
    steps.push({
      action: 'bloc',
      line: {
        type: 'table',
        content: '',
        headers: contenu.table.headers,
        rows: contenu.table.rows,
      },
    });
  }
  if (contenu.student_trace) {
    steps.push({ action: 'write', line: { type: 'box', content: contenu.student_trace, color: 'green' } });
  }

  // ── 5. Les exercices cliquables, sur le tableau désormais complété ──
  //
  // Ils viennent après l'écrit : on n'évalue pas une notion avant de l'avoir
  // posée. Et avant la parole finale, pour que le professeur commente un
  // tableau où l'élève a déjà de quoi travailler sous les doigts.
  (slide.exercises || []).forEach(exercice => {
    const enonceExercice = (exercice.prompt || '').trim();
    if (!enonceExercice) return;
    if (exercice.type === 'qcm' && exercice.choices?.length) {
      steps.push({
        action: 'bloc',
        line: {
          type: 'qcm',
          content: enonceExercice,
          choices: exercice.choices,
          correct: typeof exercice.correct === 'number' ? exercice.correct : 0,
          explanation: exercice.explanation,
        },
      });
    } else if (exercice.type === 'vrai_faux' && exercice.statements?.length) {
      steps.push({
        action: 'bloc',
        line: {
          type: 'vrai_faux',
          content: enonceExercice,
          statements: exercice.statements,
          explanation: exercice.explanation,
        },
      });
    } else if (exercice.type === 'association' && exercice.pairs?.length) {
      steps.push({
        action: 'bloc',
        line: {
          type: 'association',
          content: enonceExercice,
          pairs: exercice.pairs,
          explanation: exercice.explanation,
        },
      });
    }
  });

  // ── 6. Avec enregistrement, la question vérifie ce qui vient d'être dit ──
  //    (l'étape `ask` attend la fin de la parole avant de prendre la voix).
  if (paroleEnregistree) poserLaQuestion();

  // ── 7. Sans enregistrement : correction orale, devant le tableau complété ──
  if (parole && !paroleEnregistree) {
    steps.push({ action: 'narrate', text: parole });
  }

  // Une diapositive sans rien à écrire ni à dire laisserait un tableau vide et
  // un moteur qui se croit fini avant d'avoir commencé.
  if (steps.length === 0) {
    steps.push({ action: 'write', line: { type: 'title', content: slide.title || '…' } });
  }

  return { title: slide.title, steps };
}
