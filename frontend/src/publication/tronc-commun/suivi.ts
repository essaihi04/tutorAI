/**
 * La fiche de l'élève et son suivi sur le lien du Tronc Commun (22 novembre 2026, demande de l'utilisateur).
 *
 * L'élève remplit sa fiche UNE seule fois (nom, classe, nom du père, téléphone) : le navigateur garde l'identifiant que
 * le serveur lui a donné ; la même fiche remplie ailleurs redonne le même identifiant (`/public/tronc-commun/inscription`).
 * Ensuite la page envoie : le temps passé (par tranches de 30 s, seulement quand la page est visible et que l'élève a
 * bougé dans les 5 dernières minutes), les diapositives vues, ses réponses dans les cours, chaque question de
 * l'évaluation et la note finale. L'admin lit tout dans l'onglet « Tronc Commun ».
 */
import { useEffect } from 'react';

export interface Eleve { id: string; nom: string; classe: string }
let CLE = 'moalim:tronc-commun:eleve';
export const API_TC = '/api/v1/public/tronc-commun';
/** l'adresse du suivi : celle du Tronc Commun, ou celle d'un autre lien libre (ex. /2bacpcf, `configurerSuivi`) */
let API = API_TC;
/** Un autre lien libre avec fiche (23/11/2026 : 2ᵉ Bac PC) : sa route et sa clé de navigateur. À appeler avant tout. */
export function configurerSuivi(c: { api: string; cle: string }) { API = c.api; CLE = c.cle; }
export const apiSuivi = () => API;
const fetchBrut = window.fetch.bind(window);

export function eleveEnregistre(): Eleve | null {
  try { const e = JSON.parse(localStorage.getItem(CLE) || 'null'); return e && e.id ? e : null; } catch { return null; }
}
export function garderEleve(e: Eleve | null) {
  try { if (e) localStorage.setItem(CLE, JSON.stringify(e)); else localStorage.removeItem(CLE); } catch { /* navigation privée */ }
}

export async function inscrire(fiche: { nom: string; prenom: string; classe: string; pere: string; telephone: string }): Promise<Eleve> {
  const r = await fetchBrut(`${API}/inscription`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(fiche) });
  const d = await r.json().catch(() => ({}));
  if (!r.ok) throw new Error(typeof d?.detail === 'string' ? d.detail : 'Inscription impossible, réessaie.');
  const e = { id: d.eleve_id, nom: d.nom, classe: d.classe };
  garderEleve(e);
  return e;
}

export type EvenementSuivi = {
  type: 'temps' | 'diapo' | 'reponse_cours' | 'examen_debut' | 'examen_question' | 'examen_fin' | 'examen_reprise';
  cours?: string; secondes?: number; slide_id?: string; titre?: string; position?: number; total?: number;
  enonce?: string; reponse?: string; correct?: boolean | null; question_id?: string; partie?: string;
  note?: number; sur?: number; verdict?: string; pertes?: string[];
  /** l'état affiché d'une question de l'évaluation, pour la remontrer telle quelle (une seule réponse compte) */
  etat?: Record<string, unknown>;
};

/** Où l'élève en est dans un cours (24/11/2026 : « garder l'avancement de chaque élève, ne pas commencer à zéro ») :
 * la dernière diapositive ouverte et celles déjà vues. Le serveur la donne d'après le suivi (même élève, tout appareil) ;
 * le navigateur en garde une copie pour le cas où le serveur ne répond pas. */
export interface Reprise { derniere: string; vues: string[]; position?: number; total?: number }
const cleReprise = (cours: string) => `${CLE}:reprise:${eleveEnregistre()?.id || ''}:${cours}`;
function noterReprise(cours: string, slide: string, position?: number, total?: number) {
  try {
    const r: Reprise = JSON.parse(localStorage.getItem(cleReprise(cours)) || 'null') || { derniere: '', vues: [] };
    localStorage.setItem(cleReprise(cours), JSON.stringify({ derniere: slide, position, total, vues: r.vues.includes(slide) ? r.vues : [...r.vues, slide] }));
  } catch { /* navigation privée */ }
}
export async function maReprise(cours: string): Promise<Reprise | null> {
  const e = eleveEnregistre();
  if (!e) return null;
  let locale: Reprise | null = null;
  try { locale = JSON.parse(localStorage.getItem(cleReprise(cours)) || 'null'); } catch { /* rien */ }
  try {
    const r = await fetchBrut(`${API}/reprise`, { headers: { 'X-Eleve': e.id } });
    if (r.ok) {
      const d = (await r.json())?.cours?.[cours] as Reprise | undefined;
      if (d?.derniere) return { ...d, vues: [...new Set([...(d.vues || []), ...(locale?.vues || [])])] };
    }
  } catch { /* hors ligne */ }
  return locale?.derniere ? locale : null;
}

/** Envoie un événement de suivi (jamais bloquant : hors ligne, il se perd). */
export function suivre(ev: EvenementSuivi): Promise<void> {
  const e = eleveEnregistre();
  if (!e) return Promise.resolve();
  if (ev.type === 'diapo' && ev.cours && ev.slide_id) noterReprise(ev.cours, ev.slide_id, ev.position, ev.total);
  const corps = { ...ev, enonce: ev.enonce?.slice(0, 500), reponse: ev.reponse?.slice(0, 800), titre: ev.titre?.slice(0, 300),
    pertes: ev.pertes?.slice(0, 12).map(p => p.slice(0, 200)) };
  return fetchBrut(`${API}/suivi`, { method: 'POST', keepalive: true, headers: { 'Content-Type': 'application/json', 'X-Eleve': e.id }, body: JSON.stringify(corps) })
    .then(r => { if (r.status === 401) garderEleve(null); })
    .catch(() => { /* hors ligne */ });
}

let derniereActivite = Date.now();
['pointerdown', 'keydown', 'touchstart', 'wheel'].forEach(t => window.addEventListener(t, () => { derniereActivite = Date.now(); }, { passive: true, capture: true }));

/** Compte le temps passé sur `cours` (ou « examen ») par tranches de 30 s de présence réelle. */
export function useTempsPasse(cours: string, actif = true) {
  useEffect(() => {
    if (!actif) return;
    derniereActivite = Date.now();
    const id = window.setInterval(() => {
      // la voix et l'animation tournent seules : 5 minutes sans geste comptent encore comme présence
      if (document.visibilityState === 'visible' && Date.now() - derniereActivite < 5 * 60_000) suivre({ type: 'temps', cours, secondes: 30 });
    }, 30_000);
    return () => window.clearInterval(id);
  }, [cours, actif]);
}

/** Les questions de l'évaluation déjà rendues par l'élève (une seule réponse compte) : la page les remontre verrouillées. */
export type Progression = Record<string, { vues: number; total: number }>;
export async function monExamen(cours = 'examen'): Promise<{ debut: boolean; fini: boolean; questions: Record<string, Record<string, unknown>>;
  progression?: Progression; ouvert?: boolean; seuil?: number } | null> {
  const e = eleveEnregistre();
  if (!e) return null;
  try {
    const r = await fetchBrut(`${API}/examen${cours === 'examen' ? '' : `?cours=${encodeURIComponent(cours)}`}`, { headers: { 'X-Eleve': e.id } });
    return r.ok ? await r.json() : null;
  } catch { return null; }
}
