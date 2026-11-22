/**
 * Un exercice (partie « Exercices », 22 novembre 2026 — skill `exercices`). Ce que l'élève a sous la main :
 *  - l'énoncé, comme une feuille (texte, données, figures dessinées en code), qu'il peut écouter ;
 *  - une question à la fois : il répond avec le clavier adapté (symboles et pièges de CETTE réponse) ;
 *  - « Aide du tuteur » : des indices préparés, avec leur voix, de la piste à la méthode, jamais la réponse ;
 *  - « Explication animée » : la diapositive du cours qui explique cette question, jouée par le même lecteur ;
 *  - « Plus facile » : la même notion en QCM, vrai/faux ou association, avec une réaction préparée par réponse ;
 *  - « Ma feuille » : la copie, où il rédige toute sa réponse (clavier, photo), gardée dans le navigateur ;
 *  - à la fin, un exercice SEMBLABLE (autres données) : sans aide ni version facile, le tuteur corrige seulement.
 */
import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import CoursePlayer from '../components/course/CoursePlayer';
import type { CourseDeck, CourseSlide } from '../components/course/types';
import FiguresCahier from '../components/course/FigureCahier';
import { Formule } from '../components/course/Formule';
import ChampReponse, { BoutonPhoto } from '../components/course/SaisieReponse';
import ClavierFlottant, { clavier, hauteurClavierTelephone, largeurClavier, useClavier } from '../components/course/ClavierFlottant';
import { Touches, type MatiereClavier } from '../components/course/ClavierScientifique';
import { inscrireVoix, taireTout } from '../components/course/voixUnique';
import { pointsDe, pts, type EnonceExercice, type Exercice, type QuestionExercice } from '../components/exercice/types';
import { jugerValeur } from '../components/exercice/juger';

const CRAIE = "'Patrick Hand', 'Caveat', cursive";
/** le sujet imprimé de l'examen (22 novembre 2026 : feuille blanche, écriture noire) */
const SUJET = "'Times New Roman', Georgia, serif";
const NIVEAU: Record<string, string> = { facile: 'Facile', moyen: 'Moyen', difficile: 'Supérieur' };
const MATIERE_CLAVIER: Record<Exercice['matiere'], MatiereClavier> = { physique: 'physique-chimie', mathematiques: 'maths', svt: 'svt' };
const NOM_MATIERE: Record<Exercice['matiere'], string> = { physique: 'Physique-chimie', mathematiques: 'Mathématiques', svt: 'SVT' };

let voixCourante: HTMLAudioElement | null = null;
function jouer(url?: string) {
  voixCourante?.pause();
  voixCourante = null;
  if (!url) return;
  taireTout();
  const a = new Audio(url);
  inscrireVoix(a);
  voixCourante = a;
  void a.play().catch(() => { /* lecture refusée avant un geste : l'élève relance */ });
}

const jeton = () => { try { return localStorage.getItem('token') || ''; } catch { return ''; } };
async function corrigerParLeTuteur(titre: string, contexte: string, q: QuestionExercice, reponse: string, tentative: number, matiere: string) {
  const r = await fetch('/api/v1/course-player/answer-reaction', {
    method: 'POST', headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${jeton()}` },
    body: JSON.stringify({ diapo: { title: titre, speech: contexte }, question: { type: 'open', enonce: q.texte, attendu: q.reponse.attendu, matiere }, reponse, tentative, verdict: null }),
  });
  if (!r.ok) throw new Error(String(r.status));
  return r.json() as Promise<{ correct: boolean | null; partiel?: boolean; parole: string; ecrit: string }>;
}

type Etat = { essais: number; juste: boolean | null; retour?: string; note?: string; correction: boolean; texte?: string; autoEval?: boolean;
  /** le verdict du dernier essai, toujours affiché (22/11/2026) : juste, en partie, faux, ou non jugé */
  verdict?: 'juste' | 'partiel' | 'faux' | 'nonjuge' | 'lecture'; partiel?: boolean };
type Ouvert = null | { genre: 'explication' | 'facile'; slide: CourseSlide } | { genre: 'feuille' };

function deckDe(ex: Exercice, genre: 'explication' | 'facile', slide: CourseSlide): CourseDeck {
  return { id: `${ex.id}__${genre}__${slide.id}`, lesson_id: ex.id, title: ex.titre, mode: 'concentration', language: 'mixed',
    activities: [{ id: genre, title: genre === 'explication' ? 'Explication animée' : 'Plus facile', phase: 'apply', slides: [slide] } as unknown as CourseDeck['activities'][number]] };
}

export default function ExercicePage() {
  const { exerciceId = '' } = useParams();
  const navigate = useNavigate();
  const [ex, setEx] = useState<Exercice | null>(null);
  const [erreur, setErreur] = useState('');
  const [mode, setMode] = useState<'exercice' | 'similaire'>('exercice');
  const [qi, setQi] = useState(0);
  const [etats, setEtats] = useState<Record<string, Etat>>({});
  const [aides, setAides] = useState<Record<string, number>>({});
  const [vues, setVues] = useState({ explications: 0, faciles: 0 });
  const [ouvert, setOuvert] = useState<Ouvert>(null);
  const [enonceOuvert, setEnonceOuvert] = useState(true);
  // mode sombre : choisi en haut de la page, gardé dans ce navigateur
  const [sombre, setSombre] = useState(() => { try { return localStorage.getItem('moalim:exercices:sombre') === '1'; } catch { return false; } });
  useEffect(() => { try { localStorage.setItem('moalim:exercices:sombre', sombre ? '1' : '0'); } catch { /* stockage refusé */ } }, [sombre]);
  const NUIT: React.CSSProperties | undefined = sombre ? { filter: 'invert(0.9) hue-rotate(180deg)' } : undefined;
  // le clavier ouvert prend sa place à droite (en bas sur téléphone) : il ne cache jamais le champ à remplir
  const clavierOuvert = useClavier().ouvert && !ouvert;

  useEffect(() => {
    setEx(null); setErreur('');
    fetch(`/media/exercices/${encodeURIComponent(exerciceId)}.json`)
      .then(r => { if (!r.ok) throw new Error(String(r.status)); return r.json(); })
      .then((d: Exercice) => setEx(d))
      .catch(() => setErreur("Cet exercice n'existe pas (ou pas encore)."));
  }, [exerciceId]);
  useEffect(() => { if (ex) clavier.matiere(MATIERE_CLAVIER[ex.matiere]); }, [ex]);
  useEffect(() => () => jouer(undefined), []);

  const enonce: EnonceExercice | null = ex ? (mode === 'exercice' ? ex.enonce : ex.similaire.enonce) : null;
  const q = enonce?.questions[qi];
  const cle = (id: string) => `${mode}:${id}`;
  const etat: Etat = (q && etats[cle(q.id)]) || { essais: 0, juste: null, correction: false };
  const poser = (id: string, e: Partial<Etat>) => setEtats(s => ({ ...s, [cle(id)]: { ...((s[cle(id)]) || { essais: 0, juste: null, correction: false }), ...e } }));
  const diapo = useCallback((deck: 'explication' | 'facile', id?: string) =>
    ex?.[deck].activities.flatMap(a => a.slides).find(s => s.id === id), [ex]);

  const repondre = async (texte: string) => {
    if (!ex || !enonce || !q) return;
    const essais = etat.essais + 1;
    const similaire = mode === 'similaire';
    if (q.reponse.type === 'valeur') {
      const v = jugerValeur(q.reponse, texte);
      const finie = v.juste || similaire || essais >= 2;
      poser(q.id, { essais, juste: v.juste ? true : finie ? false : null, texte, note: v.note, correction: finie,
        verdict: v.juste ? 'juste' : v.lu == null && !finie ? undefined : 'faux',
        retour: v.juste ? 'Le résultat est bon.' : finie ? `Pas tout à fait : la réponse est ${q.reponse.attendu}.`
          : (v.lu == null ? (v.note || 'Écris la valeur.') : 'Pas encore juste. Relis la question ; tu peux demander l’aide du tuteur.') });
      if (finie) jouer(q.correction.audio);
      return;
    }
    poser(q.id, { essais, texte, retour: 'Le tuteur lit ta réponse…', verdict: 'lecture' });
    try {
      const r = await corrigerParLeTuteur(ex.titre, enonce.intro, q, texte, similaire ? 2 : essais, ex.matiere);
      const finie = r.correct === true || similaire || essais >= 2;
      const verdict = r.correct === true ? 'juste' : r.partiel ? 'partiel' : r.correct === false ? 'faux' : 'nonjuge';
      poser(q.id, { juste: r.correct === true ? true : finie ? false : null, retour: r.ecrit || r.parole, correction: finie,
        verdict, partiel: !!r.partiel });
    } catch {
      // sans le tuteur en ligne : l'élève compare lui-même avec la réponse attendue
      poser(q.id, { retour: '', autoEval: true, correction: true });
      jouer(q.correction.audio);
    }
  };

  const aide = () => {
    if (!q?.aides?.length) return;
    const n = aides[cle(q.id)] || 0;
    const k = Math.min(n, q.aides.length - 1);
    jouer(q.aides[k].audio);
    setAides(s => ({ ...s, [cle(q.id)]: Math.min(n + 1, q.aides!.length) }));
  };

  const bilan = useMemo(() => {
    if (!enonce) return null;
    const es = enonce.questions.map(x => etats[cle(x.id)]);
    const finies = es.filter(e => e && (e.juste !== null || e.correction)).length;
    const justes = es.filter(e => e?.juste === true).length;
    const aidesTotal = enonce.questions.reduce((n, x) => n + (aides[cle(x.id)] || 0), 0);
    return { finies, justes, total: enonce.questions.length, aidesTotal };
  }, [enonce, etats, aides, mode]); // eslint-disable-line react-hooks/exhaustive-deps

  if (erreur) return <Plein><p className="text-slate-700">{erreur}</p><button className="mt-4 underline" onClick={() => navigate('/exercices')}>Retour aux exercices</button></Plein>;
  if (!ex || !enonce || !q || !bilan) return <Plein><p className="text-slate-600">Chargement de l’exercice…</p></Plein>;
  const nbAides = aides[cle(q.id)] || 0;
  const fini = bilan.finies === bilan.total;
  const conseilSemblable = mode === 'exercice' && fini && (bilan.justes < bilan.total || bilan.aidesTotal >= bilan.total || vues.explications > 0);

  const total = enonce.questions.reduce((n, x) => n + pointsDe(x), 0);
  const gagne = (x: QuestionExercice, e?: Etat) => e?.juste === true ? pointsDe(x) : e?.juste === false && e.partiel ? pointsDe(x) / 2 : 0;
  const note = enonce.questions.reduce((n, x) => n + gagne(x, etats[cle(x.id)]), 0);
  const ptsQ = pointsDe(q);
  const noteQ = etat.juste === null ? null : gagne(q, etat);
  const BTN = 'rounded-md border border-slate-400 bg-white px-3 py-1.5 text-sm text-slate-900 hover:bg-slate-100';
  const LIGNES = { lineHeight: '36px', backgroundImage: 'repeating-linear-gradient(transparent 0 35px, #9bb3d6 35px 36px)' };

  return (
    <div className={`flex h-[100dvh] w-screen flex-col text-black ${sombre ? 'bg-[#1c1c22]' : 'bg-[#d6d6d0]'}`} style={{ fontFamily: 'system-ui, sans-serif' }}>
      {/* En-tête */}
      <header className="flex shrink-0 flex-wrap items-center gap-2 border-b border-slate-400 bg-white px-3 py-2" style={NUIT}>
        <button onClick={() => { jouer(undefined); navigate('/exercices'); }} className={BTN}>← Exercices</button>
        <h1 className="min-w-0 flex-1 truncate text-lg font-semibold">{mode === 'similaire' ? ex.similaire.titre : ex.titre}</h1>
        {mode === 'similaire' && <span className="rounded border border-violet-700 px-2 py-0.5 text-sm text-violet-800">Exercice semblable : le tuteur corrige seulement</span>}
        <span className="rounded border border-black px-2 py-0.5 text-sm font-semibold">Note : {pts(note)} / {pts(total)}</span>
        <button onClick={() => setOuvert({ genre: 'feuille' })} className={BTN}>📝 Ma copie</button>
        <button onClick={() => setSombre(x => !x)} className={BTN} aria-pressed={sombre} title={sombre ? 'Passer en mode clair' : 'Passer en mode sombre'}>
          <span style={sombre ? { filter: 'invert(1) hue-rotate(180deg)' } : undefined}>{sombre ? '☀️' : '🌙'}</span> {sombre ? 'Clair' : 'Sombre'}</button>
      </header>

      <div className="flex min-h-0 flex-1 flex-col gap-3 overflow-y-auto p-3 transition-[padding] lg:flex-row lg:overflow-hidden"
        style={{ paddingRight: largeurClavier(clavierOuvert) || undefined, paddingBottom: hauteurClavierTelephone(clavierOuvert) || undefined, ...NUIT }}>
        {/* Le sujet : feuille blanche, écriture noire, comme à l'examen */}
        <section className="shrink-0 bg-white p-4 text-black shadow-md ring-1 ring-black/10 sm:p-6 lg:w-[48%] lg:overflow-y-auto" style={{ fontFamily: SUJET }}>
          <table className="mb-3 w-full border-collapse text-[15px]" style={{ fontFamily: 'system-ui, sans-serif' }}>
            <tbody><tr>
              <td className="border border-black px-2 py-1 font-semibold">{NOM_MATIERE[ex.matiere]}</td>
              <td className="border border-black px-2 py-1 text-center">Exercice — {NIVEAU[ex.niveau || ''] || ''}{ex.duree_min ? ` · ~${ex.duree_min} min` : ''}</td>
              <td className="border border-black px-2 py-1 text-center font-semibold">{pts(total)} points</td>
            </tr></tbody>
          </table>
          <div className="mb-2 flex items-center gap-2" style={{ fontFamily: 'system-ui, sans-serif' }}>
            <h2 className="flex-1 text-lg font-bold underline underline-offset-4">Énoncé</h2>
            {enonce.intro_audio && <button onClick={() => jouer(enonce.intro_audio)} className={BTN}>🔊 Écouter</button>}
            <button onClick={() => setEnonceOuvert(o => !o)} className={`${BTN} lg:hidden`}>{enonceOuvert ? 'Replier' : 'Voir l’énoncé'}</button>
          </div>
          {enonceOuvert && (<>
            <p className="text-[17px] leading-relaxed"><Formule t={enonce.intro} /></p>
            {/* les dessins sont à la craie claire : inversés, ils deviennent noirs sur la feuille, couleurs gardées */}
            {!!enonce.figures?.length && <div className="my-3" style={{ filter: 'invert(1) hue-rotate(180deg)' }}><FiguresCahier figures={enonce.figures} /></div>}
            {!!enonce.donnees?.length && (
              <div className="mt-2 border border-black p-3 text-[16px]">
                <p className="mb-1 font-bold">Données :</p>
                <ul className="list-disc pl-5">{enonce.donnees.map((d, i) => <li key={i}><Formule t={d} /></li>)}</ul>
              </div>)}
            <table className="mt-3 w-full border-collapse text-[16px]">
              <tbody>
                {enonce.questions.map((x, i) => {
                  const e = etats[cle(x.id)];
                  const marque = e?.juste === true ? '✔' : e?.juste === false ? '✘' : '';
                  return (
                    <tr key={x.id} onClick={() => setQi(i)} className={`cursor-pointer align-top ${i === qi ? 'bg-amber-100' : 'hover:bg-slate-50'}`}>
                      <td className="w-16 border-r border-slate-400 py-1 pr-2 text-right text-[14px] font-semibold" style={{ fontFamily: 'system-ui, sans-serif' }}>{pts(pointsDe(x))} pt</td>
                      <td className="py-1 pl-2"><span className="font-bold">{x.id}.</span> <Formule t={x.texte} /> <span className={e?.juste ? 'text-emerald-700' : 'text-rose-700'}>{marque}</span></td>
                    </tr>);
                })}
              </tbody>
            </table>
          </>)}
        </section>

        {/* La feuille de réponses : cadre, marge du barème, lignes */}
        <section className="flex min-h-0 flex-1 flex-col bg-white text-black shadow-md ring-1 ring-black/10 lg:overflow-y-auto">
          <table className="w-full shrink-0 border-collapse text-[15px]">
            <tbody><tr>
              <td className="border-2 border-black px-3 py-2 font-bold">Question {q.id}</td>
              <td className="w-32 border-2 border-black px-2 py-2 text-center">Barème : <b>{pts(ptsQ)}</b></td>
              <td className="w-32 border-2 border-black px-2 py-2 text-center">Note : <b className={noteQ === null ? '' : noteQ > 0 ? 'text-emerald-700' : 'text-rose-700'}>{noteQ === null ? '……' : pts(noteQ)}</b></td>
            </tr></tbody>
          </table>
          <div className="flex flex-wrap items-center gap-1.5 border-b border-slate-300 px-3 py-1.5 text-sm text-slate-600">
            {enonce.questions.map((x, i) => <button key={x.id} onClick={() => setQi(i)} className={`h-6 min-w-6 rounded border px-1 text-xs ${i === qi ? 'border-black bg-black text-white' : etats[cle(x.id)]?.juste ? 'border-emerald-700 text-emerald-700' : etats[cle(x.id)]?.juste === false ? 'border-rose-700 text-rose-700' : 'border-slate-400'}`} aria-label={`Question ${x.id}`}>{x.id}</button>)}
            <span className="ml-1">Question {qi + 1} / {enonce.questions.length}</span>
          </div>

          <div className="flex min-h-0 flex-1">
            {/* la marge, comme sur la copie d'examen : le barème de la question, puis la note */}
            <div className="w-14 shrink-0 border-r-2 border-rose-400 pt-3 text-center sm:w-16">
              <span className="inline-block rounded border border-black px-1 text-[13px] font-semibold">{pts(ptsQ)}</span>
              {noteQ !== null && <p className={`mt-2 text-lg font-bold ${noteQ > 0 ? 'text-emerald-700' : 'text-rose-700'}`} style={{ fontFamily: CRAIE }}>{pts(noteQ)}</p>}
            </div>

            <div className="min-w-0 flex-1 p-3 sm:p-4">
              <p className="text-[18px] font-semibold" style={{ fontFamily: SUJET }}><span>{q.id}.</span> <Formule t={q.texte} /></p>
              {q.texte_audio && <button onClick={() => jouer(q.texte_audio)} className={`mt-1 ${BTN}`}>🔊 La question</button>}

              {/* Les aides du tuteur, une à une */}
              {mode === 'exercice' && nbAides > 0 && (
                <div className="mt-3 space-y-2">
                  {q.aides!.slice(0, nbAides).map((a, i) => (
                    <div key={i} className="border-l-4 border-sky-700 bg-sky-50 p-2 text-[16px] text-slate-900">
                      <b>🙋 Aide {i + 1} :</b> <Formule t={a.texte} />
                      {a.audio && <button onClick={() => jouer(a.audio)} className="ml-2 text-sm text-sky-800 underline">réécouter</button>}
                    </div>))}
                </div>)}

              {/* La réponse, sur les lignes de la copie */}
              {!etat.correction && etat.juste !== true && (
                <div className="mt-3">
                  <ChampReponse key={cle(q.id)} papier onEnvoyer={t => void repondre(t)} libelle="Vérifier" lignes={q.reponse.type === 'valeur' ? 4 : 7}
                    placeholder={q.reponse.type === 'valeur' ? `${q.reponse.grandeur || 'résultat'} = … ${q.reponse.unite || ''}` : 'Ta réponse, rédigée et justifiée…'}
                    contexte={{ deck_id: ex.id, title: ex.titre, enonce: q.texte, matiere: ex.matiere, chapitre: ex.chapitre }}
                    suggestions={{ deck_id: ex.id, slide_id: `${mode}_${q.id}`, enonce: q.texte, clavier: q.clavier }} />
                </div>)}
              {etat.texte && (etat.correction || etat.juste === true) && (
                <p className="mt-3 whitespace-pre-wrap text-[21px] text-black" style={{ fontFamily: CRAIE, ...LIGNES }}>{etat.texte}</p>)}
              {etat.retour && (() => {
                const V = { juste: ['✔ Juste', 'border-emerald-700 text-emerald-800'], partiel: ['◐ Juste en partie : complète ta réponse', 'border-amber-600 text-amber-800'],
                  faux: [etat.correction ? '✘ Faux' : '✘ Pas encore juste', 'border-rose-700 text-rose-800'], nonjuge: ['? Le tuteur n’a pas pu juger : précise ta réponse', 'border-slate-500 text-slate-800'],
                  lecture: ['…', 'border-slate-400 text-slate-600'] } as const;
                const [titre, couleur] = V[etat.verdict || (etat.juste === true ? 'juste' : etat.juste === false ? 'faux' : 'lecture')];
                return (
                  <div className={`mt-3 border-2 p-2 ${couleur}`}>
                    {etat.verdict !== 'lecture' && <p className="text-[15px] font-bold" style={{ fontFamily: 'system-ui, sans-serif' }}>{titre}</p>}
                    <p className="text-[18px]" style={{ fontFamily: CRAIE }}><Formule t={etat.retour} /></p>
                  </div>);
              })()}
              {etat.note && <p className="mt-2 text-[16px] text-amber-800">{etat.note}</p>}

              {/* La correction : la rédaction attendue, à l'encre rouge du correcteur */}
              {etat.correction && (
                <div className="mt-3 border-2 border-rose-700 p-3">
                  <div className="mb-1 flex items-center gap-2"><p className="flex-1 font-bold text-rose-800">✍️ Correction</p>
                    {q.correction.audio && <button onClick={() => jouer(q.correction.audio)} className={BTN}>🔊 Écouter</button>}</div>
                  {q.correction.lignes.map((l, i) => <p key={i} className="text-[19px] text-rose-900" style={{ fontFamily: CRAIE }}><Formule t={l.texte} /></p>)}
                  {etat.autoEval && etat.juste === null && (
                    <div className="mt-3 flex flex-wrap items-center gap-2 text-[15px]">
                      <span className="text-slate-700">Le tuteur n'est pas joignable : compare toi-même.</span>
                      <button onClick={() => poser(q.id, { juste: true })} className="rounded-md border border-emerald-700 px-3 py-1 text-emerald-800">J'avais juste</button>
                      <button onClick={() => poser(q.id, { juste: false })} className="rounded-md border border-rose-700 px-3 py-1 text-rose-800">Je m'étais trompé</button>
                    </div>)}
                </div>)}

              {/* Les boutons d'aide : pas dans l'exercice semblable */}
              <div className="mt-4 flex flex-wrap gap-2">
                {mode === 'exercice' && !!q.aides?.length && !etat.correction && (
                  <button onClick={aide} className="rounded-md border border-sky-800 bg-sky-50 px-3 py-1.5 text-sm text-sky-900 hover:bg-sky-100">
                    🙋 {nbAides === 0 ? 'Aide du tuteur' : nbAides < q.aides.length ? 'Une autre aide' : 'Réécouter l’aide'}</button>)}
                {mode === 'exercice' && q.explication && diapo('explication', q.explication) && (
                  <button onClick={() => { jouer(undefined); setVues(v => ({ ...v, explications: v.explications + 1 })); setOuvert({ genre: 'explication', slide: diapo('explication', q.explication)! }); }}
                    className="rounded-md border border-violet-800 bg-violet-50 px-3 py-1.5 text-sm text-violet-900 hover:bg-violet-100">🎬 Explication animée</button>)}
                {mode === 'exercice' && q.facile && diapo('facile', q.facile) && !etat.correction && (
                  <button onClick={() => { jouer(undefined); setVues(v => ({ ...v, faciles: v.faciles + 1 })); setOuvert({ genre: 'facile', slide: diapo('facile', q.facile)! }); }}
                    className="rounded-md border border-emerald-800 bg-emerald-50 px-3 py-1.5 text-sm text-emerald-900 hover:bg-emerald-100">🎯 Plus facile, pour s’entraîner</button>)}
                {!etat.correction && etat.essais > 0 && (
                  <button onClick={() => { poser(q.id, { correction: true, juste: etat.juste ?? false }); jouer(q.correction.audio); }} className={BTN}>Voir la correction</button>)}
                {qi < enonce.questions.length - 1 && (etat.correction || etat.juste === true) && (
                  <button onClick={() => { jouer(undefined); setQi(qi + 1); }} className="ml-auto rounded-md bg-black px-4 py-1.5 text-sm font-semibold text-white">Question suivante →</button>)}
              </div>

              {/* Le bilan, et l'exercice semblable */}
              {fini && (
                <div className="mt-5 border-2 border-black p-4">
                  <p className="text-xl font-bold">Note : {pts(note)} / {pts(total)} · {bilan.justes} / {bilan.total} juste{bilan.justes > 1 ? 's' : ''}{mode === 'exercice' ? ` · ${bilan.aidesTotal} aide${bilan.aidesTotal > 1 ? 's' : ''} demandée${bilan.aidesTotal > 1 ? 's' : ''}` : ''}</p>
                  {mode === 'exercice' ? (
                    <p className="mt-1 text-[16px] text-slate-800">{conseilSemblable
                      ? 'Pour être sûr d’avoir compris, refais le même exercice avec d’autres données, seul cette fois : le tuteur corrigera seulement.'
                      : 'Bravo ! Tu peux t’entraîner encore avec le même exercice et d’autres données.'}</p>
                  ) : <p className="mt-1 text-[16px] text-slate-800">{bilan.justes === bilan.total ? 'Tout juste, seul : la méthode est acquise.' : 'Relis les corrections, puis refais les questions manquées.'}</p>}
                  <div className="mt-3 flex flex-wrap gap-2">
                    {mode === 'exercice' && <button onClick={() => { jouer(undefined); setMode('similaire'); setQi(0); }} className={conseilSemblable ? 'rounded-md bg-black px-4 py-1.5 text-sm font-semibold text-white' : BTN}>🔁 Exercice semblable</button>}
                    {mode === 'similaire' && <button onClick={() => { setMode('exercice'); setQi(0); }} className={BTN}>Revenir au premier exercice</button>}
                    <button onClick={() => navigate('/exercices')} className={BTN}>Autres exercices</button>
                  </div>
                </div>)}
            </div>
          </div>
        </section>
      </div>

      {/* L'explication animée ou la version facile : le lecteur des cours, sur une seule diapositive */}
      {ouvert && ouvert.genre !== 'feuille' && (
        <div className="fixed inset-0 z-40 flex flex-col bg-[#0a0a18]/95 p-1 text-white sm:p-2">
          <div className="flex shrink-0 items-center gap-2 px-2 py-1">
            <p className="flex-1 truncate text-sm text-white/70">{ouvert.genre === 'explication' ? '🎬 Explication animée' : '🎯 Plus facile'} — question {q.id}</p>
            <button onClick={() => { taireTout(); setOuvert(null); }} className="rounded-full bg-white/15 px-4 py-1 text-sm hover:bg-white/25">× Revenir à l’exercice</button>
          </div>
          <div className="min-h-0 flex-1 overflow-hidden rounded-2xl border border-white/10">
            <CoursePlayer key={ouvert.slide.id} deck={deckDe(ex, ouvert.genre, ouvert.slide)} language="mixed" mode="concentration" tuteur3D demarrerSeul />
          </div>
        </div>)}

      {ouvert?.genre === 'feuille' && <div className="fixed inset-0 z-50" style={NUIT}><Feuille ex={ex} enonce={enonce} mode={mode} onFermer={() => setOuvert(null)} /></div>}
      {!ouvert && <ClavierFlottant droite={0} bas={16} />}
    </div>
  );
}

function Plein({ children }: { children: React.ReactNode }) {
  return <div className="grid h-[100dvh] place-items-center bg-[#d6d6d0] text-center text-black"><div>{children}</div></div>;
}

/** La copie de l'élève : une feuille lignée où il rédige chaque question ; gardée dans ce navigateur. */
function Feuille({ ex, enonce, mode, onFermer }: { ex: Exercice; enonce: EnonceExercice; mode: string; onFermer: () => void }) {
  const cleStock = `moalim:feuille:${ex.id}:${mode}`;
  const [txt, setTxt] = useState<Record<string, string>>(() => { try { return JSON.parse(localStorage.getItem(cleStock) || '{}'); } catch { return {}; } });
  const [actif, setActif] = useState(enonce.questions[0]?.id || '');
  const [clavierVu, setClavierVu] = useState(false);
  const zones = useRef<Record<string, HTMLTextAreaElement | null>>({});
  useEffect(() => { try { localStorage.setItem(cleStock, JSON.stringify(txt)); } catch { /* stockage refusé : la feuille reste en mémoire */ } }, [txt, cleStock]);
  const inserer = (s: string) => {
    const z = zones.current[actif];
    const v = txt[actif] || '';
    const a = z?.selectionStart ?? v.length, b = z?.selectionEnd ?? v.length;
    setTxt(t => ({ ...t, [actif]: v.slice(0, a) + s + v.slice(b) }));
    requestAnimationFrame(() => { if (z) { z.focus(); z.selectionStart = z.selectionEnd = a + s.length; } });
  };
  const qa = enonce.questions.find(x => x.id === actif);
  return (
    <div className="fixed inset-0 z-50 flex flex-col bg-black/70 p-2 sm:p-4" style={{ fontFamily: 'system-ui' }}>
      <div className="mx-auto flex h-full w-full max-w-4xl flex-col overflow-hidden rounded-2xl bg-[#fdfcf6] text-slate-900 shadow-2xl">
        <div className="flex items-center gap-2 border-b border-slate-200 px-4 py-2">
          <p className="flex-1 font-semibold">📝 Ma feuille — {ex.titre}</p>
          <BoutonPhoto petit contexte={{ deck_id: ex.id, title: ex.titre, enonce: qa?.texte, matiere: ex.matiere }} onTexte={t => inserer(t)} />
          <button onClick={onFermer} className="rounded-full bg-slate-200 px-3 py-1 text-sm hover:bg-slate-300">Fermer</button>
        </div>
        <div className="min-h-0 flex-1 overflow-y-auto px-4 py-3" style={{ backgroundImage: 'repeating-linear-gradient(#fdfcf6 0 31px, #c7d7ee 31px 32px)', fontFamily: CRAIE }}>
          {enonce.questions.map(x => (
            <div key={x.id} className="mb-4">
              <p className="text-lg text-rose-700">{x.id}. <Formule t={x.texte} /></p>
              <textarea ref={el => { zones.current[x.id] = el; }} value={txt[x.id] || ''} onFocus={() => setActif(x.id)}
                onChange={e => setTxt(t => ({ ...t, [x.id]: e.target.value }))} rows={4} dir="auto"
                placeholder={x.reponse.type === 'valeur' ? "Rédige ici : la relation, l'application numérique, le résultat avec son unité." : 'Rédige ici : décris (avec les valeurs), explique, puis conclus en une phrase.'}
                className="w-full resize-y bg-transparent text-[20px] leading-8 text-slate-800 outline-none placeholder:text-slate-400" />
            </div>))}
        </div>
        <div className="border-t border-slate-200 bg-slate-900 p-2 text-white">
          <div className="mb-1 flex items-center gap-2"><p className="flex-1 text-xs text-white/60">Symboles utiles (question {actif}) :</p>
            <button onClick={() => setClavierVu(v => !v)} className="rounded bg-white/15 px-2 py-0.5 text-xs hover:bg-white/25">{clavierVu ? 'Ranger le clavier' : '⌨ Tout le clavier'}</button></div>
          <div className="mb-1 flex flex-wrap gap-1">{[...(qa?.clavier?.aides || [])].map(s => (
            <button key={s} onClick={() => inserer(s)} className="rounded bg-white/15 px-2 py-0.5 text-sm hover:bg-white/25">{s}</button>))}</div>
          {clavierVu && <div className="max-h-[38vh] overflow-y-auto"><Touches matiere={MATIERE_CLAVIER[ex.matiere]} onTaper={inserer} /></div>}
        </div>
      </div>
    </div>
  );
}
