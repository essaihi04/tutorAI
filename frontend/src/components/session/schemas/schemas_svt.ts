import type { ScientificSchema } from './types';

// ═══════════════════════════════════════════════════════════════
// SVT — Ch1: Consommation matière organique & flux d'énergie
// ═══════════════════════════════════════════════════════════════

export const svt_glycolyse: ScientificSchema = {
  id: 'svt_glycolyse',
  title: 'La Glycolyse — Dégradation du glucose',
  subject: 'svt',
  keywords: ['glycolyse', 'glucose', 'pyruvate', 'atp', 'cytoplasme', 'تحلل سكري', 'التحلل السكري', 'dégradation'],
  category: 'process',
  viewBox: '0 0 800 600',
  backgroundColor: '#f0f9ff',
  layers: [
    { id: 'bg', label: 'Fond', delay: 0, svgContent: `
      <rect x="40" y="40" width="720" height="520" rx="24" fill="#e0f2fe" stroke="#0284c7" stroke-width="2.5" opacity="0.35"/>
      <text x="400" y="78" text-anchor="middle" font-size="26" font-weight="bold" fill="#0c4a6e" font-family="system-ui">LA GLYCOLYSE</text>
      <text x="400" y="102" text-anchor="middle" font-size="14" fill="#64748b" font-family="system-ui">Dégradation du glucose dans le cytoplasme — التحلل السكري</text>
    `},
    { id: 'glucose', label: 'Glucose', delay: 300, svgContent: `
      <rect x="290" y="125" width="220" height="50" rx="14" fill="url(#grad_blue)" stroke="#2563eb" stroke-width="2"/>
      <text x="400" y="156" text-anchor="middle" font-size="18" font-weight="bold" fill="white" font-family="system-ui">Glucose C₆H₁₂O₆</text>
      <circle cx="255" cy="150" r="20" fill="#fbbf24" stroke="#d97706" stroke-width="2"/>
      <text x="255" y="156" text-anchor="middle" font-size="13" font-weight="bold" fill="#92400e" font-family="system-ui">C6</text>
    `},
    { id: 'phase1', label: 'Phase activation', delay: 600, svgContent: `
      <line x1="400" y1="175" x2="400" y2="215" stroke="#ef4444" stroke-width="2.5" marker-end="url(#arrowRed)"/>
      <rect x="300" y="220" width="200" height="42" rx="10" fill="#fef2f2" stroke="#ef4444" stroke-width="2"/>
      <text x="400" y="246" text-anchor="middle" font-size="14" font-weight="600" fill="#dc2626" font-family="system-ui">Phase d'activation</text>
      <text x="540" y="240" font-size="14" font-weight="bold" fill="#ef4444" font-family="system-ui">−2 ATP</text>
    `},
    { id: 'clivage', label: 'Clivage', delay: 900, svgContent: `
      <line x1="400" y1="262" x2="400" y2="300" stroke="#8b5cf6" stroke-width="2.5" marker-end="url(#arrowPurple)"/>
      <rect x="275" y="305" width="110" height="38" rx="8" fill="#f5f3ff" stroke="#8b5cf6" stroke-width="2"/>
      <text x="330" y="329" text-anchor="middle" font-size="13" font-weight="600" fill="#7c3aed" font-family="system-ui">G3P (C₃)</text>
      <rect x="415" y="305" width="110" height="38" rx="8" fill="#f5f3ff" stroke="#8b5cf6" stroke-width="2"/>
      <text x="470" y="329" text-anchor="middle" font-size="13" font-weight="600" fill="#7c3aed" font-family="system-ui">G3P (C₃)</text>
      <text x="400" y="298" text-anchor="middle" font-size="11" fill="#8b5cf6" font-family="system-ui">Clivage → 2 trioses</text>
    `},
    { id: 'phase2', label: 'Phase rendement', delay: 1200, svgContent: `
      <line x1="330" y1="343" x2="330" y2="385" stroke="#16a34a" stroke-width="2" marker-end="url(#arrowGreen)"/>
      <line x1="470" y1="343" x2="470" y2="385" stroke="#16a34a" stroke-width="2" marker-end="url(#arrowGreen)"/>
      <rect x="275" y="390" width="250" height="42" rx="10" fill="#f0fdf4" stroke="#16a34a" stroke-width="2"/>
      <text x="400" y="416" text-anchor="middle" font-size="14" font-weight="600" fill="#15803d" font-family="system-ui">Phase de rendement</text>
      <text x="560" y="405" font-size="14" font-weight="bold" fill="#16a34a" font-family="system-ui">+4 ATP</text>
      <text x="560" y="425" font-size="12" fill="#0891b2" font-family="system-ui">+2 NADH,H⁺</text>
    `},
    { id: 'pyruvate', label: 'Pyruvate', delay: 1500, svgContent: `
      <line x1="400" y1="432" x2="400" y2="465" stroke="#ea580c" stroke-width="2.5" marker-end="url(#arrowOrange)"/>
      <rect x="280" y="470" width="240" height="50" rx="14" fill="url(#grad_orange)" stroke="#ea580c" stroke-width="2"/>
      <text x="400" y="501" text-anchor="middle" font-size="18" font-weight="bold" fill="white" font-family="system-ui">2 Pyruvate C₃H₄O₃</text>
    `},
    { id: 'bilan', label: 'Bilan', delay: 1800, svgContent: `
      <rect x="60" y="430" width="175" height="110" rx="12" fill="#fefce8" stroke="#ca8a04" stroke-width="2"/>
      <text x="148" y="458" text-anchor="middle" font-size="15" font-weight="bold" fill="#854d0e" font-family="system-ui">BILAN NET</text>
      <text x="148" y="485" text-anchor="middle" font-size="22" font-weight="bold" fill="#16a34a" font-family="system-ui">+2 ATP</text>
      <text x="148" y="510" text-anchor="middle" font-size="13" fill="#0891b2" font-family="system-ui">+2 NADH,H⁺</text>
      <text x="148" y="530" text-anchor="middle" font-size="12" fill="#64748b" font-family="system-ui">+2 Pyruvate</text>
    `},
  ],
  annotations: [
    { id: 'a1', x: 290, y: 125, width: 220, height: 50, label: 'Glucose', description: 'Molécule à 6 carbones (hexose) — substrat initial de la glycolyse', color: '#2563eb' },
    { id: 'a2', x: 300, y: 220, width: 200, height: 42, label: 'Phase activation', description: '2 ATP investis pour phosphoryler le glucose et le préparer au clivage', color: '#ef4444' },
    { id: 'a3', x: 275, y: 305, width: 250, height: 38, label: 'Clivage', description: 'Le fructose-1,6-bisphosphate est coupé en 2 trioses-phosphate (G3P)', color: '#8b5cf6' },
    { id: 'a4', x: 275, y: 390, width: 250, height: 42, label: 'Phase rendement', description: 'Oxydation de 2 G3P produit 4 ATP et 2 NADH,H⁺', color: '#16a34a' },
    { id: 'a5', x: 280, y: 470, width: 240, height: 50, label: 'Pyruvate', description: '2 pyruvates (C₃) — iront vers le cycle de Krebs (aérobie) ou la fermentation (anaérobie)', color: '#ea580c' },
  ],
  highlights: [
    { id: 'h1', cx: 400, cy: 150, radius: 120, label: 'Glucose' },
    { id: 'h2', cx: 400, cy: 495, radius: 130, label: 'Pyruvate' },
  ],
};

export const svt_respiration_cellulaire: ScientificSchema = {
  id: 'svt_respiration_cellulaire',
  title: 'Respiration cellulaire — Vue d\'ensemble',
  subject: 'svt',
  keywords: ['respiration', 'cellulaire', 'aérobie', 'mitochondrie', 'krebs', 'chaîne respiratoire', 'atp', 'oxygène', 'تنفس خلوي', 'السلسلة التنفسية'],
  category: 'process',
  viewBox: '0 0 900 620',
  backgroundColor: '#f8fafc',
  layers: [
    { id: 'bg', label: 'Fond', delay: 0, svgContent: `
      <text x="450" y="42" text-anchor="middle" font-size="24" font-weight="bold" fill="#0f172a" font-family="system-ui">RESPIRATION CELLULAIRE AÉROBIE</text>
      <text x="450" y="65" text-anchor="middle" font-size="13" fill="#64748b" font-family="system-ui">C₆H₁₂O₆ + 6O₂ → 6CO₂ + 6H₂O + 36-38 ATP</text>
      <rect x="20" y="82" width="340" height="490" rx="18" fill="#eff6ff" stroke="#3b82f6" stroke-width="2" stroke-dasharray="8,4"/>
      <text x="190" y="108" text-anchor="middle" font-size="14" font-weight="600" fill="#1d4ed8" font-family="system-ui">CYTOPLASME</text>
      <ellipse cx="635" cy="360" rx="225" ry="210" fill="#fef3c7" stroke="#d97706" stroke-width="2.5"/>
      <text x="635" y="170" text-anchor="middle" font-size="14" font-weight="600" fill="#92400e" font-family="system-ui">MITOCHONDRIE</text>
    `},
    { id: 'glyc', label: 'Glycolyse', delay: 400, svgContent: `
      <rect x="95" y="130" width="190" height="45" rx="12" fill="url(#grad_blue)" stroke="#2563eb" stroke-width="2"/>
      <text x="190" y="158" text-anchor="middle" font-size="16" font-weight="bold" fill="white" font-family="system-ui">Glucose (C₆)</text>
      <line x1="190" y1="175" x2="190" y2="215" stroke="#2563eb" stroke-width="2.5" marker-end="url(#arrowBlue)"/>
      <rect x="80" y="222" width="220" height="50" rx="10" fill="#dbeafe" stroke="#2563eb" stroke-width="2"/>
      <text x="190" y="244" text-anchor="middle" font-size="15" font-weight="bold" fill="#1e40af" font-family="system-ui">GLYCOLYSE</text>
      <text x="190" y="263" text-anchor="middle" font-size="11" fill="#3b82f6" font-family="system-ui">التحلل السكري</text>
      <text x="320" y="245" font-size="12" font-weight="600" fill="#16a34a" font-family="system-ui">+2 ATP</text>
      <text x="320" y="262" font-size="11" fill="#0891b2" font-family="system-ui">+2 NADH</text>
    `},
    { id: 'pyr', label: 'Pyruvate', delay: 700, svgContent: `
      <line x1="190" y1="272" x2="190" y2="310" stroke="#ea580c" stroke-width="2.5" marker-end="url(#arrowOrange)"/>
      <rect x="100" y="315" width="180" height="42" rx="10" fill="url(#grad_orange)" stroke="#ea580c" stroke-width="2"/>
      <text x="190" y="341" text-anchor="middle" font-size="15" font-weight="bold" fill="white" font-family="system-ui">2 Pyruvate (C₃)</text>
      <path d="M 280 336 C 330 336, 370 310, 430 300" stroke="#ea580c" stroke-width="2" fill="none" stroke-dasharray="5,3" marker-end="url(#arrowOrange)"/>
      <text x="355" y="310" font-size="10" fill="#ea580c" font-family="system-ui">→ Acétyl-CoA</text>
    `},
    { id: 'krebs', label: 'Cycle de Krebs', delay: 1100, svgContent: `
      <circle cx="555" cy="320" r="70" fill="#bbf7d0" stroke="#16a34a" stroke-width="2.5"/>
      <text x="555" y="312" text-anchor="middle" font-size="14" font-weight="bold" fill="#14532d" font-family="system-ui">Cycle de</text>
      <text x="555" y="332" text-anchor="middle" font-size="14" font-weight="bold" fill="#14532d" font-family="system-ui">Krebs</text>
      <text x="555" y="350" text-anchor="middle" font-size="10" fill="#16a34a" font-family="system-ui">حلقة كريبس</text>
      <path d="M 515 260 A 65 65 0 0 1 595 260" fill="none" stroke="#16a34a" stroke-width="2" marker-end="url(#arrowGreen)"/>
      <path d="M 618 295 A 65 65 0 0 1 618 345" fill="none" stroke="#16a34a" stroke-width="2" marker-end="url(#arrowGreen)"/>
      <path d="M 595 380 A 65 65 0 0 1 515 380" fill="none" stroke="#16a34a" stroke-width="2" marker-end="url(#arrowGreen)"/>
      <path d="M 492 345 A 65 65 0 0 1 492 295" fill="none" stroke="#16a34a" stroke-width="2" marker-end="url(#arrowGreen)"/>
      <text x="660" y="295" font-size="11" fill="#dc2626" font-family="system-ui">2 CO₂</text>
      <text x="660" y="312" font-size="11" fill="#16a34a" font-family="system-ui">+2 ATP</text>
      <text x="660" y="329" font-size="11" fill="#0891b2" font-family="system-ui">+6 NADH</text>
      <text x="660" y="346" font-size="11" fill="#7c3aed" font-family="system-ui">+2 FADH₂</text>
    `},
    { id: 'chain', label: 'Chaîne respiratoire', delay: 1500, svgContent: `
      <line x1="555" y1="390" x2="585" y2="420" stroke="#dc2626" stroke-width="2" marker-end="url(#arrowRed)"/>
      <rect x="510" y="425" width="250" height="85" rx="14" fill="url(#grad_red)" stroke="#dc2626" stroke-width="2"/>
      <text x="635" y="452" text-anchor="middle" font-size="14" font-weight="bold" fill="white" font-family="system-ui">Chaîne respiratoire</text>
      <text x="635" y="472" text-anchor="middle" font-size="11" fill="#fecaca" font-family="system-ui">NADH + FADH₂ → e⁻ → H₂O</text>
      <text x="635" y="500" text-anchor="middle" font-size="11" fill="#fecaca" font-family="system-ui">Gradient H⁺ → ATP synthase</text>
      <text x="790" y="455" font-size="14" font-weight="bold" fill="#16a34a" font-family="system-ui">+32-34</text>
      <text x="790" y="473" font-size="14" font-weight="bold" fill="#16a34a" font-family="system-ui">ATP</text>
    `},
    { id: 'bilan', label: 'Bilan', delay: 1900, svgContent: `
      <rect x="50" y="475" width="300" height="85" rx="14" fill="#ecfdf5" stroke="#059669" stroke-width="2.5"/>
      <text x="200" y="502" text-anchor="middle" font-size="16" font-weight="bold" fill="#065f46" font-family="system-ui">BILAN TOTAL</text>
      <text x="200" y="528" text-anchor="middle" font-size="22" font-weight="bold" fill="#16a34a" font-family="system-ui">36 à 38 ATP</text>
      <text x="200" y="550" text-anchor="middle" font-size="12" fill="#64748b" font-family="system-ui">Glycolyse: 2 | Krebs: 2 | Chaîne: 32-34</text>
    `},
  ],
  annotations: [
    { id: 'a1', x: 80, y: 222, width: 220, height: 50, label: 'Glycolyse', description: 'Dégradation du glucose (C₆) en 2 pyruvate (C₃) dans le cytoplasme. Bilan: 2 ATP + 2 NADH', color: '#2563eb' },
    { id: 'a2', x: 485, y: 250, width: 140, height: 140, label: 'Cycle de Krebs', description: 'Oxydation de l\'acétyl-CoA dans la matrice mitochondriale. 2 tours: 2 ATP + 6 NADH + 2 FADH₂', color: '#16a34a' },
    { id: 'a3', x: 510, y: 425, width: 250, height: 85, label: 'Chaîne respiratoire', description: 'Transfert d\'électrons → gradient H⁺ → ATP synthase. Produit 32-34 ATP. L\'O₂ est l\'accepteur final', color: '#dc2626' },
  ],
  highlights: [
    { id: 'h1', cx: 190, cy: 245, radius: 120, label: 'Glycolyse' },
    { id: 'h2', cx: 555, cy: 320, radius: 85, label: 'Krebs' },
    { id: 'h3', cx: 635, cy: 465, radius: 135, label: 'Chaîne respiratoire' },
  ],
};

export const svt_fermentation: ScientificSchema = {
  id: 'svt_fermentation',
  title: 'Fermentation — Voies anaérobies',
  subject: 'svt',
  keywords: ['fermentation', 'anaérobie', 'lactique', 'alcoolique', 'éthanol', 'sans oxygène', 'تخمر', 'comparaison'],
  category: 'comparison',
  viewBox: '0 0 850 520',
  backgroundColor: '#fefce8',
  layers: [
    { id: 'bg', label: 'Titre', delay: 0, svgContent: `
      <text x="425" y="38" text-anchor="middle" font-size="24" font-weight="bold" fill="#0f172a" font-family="system-ui">FERMENTATION — Voies anaérobies</text>
      <text x="425" y="60" text-anchor="middle" font-size="13" fill="#64748b" font-family="system-ui">En absence d'O₂ — Cytoplasme uniquement — Bilan: 2 ATP seulement</text>
      <line x1="425" y1="75" x2="425" y2="490" stroke="#d1d5db" stroke-width="1" stroke-dasharray="5,4"/>
      <text x="212" y="90" text-anchor="middle" font-size="15" font-weight="600" fill="#b91c1c" font-family="system-ui">🫙 Fermentation LACTIQUE</text>
      <text x="637" y="90" text-anchor="middle" font-size="15" font-weight="600" fill="#7c3aed" font-family="system-ui">🍺 Fermentation ALCOOLIQUE</text>
    `},
    { id: 'common', label: 'Étape commune', delay: 300, svgContent: `
      <rect x="310" y="105" width="230" height="45" rx="12" fill="url(#grad_blue)" stroke="#2563eb" stroke-width="2"/>
      <text x="425" y="133" text-anchor="middle" font-size="16" font-weight="bold" fill="white" font-family="system-ui">Glucose C₆H₁₂O₆</text>
      <line x1="425" y1="150" x2="425" y2="180" stroke="#2563eb" stroke-width="2.5" marker-end="url(#arrowBlue)"/>
      <rect x="335" y="185" width="180" height="38" rx="8" fill="#dbeafe" stroke="#2563eb" stroke-width="2"/>
      <text x="425" y="209" text-anchor="middle" font-size="14" font-weight="bold" fill="#1e40af" font-family="system-ui">GLYCOLYSE → +2 ATP</text>
      <line x1="425" y1="223" x2="425" y2="252" stroke="#ea580c" stroke-width="2" marker-end="url(#arrowOrange)"/>
      <rect x="340" y="257" width="170" height="38" rx="8" fill="url(#grad_orange)" stroke="#ea580c" stroke-width="2"/>
      <text x="425" y="281" text-anchor="middle" font-size="14" font-weight="bold" fill="white" font-family="system-ui">2 Pyruvate (C₃)</text>
    `},
    { id: 'lactique', label: 'Voie lactique', delay: 700, svgContent: `
      <line x1="340" y1="276" x2="212" y2="330" stroke="#b91c1c" stroke-width="2.5" marker-end="url(#arrowRed)"/>
      <text x="260" y="310" font-size="10" fill="#b91c1c" font-family="system-ui" transform="rotate(-22,260,310)">NADH→NAD⁺</text>
      <rect x="95" y="340" width="235" height="52" rx="12" fill="#fef2f2" stroke="#dc2626" stroke-width="2.5"/>
      <text x="212" y="365" text-anchor="middle" font-size="16" font-weight="bold" fill="#dc2626" font-family="system-ui">2 Acide lactique</text>
      <text x="212" y="385" text-anchor="middle" font-size="12" fill="#b91c1c" font-family="system-ui">(C₃H₆O₃)</text>
      <rect x="95" y="410" width="235" height="75" rx="8" fill="white" stroke="#e5e7eb" stroke-width="1.5"/>
      <text x="212" y="432" text-anchor="middle" font-size="12" font-weight="600" fill="#1f2937" font-family="system-ui">Exemples:</text>
      <text x="212" y="452" text-anchor="middle" font-size="11" fill="#64748b" font-family="system-ui">• Muscle strié (effort intense → crampes)</text>
      <text x="212" y="470" text-anchor="middle" font-size="11" fill="#64748b" font-family="system-ui">• Bactéries lactiques (yaourt, fromage)</text>
    `},
    { id: 'alcoolique', label: 'Voie alcoolique', delay: 700, svgContent: `
      <line x1="510" y1="276" x2="637" y2="330" stroke="#7c3aed" stroke-width="2.5" marker-end="url(#arrowPurple)"/>
      <text x="580" y="310" font-size="10" fill="#7c3aed" font-family="system-ui" transform="rotate(22,580,310)">NADH→NAD⁺</text>
      <rect x="520" y="340" width="235" height="52" rx="12" fill="#f5f3ff" stroke="#7c3aed" stroke-width="2.5"/>
      <text x="637" y="365" text-anchor="middle" font-size="16" font-weight="bold" fill="#7c3aed" font-family="system-ui">2 Éthanol + 2 CO₂</text>
      <text x="637" y="385" text-anchor="middle" font-size="12" fill="#6d28d9" font-family="system-ui">(C₂H₅OH)</text>
      <rect x="520" y="410" width="235" height="75" rx="8" fill="white" stroke="#e5e7eb" stroke-width="1.5"/>
      <text x="637" y="432" text-anchor="middle" font-size="12" font-weight="600" fill="#1f2937" font-family="system-ui">Exemples:</text>
      <text x="637" y="452" text-anchor="middle" font-size="11" fill="#64748b" font-family="system-ui">• Levures (bière, vin, pain)</text>
      <text x="637" y="470" text-anchor="middle" font-size="11" fill="#64748b" font-family="system-ui">• Certaines bactéries anaérobies</text>
    `},
  ],
  annotations: [
    { id: 'a1', x: 95, y: 340, width: 235, height: 52, label: 'Ferm. lactique', description: 'Pyruvate réduit en acide lactique par NADH. Muscles lors effort intense (crampes). Réversible.', color: '#dc2626' },
    { id: 'a2', x: 520, y: 340, width: 235, height: 52, label: 'Ferm. alcoolique', description: 'Pyruvate décarboxylé puis réduit en éthanol. Libère CO₂. Irréversible. Levures.', color: '#7c3aed' },
  ],
  highlights: [
    { id: 'h1', cx: 212, cy: 366, radius: 130, label: 'Lactique' },
    { id: 'h2', cx: 637, cy: 366, radius: 130, label: 'Alcoolique' },
  ],
};

const svt_muscle_sarcomere: ScientificSchema = {
  id: 'svt_muscle_sarcomere',
  title: 'Structure du sarcomère',
  subject: 'svt',
  keywords: ['sarcomère', 'sarcomere', 'muscle', 'strié', 'actine', 'myosine', 'contraction', 'عضلة', 'بنية العضلة'],
  category: 'structure',
  viewBox: '0 0 860 480',
  backgroundColor: '#fef2f2',
  layers: [
    { id: 'title', label: 'Titre', delay: 0, svgContent: `
      <text x="430" y="38" text-anchor="middle" font-size="22" font-weight="bold" fill="#0f172a" font-family="system-ui">STRUCTURE DU SARCOMÈRE</text>
      <text x="430" y="58" text-anchor="middle" font-size="13" fill="#64748b" font-family="system-ui">Unité contractile du muscle strié squelettique — القطعة العضلية</text>
    `},
    { id: 'z_lines', label: 'Lignes Z', delay: 200, svgContent: `
      <line x1="140" y1="90" x2="140" y2="330" stroke="#1e40af" stroke-width="4"/>
      <line x1="720" y1="90" x2="720" y2="330" stroke="#1e40af" stroke-width="4"/>
      <text x="140" y="82" text-anchor="middle" font-size="13" font-weight="bold" fill="#1e40af" font-family="system-ui">Ligne Z</text>
      <text x="720" y="82" text-anchor="middle" font-size="13" font-weight="bold" fill="#1e40af" font-family="system-ui">Ligne Z</text>
      <line x1="140" y1="355" x2="720" y2="355" stroke="#64748b" stroke-width="1.5" marker-start="url(#arrowGray)" marker-end="url(#arrowGray)"/>
      <text x="430" y="375" text-anchor="middle" font-size="13" font-weight="600" fill="#374151" font-family="system-ui">1 Sarcomère</text>
    `},
    { id: 'actine', label: 'Actine (fins)', delay: 500, svgContent: `
      <line x1="140" y1="140" x2="400" y2="140" stroke="#ef4444" stroke-width="5" stroke-linecap="round"/>
      <line x1="140" y1="180" x2="400" y2="180" stroke="#ef4444" stroke-width="5" stroke-linecap="round"/>
      <line x1="140" y1="220" x2="400" y2="220" stroke="#ef4444" stroke-width="5" stroke-linecap="round"/>
      <line x1="140" y1="260" x2="400" y2="260" stroke="#ef4444" stroke-width="5" stroke-linecap="round"/>
      <line x1="460" y1="140" x2="720" y2="140" stroke="#ef4444" stroke-width="5" stroke-linecap="round"/>
      <line x1="460" y1="180" x2="720" y2="180" stroke="#ef4444" stroke-width="5" stroke-linecap="round"/>
      <line x1="460" y1="220" x2="720" y2="220" stroke="#ef4444" stroke-width="5" stroke-linecap="round"/>
      <line x1="460" y1="260" x2="720" y2="260" stroke="#ef4444" stroke-width="5" stroke-linecap="round"/>
      <rect x="755" y="130" width="90" height="28" rx="6" fill="#fef2f2" stroke="#ef4444" stroke-width="1.5"/>
      <text x="800" y="149" text-anchor="middle" font-size="12" font-weight="600" fill="#dc2626" font-family="system-ui">Actine</text>
    `},
    { id: 'myosine', label: 'Myosine (épais)', delay: 800, svgContent: `
      <line x1="280" y1="135" x2="580" y2="135" stroke="#2563eb" stroke-width="8" stroke-linecap="round"/>
      <line x1="280" y1="175" x2="580" y2="175" stroke="#2563eb" stroke-width="8" stroke-linecap="round"/>
      <line x1="280" y1="215" x2="580" y2="215" stroke="#2563eb" stroke-width="8" stroke-linecap="round"/>
      <line x1="280" y1="255" x2="580" y2="255" stroke="#2563eb" stroke-width="8" stroke-linecap="round"/>
      <rect x="755" y="170" width="90" height="28" rx="6" fill="#eff6ff" stroke="#2563eb" stroke-width="1.5"/>
      <text x="800" y="189" text-anchor="middle" font-size="12" font-weight="600" fill="#1d4ed8" font-family="system-ui">Myosine</text>
      <line x1="430" y1="90" x2="430" y2="330" stroke="#94a3b8" stroke-width="2" stroke-dasharray="5,4"/>
      <text x="430" y="345" text-anchor="middle" font-size="11" font-weight="600" fill="#64748b" font-family="system-ui">Ligne M</text>
    `},
    { id: 'bandes', label: 'Bandes', delay: 1200, svgContent: `
      <rect x="140" y="280" width="140" height="18" rx="4" fill="#fecaca" opacity="0.5"/>
      <text x="210" y="315" text-anchor="middle" font-size="12" font-weight="600" fill="#dc2626" font-family="system-ui">Bande I (claire)</text>
      <rect x="280" y="280" width="300" height="18" rx="4" fill="#bfdbfe" opacity="0.5"/>
      <text x="430" y="315" text-anchor="middle" font-size="12" font-weight="600" fill="#1d4ed8" font-family="system-ui">Bande A (sombre)</text>
      <rect x="580" y="280" width="140" height="18" rx="4" fill="#fecaca" opacity="0.5"/>
    `},
    { id: 'note', label: 'Contraction', delay: 1500, svgContent: `
      <rect x="130" y="400" width="600" height="55" rx="12" fill="#ecfdf5" stroke="#059669" stroke-width="2"/>
      <text x="430" y="425" text-anchor="middle" font-size="13" font-weight="bold" fill="#065f46" font-family="system-ui">Contraction: les filaments d'actine GLISSENT sur la myosine</text>
      <text x="430" y="445" text-anchor="middle" font-size="12" fill="#059669" font-family="system-ui">→ Bande I et zone H raccourcissent | Bande A constante</text>
    `},
  ],
  annotations: [
    { id: 'a1', x: 140, y: 125, width: 260, height: 150, label: 'Actine', description: 'Filaments fins fixés aux lignes Z. Glissent vers le centre lors de la contraction.', color: '#ef4444' },
    { id: 'a2', x: 280, y: 125, width: 300, height: 150, label: 'Myosine', description: 'Filaments épais avec têtes pivotantes. Cycle des ponts actine-myosine (nécessite ATP+Ca²⁺).', color: '#2563eb' },
  ],
  highlights: [
    { id: 'h1', cx: 270, cy: 200, radius: 140, label: 'Actine' },
    { id: 'h2', cx: 430, cy: 195, radius: 160, label: 'Myosine' },
  ],
};

// ═══════════════════════════════════════════════════════════════
// SVT — Ch2: Information génétique
// ═══════════════════════════════════════════════════════════════

const svt_adn_structure: ScientificSchema = {
  id: 'svt_adn_structure',
  title: 'Structure de l\'ADN — Double hélice',
  subject: 'svt',
  keywords: ['adn', 'double hélice', 'nucléotide', 'base azotée', 'watson', 'crick', 'complémentarité', 'الحمض النووي', 'بنية'],
  category: 'structure',
  viewBox: '0 0 800 550',
  backgroundColor: '#fdf4ff',
  layers: [
    { id: 'title', label: 'Titre', delay: 0, svgContent: `
      <text x="400" y="38" text-anchor="middle" font-size="22" font-weight="bold" fill="#0f172a" font-family="system-ui">STRUCTURE DE L'ADN</text>
      <text x="400" y="58" text-anchor="middle" font-size="13" fill="#64748b" font-family="system-ui">Double hélice — Modèle de Watson et Crick (1953)</text>
    `},
    { id: 'helix', label: 'Double hélice', delay: 300, svgContent: `
      <path d="M 200 100 Q 260 130, 200 160 Q 140 190, 200 220 Q 260 250, 200 280 Q 140 310, 200 340 Q 260 370, 200 400 Q 140 430, 200 460" fill="none" stroke="#dc2626" stroke-width="5" stroke-linecap="round"/>
      <path d="M 340 100 Q 280 130, 340 160 Q 400 190, 340 220 Q 280 250, 340 280 Q 400 310, 340 340 Q 280 370, 340 400 Q 400 430, 340 460" fill="none" stroke="#2563eb" stroke-width="5" stroke-linecap="round"/>
      <text x="140" y="95" font-size="12" font-weight="600" fill="#dc2626" font-family="system-ui">Brin 5'→3'</text>
      <text x="345" y="95" font-size="12" font-weight="600" fill="#2563eb" font-family="system-ui">Brin 3'→5'</text>
    `},
    { id: 'bases', label: 'Bases azotées', delay: 700, svgContent: `
      <line x1="210" y1="130" x2="270" y2="130" stroke="#16a34a" stroke-width="3"/>
      <line x1="270" y1="130" x2="330" y2="130" stroke="#f97316" stroke-width="3"/>
      <text x="230" y="125" font-size="11" font-weight="bold" fill="#16a34a" font-family="system-ui">A</text>
      <text x="310" y="125" font-size="11" font-weight="bold" fill="#f97316" font-family="system-ui">T</text>
      <line x1="182" y1="190" x2="248" y2="190" stroke="#7c3aed" stroke-width="3"/>
      <line x1="248" y1="190" x2="352" y2="190" stroke="#0891b2" stroke-width="3"/>
      <text x="208" y="185" font-size="11" font-weight="bold" fill="#7c3aed" font-family="system-ui">C</text>
      <text x="318" y="185" font-size="11" font-weight="bold" fill="#0891b2" font-family="system-ui">G</text>
      <line x1="210" y1="250" x2="270" y2="250" stroke="#0891b2" stroke-width="3"/>
      <line x1="270" y1="250" x2="330" y2="250" stroke="#7c3aed" stroke-width="3"/>
      <text x="230" y="245" font-size="11" font-weight="bold" fill="#0891b2" font-family="system-ui">G</text>
      <text x="310" y="245" font-size="11" font-weight="bold" fill="#7c3aed" font-family="system-ui">C</text>
      <line x1="182" y1="310" x2="248" y2="310" stroke="#f97316" stroke-width="3"/>
      <line x1="248" y1="310" x2="352" y2="310" stroke="#16a34a" stroke-width="3"/>
      <text x="208" y="305" font-size="11" font-weight="bold" fill="#f97316" font-family="system-ui">T</text>
      <text x="318" y="305" font-size="11" font-weight="bold" fill="#16a34a" font-family="system-ui">A</text>
      <line x1="210" y1="370" x2="270" y2="370" stroke="#16a34a" stroke-width="3"/>
      <line x1="270" y1="370" x2="330" y2="370" stroke="#f97316" stroke-width="3"/>
      <text x="230" y="365" font-size="11" font-weight="bold" fill="#16a34a" font-family="system-ui">A</text>
      <text x="310" y="365" font-size="11" font-weight="bold" fill="#f97316" font-family="system-ui">T</text>
    `},
    { id: 'legend', label: 'Légende', delay: 1100, svgContent: `
      <rect x="480" y="100" width="280" height="200" rx="12" fill="white" stroke="#e5e7eb" stroke-width="1.5"/>
      <text x="620" y="128" text-anchor="middle" font-size="15" font-weight="bold" fill="#0f172a" font-family="system-ui">Complémentarité des bases</text>
      <circle cx="510" cy="155" r="10" fill="#16a34a"/><text x="530" y="160" font-size="13" fill="#374151" font-family="system-ui">A — Adénine</text>
      <circle cx="510" cy="185" r="10" fill="#f97316"/><text x="530" y="190" font-size="13" fill="#374151" font-family="system-ui">T — Thymine</text>
      <circle cx="510" cy="215" r="10" fill="#0891b2"/><text x="530" y="220" font-size="13" fill="#374151" font-family="system-ui">G — Guanine</text>
      <circle cx="510" cy="245" r="10" fill="#7c3aed"/><text x="530" y="250" font-size="13" fill="#374151" font-family="system-ui">C — Cytosine</text>
      <text x="620" y="280" text-anchor="middle" font-size="13" font-weight="600" fill="#dc2626" font-family="system-ui">A═T (2 liaisons H) | G≡C (3 liaisons H)</text>
      <rect x="480" y="320" width="280" height="85" rx="10" fill="#fefce8" stroke="#ca8a04" stroke-width="1.5"/>
      <text x="620" y="345" text-anchor="middle" font-size="13" font-weight="bold" fill="#854d0e" font-family="system-ui">Nucléotide = </text>
      <text x="620" y="365" text-anchor="middle" font-size="12" fill="#374151" font-family="system-ui">Base azotée + Désoxyribose + Phosphate</text>
      <text x="620" y="390" text-anchor="middle" font-size="12" fill="#374151" font-family="system-ui">Brins antiparallèles: 5'→3' et 3'→5'</text>
    `},
  ],
  annotations: [
    { id: 'a1', x: 130, y: 90, width: 280, height: 380, label: 'Double hélice', description: 'Deux brins polynucléotidiques enroulés en hélice. Brins antiparallèles reliés par des liaisons hydrogène entre bases complémentaires.', color: '#7c3aed' },
  ],
  highlights: [],
};

export const svt_transcription_traduction: ScientificSchema = {
  id: 'svt_transcription_traduction',
  title: 'Expression génétique — Transcription et Traduction',
  subject: 'svt',
  keywords: ['transcription', 'traduction', 'arnm', 'protéine', 'ribosome', 'codon', 'acide aminé', 'استنساخ', 'ترجمة', 'expression'],
  category: 'process',
  viewBox: '0 0 850 550',
  backgroundColor: '#f0fdf4',
  layers: [
    { id: 'title', label: 'Titre', delay: 0, svgContent: `
      <text x="425" y="38" text-anchor="middle" font-size="22" font-weight="bold" fill="#0f172a" font-family="system-ui">EXPRESSION DU MATÉRIEL GÉNÉTIQUE</text>
      <text x="425" y="58" text-anchor="middle" font-size="13" fill="#64748b" font-family="system-ui">ADN → ARNm (transcription) → Protéine (traduction)</text>
    `},
    { id: 'noyau', label: 'Noyau', delay: 200, svgContent: `
      <rect x="40" y="80" width="350" height="260" rx="20" fill="#e9d5ff" stroke="#7c3aed" stroke-width="2.5" opacity="0.4"/>
      <text x="215" y="108" text-anchor="middle" font-size="14" font-weight="600" fill="#581c87" font-family="system-ui">NOYAU (النواة)</text>
    `},
    { id: 'transcription', label: 'Transcription', delay: 500, svgContent: `
      <rect x="70" y="125" width="130" height="38" rx="8" fill="url(#grad_blue)" stroke="#2563eb" stroke-width="2"/>
      <text x="135" y="149" text-anchor="middle" font-size="13" font-weight="bold" fill="white" font-family="system-ui">ADN (gène)</text>
      <line x1="200" y1="144" x2="250" y2="144" stroke="#16a34a" stroke-width="2.5" marker-end="url(#arrowGreen)"/>
      <text x="225" y="136" text-anchor="middle" font-size="10" font-weight="600" fill="#16a34a" font-family="system-ui">ARN pol.</text>
      <rect x="255" y="125" width="120" height="38" rx="8" fill="url(#grad_green)" stroke="#16a34a" stroke-width="2"/>
      <text x="315" y="149" text-anchor="middle" font-size="13" font-weight="bold" fill="white" font-family="system-ui">ARNm</text>
      <rect x="70" y="180" width="295" height="55" rx="8" fill="white" stroke="#d1d5db" stroke-width="1.5"/>
      <text x="217" y="200" text-anchor="middle" font-size="13" font-weight="bold" fill="#16a34a" font-family="system-ui">TRANSCRIPTION (الاستنساخ)</text>
      <text x="217" y="220" text-anchor="middle" font-size="11" fill="#374151" font-family="system-ui">ADN → ARN pré-messager → ARNm mature</text>
      <text x="217" y="260" text-anchor="middle" font-size="11" fill="#64748b" font-family="system-ui">Complémentarité: A→U, T→A, G→C, C→G</text>
      <text x="217" y="280" text-anchor="middle" font-size="11" fill="#64748b" font-family="system-ui">Enzyme: ARN polymérase | Sens 5'→3'</text>
    `},
    { id: 'export', label: 'Export ARNm', delay: 900, svgContent: `
      <path d="M 390 200 Q 430 200, 450 200" stroke="#16a34a" stroke-width="2" fill="none" stroke-dasharray="5,3" marker-end="url(#arrowGreen)"/>
      <text x="420" y="190" font-size="10" fill="#16a34a" font-family="system-ui">Pore</text>
      <text x="420" y="215" font-size="10" fill="#16a34a" font-family="system-ui">nucléaire</text>
    `},
    { id: 'cytoplasme', label: 'Cytoplasme', delay: 1100, svgContent: `
      <rect x="460" y="80" width="350" height="260" rx="20" fill="#dbeafe" stroke="#3b82f6" stroke-width="2" stroke-dasharray="8,4" opacity="0.3"/>
      <text x="635" y="108" text-anchor="middle" font-size="14" font-weight="600" fill="#1d4ed8" font-family="system-ui">CYTOPLASME (الهيولى)</text>
    `},
    { id: 'traduction', label: 'Traduction', delay: 1300, svgContent: `
      <rect x="480" y="125" width="120" height="35" rx="8" fill="url(#grad_green)" stroke="#16a34a" stroke-width="2"/>
      <text x="540" y="147" text-anchor="middle" font-size="12" font-weight="bold" fill="white" font-family="system-ui">ARNm</text>
      <ellipse cx="640" cy="142" rx="35" ry="20" fill="#fbbf24" stroke="#d97706" stroke-width="2"/>
      <text x="640" y="147" text-anchor="middle" font-size="10" font-weight="600" fill="#92400e" font-family="system-ui">Ribosome</text>
      <line x1="675" y1="142" x2="720" y2="142" stroke="#ea580c" stroke-width="2.5" marker-end="url(#arrowOrange)"/>
      <rect x="725" y="125" width="70" height="35" rx="8" fill="url(#grad_orange)" stroke="#ea580c" stroke-width="2"/>
      <text x="760" y="147" text-anchor="middle" font-size="11" font-weight="bold" fill="white" font-family="system-ui">Protéine</text>
      <rect x="480" y="178" width="315" height="75" rx="8" fill="white" stroke="#d1d5db" stroke-width="1.5"/>
      <text x="637" y="198" text-anchor="middle" font-size="13" font-weight="bold" fill="#ea580c" font-family="system-ui">TRADUCTION (الترجمة)</text>
      <text x="637" y="218" text-anchor="middle" font-size="11" fill="#374151" font-family="system-ui">ARNm → Chaîne polypeptidique (protéine)</text>
      <text x="637" y="240" text-anchor="middle" font-size="11" fill="#64748b" font-family="system-ui">Codon (3 bases) → 1 acide aminé</text>
    `},
    { id: 'resume', label: 'Résumé', delay: 1700, svgContent: `
      <rect x="120" y="380" width="610" height="70" rx="14" fill="#fefce8" stroke="#ca8a04" stroke-width="2"/>
      <text x="425" y="410" text-anchor="middle" font-size="16" font-weight="bold" fill="#854d0e" font-family="system-ui">Dogme central de la biologie moléculaire</text>
      <text x="425" y="435" text-anchor="middle" font-size="15" fill="#374151" font-family="system-ui">ADN  →  ARNm  →  Protéine</text>
      <text x="295" y="435" text-anchor="middle" font-size="11" fill="#16a34a" font-family="system-ui">transcription</text>
      <text x="525" y="435" text-anchor="middle" font-size="11" fill="#ea580c" font-family="system-ui">traduction</text>
      <rect x="120" y="465" width="610" height="55" rx="10" fill="white" stroke="#e5e7eb" stroke-width="1.5"/>
      <text x="425" y="488" text-anchor="middle" font-size="12" fill="#374151" font-family="system-ui">Code génétique: universel, redondant (dégénéré), non chevauchant, non ambigu</text>
      <text x="425" y="508" text-anchor="middle" font-size="12" fill="#374151" font-family="system-ui">Codon initiateur: AUG (Met) | Codons stop: UAA, UAG, UGA</text>
    `},
  ],
  annotations: [
    { id: 'a1', x: 70, y: 125, width: 295, height: 170, label: 'Transcription', description: 'Copie d\'un gène (ADN) en ARN messager par l\'ARN polymérase dans le noyau. Complémentarité: A↔U, G↔C.', color: '#16a34a' },
    { id: 'a2', x: 480, y: 125, width: 315, height: 130, label: 'Traduction', description: 'Lecture de l\'ARNm par le ribosome dans le cytoplasme. Chaque codon (3 bases) = 1 acide aminé.', color: '#ea580c' },
  ],
  highlights: [],
};

export const svt_mitose: ScientificSchema = {
  id: 'svt_mitose',
  title: 'La Mitose — Division cellulaire conservatrice',
  subject: 'svt',
  keywords: ['mitose', 'division', 'prophase', 'métaphase', 'anaphase', 'télophase', 'chromosome', 'انقسام غير مباشر'],
  category: 'process',
  viewBox: '0 0 900 500',
  backgroundColor: '#eff6ff',
  layers: [
    { id: 'title', label: 'Titre', delay: 0, svgContent: `
      <text x="450" y="38" text-anchor="middle" font-size="22" font-weight="bold" fill="#0f172a" font-family="system-ui">LA MITOSE — 4 phases</text>
      <text x="450" y="58" text-anchor="middle" font-size="13" fill="#64748b" font-family="system-ui">1 cellule (2n) → 2 cellules filles identiques (2n) — الانقسام غير المباشر</text>
    `},
    { id: 'prophase', label: 'Prophase', delay: 300, svgContent: `
      <circle cx="130" cy="220" r="85" fill="#fef2f2" stroke="#dc2626" stroke-width="2.5"/>
      <text x="130" y="135" text-anchor="middle" font-size="15" font-weight="bold" fill="#dc2626" font-family="system-ui">1. PROPHASE</text>
      <text x="130" y="155" text-anchor="middle" font-size="10" fill="#64748b" font-family="system-ui">الطور التمهيدي</text>
      <line x1="110" y1="185" x2="150" y2="210" stroke="#7c3aed" stroke-width="4" stroke-linecap="round"/>
      <line x1="115" y1="210" x2="145" y2="190" stroke="#7c3aed" stroke-width="4" stroke-linecap="round"/>
      <line x1="100" y1="230" x2="140" y2="255" stroke="#2563eb" stroke-width="4" stroke-linecap="round"/>
      <line x1="105" y1="255" x2="135" y2="235" stroke="#2563eb" stroke-width="4" stroke-linecap="round"/>
      <text x="130" y="290" text-anchor="middle" font-size="10" fill="#dc2626" font-family="system-ui">Condensation</text>
      <text x="130" y="305" text-anchor="middle" font-size="10" fill="#dc2626" font-family="system-ui">chromosomes</text>
    `},
    { id: 'metaphase', label: 'Métaphase', delay: 600, svgContent: `
      <circle cx="340" cy="220" r="85" fill="#f0fdf4" stroke="#16a34a" stroke-width="2.5"/>
      <text x="340" y="135" text-anchor="middle" font-size="15" font-weight="bold" fill="#16a34a" font-family="system-ui">2. MÉTAPHASE</text>
      <text x="340" y="155" text-anchor="middle" font-size="10" fill="#64748b" font-family="system-ui">الطور الاستوائي</text>
      <line x1="340" y1="175" x2="340" y2="265" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="4,3"/>
      <line x1="320" y1="198" x2="360" y2="198" stroke="#7c3aed" stroke-width="5" stroke-linecap="round"/>
      <line x1="320" y1="218" x2="360" y2="218" stroke="#2563eb" stroke-width="5" stroke-linecap="round"/>
      <line x1="320" y1="238" x2="360" y2="238" stroke="#7c3aed" stroke-width="5" stroke-linecap="round"/>
      <text x="340" y="290" text-anchor="middle" font-size="10" fill="#16a34a" font-family="system-ui">Alignement</text>
      <text x="340" y="305" text-anchor="middle" font-size="10" fill="#16a34a" font-family="system-ui">plaque équatoriale</text>
    `},
    { id: 'anaphase', label: 'Anaphase', delay: 900, svgContent: `
      <circle cx="560" cy="220" r="85" fill="#fff7ed" stroke="#ea580c" stroke-width="2.5"/>
      <text x="560" y="135" text-anchor="middle" font-size="15" font-weight="bold" fill="#ea580c" font-family="system-ui">3. ANAPHASE</text>
      <text x="560" y="155" text-anchor="middle" font-size="10" fill="#64748b" font-family="system-ui">الطور الانفصالي</text>
      <line x1="530" y1="195" x2="510" y2="185" stroke="#7c3aed" stroke-width="4" stroke-linecap="round"/>
      <line x1="590" y1="195" x2="610" y2="185" stroke="#7c3aed" stroke-width="4" stroke-linecap="round"/>
      <line x1="530" y1="220" x2="510" y2="210" stroke="#2563eb" stroke-width="4" stroke-linecap="round"/>
      <line x1="590" y1="220" x2="610" y2="210" stroke="#2563eb" stroke-width="4" stroke-linecap="round"/>
      <line x1="530" y1="245" x2="510" y2="235" stroke="#7c3aed" stroke-width="4" stroke-linecap="round"/>
      <line x1="590" y1="245" x2="610" y2="235" stroke="#7c3aed" stroke-width="4" stroke-linecap="round"/>
      <text x="505" y="260" text-anchor="middle" font-size="8" fill="#ea580c" font-family="system-ui">←</text>
      <text x="615" y="260" text-anchor="middle" font-size="8" fill="#ea580c" font-family="system-ui">→</text>
      <text x="560" y="290" text-anchor="middle" font-size="10" fill="#ea580c" font-family="system-ui">Séparation</text>
      <text x="560" y="305" text-anchor="middle" font-size="10" fill="#ea580c" font-family="system-ui">chromatides</text>
    `},
    { id: 'telophase', label: 'Télophase', delay: 1200, svgContent: `
      <circle cx="770" cy="190" r="55" fill="#f5f3ff" stroke="#7c3aed" stroke-width="2"/>
      <circle cx="770" cy="260" r="55" fill="#f5f3ff" stroke="#7c3aed" stroke-width="2"/>
      <text x="770" y="135" text-anchor="middle" font-size="15" font-weight="bold" fill="#7c3aed" font-family="system-ui">4. TÉLOPHASE</text>
      <text x="770" y="155" text-anchor="middle" font-size="10" fill="#64748b" font-family="system-ui">الطور النهائي</text>
      <text x="770" y="195" text-anchor="middle" font-size="10" fill="#7c3aed" font-family="system-ui">2n</text>
      <text x="770" y="265" text-anchor="middle" font-size="10" fill="#7c3aed" font-family="system-ui">2n</text>
      <text x="770" y="305" text-anchor="middle" font-size="10" fill="#7c3aed" font-family="system-ui">Cytocinèse</text>
    `},
    { id: 'arrows', label: 'Flèches', delay: 400, svgContent: `
      <line x1="215" y1="220" x2="250" y2="220" stroke="#94a3b8" stroke-width="2" marker-end="url(#arrowGray)"/>
      <line x1="425" y1="220" x2="465" y2="220" stroke="#94a3b8" stroke-width="2" marker-end="url(#arrowGray)"/>
      <line x1="645" y1="220" x2="705" y2="220" stroke="#94a3b8" stroke-width="2" marker-end="url(#arrowGray)"/>
    `},
    { id: 'bilan', label: 'Bilan', delay: 1500, svgContent: `
      <rect x="150" y="380" width="600" height="50" rx="12" fill="#ecfdf5" stroke="#059669" stroke-width="2"/>
      <text x="450" y="410" text-anchor="middle" font-size="15" font-weight="bold" fill="#065f46" font-family="system-ui">Résultat: 2 cellules filles IDENTIQUES (2n) = conservation de l'information génétique</text>
      <rect x="150" y="440" width="600" height="35" rx="8" fill="white" stroke="#e5e7eb" stroke-width="1.5"/>
      <text x="450" y="463" text-anchor="middle" font-size="12" fill="#374151" font-family="system-ui">Rôle: croissance, renouvellement cellulaire, cicatrisation</text>
    `},
  ],
  annotations: [
    { id: 'a1', x: 45, y: 135, width: 170, height: 170, label: 'Prophase', description: 'Condensation de la chromatine en chromosomes visibles. Disparition de l\'enveloppe nucléaire. Formation du fuseau.', color: '#dc2626' },
    { id: 'a2', x: 255, y: 135, width: 170, height: 170, label: 'Métaphase', description: 'Les chromosomes s\'alignent sur la plaque équatoriale (plan médian de la cellule).', color: '#16a34a' },
    { id: 'a3', x: 475, y: 135, width: 170, height: 170, label: 'Anaphase', description: 'Clivage des centromères. Les chromatides sœurs migrent vers les pôles opposés.', color: '#ea580c' },
    { id: 'a4', x: 715, y: 135, width: 110, height: 190, label: 'Télophase', description: 'Décondensation. Reformation des enveloppes nucléaires. Cytocinèse (division du cytoplasme).', color: '#7c3aed' },
  ],
  highlights: [],
};

// ═══════════════════════════════════════════════════════════════
// SVT — Ch4: Géologie
// ═══════════════════════════════════════════════════════════════

export const svt_subduction: ScientificSchema = {
  id: 'svt_subduction',
  title: 'Subduction — Plongement d\'une plaque océanique',
  subject: 'svt',
  keywords: ['subduction', 'plaque', 'océanique', 'fosse', 'volcanisme', 'métamorphisme', 'الغوص', 'صفيحة'],
  category: 'process',
  viewBox: '0 0 900 500',
  backgroundColor: '#f0f9ff',
  layers: [
    { id: 'title', label: 'Titre', delay: 0, svgContent: `
      <text x="450" y="38" text-anchor="middle" font-size="22" font-weight="bold" fill="#0f172a" font-family="system-ui">ZONE DE SUBDUCTION</text>
      <text x="450" y="58" text-anchor="middle" font-size="13" fill="#64748b" font-family="system-ui">Plongement d'une plaque océanique sous une autre plaque — الغوص</text>
    `},
    { id: 'surface', label: 'Surface', delay: 200, svgContent: `
      <line x1="0" y1="200" x2="900" y2="200" stroke="#0284c7" stroke-width="2"/>
      <rect x="0" y="200" width="420" height="20" fill="#0ea5e9" opacity="0.3"/>
      <text x="200" y="190" text-anchor="middle" font-size="13" font-weight="600" fill="#0369a1" font-family="system-ui">Océan</text>
      <rect x="500" y="160" width="400" height="40" rx="4" fill="#a3e635" opacity="0.3"/>
      <text x="700" y="185" text-anchor="middle" font-size="13" font-weight="600" fill="#4d7c0f" font-family="system-ui">Continent</text>
    `},
    { id: 'plaques', label: 'Plaques', delay: 500, svgContent: `
      <rect x="0" y="220" width="450" height="30" fill="#60a5fa" stroke="#2563eb" stroke-width="2"/>
      <text x="200" y="242" text-anchor="middle" font-size="12" font-weight="600" fill="white" font-family="system-ui">Lithosphère océanique</text>
      <rect x="480" y="200" width="420" height="50" fill="#fbbf24" stroke="#d97706" stroke-width="2"/>
      <text x="690" y="230" text-anchor="middle" font-size="12" font-weight="600" fill="#92400e" font-family="system-ui">Lithosphère continentale</text>
      <polygon points="420,250 480,200 480,250" fill="#60a5fa" stroke="#2563eb" stroke-width="2"/>
      <path d="M 350 250 L 250 350 L 200 430 L 180 480" stroke="#2563eb" stroke-width="3" fill="none" stroke-dasharray="8,4"/>
      <text x="230" y="370" font-size="12" font-weight="600" fill="#1d4ed8" font-family="system-ui" transform="rotate(50,230,370)">Plaque plongeante</text>
    `},
    { id: 'fosse', label: 'Fosse', delay: 800, svgContent: `
      <path d="M 400 200 L 440 270 L 480 200" fill="#1e3a5f" opacity="0.4"/>
      <text x="440" y="195" text-anchor="middle" font-size="12" font-weight="bold" fill="#dc2626" font-family="system-ui">Fosse océanique</text>
    `},
    { id: 'volcans', label: 'Volcans', delay: 1100, svgContent: `
      <polygon points="600,160 620,100 640,160" fill="#ef4444" stroke="#dc2626" stroke-width="2"/>
      <text x="620" y="90" text-anchor="middle" font-size="11" font-weight="bold" fill="#dc2626" font-family="system-ui">Volcans</text>
      <circle cx="615" cy="85" r="8" fill="#fbbf24" opacity="0.6"/>
      <circle cx="625" cy="80" r="6" fill="#fbbf24" opacity="0.4"/>
      <polygon points="670,160 685,115 700,160" fill="#ef4444" stroke="#dc2626" stroke-width="1.5"/>
    `},
    { id: 'manteau', label: 'Manteau', delay: 1300, svgContent: `
      <rect x="0" y="250" width="900" height="250" fill="#ea580c" opacity="0.15"/>
      <text x="700" y="400" text-anchor="middle" font-size="16" font-weight="600" fill="#c2410c" font-family="system-ui">ASTHÉNOSPHÈRE</text>
      <text x="700" y="420" text-anchor="middle" font-size="12" fill="#ea580c" font-family="system-ui">(manteau ductile)</text>
      <text x="350" y="460" font-size="11" fill="#dc2626" font-family="system-ui">Métamorphisme HP-BT (schiste bleu → éclogite)</text>
      <path d="M 300 430 L 250 460" stroke="#0891b2" stroke-width="2" marker-end="url(#arrowCyan)"/>
      <text x="220" y="475" font-size="10" fill="#0891b2" font-family="system-ui">Déshydratation</text>
      <path d="M 350 370 Q 400 330, 550 280" stroke="#dc2626" stroke-width="1.5" fill="none" stroke-dasharray="4,3" marker-end="url(#arrowRed)"/>
      <text x="460" y="310" font-size="10" fill="#dc2626" font-family="system-ui">Fusion partielle → magma</text>
    `},
  ],
  annotations: [
    { id: 'a1', x: 400, y: 180, width: 80, height: 90, label: 'Fosse', description: 'Zone de convergence: la plaque océanique (dense) plonge sous la plaque continentale (légère). Profondeur: 8-11 km.', color: '#1e40af' },
    { id: 'a2', x: 600, y: 80, width: 100, height: 80, label: 'Volcans', description: 'Arc volcanique formé par la fusion partielle du manteau (due à la déshydratation de la plaque plongeante).', color: '#dc2626' },
  ],
  highlights: [],
};

// ═══════════════════════════════════════════════════════════════
// SVT — Ch1: Schémas détaillés manquants
// ═══════════════════════════════════════════════════════════════

const svt_mitochondrie_structure: ScientificSchema = {
  id: 'svt_mitochondrie_structure',
  title: 'Structure de la Mitochondrie — Ultrastructure',
  subject: 'svt',
  keywords: ['mitochondrie', 'membrane interne', 'membrane externe', 'crêtes', 'matrice', 'espace intermembranaire', 'الميتوكندري', 'بنية الميتوكندري'],
  category: 'structure',
  viewBox: '0 0 920 620',
  backgroundColor: '#fffbf0',
  layers: [
    { id: 'title', label: 'Titre', delay: 0, svgContent: `
      <text x="460" y="34" text-anchor="middle" font-size="26" font-weight="bold" fill="#6b21a8" font-family="system-ui">L'ultrastructure de la</text>
      <text x="460" y="68" text-anchor="middle" font-size="32" font-weight="900" fill="#6b21a8" font-family="system-ui">Mitochondrie</text>
      <text x="460" y="90" text-anchor="middle" font-size="12" fill="#64748b" font-family="system-ui">بنية الميتوكندري — « Centrale énergétique » de la cellule</text>
    `},
    { id: 'membrane_ext', label: 'Membrane externe', delay: 300, svgContent: `
      <!-- Outer membrane: bean / kidney shape using cubic beziers -->
      <path d="
        M 180 310
        C 180 200, 250 130, 400 120
        C 500 113, 600 118, 680 140
        C 760 162, 800 210, 800 300
        C 800 390, 760 445, 680 468
        C 600 500, 500 505, 400 498
        C 250 488, 180 420, 180 310
        Z
      " fill="#f5deb3" stroke="#c2710e" stroke-width="4" />
      <!-- Label: Membrane externe -->
      <line x1="750" y1="170" x2="820" y2="120" stroke="#8b5e3c" stroke-width="1.5"/>
      <text x="825" y="115" font-size="13" font-weight="700" fill="#8b5e3c" font-family="system-ui">Membrane</text>
      <text x="825" y="131" font-size="13" font-weight="700" fill="#8b5e3c" font-family="system-ui">externe</text>
    `},
    { id: 'espace_inter', label: 'Espace intermembranaire', delay: 500, svgContent: `
      <!-- Inner membrane outline (smaller bean, creates gap = espace intermembranaire) -->
      <path d="
        M 210 310
        C 210 215, 270 155, 405 145
        C 505 138, 595 143, 665 162
        C 735 180, 770 225, 770 308
        C 770 390, 735 435, 665 455
        C 595 480, 505 483, 405 477
        C 270 467, 210 405, 210 310
        Z
      " fill="#efd79a" stroke="#b8860b" stroke-width="3" />
      <path d="
        M 194 310
        C 194 208, 260 145, 403 135
        C 504 128, 597 133, 672 153
        C 745 173, 783 221, 783 307
        C 783 393, 745 440, 672 463
        C 597 488, 504 492, 403 486
        C 260 476, 194 412, 194 310
        Z
      " fill="none" stroke="#f8e7b8" stroke-width="11" opacity="0.9" />
      <!-- Label: Espace intermembranaire -->
      <line x1="202" y1="246" x2="118" y2="198" stroke="#0891b2" stroke-width="1.5"/>
      <text x="15" y="190" font-size="12" font-weight="700" fill="#0891b2" font-family="system-ui">Espace</text>
      <text x="15" y="206" font-size="12" font-weight="700" fill="#0891b2" font-family="system-ui">intermembranaire</text>
      <text x="15" y="222" font-size="10" fill="#0891b2" font-family="system-ui">entre les 2 membranes</text>
    `},
    { id: 'matrice_fill', label: 'Matrice (fond)', delay: 700, svgContent: `
      <!-- Matrix interior fill -->
      <path d="
        M 230 310
        C 230 225, 285 170, 410 160
        C 500 154, 585 158, 650 175
        C 720 192, 750 235, 750 310
        C 750 385, 720 425, 650 443
        C 585 468, 500 471, 410 465
        C 285 455, 230 395, 230 310
        Z
      " fill="#daa520" opacity="0.35" stroke="none" />
    `},
    { id: 'cretes', label: 'Crêtes mitochondriales', delay: 900, svgContent: `
      <!-- Villosité-like cristae -->
      <path d="M 252 214 C 296 206, 336 210, 358 230 C 380 251, 382 286, 364 306 C 345 329, 307 335, 272 328 C 312 321, 333 300, 336 276 C 339 252, 324 235, 294 229 C 277 226, 264 226, 252 228" fill="none" stroke="#c7961a" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
      <path d="M 271 170 C 338 162, 400 169, 432 198 C 463 226, 468 271, 452 313 C 435 357, 393 387, 347 404 C 387 386, 417 357, 425 320 C 433 285, 422 249, 396 224 C 369 198, 320 187, 271 188" fill="none" stroke="#c7961a" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
      <path d="M 468 167 C 525 162, 573 176, 597 208 C 621 240, 623 285, 610 326 C 597 366, 570 397, 523 420 C 557 398, 581 367, 589 330 C 598 290, 594 252, 576 223 C 557 193, 520 178, 468 184" fill="none" stroke="#c7961a" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
      <path d="M 655 190 C 697 197, 724 221, 733 259 C 742 296, 735 334, 719 366 C 703 398, 676 423, 635 440 C 665 419, 687 392, 698 360 C 710 327, 713 293, 705 261 C 697 229, 681 206, 655 202" fill="none" stroke="#c7961a" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
      <path d="M 286 258 C 310 248, 334 251, 347 266 C 360 281, 360 304, 350 320 C 339 338, 317 347, 294 346" fill="none" stroke="#e1b23a" stroke-width="1.8" stroke-linecap="round"/>
      <path d="M 372 235 C 401 222, 432 225, 449 247 C 466 270, 467 304, 454 333 C 441 361, 415 378, 385 385" fill="none" stroke="#e1b23a" stroke-width="1.8" stroke-linecap="round"/>
      <path d="M 533 230 C 557 220, 581 223, 595 241 C 610 261, 612 292, 603 320 C 593 349, 574 372, 545 389" fill="none" stroke="#e1b23a" stroke-width="1.8" stroke-linecap="round"/>
      <path d="M 671 240 C 689 244, 700 256, 705 277 C 710 299, 707 322, 698 344 C 689 367, 673 387, 651 401" fill="none" stroke="#e1b23a" stroke-width="1.8" stroke-linecap="round"/>

      <!-- Label: Crête mitochondriale -->
      <line x1="335" y1="395" x2="260" y2="480" stroke="#b8860b" stroke-width="1.5"/>
      <text x="140" y="490" font-size="13" font-weight="700" fill="#b8860b" font-family="system-ui">Crête mitochondriale</text>
    `},
    { id: 'matrice_label', label: 'Matrice', delay: 1200, svgContent: `
      <!-- Matrix label -->
      <text x="490" y="305" text-anchor="middle" font-size="18" font-weight="bold" fill="#7c2d12" font-family="system-ui" opacity="0.9">Matrice</text>
      <!-- Leader line from label to center -->
      <line x1="520" y1="290" x2="580" y2="260" stroke="#7c2d12" stroke-width="1" opacity="0.5"/>
      <!-- Label outside -->
      <line x1="280" y1="310" x2="120" y2="340" stroke="#7c2d12" stroke-width="1.5"/>
      <text x="15" y="335" font-size="13" font-weight="700" fill="#7c2d12" font-family="system-ui">Matrice</text>
    `},
    { id: 'membrane_int_label', label: 'Membrane interne', delay: 1000, svgContent: `
      <!-- Label: Membrane interne -->
      <line x1="230" y1="420" x2="120" y2="470" stroke="#b8860b" stroke-width="1.5"/>
      <text x="15" y="465" font-size="13" font-weight="700" fill="#b8860b" font-family="system-ui">Membrane</text>
      <text x="15" y="481" font-size="13" font-weight="700" fill="#b8860b" font-family="system-ui">interne</text>
    `},
    { id: 'contenu_matrice', label: 'Contenu de la matrice', delay: 1400, svgContent: `
      <!-- ADN mitochondrial (circular) -->
      <circle cx="600" cy="340" r="16" fill="none" stroke="#dc2626" stroke-width="2.5" stroke-dasharray="6,3"/>
      <circle cx="600" cy="340" r="10" fill="none" stroke="#dc2626" stroke-width="1.5" stroke-dasharray="4,2"/>
      <text x="600" y="370" text-anchor="middle" font-size="9" font-weight="600" fill="#dc2626" font-family="system-ui">ADN mt</text>

      <!-- Ribosomes (small dots) -->
      <circle cx="530" cy="370" r="6" fill="#4ade80" stroke="#16a34a" stroke-width="1.5"/>
      <circle cx="548" cy="380" r="5" fill="#4ade80" stroke="#16a34a" stroke-width="1.5"/>
      <circle cx="520" cy="388" r="5.5" fill="#4ade80" stroke="#16a34a" stroke-width="1.5"/>
      <text x="535" y="410" text-anchor="middle" font-size="9" font-weight="600" fill="#16a34a" font-family="system-ui">Ribosomes</text>

      <!-- Enzymes scattered (small shapes) -->
      <circle cx="430" cy="260" r="4" fill="#f59e0b" opacity="0.7"/>
      <circle cx="460" cy="350" r="3.5" fill="#f59e0b" opacity="0.7"/>
      <circle cx="380" cy="330" r="4" fill="#f59e0b" opacity="0.7"/>
      <circle cx="510" cy="270" r="3.5" fill="#f59e0b" opacity="0.7"/>
      <circle cx="550" cy="290" r="3" fill="#f59e0b" opacity="0.7"/>
      <circle cx="650" cy="280" r="3.5" fill="#f59e0b" opacity="0.7"/>
      <text x="670" y="430" font-size="9" fill="#92400e" font-family="system-ui" font-style="italic">Enzymes: cycle de Krebs,</text>
      <text x="670" y="444" font-size="9" fill="#92400e" font-family="system-ui" font-style="italic">pyruvate déshydrogénase</text>
    `},
    { id: 'legende', label: 'Légende', delay: 1700, svgContent: `
      <rect x="700" y="500" width="200" height="105" rx="10" fill="white" stroke="#d4d4d8" stroke-width="1.5" opacity="0.95"/>
      <text x="800" y="522" text-anchor="middle" font-size="12" font-weight="bold" fill="#6b21a8" font-family="system-ui">Fonctions</text>
      <text x="710" y="542" font-size="10" fill="#374151" font-family="system-ui">• Cycle de Krebs (matrice)</text>
      <text x="710" y="558" font-size="10" fill="#374151" font-family="system-ui">• Chaîne resp. (crêtes)</text>
      <text x="710" y="574" font-size="10" fill="#374151" font-family="system-ui">• Phosphorylation oxydative</text>
      <text x="800" y="596" text-anchor="middle" font-size="11" font-weight="bold" fill="#16a34a" font-family="system-ui">→ 36-38 ATP / glucose</text>
    `},
  ],
  annotations: [
    { id: 'a1', x: 175, y: 115, width: 630, height: 395, label: 'Membrane externe', description: 'Lisse, perméable grâce aux porines. Délimite la mitochondrie. Contient des enzymes variées.', color: '#c2710e' },
    { id: 'a2', x: 205, y: 140, width: 570, height: 350, label: 'Membrane interne + crêtes', description: 'Imperméable, repliée en crêtes pour augmenter la surface. Porte les complexes de la chaîne respiratoire (I, II, III, IV) et l\'ATP synthase (V). Les crêtes = + de surface = + d\'ATP.', color: '#b8860b' },
    { id: 'a3', x: 230, y: 155, width: 525, height: 320, label: 'Matrice mitochondriale', description: 'Gel riche en enzymes (cycle de Krebs, β-oxydation), ADN mitochondrial circulaire, ribosomes mitochondriaux, ions Ca²⁺. C\'est le lieu du cycle de Krebs.', color: '#7c2d12' },
    { id: 'a4', x: 185, y: 200, width: 50, height: 200, label: 'Espace intermembranaire', description: 'Espace entre les deux membranes. Riche en H⁺ (protons) grâce au pompage par les complexes respiratoires. Ce gradient de H⁺ est la force proton-motrice.', color: '#0891b2' },
  ],
  highlights: [
    { id: 'h1', cx: 490, cy: 310, radius: 220, label: 'Mitochondrie' },
  ],
};

export const svt_chaine_respiratoire: ScientificSchema = {
  id: 'svt_chaine_respiratoire',
  title: 'Chaîne respiratoire et Phosphorylation oxydative',
  subject: 'svt',
  keywords: ['chaîne respiratoire', 'phosphorylation oxydative', 'atp synthase', 'complexe', 'gradient', 'nadh', 'fadh2', 'السلسلة التنفسية', 'الفسفرة التأكسدية'],
  category: 'process',
  viewBox: '0 0 950 580',
  backgroundColor: '#f0f9ff',
  layers: [
    { id: 'title', label: 'Titre', delay: 0, svgContent: `
      <text x="475" y="35" text-anchor="middle" font-size="22" font-weight="bold" fill="#0f172a" font-family="system-ui">CHAÎNE RESPIRATOIRE — Membrane interne mitochondriale</text>
      <text x="475" y="55" text-anchor="middle" font-size="12" fill="#64748b" font-family="system-ui">Phosphorylation oxydative: NADH/FADH₂ → gradient H⁺ → ATP — الفسفرة التأكسدية</text>
    `},
    { id: 'membrane', label: 'Membrane', delay: 200, svgContent: `
      <rect x="30" y="230" width="890" height="90" rx="6" fill="#fde68a" stroke="#d97706" stroke-width="2.5" opacity="0.6"/>
      <text x="475" y="280" text-anchor="middle" font-size="11" font-weight="600" fill="#92400e" font-family="system-ui">MEMBRANE INTERNE MITOCHONDRIALE</text>
      <text x="80" y="100" font-size="13" font-weight="600" fill="#0891b2" font-family="system-ui">ESPACE INTERMEMBRANAIRE (H⁺ concentré)</text>
      <text x="80" y="380" font-size="13" font-weight="600" fill="#92400e" font-family="system-ui">MATRICE MITOCHONDRIALE</text>
    `},
    { id: 'complexe1', label: 'Complexe I', delay: 400, svgContent: `
      <path d="M 80 235 L 80 195 Q 80 180, 95 180 L 135 180 Q 150 180, 150 195 L 150 235" fill="#ef4444" stroke="#dc2626" stroke-width="2"/>
      <path d="M 80 285 L 80 310 Q 80 325, 95 325 L 135 325 Q 150 325, 150 310 L 150 285" fill="#ef4444" stroke="#dc2626" stroke-width="2"/>
      <text x="115" y="215" text-anchor="middle" font-size="10" font-weight="bold" fill="white" font-family="system-ui">I</text>
      <text x="115" y="310" text-anchor="middle" font-size="9" fill="white" font-family="system-ui">NADH</text>
      <text x="115" y="350" text-anchor="middle" font-size="10" fill="#dc2626" font-family="system-ui">NADH</text>
      <text x="115" y="365" text-anchor="middle" font-size="10" fill="#dc2626" font-family="system-ui">déshydrog.</text>
      <path d="M 115 180 L 115 140" stroke="#0891b2" stroke-width="2" marker-end="url(#arrowCyan)"/>
      <text x="115" y="130" text-anchor="middle" font-size="10" font-weight="bold" fill="#0891b2" font-family="system-ui">H⁺</text>
      <text x="115" y="400" text-anchor="middle" font-size="9" fill="#64748b" font-family="system-ui">NAD⁺ + H⁺</text>
      <path d="M 115 375 L 115 390" stroke="#64748b" stroke-width="1" marker-end="url(#arrowGray)"/>
    `},
    { id: 'complexe2', label: 'Complexe II', delay: 600, svgContent: `
      <path d="M 220 250 L 220 215 Q 220 200, 235 200 L 265 200 Q 280 200, 280 215 L 280 250" fill="#f97316" stroke="#ea580c" stroke-width="2"/>
      <path d="M 220 285 L 220 310 Q 220 325, 235 325 L 265 325 Q 280 325, 280 310 L 280 285" fill="#f97316" stroke="#ea580c" stroke-width="2"/>
      <text x="250" y="232" text-anchor="middle" font-size="10" font-weight="bold" fill="white" font-family="system-ui">II</text>
      <text x="250" y="310" text-anchor="middle" font-size="9" fill="white" font-family="system-ui">FADH₂</text>
      <text x="250" y="350" text-anchor="middle" font-size="10" fill="#ea580c" font-family="system-ui">Succinate</text>
      <text x="250" y="365" text-anchor="middle" font-size="10" fill="#ea580c" font-family="system-ui">déshydrog.</text>
    `},
    { id: 'ubiquinone', label: 'Ubiquinone', delay: 750, svgContent: `
      <circle cx="350" cy="260" r="18" fill="#fbbf24" stroke="#d97706" stroke-width="2"/>
      <text x="350" y="264" text-anchor="middle" font-size="9" font-weight="bold" fill="#92400e" font-family="system-ui">UQ</text>
      <path d="M 150 260 Q 200 245, 332 260" stroke="#fbbf24" stroke-width="2" fill="none" marker-end="url(#arrowOrange)"/>
      <path d="M 280 265 Q 310 262, 332 260" stroke="#fbbf24" stroke-width="2" fill="none"/>
      <text x="350" y="300" text-anchor="middle" font-size="9" fill="#d97706" font-family="system-ui">Coenzyme Q</text>
      <text x="200" y="245" text-anchor="middle" font-size="8" fill="#dc2626" font-family="system-ui">e⁻</text>
    `},
    { id: 'complexe3', label: 'Complexe III', delay: 900, svgContent: `
      <path d="M 430 230 L 430 190 Q 430 175, 445 175 L 495 175 Q 510 175, 510 190 L 510 230" fill="#8b5cf6" stroke="#7c3aed" stroke-width="2"/>
      <path d="M 430 290 L 430 315 Q 430 330, 445 330 L 495 330 Q 510 330, 510 315 L 510 290" fill="#8b5cf6" stroke="#7c3aed" stroke-width="2"/>
      <text x="470" y="215" text-anchor="middle" font-size="10" font-weight="bold" fill="white" font-family="system-ui">III</text>
      <text x="470" y="320" text-anchor="middle" font-size="8" fill="white" font-family="system-ui">Cyt bc₁</text>
      <path d="M 368 260 L 430 260" stroke="#8b5cf6" stroke-width="2" marker-end="url(#arrowPurple)"/>
      <path d="M 470 175 L 470 140" stroke="#0891b2" stroke-width="2" marker-end="url(#arrowCyan)"/>
      <text x="470" y="130" text-anchor="middle" font-size="10" font-weight="bold" fill="#0891b2" font-family="system-ui">H⁺</text>
    `},
    { id: 'cytc', label: 'Cytochrome c', delay: 1050, svgContent: `
      <circle cx="570" cy="240" r="14" fill="#ec4899" stroke="#db2777" stroke-width="2"/>
      <text x="570" y="244" text-anchor="middle" font-size="8" font-weight="bold" fill="white" font-family="system-ui">Cyt c</text>
      <path d="M 510 240 L 556 240" stroke="#ec4899" stroke-width="2" marker-end="url(#arrowRed)"/>
      <text x="540" y="232" font-size="8" fill="#db2777" font-family="system-ui">e⁻</text>
    `},
    { id: 'complexe4', label: 'Complexe IV', delay: 1200, svgContent: `
      <path d="M 620 230 L 620 188 Q 620 172, 636 172 L 684 172 Q 700 172, 700 188 L 700 230" fill="#06b6d4" stroke="#0891b2" stroke-width="2"/>
      <path d="M 620 290 L 620 318 Q 620 333, 636 333 L 684 333 Q 700 333, 700 318 L 700 290" fill="#06b6d4" stroke="#0891b2" stroke-width="2"/>
      <text x="660" y="212" text-anchor="middle" font-size="10" font-weight="bold" fill="white" font-family="system-ui">IV</text>
      <text x="660" y="318" text-anchor="middle" font-size="8" fill="white" font-family="system-ui">Cyt oxyd.</text>
      <path d="M 584 240 L 620 240" stroke="#06b6d4" stroke-width="2" marker-end="url(#arrowCyan)"/>
      <path d="M 660 172 L 660 140" stroke="#0891b2" stroke-width="2" marker-end="url(#arrowCyan)"/>
      <text x="660" y="130" text-anchor="middle" font-size="10" font-weight="bold" fill="#0891b2" font-family="system-ui">H⁺</text>
      <text x="660" y="360" text-anchor="middle" font-size="10" fill="#0891b2" font-family="system-ui">½O₂ + 2H⁺ → H₂O</text>
      <text x="660" y="400" text-anchor="middle" font-size="10" font-weight="bold" fill="#dc2626" font-family="system-ui">O₂ = accepteur final</text>
    `},
    { id: 'atp_synthase', label: 'ATP Synthase', delay: 1500, svgContent: `
      <path d="M 800 175 L 800 230" stroke="#16a34a" stroke-width="3"/>
      <ellipse cx="800" cy="165" rx="30" ry="18" fill="#bbf7d0" stroke="#16a34a" stroke-width="2.5"/>
      <text x="800" y="170" text-anchor="middle" font-size="9" font-weight="bold" fill="#166534" font-family="system-ui">F₀</text>
      <path d="M 800 290 L 800 330" stroke="#16a34a" stroke-width="3"/>
      <ellipse cx="800" cy="345" rx="35" ry="22" fill="#bbf7d0" stroke="#16a34a" stroke-width="2.5"/>
      <text x="800" y="350" text-anchor="middle" font-size="10" font-weight="bold" fill="#166534" font-family="system-ui">F₁</text>
      <path d="M 800 175 Q 825 140, 820 120" stroke="#0891b2" stroke-width="2" fill="none"/>
      <text x="838" y="140" font-size="10" font-weight="bold" fill="#0891b2" font-family="system-ui">H⁺</text>
      <text x="800" y="420" text-anchor="middle" font-size="12" font-weight="bold" fill="#16a34a" font-family="system-ui">ADP + Pi → ATP</text>
      <text x="800" y="440" text-anchor="middle" font-size="10" fill="#16a34a" font-family="system-ui">ATP SYNTHASE</text>
      <text x="800" y="455" text-anchor="middle" font-size="9" fill="#16a34a" font-family="system-ui">(Complexe V)</text>
    `},
    { id: 'bilan', label: 'Bilan', delay: 1800, svgContent: `
      <rect x="200" y="480" width="550" height="60" rx="12" fill="#ecfdf5" stroke="#059669" stroke-width="2"/>
      <text x="475" y="505" text-anchor="middle" font-size="14" font-weight="bold" fill="#065f46" font-family="system-ui">BILAN: NADH → 3 ATP | FADH₂ → 2 ATP | Total ≈ 32-34 ATP</text>
      <text x="475" y="528" text-anchor="middle" font-size="11" fill="#059669" font-family="system-ui">Gradient chimiosmotique de H⁺ (force proton-motrice) → rotation ATP synthase</text>
    `},
  ],
  annotations: [
    { id: 'a1', x: 70, y: 170, width: 90, height: 170, label: 'Complexe I', description: 'NADH déshydrogénase. Oxyde NADH, transfère 2e⁻ à l\'ubiquinone, pompe 4 H⁺ vers l\'espace intermembranaire.', color: '#ef4444' },
    { id: 'a2', x: 215, y: 195, width: 70, height: 140, label: 'Complexe II', description: 'Succinate déshydrogénase. Oxyde FADH₂, transfère e⁻ à l\'ubiquinone. Ne pompe PAS de H⁺.', color: '#f97316' },
    { id: 'a3', x: 425, y: 170, width: 90, height: 170, label: 'Complexe III', description: 'Cytochrome bc₁. Transfère e⁻ de l\'ubiquinone au cytochrome c. Pompe 4 H⁺.', color: '#8b5cf6' },
    { id: 'a4', x: 615, y: 165, width: 90, height: 175, label: 'Complexe IV', description: 'Cytochrome c oxydase. Transfère e⁻ à O₂ (accepteur final) → H₂O. Pompe 2 H⁺.', color: '#06b6d4' },
    { id: 'a5', x: 765, y: 155, width: 70, height: 220, label: 'ATP Synthase', description: 'Complexe V (F₀F₁). Le flux de H⁺ fait tourner F₀ → changement conformationnel de F₁ → ADP + Pi → ATP.', color: '#16a34a' },
  ],
  highlights: [
    { id: 'h1', cx: 115, cy: 260, radius: 60, label: 'Complexe I' },
    { id: 'h2', cx: 800, cy: 280, radius: 80, label: 'ATP Synthase' },
  ],
};

export const svt_cycle_krebs: ScientificSchema = {
  id: 'svt_cycle_krebs',
  title: 'Cycle de Krebs — Détail des réactions',
  subject: 'svt',
  keywords: ['krebs', 'cycle', 'acétyl-coa', 'citrate', 'oxaloacétate', 'matrice', 'حلقة كريبس', 'دورة كريبس'],
  category: 'cycle',
  viewBox: '0 0 850 620',
  backgroundColor: '#f0fdf4',
  layers: [
    { id: 'title', label: 'Titre', delay: 0, svgContent: `
      <text x="425" y="35" text-anchor="middle" font-size="22" font-weight="bold" fill="#0f172a" font-family="system-ui">CYCLE DE KREBS (Cycle de l'acide citrique)</text>
      <text x="425" y="55" text-anchor="middle" font-size="12" fill="#64748b" font-family="system-ui">Dans la matrice mitochondriale — 2 tours par glucose — حلقة كريبس</text>
    `},
    { id: 'entree', label: 'Entrée pyruvate', delay: 300, svgContent: `
      <rect x="310" y="70" width="160" height="35" rx="10" fill="url(#grad_orange)" stroke="#ea580c" stroke-width="2"/>
      <text x="390" y="93" text-anchor="middle" font-size="13" font-weight="bold" fill="white" font-family="system-ui">Pyruvate (C₃)</text>
      <line x1="390" y1="105" x2="390" y2="135" stroke="#ea580c" stroke-width="2" marker-end="url(#arrowOrange)"/>
      <text x="475" y="125" font-size="10" fill="#dc2626" font-family="system-ui">CO₂ ↑ + NADH</text>
      <rect x="320" y="140" width="140" height="35" rx="10" fill="url(#grad_green)" stroke="#16a34a" stroke-width="2"/>
      <text x="390" y="163" text-anchor="middle" font-size="13" font-weight="bold" fill="white" font-family="system-ui">Acétyl-CoA (C₂)</text>
      <line x1="390" y1="175" x2="390" y2="205" stroke="#16a34a" stroke-width="2" marker-end="url(#arrowGreen)"/>
    `},
    { id: 'cycle_circle', label: 'Cercle du cycle', delay: 500, svgContent: `
      <circle cx="390" cy="370" r="155" fill="none" stroke="#16a34a" stroke-width="3" stroke-dasharray="12,6" opacity="0.4"/>
      <text x="390" y="365" text-anchor="middle" font-size="15" font-weight="bold" fill="#14532d" font-family="system-ui" opacity="0.3">CYCLE DE</text>
      <text x="390" y="385" text-anchor="middle" font-size="15" font-weight="bold" fill="#14532d" font-family="system-ui" opacity="0.3">KREBS</text>
    `},
    { id: 'molecules', label: 'Molécules', delay: 800, svgContent: `
      <ellipse cx="390" cy="215" rx="65" ry="22" fill="#bbf7d0" stroke="#16a34a" stroke-width="2"/>
      <text x="390" y="220" text-anchor="middle" font-size="12" font-weight="bold" fill="#166534" font-family="system-ui">Citrate (C₆)</text>
      <ellipse cx="560" cy="280" rx="68" ry="22" fill="#dbeafe" stroke="#2563eb" stroke-width="2"/>
      <text x="560" y="285" text-anchor="middle" font-size="11" font-weight="bold" fill="#1e40af" font-family="system-ui">Isocitrate (C₆)</text>
      <ellipse cx="580" cy="370" rx="75" ry="22" fill="#fef3c7" stroke="#d97706" stroke-width="2"/>
      <text x="580" y="375" text-anchor="middle" font-size="11" font-weight="bold" fill="#92400e" font-family="system-ui">α-Cétoglutarate (C₅)</text>
      <ellipse cx="540" cy="460" rx="65" ry="22" fill="#fce7f3" stroke="#db2777" stroke-width="2"/>
      <text x="540" y="465" text-anchor="middle" font-size="11" font-weight="bold" fill="#9d174d" font-family="system-ui">Succinyl-CoA (C₄)</text>
      <ellipse cx="390" cy="525" rx="60" ry="22" fill="#e0e7ff" stroke="#4f46e5" stroke-width="2"/>
      <text x="390" y="530" text-anchor="middle" font-size="11" font-weight="bold" fill="#3730a3" font-family="system-ui">Succinate (C₄)</text>
      <ellipse cx="235" cy="460" rx="60" ry="22" fill="#ccfbf1" stroke="#0d9488" stroke-width="2"/>
      <text x="235" y="465" text-anchor="middle" font-size="11" font-weight="bold" fill="#115e59" font-family="system-ui">Fumarate (C₄)</text>
      <ellipse cx="215" cy="370" rx="55" ry="22" fill="#fef2f2" stroke="#dc2626" stroke-width="2"/>
      <text x="215" y="375" text-anchor="middle" font-size="11" font-weight="bold" fill="#991b1b" font-family="system-ui">Malate (C₄)</text>
      <ellipse cx="255" cy="275" rx="70" ry="22" fill="#fefce8" stroke="#ca8a04" stroke-width="2"/>
      <text x="255" y="280" text-anchor="middle" font-size="11" font-weight="bold" fill="#854d0e" font-family="system-ui">Oxaloacétate (C₄)</text>
    `},
    { id: 'arrows_products', label: 'Flèches et produits', delay: 1200, svgContent: `
      <path d="M 450 225 Q 510 240, 500 268" stroke="#16a34a" stroke-width="2" fill="none" marker-end="url(#arrowGreen)"/>
      <path d="M 585 302 Q 590 330, 585 348" stroke="#d97706" stroke-width="2" fill="none" marker-end="url(#arrowOrange)"/>
      <text x="650" y="325" font-size="9" fill="#dc2626" font-family="system-ui">CO₂ + NADH</text>
      <path d="M 575 392 Q 565 420, 555 438" stroke="#db2777" stroke-width="2" fill="none" marker-end="url(#arrowRed)"/>
      <text x="650" y="415" font-size="9" fill="#dc2626" font-family="system-ui">CO₂ + NADH</text>
      <path d="M 485 470 Q 440 500, 420 515" stroke="#4f46e5" stroke-width="2" fill="none" marker-end="url(#arrowPurple)"/>
      <text x="480" y="510" font-size="9" fill="#16a34a" font-family="system-ui">GTP (=ATP)</text>
      <path d="M 335 530 Q 290 520, 270 480" stroke="#0d9488" stroke-width="2" fill="none" marker-end="url(#arrowCyan)"/>
      <text x="290" y="530" font-size="9" fill="#7c3aed" font-family="system-ui">FADH₂</text>
      <path d="M 230 438 Q 225 410, 220 392" stroke="#dc2626" stroke-width="2" fill="none" marker-end="url(#arrowRed)"/>
      <path d="M 220 348 Q 235 315, 260 297" stroke="#ca8a04" stroke-width="2" fill="none" marker-end="url(#arrowOrange)"/>
      <text x="150" y="340" font-size="9" fill="#0891b2" font-family="system-ui">NADH</text>
      <path d="M 310 265 Q 350 235, 355 218" stroke="#16a34a" stroke-width="2" fill="none" marker-end="url(#arrowGreen)"/>
    `},
    { id: 'bilan', label: 'Bilan', delay: 1600, svgContent: `
      <rect x="660" y="80" width="170" height="160" rx="12" fill="#ecfdf5" stroke="#059669" stroke-width="2"/>
      <text x="745" y="105" text-anchor="middle" font-size="13" font-weight="bold" fill="#065f46" font-family="system-ui">BILAN (×2 tours)</text>
      <text x="745" y="128" text-anchor="middle" font-size="11" fill="#dc2626" font-family="system-ui">→ 4 CO₂</text>
      <text x="745" y="148" text-anchor="middle" font-size="11" fill="#0891b2" font-family="system-ui">→ 6 NADH,H⁺</text>
      <text x="745" y="168" text-anchor="middle" font-size="11" fill="#7c3aed" font-family="system-ui">→ 2 FADH₂</text>
      <text x="745" y="188" text-anchor="middle" font-size="11" fill="#16a34a" font-family="system-ui">→ 2 GTP (=2 ATP)</text>
      <text x="745" y="220" text-anchor="middle" font-size="10" fill="#64748b" font-family="system-ui">+1 NADH décarboxylation</text>
      <text x="745" y="235" text-anchor="middle" font-size="10" fill="#64748b" font-family="system-ui">pyruvate → acétyl-CoA</text>
    `},
  ],
  annotations: [
    { id: 'a1', x: 310, y: 70, width: 160, height: 110, label: 'Entrée', description: 'Le pyruvate (C₃) perd un CO₂ et se lie au CoA → Acétyl-CoA (C₂). Produit 1 NADH par tour.', color: '#ea580c' },
    { id: 'a2', x: 325, y: 193, width: 130, height: 50, label: 'Citrate', description: 'L\'acétyl-CoA (C₂) + oxaloacétate (C₄) → citrate (C₆). Première réaction du cycle.', color: '#16a34a' },
    { id: 'a3', x: 660, y: 80, width: 170, height: 160, label: 'Bilan', description: 'Par glucose (2 tours): 6 NADH, 2 FADH₂, 2 ATP, 4 CO₂. Les coenzymes réduits iront à la chaîne respiratoire.', color: '#059669' },
  ],
  highlights: [
    { id: 'h1', cx: 390, cy: 370, radius: 170, label: 'Cycle' },
  ],
};

const svt_fibre_musculaire: ScientificSchema = {
  id: 'svt_fibre_musculaire',
  title: 'Ultrastructure de la fibre musculaire striée',
  subject: 'svt',
  keywords: ['fibre musculaire', 'myofibrille', 'réticulum sarcoplasmique', 'tubule t', 'triade', 'ultrastructure', 'الألياف العضلية', 'بنية العضلة'],
  category: 'structure',
  viewBox: '0 0 900 560',
  backgroundColor: '#fef2f2',
  layers: [
    { id: 'title', label: 'Titre', delay: 0, svgContent: `
      <text x="450" y="35" text-anchor="middle" font-size="22" font-weight="bold" fill="#0f172a" font-family="system-ui">ULTRASTRUCTURE DE LA FIBRE MUSCULAIRE STRIÉE</text>
      <text x="450" y="55" text-anchor="middle" font-size="12" fill="#64748b" font-family="system-ui">Du muscle au sarcomère — بنية الليف العضلي المخطط</text>
    `},
    { id: 'muscle', label: 'Muscle entier', delay: 200, svgContent: `
      <path d="M 30 110 Q 50 85, 100 90 Q 180 95, 200 120 Q 210 135, 200 150 Q 180 175, 100 180 Q 50 185, 30 160 Q 20 135, 30 110 Z" fill="#fca5a5" stroke="#dc2626" stroke-width="2"/>
      <path d="M 200 120 Q 220 110, 240 115 L 260 130 Q 250 145, 230 145 L 200 150" fill="#fca5a5" stroke="#dc2626" stroke-width="1.5"/>
      <path d="M 30 135 Q 10 125, 0 115" stroke="#dc2626" stroke-width="2"/>
      <path d="M 30 135 Q 10 145, 0 155" stroke="#dc2626" stroke-width="2"/>
      <text x="115" y="142" text-anchor="middle" font-size="11" font-weight="bold" fill="#991b1b" font-family="system-ui">Muscle</text>
      <text x="115" y="200" text-anchor="middle" font-size="10" fill="#dc2626" font-family="system-ui">العضلة</text>
    `},
    { id: 'faisceau', label: 'Faisceau', delay: 400, svgContent: `
      <path d="M 280 95 Q 290 85, 320 88 L 440 88 Q 470 88, 480 95 L 480 175 Q 470 182, 440 182 L 320 182 Q 290 182, 280 175 Z" fill="#fecaca" stroke="#ef4444" stroke-width="2"/>
      <line x1="300" y1="105" x2="460" y2="105" stroke="#ef4444" stroke-width="1" opacity="0.5"/>
      <line x1="300" y1="120" x2="460" y2="120" stroke="#ef4444" stroke-width="1" opacity="0.5"/>
      <line x1="300" y1="135" x2="460" y2="135" stroke="#ef4444" stroke-width="1" opacity="0.5"/>
      <line x1="300" y1="150" x2="460" y2="150" stroke="#ef4444" stroke-width="1" opacity="0.5"/>
      <line x1="300" y1="165" x2="460" y2="165" stroke="#ef4444" stroke-width="1" opacity="0.5"/>
      <text x="380" y="140" text-anchor="middle" font-size="10" font-weight="600" fill="#991b1b" font-family="system-ui">Faisceau</text>
      <text x="380" y="200" text-anchor="middle" font-size="10" fill="#ef4444" font-family="system-ui">حزمة عضلية</text>
      <path d="M 200 135 L 280 135" stroke="#dc2626" stroke-width="1.5" stroke-dasharray="4,3" marker-end="url(#arrowRed)"/>
    `},
    { id: 'fibre', label: 'Fibre musculaire', delay: 600, svgContent: `
      <rect x="520" y="80" width="350" height="130" rx="12" fill="#fee2e2" stroke="#ef4444" stroke-width="2"/>
      <text x="695" y="100" text-anchor="middle" font-size="11" font-weight="bold" fill="#991b1b" font-family="system-ui">FIBRE MUSCULAIRE (= 1 cellule)</text>
      <ellipse cx="545" cy="135" rx="8" ry="12" fill="#7c3aed" stroke="#6d28d9" stroke-width="1.5"/>
      <text x="545" y="165" text-anchor="middle" font-size="7" fill="#7c3aed" font-family="system-ui">Noyaux</text>
      <ellipse cx="565" cy="130" rx="8" ry="12" fill="#7c3aed" stroke="#6d28d9" stroke-width="1.5"/>
      <rect x="590" y="115" width="260" height="40" rx="4" fill="#fecdd3" stroke="#f43f5e" stroke-width="1.5"/>
      <text x="720" y="140" text-anchor="middle" font-size="10" font-weight="600" fill="#be123c" font-family="system-ui">Myofibrilles (filaments contractiles)</text>
      <text x="695" y="185" text-anchor="middle" font-size="9" fill="#ef4444" font-family="system-ui">Sarcolemme (membrane) | Sarcoplasme (cytoplasme)</text>
      <path d="M 480 135 L 520 135" stroke="#ef4444" stroke-width="1.5" stroke-dasharray="4,3" marker-end="url(#arrowRed)"/>
    `},
    { id: 'detail', label: 'Détail ultrastructure', delay: 900, svgContent: `
      <rect x="60" y="245" width="780" height="230" rx="14" fill="#fff1f2" stroke="#fb7185" stroke-width="2"/>
      <text x="450" y="270" text-anchor="middle" font-size="13" font-weight="bold" fill="#881337" font-family="system-ui">DÉTAIL — ULTRASTRUCTURE</text>
      <line x1="130" y1="310" x2="130" y2="440" stroke="#1e40af" stroke-width="3"/>
      <line x1="450" y1="310" x2="450" y2="440" stroke="#1e40af" stroke-width="3"/>
      <line x1="770" y1="310" x2="770" y2="440" stroke="#1e40af" stroke-width="3"/>
      <text x="130" y="305" text-anchor="middle" font-size="9" font-weight="bold" fill="#1e40af" font-family="system-ui">Z</text>
      <text x="450" y="305" text-anchor="middle" font-size="9" font-weight="bold" fill="#1e40af" font-family="system-ui">Z</text>
      <text x="770" y="305" text-anchor="middle" font-size="9" font-weight="bold" fill="#1e40af" font-family="system-ui">Z</text>
      <line x1="150" y1="340" x2="370" y2="340" stroke="#ef4444" stroke-width="3" stroke-linecap="round"/>
      <line x1="150" y1="370" x2="370" y2="370" stroke="#ef4444" stroke-width="3" stroke-linecap="round"/>
      <line x1="150" y1="400" x2="370" y2="400" stroke="#ef4444" stroke-width="3" stroke-linecap="round"/>
      <line x1="220" y1="335" x2="380" y2="335" stroke="#2563eb" stroke-width="5" stroke-linecap="round"/>
      <line x1="220" y1="365" x2="380" y2="365" stroke="#2563eb" stroke-width="5" stroke-linecap="round"/>
      <line x1="220" y1="395" x2="380" y2="395" stroke="#2563eb" stroke-width="5" stroke-linecap="round"/>
      <line x1="470" y1="340" x2="690" y2="340" stroke="#ef4444" stroke-width="3" stroke-linecap="round"/>
      <line x1="470" y1="370" x2="690" y2="370" stroke="#ef4444" stroke-width="3" stroke-linecap="round"/>
      <line x1="470" y1="400" x2="690" y2="400" stroke="#ef4444" stroke-width="3" stroke-linecap="round"/>
      <line x1="530" y1="335" x2="700" y2="335" stroke="#2563eb" stroke-width="5" stroke-linecap="round"/>
      <line x1="530" y1="365" x2="700" y2="365" stroke="#2563eb" stroke-width="5" stroke-linecap="round"/>
      <line x1="530" y1="395" x2="700" y2="395" stroke="#2563eb" stroke-width="5" stroke-linecap="round"/>
      <rect x="785" y="330" width="40" height="18" rx="4" fill="#fef2f2" stroke="#ef4444" stroke-width="1"/>
      <text x="805" y="343" text-anchor="middle" font-size="8" fill="#dc2626" font-family="system-ui">Actine</text>
      <rect x="785" y="360" width="45" height="18" rx="4" fill="#eff6ff" stroke="#2563eb" stroke-width="1"/>
      <text x="808" y="373" text-anchor="middle" font-size="8" fill="#1d4ed8" font-family="system-ui">Myosine</text>
      <text x="290" y="455" text-anchor="middle" font-size="10" font-weight="600" fill="#374151" font-family="system-ui">1 Sarcomère</text>
      <line x1="130" y1="445" x2="450" y2="445" stroke="#64748b" stroke-width="1.5" marker-start="url(#arrowGray)" marker-end="url(#arrowGray)"/>
    `},
    { id: 'organites', label: 'Organites', delay: 1300, svgContent: `
      <ellipse cx="180" cy="425" rx="22" ry="12" fill="#fef3c7" stroke="#d97706" stroke-width="1.5"/>
      <path d="M 165 425 Q 170 418, 180 425 Q 190 432, 195 425" fill="none" stroke="#d97706" stroke-width="1"/>
      <text x="180" y="450" text-anchor="middle" font-size="7" fill="#d97706" font-family="system-ui">Mitochondrie</text>
      <rect x="80" y="285" width="15" height="150" rx="3" fill="#a5b4fc" stroke="#6366f1" stroke-width="1" opacity="0.6"/>
      <text x="70" y="360" text-anchor="middle" font-size="7" fill="#6366f1" font-family="system-ui" transform="rotate(-90,70,360)">Rét. sarcoplasmique</text>
      <line x1="108" y1="370" x2="120" y2="370" stroke="#0891b2" stroke-width="2"/>
      <text x="105" y="385" text-anchor="middle" font-size="7" fill="#0891b2" font-family="system-ui">Tubule T</text>
    `},
    { id: 'note', label: 'Note énergie', delay: 1600, svgContent: `
      <rect x="140" y="495" width="620" height="45" rx="10" fill="#ecfdf5" stroke="#059669" stroke-width="2"/>
      <text x="450" y="515" text-anchor="middle" font-size="12" font-weight="bold" fill="#065f46" font-family="system-ui">Contraction = ATP (mitochondries) + Ca²⁺ (réticulum sarcoplasmique)</text>
      <text x="450" y="532" text-anchor="middle" font-size="10" fill="#059669" font-family="system-ui">Tubules T propagent l'influx → libération Ca²⁺ → ponts actine-myosine</text>
    `},
  ],
  annotations: [
    { id: 'a1', x: 30, y: 75, width: 230, height: 130, label: 'Muscle → Faisceau', description: 'Le muscle est composé de faisceaux de fibres musculaires, entourés de tissu conjonctif (périmysium).', color: '#dc2626' },
    { id: 'a2', x: 520, y: 75, width: 350, height: 140, label: 'Fibre musculaire', description: 'Cellule géante multinucléée. Contient des myofibrilles (unités contractiles), des mitochondries (énergie) et un réticulum sarcoplasmique (Ca²⁺).', color: '#ef4444' },
    { id: 'a3', x: 130, y: 295, width: 320, height: 155, label: 'Sarcomère', description: 'Unité fonctionnelle: entre 2 lignes Z. Actine (fins, rouges) et myosine (épais, bleus). Contraction = glissement.', color: '#1e40af' },
  ],
  highlights: [
    { id: 'h1', cx: 450, cy: 375, radius: 160, label: 'Sarcomère' },
  ],
};

export const svt_bilan_energetique: ScientificSchema = {
  id: 'svt_bilan_energetique',
  title: 'Bilan énergétique — Respiration vs Fermentation',
  subject: 'svt',
  keywords: ['bilan', 'énergétique', 'rendement', 'comparaison', 'respiration', 'fermentation', 'atp', 'حصيلة طاقية', 'مقارنة'],
  category: 'comparison',
  viewBox: '0 0 900 560',
  backgroundColor: '#f8fafc',
  layers: [
    { id: 'title', label: 'Titre', delay: 0, svgContent: `
      <text x="450" y="35" text-anchor="middle" font-size="22" font-weight="bold" fill="#0f172a" font-family="system-ui">BILAN ÉNERGÉTIQUE COMPARÉ</text>
      <text x="450" y="55" text-anchor="middle" font-size="12" fill="#64748b" font-family="system-ui">Respiration aérobie vs Fermentation — مقارنة الحصيلة الطاقية</text>
    `},
    { id: 'glucose_commun', label: 'Glucose commun', delay: 200, svgContent: `
      <rect x="335" y="75" width="230" height="45" rx="14" fill="url(#grad_blue)" stroke="#2563eb" stroke-width="2"/>
      <text x="450" y="103" text-anchor="middle" font-size="16" font-weight="bold" fill="white" font-family="system-ui">1 Glucose C₆H₁₂O₆</text>
      <line x1="450" y1="120" x2="450" y2="155" stroke="#2563eb" stroke-width="2.5" marker-end="url(#arrowBlue)"/>
      <rect x="350" y="160" width="200" height="38" rx="10" fill="#dbeafe" stroke="#2563eb" stroke-width="2"/>
      <text x="450" y="184" text-anchor="middle" font-size="14" font-weight="bold" fill="#1e40af" font-family="system-ui">GLYCOLYSE → 2 ATP</text>
      <text x="450" y="215" text-anchor="middle" font-size="11" fill="#64748b" font-family="system-ui">(étape commune, cytoplasme)</text>
    `},
    { id: 'branche_resp', label: 'Respiration', delay: 500, svgContent: `
      <line x1="380" y1="198" x2="200" y2="260" stroke="#16a34a" stroke-width="2.5" marker-end="url(#arrowGreen)"/>
      <text x="260" y="245" font-size="10" font-weight="600" fill="#16a34a" font-family="system-ui">Avec O₂</text>
      <rect x="50" y="270" width="300" height="240" rx="16" fill="#ecfdf5" stroke="#059669" stroke-width="2.5"/>
      <text x="200" y="298" text-anchor="middle" font-size="16" font-weight="bold" fill="#065f46" font-family="system-ui">RESPIRATION AÉROBIE</text>
      <text x="200" y="318" text-anchor="middle" font-size="11" fill="#059669" font-family="system-ui">التنفس الهوائي</text>
      <ellipse cx="200" cy="350" rx="90" ry="18" fill="#fef3c7" stroke="#d97706" stroke-width="1.5"/>
      <text x="200" y="355" text-anchor="middle" font-size="10" font-weight="600" fill="#92400e" font-family="system-ui">Mitochondrie</text>
      <text x="200" y="385" text-anchor="middle" font-size="11" fill="#374151" font-family="system-ui">Cycle de Krebs → 2 ATP</text>
      <text x="200" y="405" text-anchor="middle" font-size="11" fill="#374151" font-family="system-ui">Chaîne resp. → 32-34 ATP</text>
      <line x1="80" y1="425" x2="320" y2="425" stroke="#059669" stroke-width="1" stroke-dasharray="4,3"/>
      <text x="200" y="450" text-anchor="middle" font-size="18" font-weight="bold" fill="#16a34a" font-family="system-ui">TOTAL: 36-38 ATP</text>
      <text x="200" y="475" text-anchor="middle" font-size="11" fill="#065f46" font-family="system-ui">Rendement ≈ 40%</text>
      <text x="200" y="500" text-anchor="middle" font-size="10" fill="#dc2626" font-family="system-ui">Déchets: CO₂ + H₂O</text>
    `},
    { id: 'branche_ferm', label: 'Fermentation', delay: 500, svgContent: `
      <line x1="520" y1="198" x2="700" y2="260" stroke="#dc2626" stroke-width="2.5" marker-end="url(#arrowRed)"/>
      <text x="640" y="245" font-size="10" font-weight="600" fill="#dc2626" font-family="system-ui">Sans O₂</text>
      <rect x="550" y="270" width="300" height="240" rx="16" fill="#fef2f2" stroke="#dc2626" stroke-width="2.5"/>
      <text x="700" y="298" text-anchor="middle" font-size="16" font-weight="bold" fill="#991b1b" font-family="system-ui">FERMENTATION</text>
      <text x="700" y="318" text-anchor="middle" font-size="11" fill="#dc2626" font-family="system-ui">التخمر (لاهوائي)</text>
      <text x="700" y="350" text-anchor="middle" font-size="11" fill="#374151" font-family="system-ui">Cytoplasme uniquement</text>
      <text x="700" y="370" text-anchor="middle" font-size="11" fill="#374151" font-family="system-ui">(pas de mitochondrie)</text>
      <text x="700" y="400" text-anchor="middle" font-size="11" fill="#374151" font-family="system-ui">Lactique: → Acide lactique</text>
      <text x="700" y="420" text-anchor="middle" font-size="11" fill="#374151" font-family="system-ui">Alcoolique: → Éthanol + CO₂</text>
      <line x1="580" y1="435" x2="820" y2="435" stroke="#dc2626" stroke-width="1" stroke-dasharray="4,3"/>
      <text x="700" y="460" text-anchor="middle" font-size="18" font-weight="bold" fill="#dc2626" font-family="system-ui">TOTAL: 2 ATP</text>
      <text x="700" y="480" text-anchor="middle" font-size="11" fill="#991b1b" font-family="system-ui">Rendement ≈ 2%</text>
      <text x="700" y="500" text-anchor="middle" font-size="10" fill="#ea580c" font-family="system-ui">Molécule organique résiduelle</text>
    `},
    { id: 'comparaison', label: 'Comparaison', delay: 900, svgContent: `
      <rect x="150" y="525" width="600" height="30" rx="8" fill="#fefce8" stroke="#ca8a04" stroke-width="2"/>
      <text x="450" y="545" text-anchor="middle" font-size="13" font-weight="bold" fill="#854d0e" font-family="system-ui">Respiration = 18× plus efficace que la fermentation (36 vs 2 ATP)</text>
    `},
  ],
  annotations: [
    { id: 'a1', x: 50, y: 270, width: 300, height: 240, label: 'Respiration', description: 'Dégradation complète du glucose en présence d\'O₂. Glycolyse + Krebs + chaîne respiratoire = 36-38 ATP. Rendement ≈ 40%.', color: '#16a34a' },
    { id: 'a2', x: 550, y: 270, width: 300, height: 240, label: 'Fermentation', description: 'Dégradation incomplète sans O₂. Glycolyse seule = 2 ATP. La molécule organique produite (lactate/éthanol) contient encore de l\'énergie.', color: '#dc2626' },
  ],
  highlights: [
    { id: 'h1', cx: 200, cy: 450, radius: 50, label: '36-38 ATP' },
    { id: 'h2', cx: 700, cy: 460, radius: 50, label: '2 ATP' },
  ],
};

void [svt_muscle_sarcomere, svt_adn_structure, svt_mitochondrie_structure, svt_fibre_musculaire];

export const SVT_SCHEMAS = [
  svt_glycolyse,
  svt_respiration_cellulaire,
  svt_fermentation,
  svt_transcription_traduction,
  svt_mitose,
  svt_subduction,
  svt_chaine_respiratoire,
  svt_cycle_krebs,
  svt_bilan_energetique,
];
