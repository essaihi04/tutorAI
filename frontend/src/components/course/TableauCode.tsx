// Extrait du tableau du code génétique (20/11/2026, demande de l'utilisateur) : une question qui demande de traduire un
// codon en acide aminé montre, à côté d'elle, les codons utiles et leur acide aminé, comme le « petit tableau » donné
// dans le sujet du national. La question porte `tableau_code: ["GGC", "AGC", …]` (codons de l'ARNm, dans l'ordre voulu).

export const CODE_GENETIQUE: Record<string, string> = (() => {
  const bases = 'UCAG';
  // les 64 codons dans l'ordre UUU, UUC, UUA, UUG, UCU… ; une lettre par codon (code standard, * = stop)
  const aa = 'FFLLSSSSYY**CC*WLLLLPPPPHHQQRRRRIIIMTTTTNNKKSSRRVVVVAAAADDEEGGGG';
  const out: Record<string, string> = {};
  let i = 0;
  for (const a of bases) for (const b of bases) for (const c of bases) out[a + b + c] = aa[i++];
  return out;
})();

export const NOMS_ACIDES: Record<string, [string, string]> = {
  F: ['Phe', 'phénylalanine'], L: ['Leu', 'leucine'], S: ['Ser', 'sérine'], Y: ['Tyr', 'tyrosine'], C: ['Cys', 'cystéine'],
  W: ['Trp', 'tryptophane'], P: ['Pro', 'proline'], H: ['His', 'histidine'], Q: ['Gln', 'glutamine'], R: ['Arg', 'arginine'],
  I: ['Ile', 'isoleucine'], M: ['Met', 'méthionine'], T: ['Thr', 'thréonine'], N: ['Asn', 'asparagine'], K: ['Lys', 'lysine'],
  V: ['Val', 'valine'], A: ['Ala', 'alanine'], D: ['Asp', 'acide aspartique'], E: ['Glu', 'acide glutamique'], G: ['Gly', 'glycine'],
  '*': ['Stop', 'codon stop'],
};

const CRAIE = "'Patrick Hand', 'Caveat', cursive";

export default function TableauCode({ codons, className = '' }: { codons: string[]; className?: string }) {
  const lignes = [...new Set(codons.map(c => c.trim().toUpperCase().replace(/T/g, 'U')))].filter(c => CODE_GENETIQUE[c]);
  if (!lignes.length) return null;
  return (
    <aside data-tableau-code className={`shrink-0 self-start rounded-xl border border-amber-200/35 bg-black/20 px-3 py-2 ${className}`} style={{ fontFamily: CRAIE }}>
      <p className="mb-1.5 text-[13px] font-semibold text-amber-200">Extrait du tableau du code génétique</p>
      <table className="w-full border-collapse text-[15px]">
        <thead>
          <tr className="text-cyan-200">
            <th className="border border-white/20 px-2 py-1 text-left font-semibold">Codon (ARNm)</th>
            <th className="border border-white/20 px-2 py-1 text-left font-semibold">Acide aminé</th>
          </tr>
        </thead>
        <tbody>
          {lignes.map(c => {
            const [abr, nom] = NOMS_ACIDES[CODE_GENETIQUE[c]];
            return (
              <tr key={c}>
                <td className="border border-white/20 px-2 py-1 tracking-wider text-white">{c}</td>
                <td className="border border-white/20 px-2 py-1 text-white/90">{abr} <span className="text-[12px] text-white/50">({nom})</span></td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </aside>
  );
}
