/**
 * La fiche d'entrée d'un lien libre (Tronc Commun le 22/11/2026, 2ᵉ Bac PC le 23/11/2026) : remplie une seule fois ;
 * nom et prénom obligatoires, la classe = préfixe + numéro, le père et son téléphone, la case de confirmation.
 */
import { useState } from 'react';
import { inscrire, type Eleve } from './suivi';

/** La fiche d'entrée : remplie une seule fois (le navigateur s'en souvient ; la même fiche redonne le même élève). */
export default function Fiche({ onEntree, entete, prefixe, fond }: {
  onEntree: (e: Eleve) => void;
  /** la ligne du haut (ex. « Moalim · 2ᵉ Bac PC BIOF ») */
  entete: string;
  /** le début du nom de la classe, l'élève ne tape que le numéro (« TCSF », « 2BACPCF ») */
  prefixe: string;
  fond: string;
}) {
  const [f, setF] = useState({ nom: '', prenom: '', classe: '', pere: '', telephone: '' });
  const [certifie, setCertifie] = useState(false);
  const [essaye, setEssaye] = useState(false);
  const [erreur, setErreur] = useState('');
  const [envoi, setEnvoi] = useState(false);
  // tout est obligatoire (23/11/2026) : nom ET prénom séparés, et la case qui confirme la vraie identité
  const manque = {
    nom: f.nom.trim().length < 2, prenom: f.prenom.trim().length < 2, classe: !/^\d{1,3}$/.test(f.classe.trim()),
    pere: f.pere.trim().length < 2, telephone: f.telephone.replace(/\D/g, '').length < 9,
  };
  const pret = !Object.values(manque).some(Boolean) && certifie;
  const champ = (cle: keyof typeof f, libelle: string, aide: string, type = 'text') => (
    <label className="block">
      <span className="text-sm text-white/80">{libelle} <span className="text-rose-300">*</span></span>
      <input type={type} value={f[cle]} placeholder={aide} autoComplete="off" inputMode={type === 'tel' ? 'tel' : undefined}
        onChange={e => { setF(x => ({ ...x, [cle]: e.target.value })); setErreur(''); }}
        className={`mt-0.5 w-full rounded-lg border bg-white/10 px-3 py-2 text-[16px] text-white placeholder:text-white/35 [@media(max-height:520px)]:py-1 ${essaye && manque[cle] ? 'border-rose-400' : 'border-white/20'}`} />
      {essaye && manque[cle] && <span className="text-xs text-rose-300">Obligatoire</span>}
    </label>);
  const entrer = async (ev: React.FormEvent) => {
    ev.preventDefault();
    setEssaye(true);
    if (!pret || envoi) { if (!certifie && !Object.values(manque).some(Boolean)) setErreur('Coche la case pour confirmer ton nom et ton prénom.'); return; }
    setEnvoi(true);
    try { onEntree(await inscrire({ nom: f.nom.trim(), prenom: f.prenom.trim(), classe: f.classe.trim(), pere: f.pere.trim(), telephone: f.telephone.trim() })); }
    catch (e) { setErreur(e instanceof Error ? e.message : 'Inscription impossible, réessaie.'); }
    finally { setEnvoi(false); }
  };
  return (
    <div style={{ background: fond }} className="grid min-h-[100dvh] place-items-center px-4 py-6 text-white [@media(max-height:520px)]:py-2">
      <form onSubmit={e => void entrer(e)} className="w-full max-w-lg rounded-2xl border border-white/15 bg-white/5 p-5 [@media(max-height:520px)]:p-3">
        <p className="text-sm text-emerald-200/80">{entete}</p>
        <h1 className="mt-1 text-xl font-bold [@media(max-height:520px)]:text-lg">Avant d’entrer : ta fiche</h1>
        <p className="mt-1 text-[14px] text-white/70">Une seule fois. Ton professeur suit ainsi ton travail : temps passé, évaluation, ce qu’il faut revoir.</p>
        <div className="mt-3 grid gap-2 sm:grid-cols-2 [@media(max-height:520px)]:grid-cols-2">
          {champ('nom', 'Nom de l’élève', 'ex. El Idrissi')}
          {champ('prenom', 'Prénom de l’élève', 'ex. Salma')}
          <label className="block">
            <span className="text-sm text-white/80">Classe : le numéro seulement <span className="text-rose-300">*</span></span>
            <span className={`mt-0.5 flex items-center overflow-hidden rounded-lg border bg-white/10 ${essaye && manque.classe ? 'border-rose-400' : 'border-white/20'}`}>
              <span className="select-none border-r border-white/20 bg-white/10 px-3 py-2 font-semibold text-emerald-200 [@media(max-height:520px)]:py-1">{prefixe}</span>
              <input value={f.classe} inputMode="numeric" placeholder="ex. 12" autoComplete="off" maxLength={3}
                onChange={e => { setF(x => ({ ...x, classe: e.target.value.replace(/\D/g, '') })); setErreur(''); }}
                className="w-full bg-transparent px-3 py-2 text-[16px] text-white outline-none placeholder:text-white/35 [@media(max-height:520px)]:py-1" />
            </span>
            {essaye && manque.classe && <span className="text-xs text-rose-300">Écris le numéro de ta classe (ex. 12)</span>}
          </label>
          {champ('pere', 'Nom du père', 'ex. Ahmed El Idrissi')}
          {champ('telephone', 'Téléphone du père', 'ex. 06 12 34 56 78', 'tel')}
        </div>
        <label className={`mt-3 flex items-start gap-2 rounded-lg border p-2 text-[14px] ${essaye && !certifie ? 'border-rose-400' : 'border-white/15'}`}>
          <input type="checkbox" checked={certifie} onChange={e => { setCertifie(e.target.checked); setErreur(''); }} className="mt-0.5 h-4 w-4 shrink-0" />
          <span>Je confirme que j’ai écrit <b>mon vrai nom et mon prénom</b>. Une seule fiche par élève : chaque réponse de l’évaluation est enregistrée une seule fois.</span>
        </label>
        {erreur && <p className="mt-2 text-sm text-rose-300">{erreur}</p>}
        <button disabled={envoi} className="mt-3 w-full rounded-xl bg-emerald-500 py-2 font-semibold text-black disabled:opacity-40 [@media(max-height:520px)]:mt-2 [@media(max-height:520px)]:py-1.5">
          {envoi ? 'Enregistrement…' : 'Entrer'}</button>
      </form>
    </div>
  );
}

