/**
 * La mise en page du cahier (24 novembre 2026, demande de l'utilisateur : « le cahier doit être plus organisé : les
 * définitions de côté, pas de texte écrit partout, des tableaux, des graphes, le titre au milieu, le début de paragraphe
 * à gauche… et une charte de couleurs »). Chaque ligne de `cahier` prend sa forme selon son début (skill
 * cahier-de-l-eleve, « Mise en page et charte ») ; la même charte dans tous les cours et toutes les matières :
 *
 *   « I. Titre »            titre de partie : au milieu, jaune craie, souligné
 *   « 1. Sous-titre »       à gauche, cyan, souligné          « a) … » : à gauche, vert clair
 *   « Définition : … »      encadré vert, étiquette « Définition »
 *   « Formule : … »         encadré jaune, la formule au milieu (avec ses unités)
 *   « Méthode : 1) … 2) …»  encadré bleu, une étape par ligne
 *   « Attention : … »       rose ; « Remarque : … » et « Exemple : … » : gris clair, en retrait
 *   « Donc … » / « Conclusion : … » / « Bilan : … »   ⇒ orange, en gras
 *   « | a | b | » (lignes qui se suivent)   un tableau ; la première ligne est l'en-tête ; « |---| » est ignorée
 *   le reste                 un paragraphe, blanc craie, qui commence à gauche
 */
import { Formule } from '../Formule';

export const CHARTE = {
  titre: '#fde68a', sousTitre: '#67e8f9', sousSousTitre: '#86efac', texte: '#f5f1dc',
  definition: '#34d399', formule: '#fbbf24', methode: '#60a5fa', attention: '#fda4af', remarque: '#d4d4d8', conclusion: '#fdba74',
} as const;

type Ligne =
  | { genre: 'titre' | 'sous-titre' | 'sous-sous-titre' | 'texte' | 'attention' | 'remarque' | 'exemple' | 'conclusion'; t: string }
  | { genre: 'definition' | 'formule'; t: string }
  | { genre: 'methode'; etapes: string[]; t: string }
  | { genre: 'tableau'; lignes: string[][] };

const ROMAIN = /^\s*[IVXL]+\s*[.)\-–—]\s+/;
const NUMERO = /^\s*\d+\s*[.]\s+/;
const LETTRE = /^\s*[a-h]\)\s+/;
const PREFIXE = (mot: string) => new RegExp(`^\\s*${mot}\\s*:\\s*`, 'i');

function cellules(l: string) {
  return l.trim().replace(/^\|/, '').replace(/\|$/, '').split('|').map(c => c.trim());
}

/** Les lignes du cahier → leurs formes (les lignes « | … | » qui se suivent forment un seul tableau). */
export function formesCahier(textes: string[]): Ligne[] {
  const out: Ligne[] = [];
  for (const brut of textes) {
    const l = (brut || '').trim();
    if (!l) continue;
    if (l.startsWith('|')) {
      if (/^\|[\s:|-]+\|?$/.test(l)) continue;
      const der = out[out.length - 1];
      if (der && der.genre === 'tableau') der.lignes.push(cellules(l));
      else out.push({ genre: 'tableau', lignes: [cellules(l)] });
      continue;
    }
    if (ROMAIN.test(l)) out.push({ genre: 'titre', t: l });
    else if (NUMERO.test(l) && l.length <= 70 && !/[:;]\s*\S/.test(l.replace(NUMERO, ''))) out.push({ genre: 'sous-titre', t: l });
    else if (LETTRE.test(l) && l.length <= 70 && !/[:;]\s*\S/.test(l.replace(LETTRE, ''))) out.push({ genre: 'sous-sous-titre', t: l });
    else if (PREFIXE('Définition').test(l)) out.push({ genre: 'definition', t: l.replace(PREFIXE('Définition'), '') });
    else if (PREFIXE('Formules?').test(l)) out.push({ genre: 'formule', t: l.replace(PREFIXE('Formules?'), '') });
    else if (PREFIXE('Méthode').test(l)) {
      const reste = l.replace(PREFIXE('Méthode'), '');
      const etapes = reste.split(/\s*(?=\b\d\)\s)/).map(x => x.replace(/^\d\)\s*/, '').replace(/\s*;\s*$/, '').trim()).filter(Boolean);
      out.push({ genre: 'methode', etapes: etapes.length > 1 ? etapes : [reste], t: reste });
    }
    else if (PREFIXE('Attention').test(l)) out.push({ genre: 'attention', t: l.replace(PREFIXE('Attention'), '') });
    else if (PREFIXE('Remarque').test(l)) out.push({ genre: 'remarque', t: l.replace(PREFIXE('Remarque'), '') });
    else if (PREFIXE('Exemples?').test(l)) out.push({ genre: 'exemple', t: l.replace(PREFIXE('Exemples?'), '') });
    else if (/^\s*(Donc|Conclusion\s*:|Bilan\s*:|À retenir\s*:)/i.test(l)) out.push({ genre: 'conclusion', t: l.replace(/^\s*(Conclusion|Bilan|À retenir)\s*:\s*/i, '') });
    else out.push({ genre: 'texte', t: l });
  }
  return out;
}

function Etiquette({ texte, couleur }: { texte: string; couleur: string }) {
  return <span className="mr-2 inline-block rounded px-1.5 align-middle text-[0.62em] font-bold uppercase tracking-wide text-slate-950" style={{ background: couleur, fontFamily: 'system-ui, sans-serif' }}>{texte}</span>;
}

/** Le texte d'une partie du cahier, mis en page (craie sur le tableau vert). */
export default function LignesCahier({ textes, className = '' }: { textes: string[]; className?: string }) {
  const formes = formesCahier(textes);
  return (
    <div className={`space-y-2.5 text-xl leading-snug md:text-2xl ${className}`} style={{ color: CHARTE.texte }}>
      {formes.map((f, k) => {
        switch (f.genre) {
          case 'titre':
            return <p key={k} className="pt-1 text-center text-[1.15em] font-semibold underline decoration-2 underline-offset-8" style={{ color: CHARTE.titre, textDecorationColor: `${CHARTE.titre}88` }}><Formule t={f.t} /></p>;
          case 'sous-titre':
            return <p key={k} className="pt-1 underline underline-offset-4" style={{ color: CHARTE.sousTitre, textDecorationColor: `${CHARTE.sousTitre}66` }}><Formule t={f.t} /></p>;
          case 'sous-sous-titre':
            return <p key={k} className="pl-3" style={{ color: CHARTE.sousSousTitre }}><Formule t={f.t} /></p>;
          case 'definition':
            return <div key={k} className="rounded-lg border-2 px-3 py-1.5" style={{ borderColor: CHARTE.definition, background: '#34d39914' }} dir="auto"><Etiquette texte="Définition" couleur={CHARTE.definition} /><Formule t={f.t} /></div>;
          case 'formule': {
            // la formule seule, en grand ; ce que veut dire chaque lettre (après le premier « ; »), en petit dessous
            const [formule, ...sens] = f.t.split(/\s+;\s+/);
            return (
              <div key={k} className="mx-auto w-fit max-w-full rounded-lg border-2 px-4 py-1.5 text-center" style={{ borderColor: CHARTE.formule, background: '#fbbf2414' }}>
                <div className="text-[1.05em]"><Formule t={formule} /></div>
                {sens.length > 0 && <div className="mt-0.5 text-[0.72em]" style={{ color: CHARTE.remarque }}><Formule t={sens.join(' ; ')} /></div>}
              </div>);
          }
          case 'methode':
            return (
              <div key={k} className="rounded-lg border-2 px-3 py-1.5" style={{ borderColor: CHARTE.methode, background: '#60a5fa14' }}>
                <Etiquette texte="Méthode" couleur={CHARTE.methode} />
                {f.etapes.length > 1
                  ? <ol className="mt-1 list-decimal space-y-0.5 pl-7">{f.etapes.map((e, j) => <li key={j}><Formule t={e} /></li>)}</ol>
                  : <Formule t={f.t} />}
              </div>);
          case 'attention':
            return <p key={k} style={{ color: CHARTE.attention }}><Etiquette texte="Attention" couleur={CHARTE.attention} /><Formule t={f.t} /></p>;
          case 'remarque':
            return <p key={k} className="pl-4 text-[0.92em]" style={{ color: CHARTE.remarque }}><Etiquette texte="Remarque" couleur={CHARTE.remarque} /><Formule t={f.t} /></p>;
          case 'exemple':
            return <p key={k} className="pl-4 text-[0.92em] italic" style={{ color: CHARTE.remarque }}><Etiquette texte="Exemple" couleur={CHARTE.remarque} /><Formule t={f.t} /></p>;
          case 'conclusion':
            return <p key={k} className="font-semibold" style={{ color: CHARTE.conclusion }}>⇒ <Formule t={f.t} /></p>;
          case 'tableau': {
            const [tete, ...corps] = f.lignes;
            return (
              <div key={k} className="overflow-x-auto">
                <table className="mx-auto border-collapse text-[0.85em]">
                  <thead><tr>{tete.map((c, j) => <th key={j} className={`border px-2.5 py-1 font-semibold ${c.length <= 12 ? 'whitespace-nowrap' : ''}`} style={{ borderColor: '#f5f1dc66', color: CHARTE.titre }}><Formule t={c} /></th>)}</tr></thead>
                  <tbody>{corps.map((r, i) => <tr key={i}>{r.map((c, j) => <td key={j} className={`border px-2.5 py-1 text-center ${c.length <= 12 ? 'whitespace-nowrap' : ''}`} style={{ borderColor: '#f5f1dc66' }}><Formule t={c} /></td>)}</tr>)}</tbody>
                </table>
              </div>);
          }
          default:
            return <p key={k} dir="auto"><Formule t={f.t} /></p>;
        }
      })}
    </div>
  );
}
