/**
 * `/telephone?t=K7P4QX` (27/11/2026) : la page du téléphone relié à la page d'un exercice du site principal
 * (« 📱 Avec mon téléphone »). Sans compte : le code du canal suffit ; la photo est lue par le relais.
 */
import { PageTelephone } from '../components/course/photoTelephone';

export default function TelephoneExercice() {
  return <PageTelephone code={new URLSearchParams(window.location.search).get('t') || ''} titre="Moalim · Exercices" />;
}
