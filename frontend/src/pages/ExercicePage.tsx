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
import type { EnonceExercice, Exercice, QuestionExercice } from '../components/exercice/types';
import { jugerValeur } from '../components/exercice/juger';

const CRAIE = "'Patrick Hand', 'Caveat', cursive";
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
async function corrigerParLeTuteur(titre: string, contexte: string, q: QuestionExercice, reponse: string, tentative: number) {
  const r = await fetch('/api/v1/course-player/answer-reaction', {
    method: 'POST', headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${jeton()}` },
    body: JSON.stringify({ diapo: { title: titre, speech: contexte }, question: { type: 'open', enonce: q.texte, attendu: q.reponse.attendu }, reponse, tentative, verdict: null }),
  });
  if (!r.ok) throw new Error(String(r.status));
  return r.json() as Promise<{ correct: boolean | null; parole: string; ecrit: string }>;
}

type Etat = { essais: number; juste: boolean | null; retour?: string; note?: string; correction: boolean; texte?: string; autoEval?: boolean };
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
        retour: v.juste ? 'Juste !' : finie ? `Pas tout à fait : la réponse est ${q.reponse.attendu}.`
          : (v.lu == null ? (v.note || 'Écris la valeur.') : 'Pas encore juste. Relis la question ; tu peux demander l’aide du tuteur.') });
      if (finie) jouer(q.correction.audio);
      return;
    }
    poser(q.id, { essais, texte, retour: 'Le tuteur lit ta réponse…' });
    try {
      const r = await corrigerParLeTuteur(ex.titre, enonce.intro, q, texte, similaire ? 2 : essais);
      const finie = r.correct === true || similaire || essais >= 2;
      poser(q.id, { juste: r.correct === true ? true : finie ? false : null, retour: r.ecrit, correction: finie });
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

  if (erreur) return <Plein><p className="text-white/70">{erreur}</p><button className="mt-4 underline" onClick={() => navigate('/exercices')}>Retour aux exercices</button></Plein>;
  if (!ex || !enonce || !q || !bilan) return <Plein><p className="text-white/60">Chargement de l’exercice…</p></Plein>;
  const nbAides = aides[cle(q.id)] || 0;
  const fini = bilan.finies === bilan.total;
  const conseilSemblable = mode === 'exercice' && fini && (bilan.justes < bilan.total || bilan.aidesTotal >= bilan.total || vues.explications > 0);

  return (
    <div className="flex h-[100dvh] w-screen flex-col bg-[#0a0a18] text-white" style={{ fontFamily: CRAIE }}>
      {/* En-tête */}
      <header className="flex shrink-0 flex-wrap items-center gap-2 border-b border-white/10 px-3 py-2">
        <button onClick={() => { jouer(undefined); navigate('/exercices'); }} className="rounded-full bg-white/10 px-3 py-1 text-sm hover:bg-white/20" style={{ fontFamily: 'system-ui' }}>← Exercices</button>
        <h1 className="min-w-0 flex-1 truncate text-xl text-amber-100">{mode === 'similaire' ? ex.similaire.titre : ex.titre}</h1>
        <span className="rounded-full bg-white/10 px-3 py-0.5 text-sm text-white/70">{NOM_MATIERE[ex.matiere]}{ex.duree_min ? ` · ~${ex.duree_min} min` : ''}</span>
        {mode === 'similaire' && <span className="rounded-full bg-violet-500/30 px-3 py-0.5 text-sm">Exercice semblable : le tuteur corrige seulement</span>}
        <button onClick={() => setOuvert({ genre: 'feuille' })} className="rounded-full bg-amber-200/90 px-3 py-1 text-sm text-slate-900 hover:bg-amber-100" style={{ fontFamily: 'system-ui' }}>📝 Ma feuille</button>
      </header>

      <div className="flex min-h-0 flex-1 flex-col gap-3 overflow-y-auto p-3 transition-[padding] lg:flex-row lg:overflow-hidden"
        style={{ paddingRight: largeurClavier(clavierOuvert) || undefined, paddingBottom: hauteurClavierTelephone(clavierOuvert) || undefined }}>
        {/* L'énoncé */}
        <section className={`rounded-2xl border border-white/10 bg-[#13132a] p-4 lg:w-[46%] lg:overflow-y-auto ${enonceOuvert ? '' : 'lg:w-auto'}`}>
          <div className="mb-2 flex items-center gap-2">
            <h2 className="flex-1 text-lg text-cyan-200">📄 Énoncé</h2>
            {enonce.intro_audio && <button onClick={() => jouer(enonce.intro_audio)} className="rounded-full bg-white/10 px-3 py-0.5 text-sm hover:bg-white/20" style={{ fontFamily: 'system-ui' }}>🔊 Écouter</button>}
            <button onClick={() => setEnonceOuvert(o => !o)} className="rounded-full bg-white/10 px-3 py-0.5 text-sm lg:hidden" style={{ fontFamily: 'system-ui' }}>{enonceOuvert ? 'Replier' : 'Voir l’énoncé'}</button>
          </div>
          {enonceOuvert && (<>
            <p className="text-[17px] leading-relaxed text-white/90"><Formule t={enonce.intro} /></p>
            {!!enonce.figures?.length && <div className="my-3"><FiguresCahier figures={enonce.figures} /></div>}
            {!!enonce.donnees?.length && (
              <div className="mt-2 rounded-xl bg-white/5 p-3 text-[16px]">
                <p className="mb-1 text-amber-200">Données</p>
                <ul className="list-disc pl-5 text-white/85">{enonce.donnees.map((d, i) => <li key={i}><Formule t={d} /></li>)}</ul>
              </div>)}
            <ol className="mt-3 space-y-1 text-[16px]">
              {enonce.questions.map((x, i) => {
                const e = etats[cle(x.id)];
                const marque = e?.juste === true ? '✔' : e?.juste === false ? '✘' : e?.correction ? '•' : '';
                return (
                  <li key={x.id}>
                    <button onClick={() => setQi(i)} className={`w-full rounded-lg px-2 py-1 text-left ${i === qi ? 'bg-amber-200/15 text-amber-100' : 'text-white/80 hover:bg-white/5'}`}>
                      <span className="mr-1 text-cyan-200">{x.id}.</span><Formule t={x.texte} /> <span className="text-emerald-300">{marque}</span>
                    </button>
                  </li>);
              })}
            </ol>
          </>)}
        </section>

        {/* La question en cours */}
        <section className="flex min-h-0 flex-1 flex-col rounded-2xl border border-white/10 bg-[#101a14] p-4 lg:overflow-y-auto">
          <div className="mb-2 flex items-center gap-2 text-sm text-white/50" style={{ fontFamily: 'system-ui' }}>
            {enonce.questions.map((x, i) => <button key={x.id} onClick={() => setQi(i)} className={`h-2.5 w-2.5 rounded-full ${i === qi ? 'bg-amber-200' : etats[cle(x.id)]?.juste ? 'bg-emerald-400' : 'bg-white/25'}`} aria-label={`Question ${x.id}`} />)}
            <span className="ml-1">Question {qi + 1} / {enonce.questions.length}</span>
          </div>
          <p className="text-xl text-amber-100"><span className="text-cyan-200">{q.id}.</span> <Formule t={q.texte} /></p>
          {q.texte_audio && <button onClick={() => jouer(q.texte_audio)} className="mt-1 self-start rounded-full bg-white/10 px-3 py-0.5 text-sm hover:bg-white/20" style={{ fontFamily: 'system-ui' }}>🔊 La question</button>}

          {/* Les aides du tuteur, une à une */}
          {mode === 'exercice' && nbAides > 0 && (
            <div className="mt-3 space-y-2">
              {q.aides!.slice(0, nbAides).map((a, i) => (
                <div key={i} className="rounded-xl border border-cyan-300/30 bg-cyan-400/10 p-3 text-[17px]">
                  <span className="mr-1">🙋</span>Aide {i + 1} : <Formule t={a.texte} />
                  {a.audio && <button onClick={() => jouer(a.audio)} className="ml-2 text-sm text-cyan-200 underline" style={{ fontFamily: 'system-ui' }}>réécouter</button>}
                </div>))}
            </div>)}

          {/* La réponse */}
          {!etat.correction && etat.juste !== true && (
            <div className="mt-3">
              <ChampReponse key={cle(q.id)} onEnvoyer={t => void repondre(t)} libelle="Vérifier" lignes={q.reponse.type === 'valeur' ? 3 : 6}
                placeholder={q.reponse.type === 'valeur' ? `${q.reponse.grandeur || 'résultat'} = … ${q.reponse.unite || ''}` : 'Ta réponse, rédigée et justifiée…'}
                contexte={{ deck_id: ex.id, title: ex.titre, enonce: q.texte, matiere: ex.matiere, chapitre: ex.chapitre }}
                suggestions={{ deck_id: ex.id, slide_id: `${mode}_${q.id}`, enonce: q.texte, clavier: q.clavier }} />
            </div>)}
          {etat.retour && <p className={`mt-3 rounded-xl p-3 text-[17px] ${etat.juste === true ? 'bg-emerald-500/15 text-emerald-100' : etat.juste === false ? 'bg-rose-500/15 text-rose-100' : 'bg-white/5 text-white/85'}`}><Formule t={etat.retour} /></p>}
          {etat.note && <p className="mt-2 text-[16px] text-amber-200">{etat.note}</p>}

          {/* La correction : la rédaction attendue, ligne par ligne, avec sa voix */}
          {etat.correction && (
            <div className="mt-3 rounded-xl border border-amber-200/30 bg-amber-200/5 p-3">
              <div className="mb-1 flex items-center gap-2"><p className="flex-1 text-amber-200">✍️ Correction</p>
                {q.correction.audio && <button onClick={() => jouer(q.correction.audio)} className="rounded-full bg-white/10 px-3 py-0.5 text-sm" style={{ fontFamily: 'system-ui' }}>🔊 Écouter</button>}</div>
              {q.correction.lignes.map((l, i) => <p key={i} className="text-[18px] text-white/90"><Formule t={l.texte} /></p>)}
              {etat.autoEval && etat.juste === null && (
                <div className="mt-3 flex flex-wrap items-center gap-2 text-[15px]" style={{ fontFamily: 'system-ui' }}>
                  <span className="text-white/70">Le tuteur n'est pas joignable : compare toi-même.</span>
                  <button onClick={() => poser(q.id, { juste: true })} className="rounded-full bg-emerald-500/30 px-3 py-1">J'avais juste</button>
                  <button onClick={() => poser(q.id, { juste: false })} className="rounded-full bg-rose-500/30 px-3 py-1">Je m'étais trompé</button>
                </div>)}
            </div>)}

          {/* Les boutons d'aide : pas dans l'exercice semblable */}
          <div className="mt-4 flex flex-wrap gap-2" style={{ fontFamily: 'system-ui' }}>
            {mode === 'exercice' && !!q.aides?.length && !etat.correction && (
              <button onClick={aide} disabled={nbAides >= q.aides.length && false} className="rounded-full bg-cyan-500/25 px-4 py-2 text-sm hover:bg-cyan-500/40">
                🙋 {nbAides === 0 ? 'Aide du tuteur' : nbAides < q.aides.length ? 'Une autre aide' : 'Réécouter l’aide'}</button>)}
            {mode === 'exercice' && q.explication && diapo('explication', q.explication) && (
              <button onClick={() => { jouer(undefined); setVues(v => ({ ...v, explications: v.explications + 1 })); setOuvert({ genre: 'explication', slide: diapo('explication', q.explication)! }); }}
                className="rounded-full bg-violet-500/25 px-4 py-2 text-sm hover:bg-violet-500/40">🎬 Explication animée</button>)}
            {mode === 'exercice' && q.facile && diapo('facile', q.facile) && !etat.correction && (
              <button onClick={() => { jouer(undefined); setVues(v => ({ ...v, faciles: v.faciles + 1 })); setOuvert({ genre: 'facile', slide: diapo('facile', q.facile)! }); }}
                className="rounded-full bg-emerald-500/20 px-4 py-2 text-sm hover:bg-emerald-500/35">🎯 Plus facile, pour s’entraîner</button>)}
            {!etat.correction && etat.essais > 0 && (
              <button onClick={() => { poser(q.id, { correction: true, juste: etat.juste ?? false }); jouer(q.correction.audio); }} className="rounded-full bg-white/10 px-4 py-2 text-sm hover:bg-white/20">Voir la correction</button>)}
            {qi < enonce.questions.length - 1 && (etat.correction || etat.juste === true) && (
              <button onClick={() => { jouer(undefined); setQi(qi + 1); }} className="ml-auto rounded-full bg-amber-200 px-4 py-2 text-sm text-slate-900">Question suivante →</button>)}
          </div>

          {/* Le bilan, et l'exercice semblable */}
          {fini && (
            <div className="mt-5 rounded-2xl border border-white/15 bg-white/5 p-4">
              <p className="text-xl text-amber-100">Bilan : {bilan.justes} / {bilan.total} juste{bilan.justes > 1 ? 's' : ''}{mode === 'exercice' ? ` · ${bilan.aidesTotal} aide${bilan.aidesTotal > 1 ? 's' : ''} demandée${bilan.aidesTotal > 1 ? 's' : ''}` : ''}</p>
              {mode === 'exercice' ? (
                <p className="mt-1 text-[17px] text-white/80">{conseilSemblable
                  ? 'Pour être sûr d’avoir compris, refais le même exercice avec d’autres données, seul cette fois : le tuteur corrigera seulement.'
                  : 'Bravo ! Tu peux t’entraîner encore avec le même exercice et d’autres données.'}</p>
              ) : <p className="mt-1 text-[17px] text-white/80">{bilan.justes === bilan.total ? 'Tout juste, seul : la méthode est acquise.' : 'Relis les corrections, puis refais les questions manquées.'}</p>}
              <div className="mt-3 flex flex-wrap gap-2" style={{ fontFamily: 'system-ui' }}>
                {mode === 'exercice' && <button onClick={() => { jouer(undefined); setMode('similaire'); setQi(0); }} className={`rounded-full px-4 py-2 text-sm ${conseilSemblable ? 'bg-amber-200 text-slate-900' : 'bg-white/10'}`}>🔁 Exercice semblable</button>}
                {mode === 'similaire' && <button onClick={() => { setMode('exercice'); setQi(0); }} className="rounded-full bg-white/10 px-4 py-2 text-sm">Revenir au premier exercice</button>}
                <button onClick={() => navigate('/exercices')} className="rounded-full bg-white/10 px-4 py-2 text-sm">Autres exercices</button>
              </div>
            </div>)}
        </section>
      </div>

      {/* L'explication animée ou la version facile : le lecteur des cours, sur une seule diapositive */}
      {ouvert && ouvert.genre !== 'feuille' && (
        <div className="fixed inset-0 z-40 flex flex-col bg-[#0a0a18]/95 p-1 sm:p-2">
          <div className="flex shrink-0 items-center gap-2 px-2 py-1" style={{ fontFamily: 'system-ui' }}>
            <p className="flex-1 truncate text-sm text-white/70">{ouvert.genre === 'explication' ? '🎬 Explication animée' : '🎯 Plus facile'} — question {q.id}</p>
            <button onClick={() => { taireTout(); setOuvert(null); }} className="rounded-full bg-white/15 px-4 py-1 text-sm hover:bg-white/25">× Revenir à l’exercice</button>
          </div>
          <div className="min-h-0 flex-1 overflow-hidden rounded-2xl border border-white/10">
            <CoursePlayer key={ouvert.slide.id} deck={deckDe(ex, ouvert.genre, ouvert.slide)} language="mixed" mode="concentration" tuteur3D demarrerSeul />
          </div>
        </div>)}

      {ouvert?.genre === 'feuille' && <Feuille ex={ex} enonce={enonce} mode={mode} onFermer={() => setOuvert(null)} />}
      {!ouvert && <ClavierFlottant droite={0} bas={16} />}
    </div>
  );
}

function Plein({ children }: { children: React.ReactNode }) {
  return <div className="grid h-[100dvh] place-items-center bg-[#0a0a18] text-center text-white" style={{ fontFamily: CRAIE }}><div>{children}</div></div>;
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
