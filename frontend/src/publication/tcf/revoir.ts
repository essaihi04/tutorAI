/**
 * Ce que l'élève doit retravailler après l'évaluation de /TCF (modèle : `REVOIR_TC` de `../tronc-commun/revoir.ts`) :
 * chaque question ratée de `sujet.ts` mène aux diapositives du cours qui l'expliquent (`?cours=<id>&diapo=<id>`).
 *
 * Les trois cours (tc_chim_synthese, tc_chim_atome, tc_phys_mouvement_inertie) étaient en cours d'écriture quand
 * l'évaluation a été faite (25/11/2026) : leurs ids de diapositives n'existaient pas encore, la table est vide. À remplir,
 * question par question, avec `L(cours, diapo, titre)` dès que les cours sont finis :
 *   1-1 montage à reflux ; 1-2 rôle du chauffage à reflux ; 1-3 synthèse, réactifs/produits, phases de la CCM, révélation ;
 *   1-4, 1-5 calcul de Rf = h/H ; 1-6 identifier une espèce et la pureté sur un chromatogramme ;
 *   2-1 noyau, charge Z·e, dimensions, isotopes ; 2-2 N = A − Z ; 2-3 m ≈ A·mp ; 2-4 (K)²(L)⁸(M)…, couche externe ;
 *   2-5 ions, cation, élément chimique ; 2-6 charge d'un ion ;
 *   3-1 relativité, trajectoire, km/h → m/s, vecteur vitesse ; 3-2 vm = d/Δt ; 3-3 vᵢ = Mᵢ₋₁Mᵢ₊₁/(2τ) ;
 *   3-4 mouvement rectiligne uniforme ; 3-5 x(t) = v·t + x₀ ; 3-6 ω = v/R ; 3-7 T = 2π/ω ;
 *   4-1 pseudo-isolé, principe d'inertie, centre d'inertie ; 4-2, 4-3 inventaire des forces et principe d'inertie ;
 *   4-4, 4-5 centre d'inertie d'un système de deux corps (G₁G = m₂/(m₁ + m₂) × G₁G₂).
 */
import type { Lien } from '../tronc-commun/revoir';

export const COURS_TCF = { synthese: 'tc_chim_synthese', atome: 'tc_chim_atome', mouvement: 'tc_phys_mouvement_inertie' } as const;

/** /TCF, l'évaluation formative (clé de suivi « examen_tcf ») : question → diapositives à revoir */
export const REVOIR_TCF: Record<string, Lien[]> = {};
