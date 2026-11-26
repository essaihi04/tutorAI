/**
 * L'année du bac, à UN seul endroit (26 novembre 2026).
 *
 * Avant, « BAC 2026 », « 4 juin 2026 » et « J-28 » étaient écrits en dur dans la landing, le diagnostic, le plan
 * d'étude et l'inscription : à la rentrée, toute la vitrine parlait encore de l'examen passé. Chaque rentrée, on
 * change ces trois lignes et rien d'autre.
 *
 * DATE PROVISOIRE : au 26 novembre 2026, le ministère n'a pas encore publié le calendrier des examens 2027. Le
 * 1er juin 2027 est la date annoncée par la presse scolaire (session normale du 1er au 3 juin 2027), à confirmer
 * dès la note ministérielle (en général en janvier).
 */
export const BAC_YEAR = 2027;
export const ANNEE_SCOLAIRE = '2026-2027';
export const BAC_DATE = new Date('2027-06-01T08:00:00');
/** La date est-elle celle du calendrier officiel ? Tant que non, la page écrit « juin 2027 » sans le jour. */
export const BAC_DATE_OFFICIELLE = false;

/** Jours restants avant la première épreuve (0 une fois l'examen commencé). */
export const joursAvantBac = (maintenant = Date.now()) =>
  Math.max(0, Math.ceil((BAC_DATE.getTime() - maintenant) / 86_400_000));
