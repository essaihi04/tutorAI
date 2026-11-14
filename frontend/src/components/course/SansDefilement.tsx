import { useLayoutEffect, useRef, type CSSProperties, type ReactNode } from 'react';

/**
 * Un tableau montré à l'élève tient TOUT ENTIER dans l'écran, sans défiler (user rule, 12 novembre 2026 — skill
 * cours-concentration « The screen »). Le contenu est mis à l'échelle (`zoom`) pour remplir la place disponible :
 * réduit s'il déborde, agrandi jusqu'à `agrandirMax` s'il reste de la place. Recalculé quand la place change
 * ou quand une ligne s'ajoute (la craie qui écrit).
 */
export default function SansDefilement({ children, agrandirMax = 1, className = '', style, centrer = false }: {
  children: ReactNode; agrandirMax?: number; className?: string; style?: CSSProperties; centrer?: boolean;
}) {
  const zone = useRef<HTMLDivElement>(null);
  const contenu = useRef<HTMLDivElement>(null);
  useLayoutEffect(() => {
    const z = zone.current, c = contenu.current;
    if (!z || !c) return;
    let derniere = 1, frame = 0;
    const ajuster = () => {
      cancelAnimationFrame(frame);
      frame = requestAnimationFrame(() => {
        const cs = getComputedStyle(z);
        const H = z.clientHeight - parseFloat(cs.paddingTop) - parseFloat(cs.paddingBottom);
        const W = z.clientWidth - parseFloat(cs.paddingLeft) - parseFloat(cs.paddingRight);
        c.style.zoom = '1';
        c.style.width = `${W}px`;
        const h = c.scrollHeight, w = c.scrollWidth;
        let s = Math.min(agrandirMax, h > 0 ? H / h : 1, w > 0 ? W / w : 1);
        // agrandi, le texte revient à la ligne autrement : on vérifie, et on recule jusqu'à ce que tout tienne
        for (let i = 0; i < 12; i++) {
          c.style.zoom = String(s);
          c.style.width = `${W / s}px`;
          if (c.scrollHeight * s <= H + 1 && c.scrollWidth * s <= W + 1) break;
          s *= 0.94;
        }
        derniere = s;
      });
    };
    ajuster();
    const ro = new ResizeObserver(ajuster);
    ro.observe(z);
    const mo = new MutationObserver(ajuster);
    mo.observe(c, { childList: true, subtree: true, characterData: true });
    return () => { ro.disconnect(); mo.disconnect(); cancelAnimationFrame(frame); void derniere; };
  }, [agrandirMax]);
  return (
    <div ref={zone} className={`min-h-0 flex-1 overflow-hidden ${centrer ? 'flex flex-col justify-center' : ''} ${className}`} style={style}>
      <div ref={contenu} style={{ transformOrigin: 'top left' }}>{children}</div>
    </div>
  );
}
