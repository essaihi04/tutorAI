/**
 * Charte sémantique commune aux croquis « professeur au tableau ».
 *
 * Une couleur garde le même rôle dans toutes les matières : le LLM peut donc
 * demander une mise en évidence sans réinventer une palette pour chaque dessin.
 */
export const BAC_PENCIL_PALETTE_ID = 'bac-pencil-v1';

export const BAC_PENCIL = {
  ink: '#e2e8f0',       // contour, texte et relation principale
  muted: '#94a3b8',     // repère, milieu, construction auxiliaire
  observed: '#67e8f9',  // donnée observée, mesure, axe ou capteur
  input: '#60a5fa',     // état initial, source, réactif ou variable x
  positive: '#86efac',  // propagation, résultat valide, produit ou limite
  control: '#fbbf24',   // variable manipulée, énergie, point d'attention
  alert: '#fda4af',     // opposition, risque d'erreur, interdit ou rupture
  reference: '#c4b5fd', // référence mathématique, asymptote ou comparaison
} as const;

export const BAC_PENCIL_FONT = '"Segoe Print", "Comic Sans MS", cursive';

/** Définitions SVG locales : le préfixe évite les collisions entre croquis. */
export function pencilDefs(prefix: string): string {
  return `
    <defs>
      <marker id="${prefix}-arrow" markerWidth="9" markerHeight="7" refX="8" refY="3.5" orient="auto">
        <path d="M0,0 L9,3.5 L0,7" fill="none" stroke="${BAC_PENCIL.ink}" stroke-width="1.4"/>
      </marker>
      <marker id="${prefix}-green-arrow" markerWidth="9" markerHeight="7" refX="8" refY="3.5" orient="auto">
        <path d="M0,0 L9,3.5 L0,7" fill="none" stroke="${BAC_PENCIL.positive}" stroke-width="1.4"/>
      </marker>
      <marker id="${prefix}-alert-arrow" markerWidth="9" markerHeight="7" refX="8" refY="3.5" orient="auto">
        <path d="M0,0 L9,3.5 L0,7" fill="none" stroke="${BAC_PENCIL.alert}" stroke-width="1.4"/>
      </marker>
    </defs>`;
}
