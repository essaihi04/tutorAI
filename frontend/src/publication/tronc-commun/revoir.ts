/**
 * Ce que chaque élève doit retravailler (24 novembre 2026, demande de l'utilisateur : « câbler ce qu'il faut retravailler
 * pour chaque élève ») : chaque question d'examen ratée et chaque réponse fausse d'un cours mène à la diapositive où la
 * notion est expliquée (`?cours=<id>&diapo=<id>` : le cours s'ouvre sur cette diapositive).
 *
 * Les questions d'examen → leurs diapositives, page par page (Tronc Commun : `sujet.ts` ; 2ᵉ Bac PC : `bac2pcf/sujets.ts`).
 */
import { useEffect, useState } from 'react';
import { apiSuivi, eleveEnregistre } from './suivi';

export interface Lien { cours: string; diapo: string; titre: string }
const L = (cours: string, diapo: string, titre: string): Lien => ({ cours, diapo, titre });

const SE = 'tc_svt_sortie_ecologique', FE = 'tc_svt_facteurs_edaphiques', RV = 'tc_svt_revision';
/** Tronc Commun, l'évaluation formative (clé de suivi « examen ») */
export const REVOIR_TC: Record<string, Lien[]> = {
  '1': [L(FE, 'fe_t8_texture', 'La texture du sol'), L(FE, 'fe_c3_calcium', 'Calcifuge et calcicole'), L(FE, 'fe_h6_formes', 'Les trois formes d’eau du sol'), L(SE, 'se_a1_croix', 'La croix du bûcheron')],
  '2': [L(FE, 'fe_c7_charges', 'Le complexe argilo-humique, chargé négativement'), L(FE, 'fe_h3_permeabilite', 'La perméabilité'), L(SE, 'se_a3_indices', 'L’indice de fréquence'), L(SE, 'se_a4_ecosysteme', 'L’écosystème = biotope + biocénose')],
  '3-a': [L(FE, 'fe_h7_retention_pf', 'Capacité de rétention et point de flétrissement')],
  '3-b': [L(SE, 'se_a2_courbe', 'La courbe et l’aire minimale')],
  '1-1': [L(RV, 'rv_h2_calcul', 'Méthode : calculer P et Vr'), L(FE, 'fe_h3_permeabilite', 'Calculer la perméabilité P')],
  '1-2': [L(RV, 'rv_h2_calcul', 'Méthode : calculer P et Vr'), L(FE, 'fe_h3_permeabilite', 'Calculer la perméabilité P')],
  '1-3': [L(RV, 'rv_h2_calcul', 'Méthode : calculer P et Vr'), L(FE, 'fe_h4_retention', 'Calculer la capacité de rétention Vr')],
  '1-4': [L(RV, 'rv_h2_calcul', 'Méthode : calculer P et Vr'), L(FE, 'fe_h4_retention', 'Calculer la capacité de rétention Vr')],
  '1-5': [L(FE, 'fe_h3_permeabilite', 'La perméabilité'), L(FE, 'fe_h4_retention', 'La capacité de rétention')],
  '1-6': [L(RV, 'rv_h3_eau', 'L’eau du sol et le point de flétrissement'), L(FE, 'fe_h7_retention_pf', 'Capacité de rétention et point de flétrissement')],
  '1-7': [L(RV, 'rv_t1_triangle', 'Méthode : placer un sol dans le triangle'), L(FE, 'fe_t5_triangle', 'Le triangle des textures')],
  '2-1': [L(FE, 'fe_c6_filtration', 'Deux colorants sur un sol riche en humus')],
  '2-2': [L(FE, 'fe_c7_charges', 'Le complexe argilo-humique est chargé négativement')],
  '2-3': [L(RV, 'rv_c2_cah', 'Le complexe argilo-humique retient les cations'), L(FE, 'fe_c9_retention', 'Avec le complexe argilo-humique, les sels sont gardés')],
  '3-1': [L(RV, 'rv_s1_aire', 'Méthode : l’aire minimale'), L(SE, 'se_a2_courbe', 'La courbe et l’aire minimale')],
  '3-2': [L(RV, 'rv_s2_frequence', 'Méthode : la fréquence et l’indice'), L(SE, 'se_a3_frequence', 'La fréquence F = n/N × 100')],
  '3-3': [L(SE, 'se_a3_indices', 'L’indice de fréquence : de I à V')],
  '3-4': [L(SE, 'se_a3_faune_calcul', 'Abondance, densité, densité relative')],
  '3-5': [L(RV, 'rv_s3_histogramme', 'Méthode : l’histogramme et la courbe'), L(SE, 'se_a3_histogramme', 'L’histogramme et la courbe de fréquence')],
  '3-6': [L(SE, 'se_a3_formes', 'Unimodale ou bimodale ?')],
};

const PH = 'rev_phys_ondes_radioactivite', CH = 'rev_chim_deux_sens_equilibre';
/** 2ᵉ Bac PC : les deux examens (clés de suivi « examen_physique », « examen_chimie ») */
export const REVOIR_2BAC: Record<string, Record<string, Lien[]>> = {
  examen_physique: {
    '1-1': [L(PH, 'ol_t4_relation', 'La relation θ = λ/a')],
    '1-2': [L(PH, 'ol_l9_etablir', 'Établir la largeur L de la tache')],
    '1-3': [L(PH, 'ol_c3_rapport', 'Deux expériences : le rapport')],
    '2-1': [L(PH, 'ra_t2_demo', 'Établir t½ = ln2/λ')],
    '2-2': [L(PH, 'ra_l5_loi', 'La loi de décroissance')],
    '2-3': [L(PH, 'ra_l5_loi', 'La loi de décroissance'), L(PH, 'ra_t3_paliers', 'N₀/2, N₀/4, N₀/8')],
  },
  examen_chimie: {
    '1-1': [L(CH, 'td_p4_eau', 'Un acide réagit avec l’eau')],
    '1-2': [L(CH, 'ee_z5_ph', 'Le pH et [H₃O⁺]')],
    '1-3': [L(CH, 'td_p6_totale', 'Si la réaction était totale : x_max')],
    '1-4': [L(CH, 'ee_r1_taux', 'Le taux d’avancement final τ')],
    '2-1': [L(CH, 'td_p4_eau', 'Un acide réagit avec l’eau')],
    '2-2': [L(CH, 'ee_z5_ph', 'Le pH et [H₃O⁺]')],
    '2-3': [L(CH, 'ee_e1_concentrations', 'Les concentrations à l’équilibre')],
    '2-4': [L(CH, 'ee_e2_quotient', 'Le quotient de réaction à l’équilibre'), L(CH, 'ee_k3_constante', 'La constante d’équilibre K')],
  },
};

/** Ce que le serveur sait de l'élève : ses questions d'examen ratées et ses réponses fausses dans les cours. */
export interface ARetravailler {
  questions: { examen: string; id: string; note: number; sur: number; pertes: string[]; enonce?: string }[];
  cours: { cours: string; slide_id: string; titre?: string; enonce?: string }[];
}
export function useARetravailler() {
  const [d, setD] = useState<ARetravailler | null>(null);
  useEffect(() => {
    const e = eleveEnregistre();
    if (!e) return;
    fetch(`${apiSuivi()}/a-retravailler`, { headers: { 'X-Eleve': e.id } })
      .then(r => (r.ok ? r.json() : null)).then(setD).catch(() => setD(null));
  }, []);
  return d;
}
export const lienDiapo = (l: { cours: string; diapo: string }) => `./?cours=${encodeURIComponent(l.cours)}&diapo=${encodeURIComponent(l.diapo)}`;
