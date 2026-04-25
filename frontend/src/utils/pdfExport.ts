/**
 * PDF Export utility for MathBoard content
 * Generates formatted documents with chalkboard colors preserved
 */
import html2canvas from 'html2canvas';
import { jsPDF } from 'jspdf';

interface BoardLine {
  type: string;
  content: string;
  color?: string;
  label?: string;
  [key: string]: any;
}

/**
 * Strip LaTeX and HTML from text for plain text export
 */
function stripFormatting(text: string): string {
  if (!text) return '';
  
  // Remove LaTeX delimiters but keep the content
  let cleaned = text.replace(/\$\$(.*?)\$\$/g, '$1');
  cleaned = cleaned.replace(/\$(.*?)\$/g, '$1');
  
  // Remove HTML tags
  cleaned = cleaned.replace(/<[^>]*>/g, '');
  
  // Decode HTML entities
  const textarea = document.createElement('textarea');
  textarea.innerHTML = cleaned;
  cleaned = textarea.value;
  
  // Clean up whitespace
  cleaned = cleaned.replace(/\s+/g, ' ').trim();
  
  return cleaned;
}

/**
 * Generate printable HTML from board lines
 */
export function generatePrintableHTML(lines: BoardLine[], title?: string): string {
  const html = `
<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${title || 'Tableau de cours'}</title>
  <style>
    @page {
      size: A4;
      margin: 2cm;
    }
    
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
      -webkit-print-color-adjust: exact !important;
      print-color-adjust: exact !important;
      color-adjust: exact !important;
    }
    
    body {
      font-family: 'Segoe UI', 'Arial', sans-serif;
      font-size: 12pt;
      line-height: 1.7;
      color: #000;
      background: #fff;
      padding: 30px;
      max-width: 210mm;
      margin: 0 auto;
    }
    
    .board-title {
      font-size: 20pt;
      font-weight: bold;
      text-align: center;
      margin-bottom: 20px;
      padding-bottom: 12px;
      border-bottom: 3px solid #0055cc;
      color: #0055cc;
    }
    
    .line {
      margin-bottom: 12px;
      page-break-inside: avoid;
    }
    
    .line-title {
      font-size: 16pt;
      font-weight: bold;
      margin-top: 18px;
      margin-bottom: 10px;
      color: #cc0000;
      border-bottom: 2px solid #cc0000;
      padding-bottom: 4px;
    }
    
    .line-subtitle {
      font-size: 14pt;
      font-weight: bold;
      margin-top: 14px;
      margin-bottom: 8px;
      color: #0055cc;
    }
    
    .line-text {
      font-size: 12pt;
      margin-bottom: 8px;
      color: #000;
    }
    
    .line-math {
      font-size: 13pt;
      font-family: 'Times New Roman', serif;
      text-align: center;
      margin: 15px 0;
      padding: 12px;
      background: #f0f4ff;
      border: 1px solid #ccdaff;
      border-radius: 6px;
      color: #0033aa;
    }
    
    .line-step {
      margin-left: 20px;
      margin-bottom: 8px;
      color: #000;
    }
    
    .line-step::before {
      content: attr(data-label) ". ";
      font-weight: bold;
      color: #007a33;
      margin-right: 5px;
    }
    
    .line-box {
      border: 2px solid #0055cc;
      padding: 12px;
      margin: 12px 0;
      background: #f0f6ff;
      border-radius: 6px;
      color: #000;
    }
    
    .line-note {
      border-left: 4px solid #0055cc;
      padding: 8px 12px;
      margin: 10px 0;
      background: #eef4ff;
      color: #003399;
    }
    
    .line-note::before {
      content: "� ";
      font-weight: bold;
    }
    
    .line-warning {
      border-left: 4px solid #cc0000;
      padding: 8px 12px;
      margin: 10px 0;
      background: #fff0f0;
      color: #cc0000;
    }
    
    .line-warning::before {
      content: "⚠️ ";
      font-weight: bold;
    }
    
    .line-tip {
      border-left: 4px solid #007a33;
      padding: 8px 12px;
      margin: 10px 0;
      background: #f0fff4;
      color: #007a33;
    }
    
    .line-tip::before {
      content: "✅ ";
      font-weight: bold;
    }
    
    .line-separator {
      border-top: 1px solid #ccc;
      margin: 15px 0;
    }
    
    .line-table {
      width: 100%;
      border-collapse: collapse;
      margin: 15px 0;
    }
    
    .line-table th,
    .line-table td {
      border: 1px solid #999;
      padding: 8px;
      text-align: left;
      color: #000;
    }
    
    .line-table th {
      background: #e8f0fe;
      font-weight: bold;
      color: #0055cc;
    }
    
    .line-table td {
      background: #fff;
    }
    
    @media print {
      body {
        padding: 0;
        background: #fff !important;
      }
      
      .no-print {
        display: none !important;
      }
    }
  </style>
</head>
<body>
  ${title ? `<div class="board-title">${stripFormatting(title)}</div>` : ''}
  
  ${lines.map(line => renderLine(line)).join('\n')}
  
  <script>
    // Auto-print when opened
    window.onload = function() {
      window.print();
    };
  </script>
</body>
</html>
  `;
  
  return html;
}

function renderLine(line: BoardLine): string {
  const content = stripFormatting(line.content || '');
  
  switch (line.type) {
    case 'title':
      return `<div class="line line-title">${content}</div>`;
    
    case 'subtitle':
      return `<div class="line line-subtitle">${content}</div>`;
    
    case 'text':
      return `<div class="line line-text">${content}</div>`;
    
    case 'math':
      return `<div class="line line-math">${content}</div>`;
    
    case 'step':
      return `<div class="line line-step" data-label="${line.label || '•'}">${content}</div>`;
    
    case 'box':
      return `<div class="line line-box">${content}</div>`;
    
    case 'note':
      return `<div class="line line-note">${content}</div>`;
    
    case 'warning':
      return `<div class="line line-warning">${content}</div>`;
    
    case 'tip':
      return `<div class="line line-tip">${content}</div>`;
    
    case 'separator':
      return `<div class="line line-separator"></div>`;
    
    case 'table':
      if (line.headers && line.rows) {
        return `
          <table class="line line-table">
            <thead>
              <tr>
                ${line.headers.map((h: string) => `<th>${stripFormatting(h)}</th>`).join('')}
              </tr>
            </thead>
            <tbody>
              ${line.rows.map((row: string[]) => `
                <tr>
                  ${row.map((cell: string) => `<td>${stripFormatting(cell)}</td>`).join('')}
                </tr>
              `).join('')}
            </tbody>
          </table>
        `;
      }
      return '';
    
    case 'qcm':
      if (line.choices) {
        return `
          <div class="line line-box">
            <div style="font-weight: bold; margin-bottom: 8px;">${content}</div>
            ${line.choices.map((choice: string, i: number) => `
              <div style="margin-left: 15px;">
                ${String.fromCharCode(65 + i)}. ${stripFormatting(choice)}
              </div>
            `).join('')}
          </div>
        `;
      }
      return '';
    
    case 'vrai_faux':
      if (line.statements) {
        return `
          <div class="line line-box">
            <div style="font-weight: bold; margin-bottom: 8px;">${content}</div>
            ${line.statements.map((stmt: any, i: number) => `
              <div style="margin-left: 15px; margin-bottom: 5px;">
                ${i + 1}. ${stripFormatting(stmt.text)} : _____
              </div>
            `).join('')}
          </div>
        `;
      }
      return '';
    
    case 'association':
      if (line.pairs) {
        return `
          <div class="line line-box">
            <div style="font-weight: bold; margin-bottom: 8px;">${content}</div>
            <div style="display: flex; justify-content: space-between;">
              <div style="width: 45%;">
                ${line.pairs.map((pair: any, i: number) => `
                  <div style="margin-bottom: 5px;">${i + 1}. ${stripFormatting(pair.left)}</div>
                `).join('')}
              </div>
              <div style="width: 45%;">
                ${line.pairs.map((pair: any, i: number) => `
                  <div style="margin-bottom: 5px;">${String.fromCharCode(65 + i)}. ${stripFormatting(pair.right)}</div>
                `).join('')}
              </div>
            </div>
          </div>
        `;
      }
      return '';
    
    case 'diagram':
      // For diagram/mindmap, list the nodes hierarchically
      if (line.nodes) {
        const nodes = line.nodes as any[];
        const central = nodes.find((n: any) => n.id === 'centre' || n.id === 'center' || n.id === 'central') || nodes[0];
        const otherNodes = nodes.filter((n: any) => n !== central);
        
        return `
          <div class="line line-box">
            <div style="font-weight: bold; text-align: center; margin-bottom: 10px; font-size: 14pt; border-bottom: 1px solid #ccc; padding-bottom: 8px;">
              🧠 ${central ? stripFormatting(central.label) : (content || 'Carte Mentale')}
            </div>
            <div style="display: flex; flex-wrap: wrap; gap: 10px; justify-content: center;">
              ${otherNodes.map((node: any) => `
                <div style="background: #f0f0f0; padding: 8px 12px; border-radius: 8px; border: 1px solid #ddd; min-width: 100px; text-align: center;">
                  ${stripFormatting(node.label)}
                </div>
              `).join('')}
            </div>
          </div>
        `;
      }
      return '';
    
    case 'mindmap':
      // For mindmap, just list the nodes hierarchically
      if (line.mindmapNodes) {
        const nodes = line.mindmapNodes as any[];
        const central = nodes.find((n: any) => n.level === 0);
        const level1 = nodes.filter((n: any) => n.level === 1);
        
        return `
          <div class="line line-box">
            <div style="font-weight: bold; text-align: center; margin-bottom: 10px; font-size: 14pt;">
              ${central ? stripFormatting(central.label) : content}
            </div>
            ${level1.map((node: any) => {
              const children = nodes.filter((n: any) => n.parent === node.id);
              return `
                <div style="margin-left: 15px; margin-bottom: 8px;">
                  <div style="font-weight: bold;">• ${stripFormatting(node.label)}</div>
                  ${children.map((child: any) => `
                    <div style="margin-left: 25px;">- ${stripFormatting(child.label)}</div>
                  `).join('')}
                </div>
              `;
            }).join('')}
          </div>
        `;
      }
      return '';
    
    default:
      return `<div class="line line-text">${content}</div>`;
  }
}

/**
 * Open print dialog with formatted content
 */
export function printBoard(lines: BoardLine[], title?: string): void {
  const html = generatePrintableHTML(lines, title);
  
  // Create a blob and open it
  const blob = new Blob([html], { type: 'text/html;charset=utf-8' });
  const url = URL.createObjectURL(blob);
  
  const printWindow = window.open(url, '_blank', 'width=800,height=600');
  
  if (printWindow) {
    printWindow.onload = () => {
      setTimeout(() => {
        printWindow.print();
      }, 500);
    };
  } else {
    // Fallback: create an iframe
    const iframe = document.createElement('iframe');
    iframe.style.position = 'fixed';
    iframe.style.right = '0';
    iframe.style.bottom = '0';
    iframe.style.width = '0';
    iframe.style.height = '0';
    iframe.style.border = 'none';
    document.body.appendChild(iframe);
    
    const iframeDoc = iframe.contentDocument || iframe.contentWindow?.document;
    if (iframeDoc) {
      iframeDoc.open();
      iframeDoc.write(html);
      iframeDoc.close();
      
      setTimeout(() => {
        iframe.contentWindow?.print();
        setTimeout(() => {
          document.body.removeChild(iframe);
        }, 1000);
      }, 500);
    }
  }
  
  // Clean up blob URL after a delay
  setTimeout(() => URL.revokeObjectURL(url), 60000);
}

/**
 * Download board as a real .pdf file (direct download, no print dialog).
 * Renders the styled HTML in a hidden iframe, captures with html2canvas, builds PDF with jsPDF.
 */
export async function downloadAsPDF(lines: BoardLine[], title?: string): Promise<void> {
  const filename = (title || 'tableau-cours').replace(/[^a-zA-Z0-9\u00C0-\u017F]/g, '-').replace(/-+/g, '-').toLowerCase() + '.pdf';

  try {
    // Build the same styled HTML (without auto-print script)
    const html = generatePrintableHTML(lines, title)
      .replace(
        `<script>\n    // Auto-print when opened\n    window.onload = function() {\n      window.print();\n    };\n  </script>`,
        ''
      );

    // Render in hidden iframe
    const canvas = await renderHtmlToCanvas(html);

    const imgW = canvas.width;
    const imgH = canvas.height;

    // A4 in mm
    const pdfW = 210;
    const pdfH = 297;
    const margin = 10;
    const contentW = pdfW - margin * 2;

    const ratio = contentW / imgW;
    const pageContentH = pdfH - margin * 2;
    const scaledH = imgH * ratio;
    const totalPages = Math.max(1, Math.ceil(scaledH / pageContentH));

    const pdf = new jsPDF({ orientation: 'portrait', unit: 'mm', format: 'a4' });

    for (let page = 0; page < totalPages; page++) {
      if (page > 0) pdf.addPage();

      // White background
      pdf.setFillColor(255, 255, 255);
      pdf.rect(0, 0, pdfW, pdfH, 'F');

      const srcY = (page * pageContentH) / ratio;
      const srcH = Math.min(pageContentH / ratio, imgH - srcY);
      const destH = srcH * ratio;

      const sliceCanvas = document.createElement('canvas');
      sliceCanvas.width = imgW;
      sliceCanvas.height = Math.ceil(srcH);
      const ctx = sliceCanvas.getContext('2d');
      if (ctx) {
        ctx.drawImage(canvas, 0, srcY, imgW, srcH, 0, 0, imgW, srcH);
        const sliceData = sliceCanvas.toDataURL('image/png');
        pdf.addImage(sliceData, 'PNG', margin, margin, contentW, destH);
      }
    }

    pdf.save(filename);
  } catch (err) {
    console.error('[pdfExport] PDF generation failed:', err);
    // Fallback: open printable HTML
    const html = generatePrintableHTML(lines, title);
    const blob = new Blob([html], { type: 'text/html;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    window.open(url, '_blank');
    setTimeout(() => URL.revokeObjectURL(url), 60000);
  }
}

/**
 * Render HTML in a hidden iframe and capture with html2canvas.
 */
function renderHtmlToCanvas(html: string): Promise<HTMLCanvasElement> {
  return new Promise((resolve, reject) => {
    const iframe = document.createElement('iframe');
    iframe.style.position = 'fixed';
    iframe.style.left = '-9999px';
    iframe.style.top = '0';
    iframe.style.width = '794px'; // A4 width in px at 96dpi
    iframe.style.height = '3000px';
    iframe.style.border = 'none';
    iframe.style.opacity = '0';
    document.body.appendChild(iframe);

    const iframeDoc = iframe.contentDocument || iframe.contentWindow?.document;
    if (!iframeDoc) {
      document.body.removeChild(iframe);
      reject(new Error('Cannot access iframe document'));
      return;
    }

    iframeDoc.open();
    iframeDoc.write(html);
    iframeDoc.close();

    // Wait for fonts + layout
    setTimeout(async () => {
      try {
        const body = iframeDoc.body;
        const canvas = await html2canvas(body, {
          backgroundColor: '#ffffff',
          scale: 2,
          useCORS: true,
          logging: false,
          windowWidth: 794,
        });
        resolve(canvas);
      } catch (e) {
        reject(e);
      } finally {
        document.body.removeChild(iframe);
      }
    }, 600);
  });
}
