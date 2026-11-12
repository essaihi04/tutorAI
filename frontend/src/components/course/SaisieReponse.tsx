import { useCallback, useRef, useState } from 'react';
import ClavierScientifique, { BoutonSymboles } from './ClavierScientifique';
import { clavier, useChampClavier, useClavier, type CleSuggestions } from './ClavierFlottant';

/**
 * Une réponse libre se donne écrite, parlée ou photographiée (user rule, 10 novembre 2026).
 *  - 🎙️ parlée : appuyer pour parler, relâcher (MoulSot, `/course-player/transcrire`) ;
 *  - 📷 photographiée : la feuille de l'élève, prise de vue ou fichier, lue par l'OCR (`/course-player/ocr-reponse` :
 *    Mistral OCR puis DeepSeek, avec le contexte de la diapositive pour les symboles, unités et notations) ;
 *  - ⌨ Symboles : le clavier scientifique, qui insère au curseur.
 * Dans tous les cas le texte arrive DANS LE CHAMP et l'élève le corrige à la main avant d'envoyer : rien ne part seul.
 */

/** Ce que l'OCR doit savoir pour bien lire : la diapositive, la question, le cours. */
export type ContexteOcr = { deck_id?: string; title?: string; lead?: string; enonce?: string; matiere?: string; chapitre?: string };

const jeton = () => { try { return localStorage.getItem('token') || ''; } catch { return ''; } };
async function poster<T>(chemin: string, corps: unknown): Promise<T> {
  const r = await fetch(`/api/v1${chemin}`, { method: 'POST', headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${jeton()}` }, body: JSON.stringify(corps) });
  if (!r.ok) {
    const detail = await r.json().then((d: { detail?: unknown }) => (typeof d?.detail === 'string' ? d.detail : '')).catch(() => '');
    throw new Error(detail || `${r.status}`);
  }
  return r.json() as Promise<T>;
}

/** La photo d'un téléphone pèse plusieurs Mo : réduite (2000 px au plus, JPEG) avant l'envoi. */
async function photoEnBase64(f: File): Promise<{ b64: string; mime: string }> {
  const brut = await new Promise<string>((ok, ko) => { const fr = new FileReader(); fr.onload = () => ok(String(fr.result)); fr.onerror = ko; fr.readAsDataURL(f); });
  try {
    const img = await new Promise<HTMLImageElement>((ok, ko) => { const i = new Image(); i.onload = () => ok(i); i.onerror = ko; i.src = brut; });
    const k = Math.min(1, 2000 / Math.max(img.naturalWidth, img.naturalHeight));
    if (k >= 1 && brut.length < 3_000_000) return { b64: brut, mime: f.type || 'image/jpeg' };
    const c = document.createElement('canvas');
    c.width = Math.round(img.naturalWidth * k); c.height = Math.round(img.naturalHeight * k);
    c.getContext('2d')!.drawImage(img, 0, 0, c.width, c.height);
    return { b64: c.toDataURL('image/jpeg', 0.85), mime: 'image/jpeg' };
  } catch { return { b64: brut, mime: f.type || 'image/jpeg' }; }
}

/** La feuille photographiée, lue : le texte revient pour le champ (jamais envoyé tel quel). */
async function lireLaPhoto(f: File, contexte: ContexteOcr): Promise<string> {
  const { b64, mime } = await photoEnBase64(f);
  const { texte } = await poster<{ texte: string }>('/course-player/ocr-reponse', { image_b64: b64, image_mime: mime, ...contexte });
  return (texte || '').trim();
}

/** « 📷 Photo » : prise de vue (téléphone) ou fichier ; le texte lu est ajouté au champ. */
export function BoutonPhoto({ contexte, onTexte, onErreur, disabled, petit = false }: {
  contexte: ContexteOcr; onTexte: (t: string) => void; onErreur?: (m: string | undefined) => void; disabled?: boolean; petit?: boolean;
}) {
  const [lecture, setLecture] = useState(false);
  return (
    <label className={`shrink-0 cursor-pointer rounded-full ${petit ? 'px-3 py-1 text-xs' : 'px-4 py-2 text-sm'} ${lecture ? 'bg-sky-500/40 animate-pulse' : 'bg-white/10 hover:bg-white/20'} ${disabled ? 'pointer-events-none opacity-40' : ''}`}
      style={{ fontFamily: 'system-ui, sans-serif' }} title="Photographie ta feuille : le texte lu s'écrit dans le champ, tu le corriges avant d'envoyer">
      {lecture ? '📷 Lecture…' : '📷 Photo'}
      {/* sans `capture` : le téléphone propose l'appareil photo OU un fichier */}
      <input type="file" accept="image/*" className="hidden" disabled={disabled || lecture}
        onChange={async e => {
          const f = e.target.files?.[0]; e.target.value = '';
          if (!f) return;
          setLecture(true); onErreur?.(undefined);
          try {
            const t = await lireLaPhoto(f, contexte);
            if (t) onTexte(t); else onErreur?.('Rien de lisible sur la photo : reprends-la de plus près, ou écris ta réponse.');
          } catch (err) {
            const m = (err as Error).message;
            onErreur?.(/^\d+$/.test(m) ? 'La photo n’a pas pu être lue : écris ta réponse, ou réessaie.' : m);
          } finally { setLecture(false); }
        }} />
    </label>
  );
}

/** Le micro tenu comme un talkie-walkie : appuyer = il écoute, relâcher = il transcrit dans le champ. */
export function BoutonMicro({ onTexte, onErreur, disabled, petit = false }: {
  onTexte: (t: string) => void; onErreur?: (m: string | undefined) => void; disabled?: boolean; petit?: boolean;
}) {
  const [etat, setEtat] = useState<'repos' | 'ecoute' | 'transcrit'>('repos');
  const rec = useRef<MediaRecorder | null>(null);
  const appui = useRef(false);
  const debut = useRef(0);
  const morceaux = useRef<Blob[]>([]);
  const arreter = useCallback(() => { appui.current = false; if (rec.current?.state === 'recording') rec.current.stop(); }, []);
  const demarrer = useCallback(async () => {
    if (appui.current || rec.current?.state === 'recording') return;
    appui.current = true; onErreur?.(undefined);
    try {
      const flux = await navigator.mediaDevices.getUserMedia({ audio: true });
      if (!appui.current) { flux.getTracks().forEach(t => t.stop()); onErreur?.('Garde le bouton appuyé pendant que tu parles, puis relâche.'); return; }
      const r = new MediaRecorder(flux);
      morceaux.current = [];
      r.ondataavailable = e => { if (e.data.size) morceaux.current.push(e.data); };
      r.onstop = async () => {
        flux.getTracks().forEach(t => t.stop());
        if (performance.now() - debut.current < 500) { setEtat('repos'); onErreur?.('Garde le bouton appuyé pendant que tu parles, puis relâche.'); return; }
        setEtat('transcrit');
        const blob = new Blob(morceaux.current, { type: r.mimeType || 'audio/webm' });
        const b64 = await new Promise<string>(ok => { const fr = new FileReader(); fr.onload = () => ok(String(fr.result)); fr.readAsDataURL(blob); });
        try {
          const { texte } = await poster<{ texte: string }>('/course-player/transcrire', { audio_b64: b64 });
          if (texte?.trim()) onTexte(texte.trim());
        } catch (err) {
          const m = (err as Error).message;
          onErreur?.(/^\d+$/.test(m) ? 'La transcription n’a pas abouti : écris ta réponse.' : m);
        } finally { setEtat('repos'); }
      };
      r.start(); rec.current = r; debut.current = performance.now(); setEtat('ecoute');
      window.setTimeout(arreter, 60_000);
    } catch {
      appui.current = false;
      onErreur?.('Le micro n’est pas disponible : écris ta réponse, ou photographie ta feuille.');
    }
  }, [arreter, onErreur, onTexte]);
  return (
    <button type="button" disabled={disabled || etat === 'transcrit'}
      onPointerDown={e => { e.preventDefault(); e.currentTarget.setPointerCapture?.(e.pointerId); void demarrer(); }}
      onPointerUp={arreter} onPointerCancel={arreter} onLostPointerCapture={arreter}
      onKeyDown={e => { if ((e.key === ' ' || e.key === 'Enter') && !e.repeat) { e.preventDefault(); void demarrer(); } }}
      onKeyUp={e => { if (e.key === ' ' || e.key === 'Enter') { e.preventDefault(); arreter(); } }}
      onContextMenu={e => e.preventDefault()}
      style={{ touchAction: 'none', userSelect: 'none', WebkitUserSelect: 'none', fontFamily: 'system-ui, sans-serif' }}
      className={`shrink-0 rounded-full ${petit ? 'px-3 py-1 text-xs' : 'px-4 py-2 text-sm'} disabled:opacity-40 ${etat === 'ecoute' ? 'bg-rose-500/50 ring-2 ring-rose-300 animate-pulse' : etat === 'transcrit' ? 'bg-sky-500/40 animate-pulse' : 'bg-white/10 hover:bg-white/20'}`}>
      {etat === 'ecoute' ? '● Relâche pour finir' : etat === 'transcrit' ? '✍️ Transcription…' : '🎙️ Maintiens pour parler'}
    </button>
  );
}

/**
 * Le champ d'une réponse libre (question sans options, réponse directe d'une simulation) : écrit, parlé, photographié,
 * avec le clavier scientifique. « Répondre » n'envoie que ce que l'élève a relu.
 */
export default function ChampReponse({ onEnvoyer, disabled, contexte, placeholder = 'Ta réponse…', libelle = 'Répondre', clavierAuto = false, suggestions, actif = true }: {
  onEnvoyer: (texte: string) => void; disabled?: boolean; contexte: ContexteOcr; placeholder?: string; libelle?: string;
  /** le clavier flottant s'ouvre seul quand ce champ apparaît (question à réponse libre, « retrouver ») — 12 novembre 2026 */
  clavierAuto?: boolean;
  /** où chercher les suggestions du clavier pour cette question */
  suggestions?: CleSuggestions;
  /** le champ est celui qu'on voit (carrousel) : lui seul se déclare au clavier flottant */
  actif?: boolean;
}) {
  const [texte, setTexte] = useState('');
  const [clavierDessous, setClavier] = useState(false);
  const flottant = useClavier();
  // Dans le lecteur de cours, le clavier flotte à droite ; ailleurs il reste sous le champ, comme avant.
  const avecFlottant = flottant.hotes > 0;
  const [aVerifier, setAVerifier] = useState(false);
  const [erreur, setErreur] = useState<string | undefined>();
  const champ = useRef<HTMLTextAreaElement>(null);
  const toucher = useChampClavier(champ, texte, setTexte, { auto: clavierAuto && !disabled, actif: avecFlottant && actif && !disabled, suggestions });
  const ajouter = useCallback((t: string) => {
    setTexte(x => [x.trim(), t].filter(Boolean).join(x.trim() ? '\n' : ''));
    setAVerifier(true);
    requestAnimationFrame(() => champ.current?.focus());
  }, []);
  const envoyer = () => { const t = texte.trim(); if (t && !disabled) { setClavier(false); if (avecFlottant) clavier.fermer(); onEnvoyer(t); } };
  return (
    <div className="mt-2" style={{ fontFamily: 'system-ui, sans-serif' }}>
      <div className="flex gap-2">
        <textarea ref={champ} value={texte} onChange={e => setTexte(e.target.value)} onFocus={toucher} disabled={disabled} placeholder={placeholder} rows={2} dir="auto"
          onKeyDown={e => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); envoyer(); } }}
          className="min-w-0 flex-1 resize-none rounded-lg border border-white/20 bg-black/30 px-3 py-2 text-base outline-none focus:border-cyan-300" />
        <button type="button" onClick={envoyer} disabled={disabled || !texte.trim()} className="self-stretch rounded-lg bg-cyan-500/30 px-4 py-2 text-sm disabled:opacity-40">{libelle}</button>
      </div>
      {!disabled && (
        <div className="mt-2 flex flex-wrap items-center gap-2">
          <BoutonMicro petit onTexte={ajouter} onErreur={setErreur} />
          <BoutonPhoto petit contexte={contexte} onTexte={ajouter} onErreur={setErreur} />
          {avecFlottant
            ? <BoutonSymboles petit ouvert={flottant.ouvert} onClick={() => { toucher(); clavier.basculer(); }} />
            : <BoutonSymboles petit ouvert={clavierDessous} onClick={() => setClavier(c => !c)} />}
          {texte.trim() && <button type="button" onClick={() => { setTexte(''); setAVerifier(false); }} className="rounded-full bg-white/10 px-3 py-1 text-xs text-white/70 hover:bg-rose-500/30">✕ Effacer</button>}
        </div>
      )}
      {clavierDessous && !avecFlottant && !disabled && <ClavierScientifique cible={champ} valeur={texte} onChange={setTexte} onFermer={() => setClavier(false)} />}
      {aVerifier && !disabled && <p className="mt-1 text-xs text-sky-200/80">Relis ce qui a été lu ou entendu ; corrige si besoin, puis {libelle}.</p>}
      {erreur && <p className="mt-1 text-xs text-rose-200">{erreur}</p>}
    </div>
  );
}
