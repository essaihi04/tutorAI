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

export const svt_muscle_sarcomere: ScientificSchema = {
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

export const svt_adn_structure: ScientificSchema = {
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

/**
 * Subduction — le plongement se VOIT, il ne se devine pas.
 *
 * L'ancienne version représentait la plaque plongeante par une ligne
 * pointillée : rien n'y descendait, et la fusion partielle flottait au milieu
 * du dessin sans relier le slab aux volcans. Ici la plaque est une BANDE
 * épaisse qui s'incurve, l'eau qu'elle libère remonte dans le coin de manteau,
 * la zone de fusion s'y trouve, et le magma monte jusqu'à l'arc volcanique :
 * la chaîne de causes se suit du doigt, de gauche à droite.
 *
 * Les pastilles de métamorphisme reprennent les couleurs de
 * `svt_metamorphisme` — un élève qui a vu l'un reconnaît l'autre.
 */
export const svt_subduction: ScientificSchema = {
  id: 'svt_subduction',
  title: 'Subduction — Plongement d\'une plaque océanique',
  subject: 'svt',
  keywords: ['subduction', 'plaque plongeante', 'plaque océanique', 'fosse', 'volcanisme',
    'arc volcanique', 'fusion partielle', 'déshydratation', 'métamorphisme', 'الغوص', 'صفيحة'],
  category: 'process',
  viewBox: '0 0 920 620',
  backgroundColor: '#f8fafc',
  layers: [
    { id: 'title', label: 'Titre', delay: 0, svgContent: `
      <text x="460" y="34" text-anchor="middle" font-size="27" font-weight="bold" fill="#0f172a" font-family="system-ui">La zone de subduction</text>
      <text x="460" y="60" text-anchor="middle" font-size="15" fill="#475569" font-family="system-ui">الغوص — انغراز صفيحة محيطية تحت صفيحة أخرى</text>
    `},
    { id: 'asthenosphere', label: 'Asthénosphère', delay: 300, svgContent: `
      <rect x="24" y="188" width="872" height="316" fill="#fed7aa" stroke="#ea580c" stroke-width="1.5"/>
      <text x="250" y="470" font-size="15" font-weight="700" fill="#7c2d12" font-family="system-ui">Asthénosphère — manteau ductile</text>
    `},
    { id: 'ocean', label: 'Océan', delay: 500, svgContent: `
      <path d="M 24 96 L 404 96 L 404 150 L 24 150 Z" fill="#dbeafe" stroke="#93c5fd" stroke-width="1.5"/>
      <text x="130" y="128" font-size="15" font-weight="700" fill="#1d4ed8" font-family="system-ui">Océan — المحيط</text>
    `},
    { id: 'plaque_oceanique', label: 'Plaque plongeante', delay: 800, svgContent: `
      <path d="M 24 150 L 396 150 Q 520 196 596 300 Q 648 372 672 452
               L 616 470 Q 592 392 546 326 Q 476 228 366 196 L 24 196 Z"
            fill="#475569" stroke="#0f172a" stroke-width="2"/>
      <text x="120" y="178" font-size="14" font-weight="700" fill="#f8fafc" font-family="system-ui">Lithosphère océanique</text>
      <!-- Le nom se lit SUR la bande, pas au-dela : il en sortait par le bas. -->
      <text x="548" y="318" font-size="15" font-weight="800" fill="#f8fafc" font-family="system-ui" transform="rotate(57 548 318)">plaque plongeante</text>
    `},
    { id: 'fosse', label: 'Fosse océanique', delay: 1000, svgContent: `
      <path d="M 372 150 L 404 150 L 396 176 Z" fill="#1e293b"/>
      <line x1="388" y1="150" x2="322" y2="112" stroke="#b91c1c" stroke-width="1.8"/>
      <text x="316" y="106" text-anchor="end" font-size="15" font-weight="800" fill="#b91c1c" font-family="system-ui">Fosse océanique</text>
      <text x="316" y="126" text-anchor="end" font-size="13" fill="#b91c1c" font-family="system-ui">الخندق المحيطي</text>
    `},
    { id: 'continent', label: 'Plaque chevauchante', delay: 1200, svgContent: `
      <!-- Teinte plus soutenue que l'asthenosphere : sinon les deux se
           confondent et la plaque chevauchante disparait du dessin. -->
      <path d="M 404 150 L 896 150 L 896 250 L 500 250 Q 440 210 404 150 Z"
            fill="#e2b183" stroke="#7c2d12" stroke-width="2.5"/>
      <text x="700" y="212" text-anchor="middle" font-size="15" font-weight="700" fill="#7c2d12" font-family="system-ui">Plaque continentale chevauchante</text>
    `},
    { id: 'metamorphisme', label: 'Métamorphisme', delay: 1400, svgContent: `
      <circle cx="466" cy="204" r="11" fill="#86efac" stroke="#16a34a" stroke-width="2"/>
      <circle cx="540" cy="272" r="11" fill="#93c5fd" stroke="#2563eb" stroke-width="2"/>
      <circle cx="606" cy="368" r="11" fill="#fca5a5" stroke="#dc2626" stroke-width="2"/>
      <text x="60" y="252" font-size="15" font-weight="800" fill="#0f172a" font-family="system-ui">Le long du plongement</text>
      <circle cx="70" cy="272" r="9" fill="#86efac" stroke="#16a34a" stroke-width="2"/>
      <text x="88" y="277" font-size="13" fill="#334155" font-family="system-ui">schistes verts</text>
      <circle cx="70" cy="300" r="9" fill="#93c5fd" stroke="#2563eb" stroke-width="2"/>
      <text x="88" y="305" font-size="13" fill="#334155" font-family="system-ui">schistes bleus (glaucophane)</text>
      <circle cx="70" cy="328" r="9" fill="#fca5a5" stroke="#dc2626" stroke-width="2"/>
      <text x="88" y="333" font-size="13" fill="#334155" font-family="system-ui">éclogites (grenat, jadéite)</text>
    `},
    { id: 'eau', label: 'Déshydratation', delay: 1600, svgContent: `
      <path d="M 486 232 Q 496 208 512 190" fill="none" stroke="#0ea5e9" stroke-width="3" marker-end="url(#arrowCyan)"/>
      <path d="M 556 296 Q 566 268 582 246" fill="none" stroke="#0ea5e9" stroke-width="3" marker-end="url(#arrowCyan)"/>
      <path d="M 618 386 Q 632 356 648 330" fill="none" stroke="#0ea5e9" stroke-width="3" marker-end="url(#arrowCyan)"/>
      <text x="784" y="372" text-anchor="middle" font-size="15" font-weight="800" fill="#0369a1" font-family="system-ui">L'eau libérée monte</text>
      <text x="784" y="392" text-anchor="middle" font-size="13" fill="#0369a1" font-family="system-ui">déshydratation des roches</text>
      <line x1="716" y1="366" x2="660" y2="336" stroke="#0369a1" stroke-width="1.8"/>
    `},
    { id: 'fusion', label: 'Fusion partielle', delay: 1800, svgContent: `
      <ellipse cx="640" cy="286" rx="60" ry="30" fill="#f97316" fill-opacity="0.85" stroke="#c2410c" stroke-width="2"/>
      <text x="640" y="292" text-anchor="middle" font-size="14" font-weight="800" fill="#7c2d12" font-family="system-ui">Fusion partielle</text>
      <path d="M 640 256 Q 648 208 654 166" fill="none" stroke="#dc2626" stroke-width="5" stroke-linecap="round"/>
      <path d="M 654 152 L 645 172 L 663 172 Z" fill="#dc2626"/>
    `},
    { id: 'volcans', label: 'Arc volcanique', delay: 2000, svgContent: `
      <path d="M 610 150 L 654 96 L 698 150 Z" fill="#dc2626" stroke="#7f1d1d" stroke-width="2"/>
      <path d="M 716 150 L 748 112 L 780 150 Z" fill="#dc2626" stroke="#7f1d1d" stroke-width="2"/>
      <text x="700" y="80" text-anchor="middle" font-size="16" font-weight="800" fill="#7f1d1d" font-family="system-ui">Arc volcanique</text>
      <text x="700" y="52" text-anchor="middle" font-size="13" fill="#7f1d1d" font-family="system-ui">القوس البركاني</text>
    `},
    { id: 'bilan', label: 'À retenir', delay: 2200, svgContent: `
      <rect x="24" y="516" width="872" height="88" rx="14" fill="#ffffff" stroke="#38bdf8" stroke-width="2"/>
      <text x="44" y="542" font-size="16" font-weight="800" fill="#0369a1" font-family="system-ui">À retenir — ما يجب حفظه</text>
      <text x="44" y="566" font-size="14" fill="#334155" font-family="system-ui">• La plaque océanique, vieille, froide et DENSE, plonge sous la plaque voisine : c'est son poids qui l'entraîne.</text>
      <text x="44" y="590" font-size="14" fill="#334155" font-family="system-ui">• En plongeant elle se déshydrate ; l'eau fait fondre le manteau au-dessus → magma → volcans en arc.</text>
    `},
  ],
  annotations: [
    { id: 'a_fosse', x: 366, y: 146, width: 46, height: 40, label: 'Fosse océanique', color: '#b91c1c',
      description: "Point le plus bas du plancher océanique : c'est là que la plaque s'enfonce." },
    { id: 'a_slab', x: 520, y: 268, width: 110, height: 110, label: 'Plaque plongeante', color: '#0f172a',
      description: "Elle s'enfonce d'autant plus vite qu'elle est ancienne : en refroidissant elle est devenue plus dense que l'asthénosphère." },
    { id: 'a_fusion', x: 580, y: 256, width: 120, height: 60, label: 'Fusion partielle', color: '#c2410c',
      description: "L'eau libérée par le slab abaisse la température de fusion du manteau : il fond partiellement et donne le magma." },
    { id: 'a_arc', x: 604, y: 90, width: 180, height: 60, label: 'Arc volcanique', color: '#7f1d1d',
      description: "Les volcans s'alignent à l'aplomb de la zone de fusion, à environ 100 km au-dessus du slab." },
  ],
  highlights: [
    { id: 'h_fosse', cx: 392, cy: 160, radius: 40, label: 'Fosse océanique' },
    { id: 'h_slab', cx: 570, cy: 320, radius: 60, label: 'Plaque plongeante' },
    { id: 'h_eau', cx: 556, cy: 272, radius: 46, label: 'Déshydratation' },
    { id: 'h_fusion', cx: 640, cy: 286, radius: 58, label: 'Fusion partielle' },
    { id: 'h_arc', cx: 690, cy: 124, radius: 62, label: 'Arc volcanique' },
    { id: 'h_metamorphisme', cx: 540, cy: 272, radius: 40, label: 'Métamorphisme HP-BT' },
  ],
};

export const svt_cellule_mitochondrie: ScientificSchema = {
  id: 'svt_cellule_mitochondrie',
  title: 'De la cellule à la mitochondrie',
  subject: 'svt',
  keywords: ['cellule', 'cellule eucaryote', 'cytoplasme', 'noyau', 'mitochondrie', 'respiration cellulaire', 'خلية', 'الميتوكندري'],
  category: 'structure',
  viewBox: '0 0 960 620',
  backgroundColor: '#fffdf5',
  layers: [
    { id: 'title', label: 'Titre', delay: 0, svgContent: `
      <text x="480" y="42" text-anchor="middle" font-size="27" font-weight="bold" fill="#172554" font-family="system-ui">DE LA CELLULE À LA MITOCHONDRIE</text>
      <text x="480" y="68" text-anchor="middle" font-size="13" fill="#475569" font-family="system-ui">Localiser les étapes de la respiration cellulaire</text>
    `},
    { id: 'cellule', label: 'Cellule', delay: 250, svgContent: `
      <path d="M 72 315 C 70 188, 150 108, 288 105 C 423 102, 510 180, 512 310 C 514 447, 421 520, 282 518 C 145 516, 75 444, 72 315 Z" fill="#dbeafe" stroke="#2563eb" stroke-width="5"/>
      <path d="M 87 314 C 88 198, 158 124, 286 122 C 406 120, 492 192, 495 310 C 498 430, 412 501, 282 500 C 157 499, 89 430, 87 314 Z" fill="#eff6ff" stroke="#60a5fa" stroke-width="2" stroke-dasharray="7,5"/>
      <text x="285" y="548" text-anchor="middle" font-size="17" font-weight="bold" fill="#1d4ed8" font-family="system-ui">Cellule eucaryote</text>
      <text x="285" y="570" text-anchor="middle" font-size="12" fill="#475569" font-family="system-ui">La respiration libère l'énergie de la matière organique</text>
    `},
    { id: 'noyau', label: 'Noyau', delay: 500, svgContent: `
      <circle cx="222" cy="303" r="78" fill="#ddd6fe" stroke="#7c3aed" stroke-width="4"/>
      <circle cx="222" cy="303" r="62" fill="#ede9fe" stroke="#a78bfa" stroke-width="2" stroke-dasharray="5,4"/>
      <circle cx="242" cy="285" r="17" fill="#c4b5fd" stroke="#7c3aed" stroke-width="2"/>
      <path d="M 174 324 Q 207 280, 270 331 M 178 284 Q 221 344, 268 276" fill="none" stroke="#8b5cf6" stroke-width="2" opacity="0.6"/>
      <path d="M 142 258 L 78 210" fill="none" stroke="#7c3aed" stroke-width="2"/>
      <text x="65" y="201" font-size="15" font-weight="bold" fill="#6d28d9" font-family="system-ui">Noyau</text>
    `},
    { id: 'organites', label: 'Organites', delay: 750, svgContent: `
      <ellipse cx="376" cy="196" rx="53" ry="24" transform="rotate(-18 376 196)" fill="#fed7aa" stroke="#ea580c" stroke-width="3"/>
      <path d="M 333 199 Q 351 175, 369 198 T 413 192" fill="none" stroke="#c2410c" stroke-width="2.5"/>
      <ellipse cx="385" cy="365" rx="62" ry="29" transform="rotate(14 385 365)" fill="#fdba74" stroke="#ea580c" stroke-width="4"/>
      <path d="M 331 357 Q 352 387, 370 354 T 405 374 T 437 357" fill="none" stroke="#c2410c" stroke-width="3"/>
      <ellipse cx="305" cy="445" rx="46" ry="21" transform="rotate(-12 305 445)" fill="#fed7aa" stroke="#ea580c" stroke-width="3"/>
      <path d="M 266 446 Q 282 426, 299 448 T 339 441" fill="none" stroke="#c2410c" stroke-width="2.5"/>
      <circle cx="140" cy="395" r="10" fill="#bfdbfe" stroke="#0284c7" stroke-width="2"/>
      <circle cx="335" cy="265" r="8" fill="#bfdbfe" stroke="#0284c7" stroke-width="2"/>
      <circle cx="430" cy="270" r="11" fill="#bfdbfe" stroke="#0284c7" stroke-width="2"/>
      <path d="M 110 445 L 78 478" fill="none" stroke="#2563eb" stroke-width="2"/>
      <text x="60" y="497" font-size="14" font-weight="bold" fill="#1d4ed8" font-family="system-ui">Cytoplasme</text>
      <text x="105" y="516" font-size="11" fill="#475569" font-family="system-ui">Glycolyse</text>
    `},
    { id: 'zoom', label: 'Zoom mitochondrie', delay: 1050, svgContent: `
      <circle cx="385" cy="365" r="48" fill="none" stroke="#f97316" stroke-width="3" stroke-dasharray="8,5"/>
      <path d="M 430 337 C 505 250, 535 205, 585 190" fill="none" stroke="#f97316" stroke-width="2.5" stroke-dasharray="7,5"/>
      <path d="M 430 393 C 505 440, 540 455, 590 448" fill="none" stroke="#f97316" stroke-width="2.5" stroke-dasharray="7,5"/>
      <text x="530" y="326" text-anchor="middle" font-size="14" font-weight="bold" fill="#c2410c" font-family="system-ui">ZOOM</text>
      <path d="M 586 315 C 586 218, 662 165, 774 172 C 878 179, 917 237, 909 322 C 901 407, 832 455, 724 451 C 629 448, 586 403, 586 315 Z" fill="#ffedd5" stroke="#ea580c" stroke-width="5"/>
      <path d="M 607 315 C 607 235, 671 193, 767 196 C 850 199, 887 244, 884 319 C 881 385, 827 424, 735 425 C 651 426, 607 389, 607 315 Z" fill="#fff7ed" stroke="#fb923c" stroke-width="3"/>
      <path d="M 629 253 C 664 216, 691 218, 713 255 C 735 291, 760 292, 784 250 C 807 211, 841 225, 866 259 M 626 333 C 657 293, 688 302, 713 341 C 738 380, 764 384, 791 340 C 819 295, 848 302, 870 337" fill="none" stroke="#ea580c" stroke-width="4"/>
      <text x="748" y="318" text-anchor="middle" font-size="15" font-weight="bold" fill="#9a3412" font-family="system-ui">Matrice</text>
      <text x="748" y="365" text-anchor="middle" font-size="12" fill="#15803d" font-family="system-ui">Cycle de Krebs</text>
    `},
    { id: 'legendes', label: 'Légendes', delay: 1350, svgContent: `
      <path d="M 608 236 L 557 139" fill="none" stroke="#ea580c" stroke-width="2"/>
      <text x="548" y="128" text-anchor="end" font-size="14" font-weight="bold" fill="#c2410c" font-family="system-ui">Membrane externe</text>
      <path d="M 629 253 L 648 127" fill="none" stroke="#f97316" stroke-width="2"/>
      <text x="650" y="116" font-size="14" font-weight="bold" fill="#c2410c" font-family="system-ui">Membrane interne</text>
      <text x="650" y="136" font-size="11" fill="#475569" font-family="system-ui">Chaîne respiratoire + ATP synthase</text>
      <path d="M 850 300 L 928 252" fill="none" stroke="#ea580c" stroke-width="2"/>
      <text x="928" y="241" text-anchor="end" font-size="14" font-weight="bold" fill="#c2410c" font-family="system-ui">Crêtes</text>
      <path d="M 901 347 L 933 396" fill="none" stroke="#fb923c" stroke-width="2"/>
      <text x="935" y="414" text-anchor="end" font-size="13" font-weight="bold" fill="#c2410c" font-family="system-ui">Espace intermembranaire</text>
    `},
    { id: 'bilan', label: 'Bilan', delay: 1650, svgContent: `
      <rect x="557" y="500" width="365" height="82" rx="15" fill="#ecfdf5" stroke="#16a34a" stroke-width="2.5"/>
      <text x="740" y="526" text-anchor="middle" font-size="15" font-weight="bold" fill="#166534" font-family="system-ui">Organisation fonctionnelle</text>
      <text x="740" y="550" text-anchor="middle" font-size="12" fill="#166534" font-family="system-ui">Matrice : cycle de Krebs</text>
      <text x="740" y="570" text-anchor="middle" font-size="12" fill="#166534" font-family="system-ui">Membrane interne : gradient H⁺ et synthèse d'ATP</text>
    `},
  ],
  annotations: [
    { id: 'cell', x: 72, y: 105, width: 440, height: 413, label: 'Cellule eucaryote', description: 'La glycolyse se déroule dans le cytoplasme. Les étapes suivantes de la respiration ont lieu dans la mitochondrie.', color: '#2563eb' },
    { id: 'nucleus', x: 144, y: 225, width: 156, height: 156, label: 'Noyau', description: 'Compartiment contenant l’information génétique. Il ne réalise pas la respiration cellulaire.', color: '#7c3aed' },
    { id: 'mito', x: 586, y: 172, width: 323, height: 279, label: 'Mitochondrie', description: 'La matrice accueille le cycle de Krebs ; la membrane interne porte la chaîne respiratoire et l’ATP synthase.', color: '#ea580c' },
  ],
  highlights: [
    { id: 'h1', cx: 385, cy: 365, radius: 52, label: 'Mitochondrie cellulaire' },
    { id: 'h2', cx: 748, cy: 315, radius: 155, label: 'Zoom mitochondrie' },
  ],
};

export const svt_mitochondrie_structure: ScientificSchema = {
  id: 'svt_mitochondrie_structure',
  title: 'Structure de la Mitochondrie — Ultrastructure',
  subject: 'svt',
  keywords: ['mitochondrie', 'ultrastructure de la mitochondrie', 'crêtes mitochondriales',
    'membrane interne', 'membrane externe', 'crêtes', 'matrice', 'espace intermembranaire',
    'الميتوكندري', 'بنية الميتوكندري'],
  category: 'structure',
  viewBox: '0 0 920 620',
  backgroundColor: '#fffbf0',
  // Le dessin de l'organite est importé (Servier Medical Art via Bioicons,
  // CC BY 3.0) : enveloppe, espace intermembranaire, matrice et crêtes y sont
  // quatre formes distinctes, ce que le tracé manuel précédent ne rendait pas
  // — ses crêtes flottaient dans la matrice au lieu d'en être des replis.
  //
  // Deux règles apprises en l'important :
  //   - l'original ombre la matrice avec DEUX roses ; leur donner deux teintes
  //     franches ferait lire deux compartiments, ce qui est faux ;
  //   - son vert pâle est un milieu CONTINU (espace intermembranaire), qui se
  //     prolonge dans chaque crête. C'est ce qui permet de légender la crête
  //     sans mentir sur ce qu'elle est.
  //
  // Tout le légendage reste le nôtre : c'est lui qui rend le schéma conforme
  // au BAC. Les ancres des repères ont été relevées sur le rendu, compartiment
  // par compartiment — une flèche qui pointe à côté est pire que pas de flèche.
  credit: 'Dessin de l\'organite : Servier Medical Art via Bioicons — CC BY 3.0',
  layers: [
    { id: 'title', label: 'Titre', delay: 0, svgContent: `
      <text x="460" y="36" text-anchor="middle" font-size="28" font-weight="bold" fill="#6b21a8" font-family="system-ui">L'ultrastructure de la Mitochondrie</text>
      <text x="460" y="64" text-anchor="middle" font-size="16" fill="#64748b" font-family="system-ui">بنية الميتوكندري — « centrale énergétique » de la cellule</text>
    `},
    { id: 'organite', label: 'Organite', delay: 300, svgContent: `<g transform="translate(160.0 182.1) scale(2.3715)"><defs><clipPath clipPathUnits="userSpaceOnUse" id="mitoServierClip"><path d="M3.838 3.198h252.727v124.804H3.838z"/></clipPath></defs><path clip-path="url(#mitoServierClip)" d="M5.836 58.005c-4.197 56.326 25.945 61.682 76.994 65.24 42.694 2.679 146.471 15.191 168.218-39.336 20.907-53.647-46.012-75.114-113.811-77.793C73.635 2.558 10.034 1.64 5.837 58.005z" fill="#c2710e" fill-rule="evenodd" fill-opacity="1" stroke="none"/><path clip-path="url(#mitoServierClip)" d="M136.477 11.473c56.926 2.678 96.302 16.11 108.854 37.577 5.837 9.834 5.837 20.548.84 33.06-18.429 46.492-108.854 39.376-152.428 36.658l-10.873-.88c-30.142-2.678-52.768-4.477-64.481-18.788-6.716-8.035-9.235-21.467-7.556-40.216C15.031 8.794 67.8 7.875 136.477 11.473z" fill="#f8e7b8" fill-rule="evenodd" fill-opacity="1" stroke="none"/><path d="M216.749 39.216c-2.519-1.759-2.519 1.8-2.519 3.598.84 13.392 3.358 21.427 1.68 27.663-.84 5.357-3.359 7.156-6.677 7.156-2.518 0-5.037-1.799-5.876-10.714-.84-8.035.84-12.512 0-23.225 0-13.392-10.874-15.191-13.392-16.07-18.429-5.357-11.753 9.833-11.753 12.512.84 8.914 1.679 13.392.84 24.985 0 7.155 0 15.19-4.997 15.19-4.198 0-4.198-6.236-4.198-14.271.84-4.477.84-8.955.84-13.432 0-4.437 0-27.663-14.232-29.462-14.231-.88-12.552 21.427-12.552 27.703-.84 16.07-.84 32.14-1.68 36.618 0 3.558-3.357 5.357-5.876 4.477-2.518 0-5.037-3.598-4.197-6.276.84-3.558.84-27.663.84-50.01 0-3.557.839-16.99-13.392-16.99h-14.232c-15.91 0-14.231 15.191-14.231 15.191s3.358 21.467-5.037 21.467c-8.355 0-4.997-14.31-4.997-22.346 0-13.392-20.108-14.311-20.108 1.799 0 16.95-.84 37.497-.84 39.296 0 2.678-2.518 5.357-5.036 5.357-2.519 0-4.198-2.679-4.198-6.276 0 0 .84-24.106.84-42.854 0-1.8-.84-6.237-5.837-3.558-15.91 6.236-25.984 16.95-26.824 35.698-.84 9.834.84 17.87 4.198 24.146 3.358 5.356 10.873 7.115 10.873-2.719V61.563c0-2.679 1.68-5.357 5.037-5.357 2.519 0 5.037 2.678 5.037 5.357 0 8.914.84 25.025.84 34.819 0 1.798 0 10.713 10.873 10.713s12.552-8.915 12.552-8.915c0-9.834 0-23.225-.839-33.939 0-3.558 1.679-7.156 5.037-7.156 2.518 0 3.358 3.598 4.197 7.156v38.417c0 9.794 10.034 8.035 10.034.88 0-6.237-.84-14.272-.84-14.272.84-3.598 0-9.834 6.717-9.834 7.515 0 3.358 13.392 3.358 22.306 0 4.478 2.478 8.035 4.997 8.955 4.197 0 4.197-4.477 4.197-7.156 0-16.07-2.518-41.095-1.679-50.929 0-8.914 3.358-12.472 5.877-12.472 3.358 0 6.676 1.759 7.515 11.593 1.679 8.035-.84 30.381-.84 46.451 0 2.679 0 14.272 16.75 14.272 17.59 0 18.43-13.392 18.43-16.95 0-14.311.839-32.14.839-39.296 0-2.678 2.518-5.357 5.037-5.357 2.518 0 4.997 2.679 4.997 5.357 0 8.035 0 25.904-.8 40.176 0 3.597-.84 15.19 12.553 15.19 14.23 0 12.552-13.392 13.391-16.07 0-6.236 0-13.392-.84-20.547 0-2.679 2.52-5.357 5.038-5.357 3.318 0 5.836 1.799 5.836 5.357v26.783c0 2.679.84 6.277 5.037 4.478 15.91-4.478 27.624-12.513 32.66-25.025 7.516-18.749-.839-32.14-18.428-41.975z" fill="#f2dda2" fill-rule="evenodd" fill-opacity="1" stroke="none"/><path d="M61.003 34.659c0 10.714 0 23.226-.84 31.261.84-.88.84-.88.84-1.799.84 3.598.84 6.276-.84 9.834 0 2.679-2.478 5.357-4.996 5.357-.84 0-1.68-.88-1.68-.88.84.88.84 1.76.84 1.76.84.919.84.919 1.68.919 0 0 .839-.92.839-1.8C65.2 75.755 66.04 59.645 66.04 51.61c0-5.357 0-9.794 1.679-14.272.84-2.678.84-6.236 3.358-8.035 1.679-.88 5.876-2.678 8.355-1.799-4.997-7.155-18.429-6.236-18.429 7.156zm-15.07-8.035c-15.911 6.236-25.985 16.95-26.825 35.738-.84 9.794.84 17.83 4.198 24.106 3.358 5.356 10.913 7.115 10.913-2.679V69.478c-.84-1.759-1.679-3.558-2.518-5.357-.84-1.759-2.519-4.477-2.519-6.236 0-1.799 1.68-4.477 2.519-6.276 2.518-3.558 7.515-8.035 11.713-8.035 1.679 0 4.197.919 5.037 2.678 1.679 2.678.84 4.477 1.679 7.156l1.679 9.834v-33.06c0-1.76-.84-6.237-5.877-3.558z" fill="#e9d091" fill-rule="evenodd" fill-opacity="1" stroke="none"/><path d="M57.725 90.145c.84-1.799.84-3.557.84-6.276 0-3.558 2.558-6.276 2.558-9.874h-.84c0 2.719-2.558 5.397-5.116 5.397-.84 0-.84-.88-1.72-.88.88 1.8 1.72 2.679 1.72 4.478 1.719 3.598 1.719 8.075 0 11.633 1.719-.88 1.719-2.679 2.558-4.478z" fill="#e9d091" fill-rule="evenodd" fill-opacity="1" stroke="none"/><path d="M60.204 101.738c-1.68 0-3.358 0-5.877-.88-2.518 0-5.876-1.798-7.555-3.597-2.519-4.437-.84-9.834-1.68-14.311v13.432c0 1.798 0 10.713 10.914 10.713 6.716 0 10.074-2.678 10.913-6.236.84-2.679.84-5.357.84-8.035 0 3.558-4.198 8.035-7.555 8.914zM80.351 81.27c0-4.477 0-8.034-.88-12.472 0-3.598-.839-6.276-3.397-8.954v.92c0 .879.88 1.758.88 3.557v38.337c0 9.794 10.153 8.035 10.153.88v-7.116c-5.916-1.8-6.756-9.795-6.756-15.151zM99.58 83.83c-.84-1.8-1.68-2.72-3.358-2.72 2.518 3.599 0 13.433 0 20.588 0 4.478 2.518 8.035 5.037 8.915 4.157 0 4.157-4.437 4.157-7.116V99.02h-.8c-5.876-2.678-3.357-9.834-5.036-15.19zM87.067 59.804c-1.679-1.8-2.518-3.598-2.518-5.357-5.877-1.799-3.358-14.311-3.358-21.467 0-5.357-4.198-8.915-8.395-9.834-1.68 1.799-2.519 3.598-4.198 5.397-.84.88-.84 6.236-.84 8.035 3.359-6.276 5.038-5.357 6.717-2.679 2.518 2.679.84 7.116 1.679 10.714 0 2.678.84 7.156 1.679 9.834.84 2.678 1.679 3.558 3.358 5.357 1.679 1.759 2.518 4.477 4.197 6.236.84 1.799 2.519 1.799 4.198 3.598 2.518 3.558 1.679 6.236 0 9.794 3.358-2.679 4.157-9.794 1.679-14.271-.84-1.8-2.519-3.598-4.198-5.357zM128.042 39.216c.84 5.357 1.68 10.714 1.68 16.07 0 2.679.839 6.237 1.678 8.915v8.915c.84-2.679.84-4.438 1.68-7.116V35.658c0-3.597.799-16.99-13.393-16.99h-14.19c-15.911 0-14.232 15.191-14.232 15.191s1.679 8.915 0 15.191l1.679 1.76c1.679-3.559 3.358-6.237 4.197-10.714 0-4.438.84-8.915 3.318-11.593 4.198-3.558 11.713-1.8 15.87-1.8 6.716.92 10.034 5.358 11.713 12.513zM133 112.452c4.197 0 7.555-.88 10.033-1.76.84-2.677 0-6.275 0-8.074.84-2.679.84-5.357-.8-7.156-.839-1.759-2.518-2.678-4.197-3.558h-.84v4.478c-.839 1.798-1.678 3.557-2.518 4.477-1.679 2.678-6.716 2.678-10.074.88-3.357-2.679-4.197-7.156-5.036-10.714-.84-7.156-1.68-15.23-1.68-22.387l-.839 1.8c0 8.954-.84 18.788-.84 27.742 0 2.679 0 14.272 16.79 14.272zM169.058 60.723c0-.92.839-1.799 1.679-3.598v-4.477c0-4.477 0-27.743-14.272-29.542-14.271-.92-12.592 21.467-12.592 27.743 0 3.598 0 6.276-.84 8.955l1.68 2.678c1.678-8.035.839-28.623 12.592-25.944 4.197.88 7.555 4.477 9.234 8.035 1.68 4.477 3.358 10.753 2.519 16.15z" fill="#e9d091" fill-rule="evenodd" fill-opacity="1" stroke="none"/><path d="M149.07 38.337h3.358c2.478 0 2.478.88 4.157 2.638 2.479 4.437 1.64 6.236 0 10.634 2.479-1.76 3.318-3.518 4.118-7.076 0-3.558 2.518-5.317 5.836-2.678 1.64-4.438-7.475-8.875-10.793-8.875zM203.357 43.694c0-13.432-10.874-15.231-13.392-16.11-18.429-5.397-11.713 9.833-11.713 12.512.84 7.155 1.679 11.633 1.679 20.587l.84 7.156c0-3.558.839-7.156 1.638-10.714.84-4.477.84-8.954 2.519-12.552 1.679-4.477 5.037-3.558 7.555-.88 3.318 1.8 5.837 2.679 7.516 6.277 0 2.678.84 4.477 1.679 7.155 0 1.8-.84 5.357 0 7.156.84-.88.84-.88 1.679-1.799 0-5.357.8-10.753 0-18.788zM216.709 39.096c-2.519-1.799-2.519 1.8-2.519 3.598.84 13.432 3.358 21.507 1.68 27.783-.84 5.397-3.359 7.196-5.877 7.196v.88c1.679.919 5.876-.88 7.555-1.8 4.198-3.557 3.358-8.954 9.235-7.155 4.197.88 7.555 6.276 7.555 10.753a686.649 686.649 0 0 1-2.518 5.357c-.84 1.799-2.519 4.517-3.358 6.276 3.358-3.558 5.036-7.155 6.715-10.753 7.516-18.829-.839-32.26-18.468-42.135z" fill="#e9d091" fill-rule="evenodd" fill-opacity="1" stroke="none"/><path d="M201.718 80.311c2.518 2.719 5.876 2.719 8.395 4.518 1.679 1.798 4.197 4.477 2.518 7.155 3.358-3.558 0-10.753-3.358-13.472v-.88c-2.518 0-5.037-2.677-5.876-10.793v-5.396c-3.358 7.195-7.556 14.391-1.68 18.868z" fill="#e9d091" fill-rule="evenodd" fill-opacity="1" stroke="none"/><path d="M201.718 88.306c.84-1.758.84-4.437 2.518-5.356 1.68 0 2.519.92 3.358.92l-5.876-9.875c-1.68 0-3.358.92-4.198 2.719v25.024c0 2.679.84 6.237 5.037 4.478 1.68 0 4.198-.92 5.837-1.8-4.997-3.557-7.516-8.954-6.676-16.11zM179.051 93.583c0-2.678.8-4.437-.839-7.115-.84-1.8-1.679-3.598-3.318-5.357v-.92h-.84c-4.157 0-4.157-6.236-4.157-14.271 0-1.799.84-3.558.84-4.477-1.64 2.678-3.318 6.276-3.318 9.834-.84 3.558-.84 11.593 2.478 14.271 4.158 2.679 9.154 1.8 9.154 8.035z" fill="#e9d091" fill-rule="evenodd" fill-opacity="1" stroke="none"/><path d="M174.174 111.572c10.074 0 12.553-7.155 12.553-11.593-2.479 3.558-5.837 5.357-10.034 5.357-5.037-.92-7.556-1.799-9.234-7.156a43.788 43.788 0 0 1-4.198-18.788c0-2.678-.84-7.156 0-10.754h-.84c0 8.076 0 18.789-.839 27.744 0 3.597-.84 15.19 12.592 15.19z" fill="#e9d091" fill-rule="evenodd" fill-opacity="1" stroke="none"/><path clip-path="url(#mitoServierClip)" d="M5.876 58.045c-4.197 56.326 25.945 61.682 76.994 65.24 42.694 2.679 146.471 15.191 168.218-39.336 20.907-53.647-46.012-75.114-113.811-77.793C73.675 2.598 10.074 1.68 5.877 58.045" fill="none" stroke="#8b5e3c" stroke-width="1.6789824px" stroke-linecap="round" stroke-linejoin="round" stroke-miterlimit="4" stroke-dasharray="none" stroke-opacity="1"/><path clip-path="url(#mitoServierClip)" d="M136.517 11.513c56.926 2.678 96.302 16.11 108.854 37.577 5.837 9.834 5.837 20.548.84 33.06-18.43 46.492-108.854 39.376-152.428 36.658l-10.873-.88c-30.142-2.678-52.768-4.477-64.481-18.788-6.716-8.035-9.235-21.467-7.556-40.216 0 0 0 0 0 0C15.071 8.834 67.84 7.915 136.517 11.513" fill="none" stroke="#fff" stroke-width="1.6789824px" stroke-linecap="round" stroke-linejoin="round" stroke-miterlimit="4" stroke-dasharray="none" stroke-opacity="1"/><path d="M136.437 91.984c6.636.92 7.436 5.397 7.436 9.834M172.416 79.432c6.635 3.598 7.435 8.914 7.435 13.352M207.514 77.593c6.836 5.357 7.676 7.156 5.997 13.352M51.769 77.593c5.996 6.316 3.438 10.793 3.438 14.391M82.79 52.648c3.398 7.116 9.274 10.674 10.114 16.91.84 4.437 0 7.995-4.198 11.553M107.095 40.016c4.158 0 6.636-1.76 6.636-6.157M154.027 51.609c4.197-.88 6.716-2.639 6.716-7.116" fill="none" stroke="#fff" stroke-width=".79951543px" stroke-linecap="round" stroke-linejoin="round" stroke-miterlimit="4" stroke-dasharray="none" stroke-opacity="1"/><path d="M93.703 21.307c-5.037 5.397-4.197 12.513-4.197 13.432.84 3.558 1.679 14.311-1.68 17.87 0 0-.839.919-1.678.919-.84 0-1.68-.92-2.519-.92-1.639-2.678-1.639-8.954-.84-14.311V32.94c0-8.035-5.836-11.633-11.712-11.633-3.318 0-5.837.92-8.355 2.678-2.518 2.719-3.358 6.277-3.358 10.754l-.84 39.336c0 1.799-1.678 3.558-3.317 3.558-.84 0-2.519 0-2.519-4.437 0 0 .84-24.146.84-42.934 0-2.679-1.68-4.478-2.519-5.357-1.679-.92-3.358-.92-5.876 0-17.55 7.156-26.784 19.668-27.624 37.537-.84 9.834.84 17.91 5.037 25.025 1.68 3.598 5.877 6.276 9.195 5.397 1.679-.92 4.197-2.679 4.197-8.955V61.563c0-1.8.84-3.598 3.358-3.598 1.68 0 3.318 1.799 3.318 3.598l.84 34.859c0 8.035 4.197 12.512 12.552 12.512 11.753 0 14.231-8.915 14.231-10.714l-.84-33.979c0-2.678 1.68-5.357 3.359-5.357.84 0 1.679 2.679 2.518 5.357v38.457c0 2.678.84 4.477 1.68 6.236 1.678 1.799 2.518 2.678 5.036 2.678 3.318 0 6.676-3.557 6.676-8.035l-.84-14.311v-.88c0-1.798 0-4.477 1.68-6.276.84 0 1.679-.88 3.358-.88s1.679.88 1.679.88c1.639 1.8 1.639 8.075.8 12.513l-.8 7.155c0 5.397 2.478 8.955 6.676 9.834 1.679.92 3.358 0 4.197-.88.84-.879 1.68-3.557 1.68-7.155 0-8.035-.84-17.869-.84-26.824-.84-9.834-1.68-18.788-.84-24.145 0-8.035 2.519-10.713 4.158-10.713 4.197 0 5.876 5.356 5.876 9.834.84 5.356 0 17.869 0 30.381l-.84 15.191c0 6.276 1.68 9.874 3.359 11.633 3.357 3.598 8.354 5.357 15.07 5.357 17.55 0 20.068-13.392 20.068-18.749l.84-39.336c0-1.799 1.679-3.598 3.358-3.598s3.358 1.799 3.358 3.598l-.84 40.216v.879c0 2.718 0 8.075 3.318 11.633 2.519 2.678 5.877 4.477 10.874 4.477 5.036 0 8.394-1.799 10.913-4.477 4.157-3.558 4.157-9.834 4.157-12.512l-.84-21.467c0-1.76 1.68-3.558 3.359-3.558s2.518 0 2.518.88c.84.919 1.68 1.798 1.68 2.678v26.823c0 1.8 0 4.478 2.518 6.277.84 0 2.478.879 4.997 0 17.59-5.357 28.463-14.312 33.5-25.945 1.678-4.477 2.518-8.914 2.518-13.392 0-12.512-6.716-23.266-21.787-31.3-1.679-.88-2.518-.88-3.358 0-1.639.879-1.639 4.477-1.639 5.356l.84 14.311c.8 5.357 1.639 9.834.8 12.513-.8 6.276-2.48 6.276-4.998 6.276-.84 0-3.358 0-4.197-8.955-.84-4.477 0-7.155 0-11.633V43.654c-.84-13.392-10.874-16.95-14.232-17.87h-.84c-5.836-1.799-10.033-1.799-12.552.92-3.357 3.558-1.678 8.914-1.678 12.512l.839.88.84 6.276c0 5.357.839 9.834 0 18.749v2.678c0 4.477 0 10.753-3.358 10.753h-.8c-1.679-1.799-1.679-7.155-1.679-12.512l.84-13.432c0-5.357 0-29.502-15.91-31.3-3.359 0-6.717.919-9.195 3.597-5.877 5.357-5.877 17.87-5.037 24.145v1.76c-.84 25.943-.84 33.979-1.68 36.657 0 .92-.839 1.799-1.678 2.718h-2.519c-.84 0-1.679-.92-1.679-.92-.8-.879-.8-2.677-.8-3.557.8-4.477.8-36.658.8-50.09 0-3.557 0-9.834-4.157-14.31-2.519-2.68-5.877-4.478-10.874-4.478h-14.23c-5.038 0-9.235 1.799-11.714 4.477zm-2.518 33.1c4.157-5.357 2.518-18.789 1.679-20.587 0 0 0-6.237 3.318-9.835 1.679-2.678 5.037-3.557 9.234-3.557h14.231c4.158 0 6.676.88 9.195 3.557 2.518 2.719 2.518 8.955 2.518 10.754 0 28.623 0 47.371-.84 50.97 0 1.758 0 3.557.84 5.356 1.68 1.799 2.519 2.678 4.997 2.678 1.68.88 3.358 0 5.037-.88 1.68-.919 2.519-2.678 2.519-4.477.84-4.477.84-16.11 1.679-37.577V49.05c-.84-5.396-.84-16.99 4.157-22.346 1.68-.92 3.358-1.8 6.716-1.8 12.553.88 12.553 23.227 12.553 27.704l-.84 12.513c0 7.155 0 12.512 2.519 15.23.839 1.76 2.518 1.76 3.318 1.76 5.876 0 6.715-8.036 6.715-14.312V65.12c.84-8.915 0-14.312 0-19.669l-.839-5.356-.84-1.8c0-2.678-1.678-7.155 0-8.914 1.68-1.799 5.037-1.799 10.034 0h.84c3.358.88 11.713 3.558 11.713 14.272v11.632c0 3.598-.84 7.156 0 11.633 0 5.357 1.679 12.513 7.555 12.513 4.997 0 6.676-2.679 8.355-8.955V66.04c0-2.678 0-5.397-.84-9.834l-.839-13.432v-2.678h.84c17.589 10.713 23.425 24.145 17.589 40.255-5.037 11.593-15.91 19.668-31.82 24.106-1.68.92-2.48.92-2.48 0-.839 0-.839-1.76-.839-2.679V74.955c0-2.679-.84-4.478-2.518-5.357-.84-.88-3.358-1.8-5.037-1.8-1.68 0-3.358.92-4.198 1.8-1.639 1.799-2.478 3.598-2.478 5.357l.84 21.467c0 2.678 0 7.155-3.359 10.753-1.679 1.759-4.197 2.678-8.394 2.678-4.158 0-6.676-.919-8.355-2.678-2.519-2.718-2.519-7.156-2.519-9.874v-.88l.84-40.215c0-3.598-3.318-7.156-6.676-7.156-4.198 0-6.716 3.558-6.716 7.156l-.84 39.336c0 5.357-2.478 15.19-16.71 15.19-5.876 0-10.074-1.798-12.552-4.476-1.679-1.8-2.518-4.478-2.518-8.036l.839-16.11c0-12.512.84-25.025 0-31.3-.84-10.714-5.876-12.513-9.234-12.513-2.479 0-7.516 1.799-7.516 14.311-.84 5.357 0 14.311.84 24.145 0 8.955.84 18.79.84 26.824 0 3.598-.84 4.478-.84 4.478l-.84.879c-2.518-.88-4.197-3.558-4.197-7.156l.84-7.155c.839-6.237 1.678-11.593-1.68-15.191-.84-.88-2.478-1.8-4.157-1.8-2.519 0-4.198.92-5.877 2.72-2.518 1.758-2.518 5.356-2.518 8.034v.88l.84 14.311c0 2.679-1.68 4.478-3.319 4.478-.84 0-1.679-.88-2.518-1.8-.84-.879-.84-1.798-.84-3.557V64.24c-.84-2.678-.84-4.477-1.679-6.276-.84-1.76-2.518-2.679-5.037-2.679-3.318 0-5.836 5.357-5.836 8.955l.84 33.98s-1.68 7.155-10.914 7.155c-5.836 0-9.194-2.678-9.194-8.954l-.84-34.86c0-3.597-3.358-7.155-6.676-7.155-4.197 0-6.716 3.558-6.716 8.035V83.91c0 1.8 0 4.477-1.679 5.357-1.639 0-4.157-.88-5.836-3.558-3.358-6.276-5.037-13.432-4.198-23.266.84-16.07 8.395-26.824 25.105-33.98 1.68-.879 2.519-.879 3.358-.879 0 .88.84 1.8.84 2.679 0 18.788-.84 42.934-.84 42.934 0 4.437 2.519 8.035 5.877 8.035 4.157 0 6.675-3.598 6.675-7.156l.84-39.336c0-3.598.84-6.276 2.518-8.035 1.68-.92 3.358-1.8 5.837-1.8 4.197 0 8.395 2.68 8.395 8.036v5.357c-.84 6.276-.84 12.512 1.679 16.11 1.639 1.799 3.318 2.678 4.997 2.678 1.679 0 3.358-.88 5.037-2.678zm126.363-16.99z" fill="#f7ecc8" fill-rule="evenodd" fill-opacity="1" stroke="none"/><path d="M93.703 21.307c-5.037 5.397-4.197 12.513-4.197 13.432.84 3.558 1.679 14.311-1.68 17.87 0 0-.839.919-1.678.919-.8 0-1.64-.92-2.479-.92-1.679-2.678-1.679-8.954-.84-14.311V32.94c0-8.035-5.876-11.633-11.712-11.633-3.358 0-5.877.92-8.395 2.678-2.518 2.719-3.358 6.277-3.358 10.754l-.84 39.336c0 1.799-1.638 3.558-3.317 3.558-.84 0-2.519 0-2.519-4.437 0 0 .84-24.146.84-42.934 0-2.679-1.68-4.478-2.519-5.357-1.679-.92-3.358-.92-5.876 0-17.55 7.156-26.784 19.668-27.624 37.537-.84 9.834.84 17.91 5.037 25.025 1.68 3.598 5.877 6.276 9.195 5.397 1.679-.92 4.197-2.679 4.197-8.955V61.563c0-1.8.84-3.598 3.358-3.598 1.68 0 3.358 1.799 3.358 3.598l.84 34.859c0 8.035 4.157 12.512 12.552 12.512 11.713 0 14.231-8.915 14.231-10.714l-.84-33.979c0-2.678 1.68-5.357 3.319-5.357.84 0 1.679 2.679 2.518 5.357v38.457c0 2.678.84 4.477 1.68 6.236 1.678 1.799 2.518 2.678 5.036 2.678 3.358 0 6.676-3.557 6.676-8.035l-.84-14.311v-.88c0-1.798 0-4.477 1.68-6.276.84 0 1.679-.88 3.358-.88s1.679.88 1.679.88c1.679 1.8 1.679 8.075.84 12.513l-.84 7.155c0 5.397 2.518 8.955 6.676 9.834 1.679.92 3.358 0 4.197-.88.84-.879 1.68-3.557 1.68-7.155 0-8.035-.84-17.869-.84-26.824-.84-9.834-1.68-18.788-.84-24.145 0-8.035 2.519-10.713 4.198-10.713 4.157 0 5.836 5.356 5.836 9.834.84 5.356 0 17.869 0 30.381l-.84 15.191c0 6.276 1.68 9.874 3.359 11.633 3.357 3.598 8.394 5.357 15.07 5.357 17.59 0 20.108-13.392 20.108-18.749l.84-39.336c0-1.799 1.639-3.598 3.318-3.598s3.358 1.799 3.358 3.598l-.84 40.216v.879c0 2.718 0 8.075 3.358 11.633 2.519 2.678 5.877 4.477 10.874 4.477 5.036 0 8.394-1.799 10.873-4.477 4.197-3.558 4.197-9.834 4.197-12.512l-.84-21.467c0-1.76 1.68-3.558 3.359-3.558s2.518 0 2.518.88c.84.919 1.68 1.798 1.68 2.678v26.823c0 1.8 0 4.478 2.478 6.277.84 0 2.518.879 5.037 0 17.59-5.357 28.463-14.312 33.5-25.945 1.678-4.477 2.478-8.914 2.478-13.392 0-12.512-6.676-23.266-21.747-31.3-1.679-.88-2.518-.88-3.358 0-1.679.879-1.679 4.477-1.679 5.356l.84 14.311c.84 5.357 1.679 9.834.84 12.513-.84 6.276-2.52 6.276-4.998 6.276-.84 0-3.358 0-4.197-8.955-.84-4.477 0-7.155 0-11.633V43.654c-.84-13.392-10.874-16.95-14.232-17.87h-.84c-5.876-1.799-10.033-1.799-12.552.92-3.357 3.558-1.679 8.914-1.679 12.512l.84.88.84 6.276c0 5.357.839 9.834 0 18.749v2.678c0 4.477 0 10.753-3.358 10.753h-.84c-1.679-1.799-1.679-7.155-1.679-12.512l.84-13.432c0-5.357 0-29.502-15.91-31.3-3.319 0-6.677.919-9.195 3.597-5.837 5.357-5.837 17.87-5.037 24.145v1.76c-.8 25.943-.8 33.979-1.64 36.657 0 .92-.839 1.799-1.678 2.718h-2.519c-.84 0-1.679-.92-1.679-.92-.84-.879-.84-2.677-.84-3.557.84-4.477.84-36.658.84-50.09 0-3.557 0-9.834-4.197-14.31-2.519-2.68-5.837-4.478-10.874-4.478h-14.23c-5.038 0-9.195 1.799-11.714 4.477" fill="none" stroke="#8b5e3c" stroke-width=".79951543px" stroke-linecap="round" stroke-linejoin="round" stroke-miterlimit="4" stroke-dasharray="none" stroke-opacity="1"/><path d="M216.749 39.216c-2.519-1.759-2.519 1.8-2.519 3.598.84 13.392 3.358 21.427 1.68 27.663-.84 5.357-3.359 7.156-6.677 7.156-2.518 0-5.037-1.799-5.876-10.714-.84-8.035.84-12.512 0-23.225 0-13.392-10.874-15.191-13.392-16.07-18.429-5.357-11.753 9.833-11.753 12.512.84 8.914 1.679 13.392.84 24.985 0 7.155 0 15.19-4.997 15.19-4.198 0-4.198-6.236-4.198-14.271.84-4.477.84-8.955.84-13.432 0-4.437 0-27.663-14.232-29.462-14.231-.88-12.552 21.427-12.552 27.703-.84 16.07-.84 32.14-1.68 36.618 0 3.558-3.357 5.357-5.876 4.477-2.518 0-5.037-3.598-4.197-6.276.84-3.558.84-27.663.84-50.01 0-3.557.839-16.99-13.392-16.99h-14.232c-15.91 0-14.231 15.191-14.231 15.191s3.358 21.467-5.037 21.467c-8.355 0-4.997-14.31-4.997-22.346 0-13.392-20.108-14.311-20.108 1.799 0 16.95-.84 37.497-.84 39.296 0 2.678-2.518 5.357-5.036 5.357-2.519 0-4.198-2.679-4.198-6.276 0 0 .84-24.106.84-42.854 0-1.8-.84-6.237-5.837-3.558-15.91 6.236-25.984 16.95-26.824 35.698-.84 9.834.84 17.87 4.198 24.146 3.358 5.356 10.873 7.115 10.873-2.719V61.563c0-2.679 1.68-5.357 5.037-5.357 2.519 0 5.037 2.678 5.037 5.357 0 8.914.84 25.025.84 34.819 0 1.798 0 10.713 10.873 10.713s12.552-8.915 12.552-8.915c0-9.834 0-23.225-.839-33.939 0-3.558 1.679-7.156 5.037-7.156 2.518 0 3.358 3.598 4.197 7.156v38.417c0 9.794 10.034 8.035 10.034.88 0-6.237-.84-14.272-.84-14.272.84-3.598 0-9.834 6.717-9.834 7.515 0 3.358 13.392 3.358 22.306 0 4.478 2.478 8.035 4.997 8.955 4.197 0 4.197-4.477 4.197-7.156 0-16.07-2.518-41.095-1.679-50.929 0-8.914 3.358-12.472 5.877-12.472 3.358 0 6.676 1.759 7.515 11.593 1.679 8.035-.84 30.381-.84 46.451 0 2.679 0 14.272 16.75 14.272 17.59 0 18.43-13.392 18.43-16.95 0-14.311.839-32.14.839-39.296 0-2.678 2.518-5.357 5.037-5.357 2.518 0 4.997 2.679 4.997 5.357 0 8.035 0 25.904-.8 40.176 0 3.597-.84 15.19 12.553 15.19 14.23 0 12.552-13.392 13.391-16.07 0-6.236 0-13.392-.84-20.547 0-2.679 2.52-5.357 5.038-5.357 3.318 0 5.836 1.799 5.836 5.357v26.783c0 2.679.84 6.277 5.037 4.478 15.91-4.478 27.624-12.513 32.66-25.025 7.516-18.749-.839-32.14-18.428-41.975" fill="none" stroke="#fff" stroke-width=".79951543px" stroke-linecap="round" stroke-linejoin="round" stroke-miterlimit="4" stroke-dasharray="none" stroke-opacity="1"/></g>` },
    { id: 'legendes', label: 'Légendes', delay: 900, svgContent: `
      <line x1="200" y1="300" x2="300" y2="152" stroke="#0e7490" stroke-width="2"/>
      <circle cx="200" cy="300" r="5" fill="#0e7490"/>
      <text x="300" y="140" text-anchor="middle" font-size="19" font-weight="700" fill="#0e7490" font-family="system-ui">Espace intermembranaire</text>
      <text x="300" y="118" text-anchor="middle" font-size="16" fill="#0e7490" font-family="system-ui">الفراغ بين الغشائين</text>

      <line x1="694" y1="250" x2="800" y2="170" stroke="#8b5e3c" stroke-width="2"/>
      <circle cx="694" cy="250" r="5" fill="#8b5e3c"/>
      <text x="828" y="158" text-anchor="middle" font-size="19" font-weight="700" fill="#8b5e3c" font-family="system-ui">Membrane</text>
      <text x="828" y="180" text-anchor="middle" font-size="19" font-weight="700" fill="#8b5e3c" font-family="system-ui">externe</text>
      <text x="828" y="202" text-anchor="middle" font-size="15" fill="#8b5e3c" font-family="system-ui">الغشاء الخارجي</text>

      <line x1="596" y1="356" x2="806" y2="300" stroke="#7c2d12" stroke-width="2"/>
      <circle cx="596" cy="356" r="5" fill="#7c2d12"/>
      <text x="830" y="296" text-anchor="middle" font-size="19" font-weight="700" fill="#7c2d12" font-family="system-ui">Matrice</text>
      <text x="830" y="318" text-anchor="middle" font-size="15" fill="#7c2d12" font-family="system-ui">المادة الأساسية</text>
      <!-- Le contenu de la matrice est nommé dans l'encadré du bas : entre deux
           crêtes, la place manque pour un mot sans le poser sur le dessin. -->

      <line x1="250" y1="390" x2="215" y2="530" stroke="#b8860b" stroke-width="2"/>
      <circle cx="250" cy="390" r="5" fill="#b8860b"/>
      <text x="215" y="552" text-anchor="middle" font-size="19" font-weight="700" fill="#b8860b" font-family="system-ui">Crête mitochondriale</text>
      <text x="215" y="574" text-anchor="middle" font-size="15" fill="#b8860b" font-family="system-ui">عرف الميتوكندري — repli de la membrane interne</text>
      <!-- Les deux légendes du bas se touchaient : celle du milieu descend
           d'un cran pour qu'aucune ligne n'en morde une autre. -->

      <line x1="460" y1="452" x2="486" y2="506" stroke="#a16207" stroke-width="2"/>
      <circle cx="460" cy="452" r="5" fill="#a16207"/>
      <text x="486" y="524" text-anchor="middle" font-size="19" font-weight="700" fill="#a16207" font-family="system-ui">Membrane interne</text>
      <text x="486" y="546" text-anchor="middle" font-size="15" fill="#a16207" font-family="system-ui">الغشاء الداخلي — porte l'ATP synthase</text>
    `},
    { id: 'contenu_matrice', label: 'Contenu de la matrice', delay: 1300, svgContent: `
      <!-- ADN mitochondrial : boucle fermée, comme chez les procaryotes -->
      <ellipse cx="612" cy="306" rx="17" ry="11" fill="none" stroke="#dc2626" stroke-width="2.5" stroke-dasharray="5,3" transform="rotate(-18 612 306)"/>
      <text x="612" y="290" text-anchor="middle" font-size="13" font-weight="700" fill="#dc2626" font-family="system-ui">ADN mt</text>

      <!-- Ribosomes mitochondriaux -->
      <circle cx="600" cy="338" r="5" fill="#16a34a"/>
      <circle cx="618" cy="336" r="5" fill="#16a34a"/>
      <circle cx="609" cy="348" r="5" fill="#16a34a"/>
    `},
    { id: 'fonctions', label: 'Fonctions', delay: 1600, svgContent: `
      <rect x="640" y="444" width="268" height="160" rx="14" fill="#ffffff" stroke="#c084fc" stroke-width="2"/>
      <text x="774" y="468" text-anchor="middle" font-size="17" font-weight="800" fill="#6b21a8" font-family="system-ui">Où se passe quoi</text>
      <text x="656" y="492" font-size="13.5" fill="#334155" font-family="system-ui">• Matrice → cycle de Krebs</text>
      <text x="656" y="513" font-size="13.5" fill="#334155" font-family="system-ui">• Crêtes → chaîne respiratoire</text>
      <text x="656" y="534" font-size="13.5" fill="#334155" font-family="system-ui">• Espace → réservoir de H⁺</text>
      <text x="656" y="555" font-size="13.5" fill="#334155" font-family="system-ui">• Membrane interne → ATP synthase</text>
      <text x="656" y="576" font-size="13.5" fill="#7c2d12" font-family="system-ui">• Dans la matrice : ADN mt, ribosomes</text>
      <text x="774" y="598" text-anchor="middle" font-size="15" font-weight="800" fill="#15803d" font-family="system-ui">→ 36-38 ATP par glucose</text>
    `},
  ],
  annotations: [
    { id: 'a_membrane_externe', x: 649, y: 210, width: 90, height: 60, label: 'Membrane externe', color: '#8b5e3c',
      description: "Lisse et perméable aux petites molécules grâce aux porines. Elle délimite l'organite." },
    { id: 'a_espace', x: 155, y: 260, width: 70, height: 90, label: 'Espace intermembranaire', color: '#0e7490',
      description: "Les protons H+ y sont accumulés par la chaîne respiratoire : c'est le réservoir du gradient qui fait tourner l'ATP synthase." },
    { id: 'a_cretes', x: 205, y: 350, width: 90, height: 80, label: 'Crête mitochondriale', color: '#b8860b',
      description: "Repli de la membrane interne. Les crêtes multiplient la surface portant les complexes respiratoires et l'ATP synthase." },
    { id: 'a_matrice', x: 551, y: 316, width: 110, height: 80, label: 'Matrice', color: '#7c2d12',
      description: "Contient l'ADN mitochondrial, des ribosomes et les enzymes du cycle de Krebs." },
  ],
  highlights: [
    { id: 'h_membrane_externe', cx: 694, cy: 250, radius: 40, label: 'Membrane externe' },
    { id: 'h_espace', cx: 200, cy: 300, radius: 34, label: 'Espace intermembranaire' },
    { id: 'h_cretes', cx: 250, cy: 390, radius: 44, label: 'Crête' },
    { id: 'h_matrice', cx: 596, cy: 356, radius: 50, label: 'Matrice' },
    { id: 'h_membrane_interne', cx: 460, cy: 452, radius: 36, label: 'Membrane interne' },
    { id: 'h_adn', cx: 612, cy: 306, radius: 30, label: 'ADN mitochondrial' },
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

export const svt_fibre_musculaire: ScientificSchema = {
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

/**
 * Dorsale océanique — dessinée à la main, et c'est un choix.
 *
 * Une coupe de géologie est faite de couches et de flèches : des formes
 * régulières, que le tracé manuel rend mieux et plus vite qu'une illustration
 * importée. C'est l'inverse exact de la mitochondrie, dont les replis
 * organiques justifiaient l'import.
 *
 * Trois points du programme commandent la composition : l'accrétion est
 * SYMÉTRIQUE par rapport à l'axe, les sédiments s'épaississent en s'éloignant
 * de l'axe, et les anomalies magnétiques se lisent en bandes symétriques. Le
 * profil magnétique est donc placé au-dessus de la coupe, à la verticale des
 * bandes qu'il enregistre — un élève doit pouvoir suivre la colonne du regard.
 */
export const svt_dorsale_accretion: ScientificSchema = {
  id: 'svt_dorsale_accretion',
  title: 'Dorsale océanique — Accrétion et expansion océanique',
  subject: 'svt',
  keywords: ['dorsale', 'accrétion', 'expansion océanique', 'expansion des fonds',
    'plancher océanique', 'rift', 'basalte', 'gabbro', 'chambre magmatique',
    'anomalies magnétiques', 'asthénosphère', 'الظهرة المحيطية', 'التوسع المحيطي'],
  category: 'process',
  viewBox: '0 0 920 620',
  backgroundColor: '#f8fafc',
  layers: [
    { id: 'title', label: 'Titre', delay: 0, svgContent: `
      <text x="460" y="34" text-anchor="middle" font-size="27" font-weight="bold" fill="#0f172a" font-family="system-ui">La dorsale océanique — accrétion</text>
      <text x="460" y="58" text-anchor="middle" font-size="15" fill="#475569" font-family="system-ui">الظهرة المحيطية — تشكل قشرة محيطية جديدة وتوسع المحيط</text>
    `},
    { id: 'anomalies', label: 'Anomalies magnétiques', delay: 300, svgContent: `
      <text x="24" y="84" font-size="14" font-weight="700" fill="#1e293b" font-family="system-ui">Profil magnétique — bandes symétriques de part et d'autre de l'axe</text>
      <rect x="24" y="92" width="872" height="26" fill="#e2e8f0" stroke="#94a3b8" stroke-width="1"/>
      <rect x="24" y="92" width="70" height="26" fill="#1e293b"/>
      <rect x="164" y="92" width="66" height="26" fill="#1e293b"/>
      <rect x="298" y="92" width="58" height="26" fill="#1e293b"/>
      <rect x="418" y="92" width="84" height="26" fill="#1e293b"/>
      <rect x="564" y="92" width="58" height="26" fill="#1e293b"/>
      <rect x="690" y="92" width="66" height="26" fill="#1e293b"/>
      <rect x="826" y="92" width="70" height="26" fill="#1e293b"/>
      <line x1="460" y1="86" x2="460" y2="128" stroke="#dc2626" stroke-width="2" stroke-dasharray="5,4"/>
      <text x="470" y="134" font-size="13" font-weight="700" fill="#dc2626" font-family="system-ui">axe de la dorsale</text>
    `},
    { id: 'ocean', label: 'Océan', delay: 500, svgContent: `
      <rect x="24" y="146" width="872" height="52" fill="#dbeafe" stroke="#93c5fd" stroke-width="1.5"/>
      <text x="40" y="176" font-size="15" font-weight="700" fill="#1d4ed8" font-family="system-ui">Océan — المحيط</text>
      <line x1="300" y1="186" x2="196" y2="186" stroke="#1d4ed8" stroke-width="2.5" marker-end="url(#arrowBlue)"/>
      <line x1="620" y1="186" x2="724" y2="186" stroke="#1d4ed8" stroke-width="2.5" marker-end="url(#arrowBlue)"/>
      <text x="248" y="180" text-anchor="middle" font-size="13" font-weight="700" fill="#1d4ed8" font-family="system-ui">≈ 2 cm/an</text>
      <text x="672" y="180" text-anchor="middle" font-size="13" font-weight="700" fill="#1d4ed8" font-family="system-ui">≈ 2 cm/an</text>
    `},
    { id: 'croute', label: 'Croûte océanique', delay: 800, svgContent: `
      <!-- Basaltes en coussins : la surface se relève vers l'axe, échancrée par le rift -->
      <path d="M 24 246 Q 240 226 436 200 L 444 224 L 476 224 L 484 200 Q 680 226 896 246
               L 896 280 Q 680 260 484 234 L 476 258 L 444 258 L 436 234 Q 240 260 24 280 Z"
            fill="#475569" stroke="#0f172a" stroke-width="1.5"/>
      <!-- Gabbros -->
      <path d="M 24 280 Q 240 260 436 234 L 444 258 L 476 258 L 484 234 Q 680 260 896 280
               L 896 322 Q 680 302 484 276 L 476 300 L 444 300 L 436 276 Q 240 302 24 322 Z"
            fill="#94a3b8" stroke="#475569" stroke-width="1.5"/>
      <!-- Manteau lithosphérique : mince à l'axe, épais en s'éloignant -->
      <path d="M 24 322 Q 240 302 436 276 L 444 300 L 476 300 L 484 276 Q 680 302 896 322
               L 896 424 Q 680 392 484 330 L 476 330 L 444 330 L 436 330 Q 240 392 24 424 Z"
            fill="#4d7c0f" stroke="#365314" stroke-width="1.5"/>
      <!-- Les noms de couche se posent à DROITE, où les bandes sont les plus
           épaisses : au centre elles se pincent vers l'axe et un mot déborde
           sur la bande voisine — l'élève lirait « gabbros » sur du basalte.
           Les ordonnées sont relevées sur le rendu, pas estimées. -->
      <text x="700" y="260" font-size="14" font-weight="700" fill="#f8fafc" font-family="system-ui">Basaltes en coussins</text>
      <text x="700" y="296" font-size="14" font-weight="700" fill="#1e293b" font-family="system-ui">Gabbros</text>
      <text x="700" y="356" font-size="14" font-weight="700" fill="#f0fdf4" font-family="system-ui">Manteau lithosphérique</text>
    `},
    { id: 'sediments', label: 'Sédiments', delay: 1000, svgContent: `
      <!-- Ils s'épaississent en s'éloignant de l'axe : la croûte y est plus vieille -->
      <path d="M 24 248 L 24 216 Q 200 210 344 212 Q 240 230 24 248 Z" fill="#fde68a" stroke="#ca8a04" stroke-width="1.5"/>
      <path d="M 896 248 L 896 216 Q 720 210 576 212 Q 680 230 896 248 Z" fill="#fde68a" stroke="#ca8a04" stroke-width="1.5"/>
      <line x1="150" y1="228" x2="150" y2="208" stroke="#a16207" stroke-width="1.5"/>
      <text x="150" y="204" text-anchor="middle" font-size="13" font-weight="700" fill="#a16207" font-family="system-ui">Sédiments</text>
    `},
    { id: 'asthenosphere', label: 'Asthénosphère', delay: 1200, svgContent: `
      <path d="M 24 424 Q 240 392 436 330 L 476 330 Q 680 392 896 424 L 896 470 L 24 470 Z"
            fill="#fb923c" stroke="#ea580c" stroke-width="1.5"/>
      <path d="M 250 452 Q 330 420 400 400" fill="none" stroke="#7c2d12" stroke-width="2.5" marker-end="url(#arrowRed)"/>
      <path d="M 670 452 Q 590 420 520 400" fill="none" stroke="#7c2d12" stroke-width="2.5" marker-end="url(#arrowRed)"/>
      <text x="460" y="462" text-anchor="middle" font-size="14" font-weight="700" fill="#7c2d12" font-family="system-ui">Asthénosphère — remontée de matériel chaud</text>
    `},
    { id: 'magma', label: 'Chambre magmatique', delay: 1400, svgContent: `
      <ellipse cx="460" cy="330" rx="86" ry="36" fill="#dc2626" stroke="#7f1d1d" stroke-width="2"/>
      <path d="M 460 296 L 460 262" stroke="#dc2626" stroke-width="6" stroke-linecap="round"/>
      <path d="M 460 268 L 452 282 L 468 282 Z" fill="#dc2626"/>
      <text x="460" y="322" text-anchor="middle" font-size="14" font-weight="700" fill="#fff5f5" font-family="system-ui">Chambre magmatique</text>
      <!-- Le nom du rift ne tient pas dans l'échancrure : il se lit dans l'eau,
           relié au fossé par un trait. -->
      <line x1="528" y1="180" x2="468" y2="202" stroke="#dc2626" stroke-width="1.8"/>
      <text x="566" y="176" text-anchor="middle" font-size="15" font-weight="800" fill="#dc2626" font-family="system-ui">Rift axial</text>
    `},
    { id: 'bilan', label: 'À retenir', delay: 1600, svgContent: `
      <rect x="24" y="490" width="872" height="112" rx="14" fill="#ffffff" stroke="#38bdf8" stroke-width="2"/>
      <text x="44" y="516" font-size="16" font-weight="800" fill="#0369a1" font-family="system-ui">À retenir — ما يجب حفظه</text>
      <text x="44" y="542" font-size="14" fill="#334155" font-family="system-ui">• Le magma remonte à l'axe et forme une croûte océanique NEUVE : basaltes en coussins puis gabbros.</text>
      <text x="44" y="566" font-size="14" fill="#334155" font-family="system-ui">• Tout est SYMÉTRIQUE de part et d'autre de l'axe : âge, épaisseur des sédiments, anomalies magnétiques.</text>
      <text x="44" y="590" font-size="14" fill="#334155" font-family="system-ui">• En s'éloignant, la lithosphère refroidit, s'épaissit et s'enfonce → l'océan s'élargit d'environ 2 cm par an.</text>
    `},
  ],
  annotations: [
    { id: 'a_rift', x: 414, y: 196, width: 92, height: 46, label: 'Rift axial', color: '#dc2626',
      description: "Fossé d'effondrement à l'aplomb de l'axe : c'est là que la croûte neuve se met en place et que les deux plaques se séparent." },
    { id: 'a_magma', x: 374, y: 294, width: 172, height: 72, label: 'Chambre magmatique', color: '#7f1d1d',
      description: "Réservoir de magma issu de la fusion partielle de l'asthénosphère par décompression. Il alimente basaltes et gabbros." },
    { id: 'a_sediments', x: 30, y: 214, width: 180, height: 34, label: 'Sédiments', color: '#a16207',
      description: "Leur épaisseur augmente en s'éloignant de l'axe : plus la croûte est ancienne, plus elle a eu le temps d'en accumuler." },
    { id: 'a_anomalies', x: 24, y: 92, width: 240, height: 26, label: 'Anomalies magnétiques', color: '#1e293b',
      description: "Les basaltes enregistrent le champ magnétique au moment de leur refroidissement. Les bandes symétriques prouvent l'expansion océanique." },
    { id: 'a_asthenosphere', x: 360, y: 428, width: 200, height: 40, label: 'Asthénosphère', color: '#7c2d12',
      description: "Manteau ductile et chaud. Sa remontée sous l'axe provoque la fusion partielle par décompression." },
  ],
  highlights: [
    { id: 'h_rift', cx: 460, cy: 216, radius: 46, label: 'Rift axial' },
    { id: 'h_magma', cx: 460, cy: 330, radius: 60, label: 'Chambre magmatique' },
    { id: 'h_sediments', cx: 120, cy: 232, radius: 44, label: 'Sédiments' },
    { id: 'h_anomalies', cx: 200, cy: 105, radius: 52, label: 'Anomalies magnétiques' },
    { id: 'h_asthenosphere', cx: 460, cy: 448, radius: 56, label: 'Asthénosphère' },
  ],
};

/**
 * Métamorphisme — le diagramme pression/température, pas une coupe de plus.
 *
 * La subduction a déjà son schéma : refaire une coupe ici n'apprendrait rien.
 * Ce que l'élève doit lire, c'est POURQUOI la même roche devient schiste vert,
 * schiste bleu puis éclogite — donc un plan (T, P) où l'on suit un chemin.
 *
 * Les deux gradients sont dessinés ensemble parce que le BAC les oppose : la
 * subduction est FROIDE (pression forte, température basse, le chemin monte
 * à gauche), la collision est plus chaude (le chemin part vers la droite).
 * Séparés, on retient deux dessins ; ensemble, on retient la différence.
 */
export const svt_metamorphisme: ScientificSchema = {
  id: 'svt_metamorphisme',
  title: 'Métamorphisme — Faciès et gradients (subduction / collision)',
  subject: 'svt',
  keywords: ['métamorphisme', 'faciès métamorphique', 'schistes verts', 'schistes bleus',
    'éclogite', 'glaucophane', 'grenat', 'jadéite', 'gradient métamorphique',
    'pression température', 'التحول', 'التحول الصخري'],
  category: 'diagram',
  viewBox: '0 0 920 620',
  backgroundColor: '#f8fafc',
  layers: [
    { id: 'title', label: 'Titre', delay: 0, svgContent: `
      <text x="460" y="34" text-anchor="middle" font-size="27" font-weight="bold" fill="#0f172a" font-family="system-ui">Le métamorphisme — pression, température, minéraux</text>
      <text x="460" y="66" text-anchor="middle" font-size="15" fill="#475569" font-family="system-ui">التحول الصخري — نفس الصخرة، ظروف مختلفة، معادن جديدة</text>
    `},
    { id: 'axes', label: 'Repère P–T', delay: 300, svgContent: `
      <line x1="140" y1="470" x2="640" y2="470" stroke="#334155" stroke-width="2.5"/>
      <line x1="140" y1="470" x2="140" y2="110" stroke="#334155" stroke-width="2.5"/>
      <text x="390" y="512" text-anchor="middle" font-size="15" font-weight="700" fill="#334155" font-family="system-ui">Température (°C) — درجة الحرارة</text>
      <!-- Le titre vertical passait sur les graduations : il recule au bord. -->
      <text x="38" y="290" text-anchor="middle" font-size="15" font-weight="700" fill="#334155" font-family="system-ui" transform="rotate(-90 38 290)">Pression (GPa)</text>
      <line x1="265" y1="470" x2="265" y2="464" stroke="#334155" stroke-width="2"/>
      <text x="265" y="488" text-anchor="middle" font-size="13" fill="#475569" font-family="system-ui">200</text>
      <line x1="390" y1="470" x2="390" y2="464" stroke="#334155" stroke-width="2"/>
      <text x="390" y="488" text-anchor="middle" font-size="13" fill="#475569" font-family="system-ui">400</text>
      <line x1="515" y1="470" x2="515" y2="464" stroke="#334155" stroke-width="2"/>
      <text x="515" y="488" text-anchor="middle" font-size="13" fill="#475569" font-family="system-ui">600</text>
      <line x1="140" y1="353" x2="146" y2="353" stroke="#334155" stroke-width="2"/>
      <text x="130" y="358" text-anchor="end" font-size="13" fill="#475569" font-family="system-ui">1 — 30 km</text>
      <line x1="140" y1="237" x2="146" y2="237" stroke="#334155" stroke-width="2"/>
      <text x="130" y="242" text-anchor="end" font-size="13" fill="#475569" font-family="system-ui">2 — 60 km</text>
      <line x1="140" y1="120" x2="146" y2="120" stroke="#334155" stroke-width="2"/>
      <text x="130" y="125" text-anchor="end" font-size="13" fill="#475569" font-family="system-ui">3 — 90 km</text>
    `},
    { id: 'facies', label: 'Faciès métamorphiques', delay: 600, svgContent: `
      <rect x="327" y="377" width="140" height="70" rx="8" fill="#86efac" fill-opacity="0.55" stroke="#16a34a" stroke-width="2"/>
      <text x="397" y="418" text-anchor="middle" font-size="15" font-weight="700" fill="#14532d" font-family="system-ui">Schistes verts</text>
      <rect x="252" y="248" width="150" height="120" rx="8" fill="#93c5fd" fill-opacity="0.55" stroke="#2563eb" stroke-width="2"/>
      <text x="327" y="314" text-anchor="middle" font-size="15" font-weight="700" fill="#1e3a8a" font-family="system-ui">Schistes bleus</text>
      <rect x="412" y="140" width="165" height="120" rx="8" fill="#fca5a5" fill-opacity="0.55" stroke="#dc2626" stroke-width="2"/>
      <text x="494" y="206" text-anchor="middle" font-size="15" font-weight="700" fill="#7f1d1d" font-family="system-ui">Éclogites</text>
    `},
    { id: 'gradients', label: 'Les deux gradients', delay: 900, svgContent: `
      <path d="M 150 466 Q 210 400 262 320 Q 320 240 470 176" fill="none" stroke="#1d4ed8" stroke-width="4" stroke-linecap="round" marker-end="url(#arrowBlue)"/>
      <text x="196" y="248" font-size="15" font-weight="800" fill="#1d4ed8" font-family="system-ui" transform="rotate(-52 196 248)">Subduction — froid</text>
      <path d="M 150 466 Q 300 442 420 404 Q 520 372 596 344" fill="none" stroke="#b45309" stroke-width="4" stroke-linecap="round" marker-end="url(#arrowOrange)"/>
      <text x="470" y="452" font-size="15" font-weight="800" fill="#b45309" font-family="system-ui" transform="rotate(-14 470 452)">Collision — plus chaud</text>
    `},
    { id: 'mineraux', label: 'Minéraux repères', delay: 1200, svgContent: `
      <text x="660" y="132" font-size="16" font-weight="800" fill="#0f172a" font-family="system-ui">Le minéral qui signe le faciès</text>
      <rect x="660" y="146" width="18" height="18" rx="4" fill="#86efac" stroke="#16a34a" stroke-width="2"/>
      <text x="688" y="161" font-size="14" font-weight="700" fill="#14532d" font-family="system-ui">Schistes verts</text>
      <text x="688" y="181" font-size="13" fill="#334155" font-family="system-ui">chlorite, actinote — الكلوريت</text>
      <rect x="660" y="212" width="18" height="18" rx="4" fill="#93c5fd" stroke="#2563eb" stroke-width="2"/>
      <text x="688" y="227" font-size="14" font-weight="700" fill="#1e3a8a" font-family="system-ui">Schistes bleus</text>
      <text x="688" y="247" font-size="13" fill="#334155" font-family="system-ui">GLAUCOPHANE — الغلوكوفان</text>
      <text x="688" y="266" font-size="12" fill="#64748b" font-family="system-ui">pression forte, température basse</text>
      <rect x="660" y="292" width="18" height="18" rx="4" fill="#fca5a5" stroke="#dc2626" stroke-width="2"/>
      <text x="688" y="307" font-size="14" font-weight="700" fill="#7f1d1d" font-family="system-ui">Éclogites</text>
      <text x="688" y="327" font-size="13" fill="#334155" font-family="system-ui">GRENAT + JADÉITE — الغارنيت</text>
      <text x="688" y="346" font-size="12" fill="#64748b" font-family="system-ui">le stade le plus profond</text>
      <rect x="654" y="376" width="252" height="86" rx="12" fill="#eff6ff" stroke="#38bdf8" stroke-width="2"/>
      <text x="668" y="400" font-size="14" font-weight="800" fill="#0369a1" font-family="system-ui">Chaque transformation</text>
      <text x="668" y="422" font-size="13" fill="#334155" font-family="system-ui">libère de l'EAU vers le manteau,</text>
      <text x="668" y="442" font-size="13" fill="#334155" font-family="system-ui">qui fond partiellement → magma.</text>
    `},
    { id: 'bilan', label: 'À retenir', delay: 1500, svgContent: `
      <rect x="24" y="526" width="882" height="78" rx="14" fill="#ffffff" stroke="#38bdf8" stroke-width="2"/>
      <text x="44" y="550" font-size="16" font-weight="800" fill="#0369a1" font-family="system-ui">À retenir — ما يجب حفظه</text>
      <text x="44" y="572" font-size="14" fill="#334155" font-family="system-ui">• La roche ne fond PAS : elle change de minéraux à l'état solide. Même chimie, minéraux nouveaux.</text>
      <text x="44" y="594" font-size="14" fill="#334155" font-family="system-ui">• Le glaucophane signe la subduction (P forte, T basse) ; le grenat et la jadéite, le stade éclogite.</text>
    `},
  ],
  annotations: [
    { id: 'a_verts', x: 327, y: 377, width: 140, height: 70, label: 'Faciès des schistes verts', color: '#16a34a',
      description: "Premier stade : chlorite et actinote apparaissent vers 300-500 °C, à faible profondeur." },
    { id: 'a_bleus', x: 252, y: 248, width: 150, height: 120, label: 'Faciès des schistes bleus', color: '#2563eb',
      description: "Le glaucophane, bleu, ne se forme qu'à pression forte et température basse : c'est la signature de la subduction." },
    { id: 'a_eclogites', x: 412, y: 140, width: 165, height: 120, label: 'Faciès des éclogites', color: '#dc2626',
      description: "Grenat et jadéite, au-delà de 60 km. La roche devient très dense : elle entraîne la plaque vers le bas." },
    { id: 'a_gradient', x: 168, y: 300, width: 120, height: 90, label: 'Gradient de subduction', color: '#1d4ed8',
      description: "Chemin froid : la pression augmente vite, la température peu. C'est ce qui distingue la subduction de la collision." },
  ],
  highlights: [
    { id: 'h_verts', cx: 397, cy: 412, radius: 56, label: 'Schistes verts' },
    { id: 'h_bleus', cx: 327, cy: 308, radius: 60, label: 'Schistes bleus' },
    { id: 'h_eclogites', cx: 494, cy: 200, radius: 66, label: 'Éclogites' },
    { id: 'h_subduction', cx: 262, cy: 320, radius: 52, label: 'Gradient de subduction' },
    { id: 'h_collision', cx: 470, cy: 396, radius: 52, label: 'Gradient de collision' },
  ],
};

/**
 * Chaîne de montagnes — la coupe d'une collision, avec sa racine.
 *
 * Le réflexe de l'élève est de croire que la montagne, c'est ce qui dépasse.
 * La figure est donc construite pour montrer l'inverse : le relief est petit,
 * la RACINE crustale sous lui est énorme. Le Moho est tracé d'un bout à
 * l'autre pour qu'on voie le plongeon, et l'échelle verticale des deux côtés
 * rappelle les ordres de grandeur (5 km de relief, 70 km de croûte).
 *
 * Les trois indices de l'océan disparu — ophiolites, suture, métamorphisme —
 * sont posés au même endroit, parce que c'est ensemble qu'ils font preuve.
 */
export const svt_chaine_montagnes: ScientificSchema = {
  id: 'svt_chaine_montagnes',
  title: 'Chaîne de montagnes — Collision continentale',
  subject: 'svt',
  keywords: ['chaîne de montagnes', 'collision', 'collision continentale', 'orogenèse',
    'racine crustale', 'nappe de charriage', 'pli', 'faille inverse', 'ophiolite',
    'suture', 'moho', 'raccourcissement', 'سلسلة جبلية', 'التصادم القاري'],
  category: 'structure',
  viewBox: '0 0 920 620',
  backgroundColor: '#fdfaf5',
  layers: [
    { id: 'title', label: 'Titre', delay: 0, svgContent: `
      <text x="460" y="34" text-anchor="middle" font-size="27" font-weight="bold" fill="#0f172a" font-family="system-ui">La chaîne de montagnes — collision continentale</text>
      <text x="460" y="62" text-anchor="middle" font-size="15" fill="#475569" font-family="system-ui">السلسلة الجبلية — تصادم قارتين بعد اختفاء المحيط</text>
    `},
    { id: 'manteau', label: 'Manteau', delay: 300, svgContent: `
      <rect x="24" y="300" width="872" height="200" fill="#fdba74" stroke="#ea580c" stroke-width="1.5"/>
      <text x="820" y="470" text-anchor="middle" font-size="15" font-weight="700" fill="#7c2d12" font-family="system-ui">Manteau</text>
    `},
    { id: 'croute', label: 'Croûte continentale', delay: 600, svgContent: `
      <!-- Le relief est modeste, la racine est immense : c'est TOUT le message. -->
      <path d="M 24 250 L 300 250 Q 380 246 420 176 Q 460 130 500 176 Q 540 246 620 250 L 896 250
               L 896 330 Q 700 340 560 366 Q 500 434 460 446 Q 420 434 360 366 Q 220 340 24 330 Z"
            fill="#f5d0a9" stroke="#92400e" stroke-width="2.5"/>
      <text x="150" y="300" font-size="15" font-weight="700" fill="#7c2d12" font-family="system-ui">Croûte continentale</text>
      <text x="150" y="322" font-size="13" fill="#92400e" font-family="system-ui">القشرة القارية</text>
    `},
    { id: 'moho', label: 'Moho', delay: 900, svgContent: `
      <path d="M 24 330 Q 220 340 360 366 Q 420 434 460 446 Q 500 434 560 366 Q 700 340 896 330"
            fill="none" stroke="#1e293b" stroke-width="3" stroke-dasharray="9,5"/>
      <text x="700" y="322" font-size="15" font-weight="800" fill="#1e293b" font-family="system-ui">Moho</text>
      <text x="700" y="300" font-size="12" fill="#334155" font-family="system-ui">limite croûte / manteau</text>
    `},
    { id: 'plis', label: 'Plis et failles', delay: 1100, svgContent: `
      <path d="M 330 244 Q 360 214 392 238 Q 424 208 456 232 Q 488 206 520 230" fill="none" stroke="#92400e" stroke-width="2.5"/>
      <path d="M 336 258 Q 366 230 398 252 Q 430 224 462 246 Q 494 222 526 244" fill="none" stroke="#92400e" stroke-width="2" opacity="0.7"/>
      <line x1="300" y1="268" x2="404" y2="212" stroke="#b91c1c" stroke-width="3"/>
      <path d="M 356 246 L 372 232" stroke="#b91c1c" stroke-width="3" marker-end="url(#arrowRed)"/>
      <text x="196" y="212" font-size="15" font-weight="700" fill="#b91c1c" font-family="system-ui">Faille inverse</text>
      <text x="196" y="232" font-size="13" fill="#b91c1c" font-family="system-ui">et nappe de charriage</text>
      <line x1="296" y1="216" x2="330" y2="240" stroke="#b91c1c" stroke-width="1.8"/>
      <text x="596" y="186" font-size="15" font-weight="700" fill="#92400e" font-family="system-ui">Plis</text>
      <text x="596" y="206" font-size="13" fill="#92400e" font-family="system-ui">الطيات</text>
      <line x1="592" y1="196" x2="528" y2="226" stroke="#92400e" stroke-width="1.8"/>
    `},
    { id: 'suture', label: "Indices de l'océan disparu", delay: 1400, svgContent: `
      <ellipse cx="460" cy="222" rx="26" ry="14" fill="#065f46" stroke="#022c22" stroke-width="2"/>
      <line x1="460" y1="236" x2="460" y2="286" stroke="#065f46" stroke-width="2.5" stroke-dasharray="6,4"/>
      <text x="460" y="112" text-anchor="middle" font-size="15" font-weight="800" fill="#065f46" font-family="system-ui">Ophiolites sur la suture</text>
      <text x="460" y="132" text-anchor="middle" font-size="13" fill="#065f46" font-family="system-ui">restes de l'ancienne croûte océanique</text>
      <line x1="460" y1="140" x2="460" y2="206" stroke="#065f46" stroke-width="1.8"/>
    `},
    { id: 'convergence', label: 'Raccourcissement', delay: 1600, svgContent: `
      <line x1="150" y1="480" x2="256" y2="480" stroke="#1d4ed8" stroke-width="4" marker-end="url(#arrowBlue)"/>
      <line x1="770" y1="480" x2="664" y2="480" stroke="#1d4ed8" stroke-width="4" marker-end="url(#arrowBlue)"/>
      <text x="203" y="470" text-anchor="middle" font-size="14" font-weight="700" fill="#1d4ed8" font-family="system-ui">convergence</text>
      <text x="717" y="470" text-anchor="middle" font-size="14" font-weight="700" fill="#1d4ed8" font-family="system-ui">convergence</text>
      <text x="460" y="486" text-anchor="middle" font-size="15" font-weight="800" fill="#1d4ed8" font-family="system-ui">La croûte se raccourcit et s'épaissit</text>
    `},
    { id: 'bilan', label: 'À retenir', delay: 1800, svgContent: `
      <rect x="24" y="512" width="882" height="92" rx="14" fill="#ffffff" stroke="#f59e0b" stroke-width="2"/>
      <text x="44" y="538" font-size="16" font-weight="800" fill="#b45309" font-family="system-ui">À retenir — ما يجب حفظه</text>
      <text x="44" y="562" font-size="14" fill="#334155" font-family="system-ui">• Le relief visible (≈ 5 km) est petit devant la RACINE crustale (croûte jusqu'à 70 km) : la montagne « flotte ».</text>
      <text x="44" y="586" font-size="14" fill="#334155" font-family="system-ui">• Trois preuves de l'océan disparu : ophiolites, suture, roches métamorphiques de haute pression.</text>
    `},
  ],
  annotations: [
    { id: 'a_racine', x: 380, y: 350, width: 160, height: 90, label: 'Racine crustale', color: '#7c2d12',
      description: "Sous une chaîne, la croûte s'enfonce jusqu'à 70 km. C'est l'équilibre isostatique : ce qui dépasse en haut est porté par ce qui plonge en bas." },
    { id: 'a_ophiolites', x: 428, y: 206, width: 64, height: 32, label: 'Ophiolites', color: '#065f46',
      description: "Fragments de croûte océanique (basaltes, gabbros, péridotites) charriés sur le continent : la preuve qu'un océan existait ici." },
    { id: 'a_plis', x: 330, y: 206, width: 200, height: 56, label: 'Plis et failles inverses', color: '#92400e',
      description: "Marqueurs du raccourcissement : les couches se plissent, se chevauchent, et forment des nappes de charriage." },
    { id: 'a_moho', x: 620, y: 300, width: 170, height: 44, label: 'Moho', color: '#1e293b',
      description: "La limite croûte/manteau plonge sous la chaîne. Sa profondeur mesure l'épaississement." },
  ],
  highlights: [
    { id: 'h_racine', cx: 460, cy: 400, radius: 70, label: 'Racine crustale' },
    { id: 'h_ophiolites', cx: 460, cy: 222, radius: 40, label: 'Ophiolites' },
    { id: 'h_plis', cx: 430, cy: 232, radius: 60, label: 'Plis' },
    { id: 'h_faille', cx: 352, cy: 240, radius: 48, label: 'Faille inverse' },
    { id: 'h_moho', cx: 700, cy: 336, radius: 50, label: 'Moho' },
  ],
};

/**
 * Cellule végétale — le schéma qui manquait, et son absence se voyait.
 *
 * Faute de l'avoir, le tuteur répondait « structure de la cellule végétale »
 * par un TABLEAU organite / rôle. Le tableau était juste, mais on ne peut pas
 * situer une paroi dans un tableau : l'élève doit voir que la vacuole occupe
 * presque tout le volume et REPOUSSE le noyau contre la membrane.
 *
 * Aucun des moteurs ne pouvait le dessiner — ni repère, ni réseau, ni
 * mécanique — et rien n'existait à afficher. Le seul remède était de le
 * dessiner.
 *
 * La composition suit les trois questions du BAC : ce qui entoure (paroi puis
 * membrane, deux traits distincts qu'on confond sans cesse), ce qui occupe
 * (la vacuole), et ce qui est PROPRE au végétal — rappelé en bas, parce que
 * c'est la comparaison qui est demandée, pas la liste.
 */
export const svt_cellule_vegetale: ScientificSchema = {
  id: 'svt_cellule_vegetale',
  title: 'La cellule végétale et ses organites',
  subject: 'svt',
  keywords: ['cellule végétale', 'paroi cellulosique', 'paroi', 'vacuole', 'chloroplaste',
    'chlorophylle', 'photosynthèse', 'membrane plasmique', 'cytoplasme', 'organite',
    'الخلية النباتية', 'الجدار السليلوزي', 'الفجوة'],
  category: 'structure',
  viewBox: '0 0 920 620',
  backgroundColor: '#f7fee7',
  layers: [
    { id: 'title', label: 'Titre', delay: 0, svgContent: `
      <text x="460" y="34" text-anchor="middle" font-size="27" font-weight="bold" fill="#14532d" font-family="system-ui">La cellule végétale et ses organites</text>
      <text x="460" y="60" text-anchor="middle" font-size="15" fill="#3f6212" font-family="system-ui">الخلية النباتية ومكوناتها</text>
    `},
    { id: 'paroi', label: 'Paroi cellulosique', delay: 300, svgContent: `
      <rect x="270" y="96" width="430" height="360" rx="24" fill="#fde68a" stroke="#a16207" stroke-width="8"/>
    `},
    { id: 'membrane', label: 'Membrane et cytoplasme', delay: 600, svgContent: `
      <rect x="286" y="112" width="398" height="328" rx="18" fill="#ecfccb" stroke="#4d7c0f" stroke-width="3"/>
    `},
    { id: 'vacuole', label: 'Vacuole', delay: 900, svgContent: `
      <rect x="330" y="160" width="300" height="190" rx="34" fill="#bfdbfe" fill-opacity="0.9" stroke="#2563eb" stroke-width="2.5"/>
      <text x="480" y="252" text-anchor="middle" font-size="17" font-weight="800" fill="#1e3a8a" font-family="system-ui">Vacuole</text>
      <text x="480" y="276" text-anchor="middle" font-size="13" fill="#1e40af" font-family="system-ui">elle occupe presque tout le volume</text>
    `},
    { id: 'noyau', label: 'Noyau', delay: 1100, svgContent: `
      <circle cx="345" cy="398" r="28" fill="#f5d0a9" stroke="#92400e" stroke-width="2.5"/>
      <circle cx="345" cy="398" r="10" fill="#92400e"/>
    `},
    { id: 'chloroplastes', label: 'Chloroplastes', delay: 1300, svgContent: `
      <g fill="#22c55e" stroke="#15803d" stroke-width="2">
        <ellipse cx="432" cy="398" rx="26" ry="13"/>
        <ellipse cx="500" cy="400" rx="26" ry="13"/>
        <ellipse cx="568" cy="396" rx="26" ry="13"/>
      </g>
      <g stroke="#14532d" stroke-width="1.5" opacity="0.8">
        <line x1="418" y1="398" x2="446" y2="398"/>
        <line x1="486" y1="400" x2="514" y2="400"/>
        <line x1="554" y1="396" x2="582" y2="396"/>
      </g>
    `},
    { id: 'mitochondries', label: 'Mitochondries', delay: 1450, svgContent: `
      <g fill="#f97316" stroke="#c2410c" stroke-width="2">
        <ellipse cx="624" cy="138" rx="16" ry="9"/>
        <ellipse cx="308" cy="248" rx="16" ry="9"/>
      </g>
    `},
    { id: 'legendes', label: 'Légendes', delay: 1600, svgContent: `
      <line x1="274" y1="132" x2="248" y2="146" stroke="#a16207" stroke-width="2"/>
      <text x="242" y="142" text-anchor="end" font-size="16" font-weight="700" fill="#a16207" font-family="system-ui">Paroi cellulosique</text>
      <text x="242" y="162" text-anchor="end" font-size="13" fill="#a16207" font-family="system-ui">الجدار السليلوزي — rigide</text>

      <line x1="288" y1="196" x2="248" y2="212" stroke="#4d7c0f" stroke-width="2"/>
      <text x="242" y="208" text-anchor="end" font-size="16" font-weight="700" fill="#3f6212" font-family="system-ui">Membrane plasmique</text>
      <text x="242" y="228" text-anchor="end" font-size="13" fill="#3f6212" font-family="system-ui">الغشاء السيتوبلازمي</text>

      <line x1="304" y1="290" x2="248" y2="290" stroke="#4d7c0f" stroke-width="2"/>
      <text x="242" y="286" text-anchor="end" font-size="16" font-weight="700" fill="#3f6212" font-family="system-ui">Cytoplasme</text>
      <text x="242" y="306" text-anchor="end" font-size="13" fill="#3f6212" font-family="system-ui">السيتوبلازم</text>

      <line x1="317" y1="398" x2="248" y2="382" stroke="#92400e" stroke-width="2"/>
      <text x="242" y="378" text-anchor="end" font-size="16" font-weight="700" fill="#92400e" font-family="system-ui">Noyau</text>
      <text x="242" y="398" text-anchor="end" font-size="13" fill="#92400e" font-family="system-ui">النواة — repoussé par la vacuole</text>

      <line x1="640" y1="138" x2="726" y2="126" stroke="#c2410c" stroke-width="2"/>
      <text x="732" y="122" font-size="16" font-weight="700" fill="#c2410c" font-family="system-ui">Mitochondrie</text>
      <text x="732" y="142" font-size="13" fill="#c2410c" font-family="system-ui">الميتوكندري — respiration</text>

      <line x1="622" y1="248" x2="726" y2="216" stroke="#1d4ed8" stroke-width="2"/>
      <text x="732" y="212" font-size="16" font-weight="700" fill="#1d4ed8" font-family="system-ui">Vacuole</text>
      <text x="732" y="232" font-size="13" fill="#1d4ed8" font-family="system-ui">الفجوة — eau, sels, pigments</text>

      <line x1="594" y1="392" x2="726" y2="330" stroke="#15803d" stroke-width="2"/>
      <text x="732" y="326" font-size="16" font-weight="700" fill="#15803d" font-family="system-ui">Chloroplaste</text>
      <text x="732" y="346" font-size="13" fill="#15803d" font-family="system-ui">البلاستيدة الخضراء</text>
      <text x="732" y="366" font-size="13" fill="#15803d" font-family="system-ui">siège de la photosynthèse</text>
    `},
    { id: 'comparaison', label: 'Végétal vs animal', delay: 1900, svgContent: `
      <rect x="24" y="480" width="872" height="124" rx="14" fill="#ffffff" stroke="#65a30d" stroke-width="2"/>
      <text x="44" y="508" font-size="17" font-weight="800" fill="#3f6212" font-family="system-ui">Ce que la cellule ANIMALE n'a pas — ما يميز الخلية النباتية</text>
      <rect x="44" y="522" width="16" height="16" rx="4" fill="#fde68a" stroke="#a16207" stroke-width="2"/>
      <text x="70" y="536" font-size="14" fill="#334155" font-family="system-ui">la PAROI cellulosique, qui rigidifie et donne sa forme à la cellule ;</text>
      <rect x="44" y="548" width="16" height="16" rx="4" fill="#bfdbfe" stroke="#2563eb" stroke-width="2"/>
      <text x="70" y="562" font-size="14" fill="#334155" font-family="system-ui">une GRANDE vacuole, qui stocke l'eau et pousse le reste contre la membrane ;</text>
      <rect x="44" y="574" width="16" height="16" rx="4" fill="#22c55e" stroke="#15803d" stroke-width="2"/>
      <text x="70" y="588" font-size="14" fill="#334155" font-family="system-ui">les CHLOROPLASTES, où se fait la photosynthèse. Noyau, cytoplasme et mitochondries, eux, sont communs.</text>
    `},
  ],
  annotations: [
    { id: 'a_paroi', x: 270, y: 96, width: 430, height: 20, label: 'Paroi cellulosique', color: '#a16207',
      description: "Enveloppe rigide de cellulose, à l'extérieur de la membrane. Elle donne sa forme à la cellule et l'empêche d'éclater quand elle absorbe l'eau." },
    { id: 'a_vacuole', x: 330, y: 160, width: 300, height: 190, label: 'Vacuole', color: '#2563eb',
      description: "Poche remplie de suc cellulaire. Chez une cellule végétale adulte, elle occupe l'essentiel du volume et plaque le cytoplasme contre la membrane." },
    { id: 'a_chloroplastes', x: 400, y: 378, width: 200, height: 44, label: 'Chloroplastes', color: '#15803d',
      description: "Organites verts contenant la chlorophylle : ils captent la lumière et réalisent la photosynthèse." },
    { id: 'a_noyau', x: 313, y: 366, width: 64, height: 64, label: 'Noyau', color: '#92400e',
      description: "Il contient l'information génétique. Repoussé en périphérie par la vacuole — position typique de la cellule végétale." },
  ],
  highlights: [
    { id: 'h_paroi', cx: 274, cy: 200, radius: 40, label: 'Paroi cellulosique' },
    { id: 'h_membrane', cx: 288, cy: 300, radius: 34, label: 'Membrane plasmique' },
    { id: 'h_vacuole', cx: 480, cy: 254, radius: 90, label: 'Vacuole' },
    { id: 'h_noyau', cx: 345, cy: 398, radius: 42, label: 'Noyau' },
    { id: 'h_chloroplastes', cx: 500, cy: 398, radius: 60, label: 'Chloroplastes' },
    { id: 'h_mitochondries', cx: 624, cy: 138, radius: 32, label: 'Mitochondries' },
  ],
};

export const SVT_SCHEMAS = [
  svt_cellule_vegetale,
  svt_dorsale_accretion,
  svt_metamorphisme,
  svt_chaine_montagnes,
  svt_glycolyse,
  svt_respiration_cellulaire,
  svt_fermentation,
  svt_muscle_sarcomere,
  svt_adn_structure,
  svt_transcription_traduction,
  svt_mitose,
  svt_subduction,
  svt_cellule_mitochondrie,
  svt_mitochondrie_structure,
  svt_chaine_respiratoire,
  svt_cycle_krebs,
  svt_fibre_musculaire,
  svt_bilan_energetique,
];
