/* ════════════════════════════════════════════════════════════
   Moalim — Umami Analytics Loader
   ────────────────────────────────────────────────────────────
   Ce fichier est inclus dans TOUTES les pages publiques :
   - frontend/index.html (SPA React)
   - frontend/public/about.html, contact.html, mentions-legales.html
   - frontend/public/blog/*.html

   POUR ACTIVER LE TRACKING :
   1) Setup Umami sur le VPS (cf. deploy/umami/README.md)
   2) Crée un site dans Umami → copie le Website ID (UUID)
   3) Remplace ci-dessous WEBSITE_ID par ton UUID réel
   4) Redéploie : remote-deploy.ps1 -UpdateOnly
   ════════════════════════════════════════════════════════════ */

(function () {
  // ⚠️ REMPLACE CETTE VALEUR PAR TON UMAMI WEBSITE ID
  var WEBSITE_ID = "WEBSITE_ID_PLACEHOLDER";

  // URL du serveur Umami self-hosted
  var UMAMI_URL = "https://analytics.moalim.online";

  // Sécurité : ne charge rien tant que le placeholder n'est pas remplacé
  if (WEBSITE_ID === "WEBSITE_ID_PLACEHOLDER" || !WEBSITE_ID) {
    if (window.console && console.info) {
      console.info("[Moalim Analytics] Tracking inactif. Configure WEBSITE_ID dans /js/umami.js");
    }
    return;
  }

  // Pas de tracking en local (dev) sauf si forcé via ?umami=1
  var isLocal = /^(localhost|127\.|192\.168\.|0\.0\.0\.0)/.test(window.location.hostname);
  var force = window.location.search.indexOf("umami=1") !== -1;
  if (isLocal && !force) {
    return;
  }

  // Charge le script Umami de manière non-bloquante
  var s = document.createElement("script");
  s.async = true;
  s.defer = true;
  s.src = UMAMI_URL + "/script.js";
  s.setAttribute("data-website-id", WEBSITE_ID);
  // Désactive le tracking auto sur les pages où l'on veut un contrôle manuel
  // (laisse activé par défaut)
  // s.setAttribute("data-auto-track", "false");
  document.head.appendChild(s);

  // Expose un helper global pour les events custom React
  window.moalimTrack = function (eventName, eventData) {
    if (window.umami && typeof window.umami.track === "function") {
      try {
        if (eventData) {
          window.umami.track(eventName, eventData);
        } else {
          window.umami.track(eventName);
        }
      } catch (e) {
        // silent fail
      }
    }
  };
})();
