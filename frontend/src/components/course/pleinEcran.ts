import { useEffect, useState } from 'react';

/**
 * Plein écran « diaporama » du lecteur de cours (17 novembre 2026) : c'est le lecteur lui-même qui prend l'écran,
 * pas la page. La barre du site, la colonne de la séance et la barre du navigateur disparaissent ; le tableau, les
 * simulations, le cahier et le tuteur (son portail suit `document.fullscreenElement`) gardent toute la place.
 * Sur téléphone en paysage, c'est aussi ce qui cache la barre d'adresse.
 *
 * Sans l'API (iPhone) ou si le navigateur la refuse, le lecteur couvre au moins toute la page (`data-plein-page`,
 * `fixed inset-0 z-[100]` dans index.css) : la barre du site et la colonne de la séance disparaissent quand même.
 */
const EVENEMENT = 'moalim-plein-ecran';
const lecteur = () => document.querySelector<HTMLElement>('[data-lecteur-cours]');

const enPage = () => !!lecteur()?.hasAttribute('data-plein-page');
const estPlein = () => typeof document !== 'undefined' && (!!document.fullscreenElement || enPage());

function poserPage(oui: boolean) {
  const el = lecteur();
  if (!el) return;
  if (oui) el.setAttribute('data-plein-page', '');
  else el.removeAttribute('data-plein-page');
  window.dispatchEvent(new Event(EVENEMENT));
  window.dispatchEvent(new Event('resize'));   // les simulations et le tuteur se recalent sur la nouvelle taille
}

export function entrerPleinEcran() {
  if (estPlein()) return;
  const el = lecteur();
  if (el && document.fullscreenEnabled && el.requestFullscreen)
    void el.requestFullscreen({ navigationUI: 'hide' }).catch(() => poserPage(true));
  else poserPage(true);
}

export function quitterPleinEcran() {
  if (document.fullscreenElement) void document.exitFullscreen?.().catch(() => {});
  if (enPage()) poserPage(false);
}

export function basculerPleinEcran() {
  if (estPlein()) quitterPleinEcran();
  else entrerPleinEcran();
}

export function usePleinEcran() {
  const [plein, setPlein] = useState(estPlein);
  useEffect(() => {
    const suivre = () => setPlein(estPlein());
    // Échap sort aussi du plein écran de secours, comme du vrai
    const echap = (e: KeyboardEvent) => { if (e.key === 'Escape' && enPage() && !document.fullscreenElement) poserPage(false); };
    document.addEventListener('fullscreenchange', suivre);
    window.addEventListener(EVENEMENT, suivre);
    window.addEventListener('keydown', echap);
    return () => {
      document.removeEventListener('fullscreenchange', suivre);
      window.removeEventListener(EVENEMENT, suivre);
      window.removeEventListener('keydown', echap);
    };
  }, []);
  return plein;
}
