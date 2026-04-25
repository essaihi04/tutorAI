import { useState, useEffect, useRef } from 'react';

interface MediaResource {
  type: 'image' | 'simulation' | 'video';
  url: string;
  caption?: string;
  trigger?: string;
}

interface MediaViewerProps {
  media: MediaResource | null;
  onClose?: () => void;
  onSimulationUpdate?: (state: any) => void;
}

export function MediaViewer({ media, onClose, onSimulationUpdate }: MediaViewerProps) {
  const [imageError, setImageError] = useState(false);
  const [imageLoading, setImageLoading] = useState(true);
  const iframeRef = useRef<HTMLIFrameElement>(null);

  useEffect(() => {
    const handleSimulationMessage = (event: MessageEvent) => {
      if (event.data.type === 'simulation_state') {
        console.log('[MediaViewer] Simulation state received:', event.data);
        if (onSimulationUpdate) {
          onSimulationUpdate(event.data);
        }
      }
    };

    window.addEventListener('message', handleSimulationMessage);
    return () => window.removeEventListener('message', handleSimulationMessage);
  }, [onSimulationUpdate]);

  if (!media) return null;

  // Convert local paths to proper URLs or clean Supabase URLs
  let cleanUrl = media.url;
  
  // If it's a local path starting with /media/, it's a legacy resource
  // These files don't exist anymore, so we'll show an error
  if (cleanUrl.startsWith('/media/')) {
    // For now, we'll let it try to load and fail gracefully
    cleanUrl = media.url;
  } else if (cleanUrl.endsWith('?')) {
    // Clean Supabase URLs by removing trailing '?'
    cleanUrl = cleanUrl.slice(0, -1);
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg max-w-4xl w-full max-h-[90vh] overflow-auto">
        {/* Header */}
        <div className="flex justify-between items-center p-4 border-b">
          <h3 className="text-lg font-semibold">
            {media.type === 'image' && '📸 Image'}
            {media.type === 'simulation' && '🔬 Simulation Interactive'}
            {media.type === 'video' && '🎥 Vidéo'}
          </h3>
          {onClose && (
            <button
              onClick={onClose}
              className="text-gray-500 hover:text-gray-700 text-2xl"
              aria-label="Fermer"
            >
              ×
            </button>
          )}
        </div>

        {/* Content */}
        <div className="p-6">
          {media.type === 'image' && (
            <div className="space-y-4">
              {imageLoading && (
                <div className="flex items-center justify-center py-8">
                  <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
                </div>
              )}
              {imageError && (
                <div className="text-center py-8">
                  <p className="text-red-600 mb-2">❌ Erreur de chargement de l'image</p>
                  <p className="text-sm text-gray-500">URL: {cleanUrl}</p>
                </div>
              )}
              <img
                src={cleanUrl}
                alt={media.caption || 'Image explicative'}
                className={`w-full h-auto rounded-lg shadow-lg ${imageLoading || imageError ? 'hidden' : ''}`}
                onLoad={() => setImageLoading(false)}
                onError={() => {
                  setImageError(true);
                  setImageLoading(false);
                  console.error('[MediaViewer] Failed to load image:', cleanUrl);
                }}
              />
              {media.caption && !imageError && (
                <p className="text-center text-gray-600 italic">{media.caption}</p>
              )}
            </div>
          )}

          {media.type === 'simulation' && (
            <div className="space-y-4">
              <iframe
                ref={iframeRef}
                src={media.url}
                className="w-full h-[600px] rounded-lg border-2 border-gray-200"
                title="Simulation interactive"
                allowFullScreen
              />
              {media.caption && (
                <p className="text-center text-gray-600 italic">{media.caption}</p>
              )}
            </div>
          )}

          {media.type === 'video' && (
            <div className="space-y-4">
              <video
                src={media.url}
                controls
                className="w-full h-auto rounded-lg shadow-lg"
              >
                Votre navigateur ne supporte pas la lecture de vidéos.
              </video>
              {media.caption && (
                <p className="text-center text-gray-600 italic">{media.caption}</p>
              )}
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="p-4 border-t bg-gray-50 rounded-b-lg">
          <p className="text-sm text-gray-500 text-center">
            💡 Prends le temps d'observer et de comprendre avant de continuer
          </p>
        </div>
      </div>
    </div>
  );
}

// Composant pour afficher les médias dans le contexte de la session
interface SessionMediaDisplayProps {
  media: MediaResource | null;
  isVisible: boolean;
  onSimulationUpdate?: (state: any) => void;
}

function buildSimulationHtml(url: string): string | null {
  if (!url.startsWith('data:text/html')) {
    return null;
  }

  const firstCommaIndex = url.indexOf(',');
  if (firstCommaIndex === -1) {
    return null;
  }

  const encodedHtml = url.slice(firstCommaIndex + 1);
  const html = decodeURIComponent(encodedHtml);

  if (html.includes('window.__AI_AUTOSTART_BRIDGE__')) {
    return html;
  }

  const injectedBridge = `
<script>
window.__AI_AUTOSTART_BRIDGE__ = true;
(function () {
  // ---- Generic guidance overlay ----
  function showGuidanceMessage(text) {
    if (!text) return;
    var old = document.getElementById('ai-guidance-msg');
    if (old) old.remove();
    var el = document.createElement('div');
    el.id = 'ai-guidance-msg';
    el.style.cssText = 'position:fixed;top:12px;left:50%;transform:translateX(-50%);background:#2563eb;color:#fff;padding:12px 18px;border-radius:8px;box-shadow:0 4px 12px rgba(0,0,0,.2);z-index:9999;max-width:85%;text-align:center;font-size:14px;line-height:1.4;';
    el.textContent = text;
    document.body.appendChild(el);
    setTimeout(function(){ if(el.parentNode) el.parentNode.removeChild(el); }, 5000);
  }

  // ---- Discover what the simulation exposes ----
  function discoverCapabilities() {
    var caps = { commands: [], buttons: [], globals: [] };
    // Check standard template functions
    var fnNames = ['executeAICommand','simulate','startSimulation','resetSimulation',
                   'pauseSimulation','setParameter','runSimulation','runVariant','setO2State','contract','relax'];
    for (var i = 0; i < fnNames.length; i++) {
      if (typeof window[fnNames[i]] === 'function') caps.globals.push(fnNames[i]);
    }
    // Check for SIMULATION_CONFIG (template-based)
    // const variables aren't on window, so also parse from script text
    var simCfg = window.SIMULATION_CONFIG || null;
    if (!simCfg) {
      try { simCfg = SIMULATION_CONFIG; } catch(e) { /* const not accessible from IIFE */ }
    }
    if (!simCfg) { simCfg = _parseSIMULATION_CONFIG(); }
    if (simCfg) {
      try { caps.config = JSON.parse(JSON.stringify(simCfg)); } catch(e) { /* ignore */ }
    }
    // Discover clickable buttons
    var btns = document.querySelectorAll('button');
    for (var j = 0; j < btns.length; j++) {
      var b = btns[j];
      caps.buttons.push({
        id: b.id || null,
        text: (b.textContent || '').trim().substring(0, 60),
        className: b.className || null,
        disabled: b.disabled
      });
    }
    // Standard commands we can always handle
    caps.commands = ['start','reset','click_button','call_function'];
    return caps;
  }

  // ---- Parse SIMULATION_CONFIG from script text (fallback for const) ----
  var _parsedConfig = null;
  function _parseSIMULATION_CONFIG() {
    if (_parsedConfig) return _parsedConfig;
    var scripts = document.querySelectorAll('script');
    for (var i = 0; i < scripts.length; i++) {
      var txt = scripts[i].textContent || '';
      // Find SIMULATION_CONFIG = { ... } block
      var idx = txt.indexOf('SIMULATION_CONFIG');
      if (idx === -1) continue;
      // Find the opening brace
      var braceStart = txt.indexOf('{', idx);
      if (braceStart === -1) continue;
      // Count braces to find the matching close
      var depth = 0; var end = braceStart;
      for (var c = braceStart; c < txt.length && c < braceStart + 5000; c++) {
        if (txt[c] === '{') depth++;
        else if (txt[c] === '}') { depth--; if (depth === 0) { end = c + 1; break; } }
      }
      if (depth !== 0) continue;
      var objStr = txt.substring(braceStart, end);
      // Clean JS object to valid JSON: add quotes to keys, handle trailing commas
      try {
        // Simple approach: extract id and variants via regex
        var idMatch = objStr.match(/id\s*:\s*['"]([^'"]+)['"]/);
        var parsed = { id: idMatch ? idMatch[1] : null, variants: [], objectives: [] };
        // Extract variants array
        var variantsMatch = objStr.match(/variants\s*:\s*\[([\s\S]*?)\]\s*,/);
        if (variantsMatch) {
          var varBlock = variantsMatch[1];
          var varRegex = /\{[^}]*id\s*:\s*['"]([^'"]+)['"][^}]*label\s*:\s*['"]([^'"]+)['"][^}]*\}/g;
          var vm;
          while ((vm = varRegex.exec(varBlock)) !== null) {
            parsed.variants.push({ id: vm[1], label: vm[2] });
          }
        }
        if (parsed.id) { _parsedConfig = parsed; return parsed; }
      } catch(e) { /* parsing failed */ }
    }
    return null;
  }

  // ---- Detect the real simulation_id from the page ----
  var _detectedSimId = null;
  function detectSimulationId() {
    if (_detectedSimId) return _detectedSimId;
    // 1) SIMULATION_CONFIG via scope or window
    var _cfg = window.SIMULATION_CONFIG || null;
    try { if (!_cfg) _cfg = SIMULATION_CONFIG; } catch(e) {}
    if (_cfg && _cfg.id) { _detectedSimId = _cfg.id; return _detectedSimId; }
    // 2) Parse SIMULATION_CONFIG from script text (handles const)
    var parsed = _parseSIMULATION_CONFIG();
    if (parsed && parsed.id) { _detectedSimId = parsed.id; return _detectedSimId; }
    // 3) simulationState.id (template pattern)
    var _ss = window.simulationState || null;
    try { if (!_ss) _ss = simulationState; } catch(e) {}
    if (_ss && _ss.id) { _detectedSimId = _ss.id; return _detectedSimId; }
    // 4) Scan all scripts for simulation_id patterns
    var scripts = document.querySelectorAll('script');
    for (var i = 0; i < scripts.length; i++) {
      var txt = scripts[i].textContent || '';
      var m = txt.match(/SIMULATION_ID\s*=\s*['"]([^'"]+)['"]/);
      if (m) { _detectedSimId = m[1]; return _detectedSimId; }
      m = txt.match(/simulation_id\s*[:=]\s*['"]([^'"]+)['"]/);
      if (m) { _detectedSimId = m[1]; return _detectedSimId; }
    }
    // 5) Fallback to page title
    _detectedSimId = document.title || 'unknown_simulation';
    return _detectedSimId;
  }

  // Listen for the simulation's OWN state messages to learn the real ID
  window.addEventListener('message', function(e) {
    if (e.data && e.data.type === 'simulation_state' && e.data.simulation_id && !e.data._bridgeRelayed) {
      if (_detectedSimId !== e.data.simulation_id) {
        console.log('[Bridge] Learned real simulation_id from state message:', e.data.simulation_id);
        _detectedSimId = e.data.simulation_id;
      }
    }
  });

  // ---- Send manifest to parent on load ----
  function sendManifest() {
    var simId = detectSimulationId();
    var caps = discoverCapabilities();
    // Grab initial visible text as context for the LLM
    var bodyText = (document.body.innerText || '').substring(0, 800);
    window.parent.postMessage({
      type: 'simulation_manifest',
      simulation_id: simId,
      capabilities: caps,
      page_text: bodyText
    }, '*');
    console.log('[Bridge] Manifest sent:', simId, caps);
  }

  // ---- Does this simulation handle commands natively? ----
  var hasNativeCommandHandler = (typeof window.executeAICommand === 'function');
  if (!hasNativeCommandHandler) {
    try { hasNativeCommandHandler = (typeof executeAICommand === 'function'); } catch(e) {}
  }

  // ---- Generic command executor (only for simulations WITHOUT native handling) ----
  function executeCommand(command, params) {
    params = params || {};
    console.log('[Bridge] Executing command:', command, params);

    switch(command) {
      case 'start':
        if (typeof startSimulation === 'function') { startSimulation(); }
        else if (typeof runSimulation === 'function') { runSimulation(); }
        else if (typeof simulate === 'function') { simulate(true); }
        else {
          var startBtn = document.getElementById('btnStart');
          if (startBtn && !startBtn.disabled) startBtn.click();
        }
        break;
      case 'reset':
        if (typeof resetSimulation === 'function') { resetSimulation(); }
        else {
          var rstBtn = document.getElementById('btnReset');
          if (rstBtn && !rstBtn.disabled) rstBtn.click();
        }
        break;
      case 'click_button':
        var selector = params.selector || (params.id ? '#' + params.id : null);
        if (selector) {
          var target = document.querySelector(selector);
          if (target instanceof HTMLElement) target.click();
        }
        break;
      case 'set_variant':
        // New template: runVariant(variant_id)
        var vid = params.variant_id;
        if (vid && typeof window.runVariant === 'function') {
          console.log('[Bridge] runVariant:', vid);
          window.runVariant(vid);
        }
        break;
      case 'set_oxygen':
        // Respiration simulation: simulate(bool)
        var withO2 = params.oxygen_present;
        if (typeof window.simulate === 'function') {
          console.log('[Bridge] simulate:', withO2);
          window.simulate(withO2 === true || withO2 === 'true');
        }
        break;
      case 'call_function':
        var fnName = params.function_name || params.name;
        var fnArgs = params.args || [];
        // Parse string args like '[false]' or '[true]' into real JS values
        if (typeof fnArgs === 'string') {
          try { fnArgs = JSON.parse(fnArgs); } catch(e) { fnArgs = [fnArgs]; }
        }
        if (!Array.isArray(fnArgs)) fnArgs = [fnArgs];
        if (fnName && typeof window[fnName] === 'function') {
          console.log('[Bridge] Calling', fnName, 'with args:', fnArgs);
          window[fnName].apply(null, fnArgs);
        }
        break;
      default:
        console.warn('[Bridge] Unknown generic command:', command);
    }
  }

  // ---- Listen for commands from parent / IA ----
  window.addEventListener('message', function (event) {
    var data = event.data || {};
    if (data.type === 'simulation_control') {
      console.log('[Bridge] Control command received:', data.command, data.parameters);
      if (data.guidance_text) showGuidanceMessage(data.guidance_text);
      // If the simulation has its own command handler AND the simulation_id matches,
      // the native listener will handle it. Otherwise, use the bridge.
      if (hasNativeCommandHandler) {
        // Directly call native handler — more reliable than re-posting messages
        console.log('[Bridge] Forwarding to native executeAICommand:', data.command, data.parameters);
        try {
          var _execFn = window.executeAICommand || executeAICommand;
          _execFn(data.command, data.parameters || {});
        } catch(e) {
          console.warn('[Bridge] Native handler failed, using generic:', e);
          executeCommand(data.command, data.parameters);
        }
      } else {
        executeCommand(data.command, data.parameters);
      }
    }
    if (data.type === 'ai_instruction' && data.instruction) {
      if (data.instruction === 'auto_start') {
        setTimeout(function(){ executeCommand('start', {}); }, 250);
      }
    }
  });

  // ---- Auto-start and send manifest after DOM ready ----
  setTimeout(function(){
    sendManifest();
    // For auto-start, call directly (not via postMessage) to avoid double execution
    if (hasNativeCommandHandler) {
      try {
        var _nativeFn = window.executeAICommand || executeAICommand;
        _nativeFn('start', {});
      } catch(e) { executeCommand('start', {}); }
    } else {
      executeCommand('start', {});
    }
  }, 900);
})();
</script>`;

  if (html.includes('</body>')) {
    return html.replace('</body>', `${injectedBridge}</body>`);
  }

  return `${html}${injectedBridge}`;
}

export function SessionMediaDisplay({ media, isVisible, onSimulationUpdate }: SessionMediaDisplayProps) {
  const [imageError, setImageError] = useState(false);
  const iframeRef = useRef<HTMLIFrameElement>(null);
  const onSimUpdateRef = useRef(onSimulationUpdate);
  onSimUpdateRef.current = onSimulationUpdate;

  useEffect(() => {
    const handleSimulationMessage = (event: MessageEvent) => {
      const data = event.data;
      if (!data || typeof data !== 'object') return;
      if (data.type === 'simulation_state' || data.type === 'simulation_manifest') {
        console.log('[SessionMediaDisplay] Simulation message received:', data.type, data);
        if (onSimUpdateRef.current) {
          onSimUpdateRef.current(data);
        }
      }
    };

    window.addEventListener('message', handleSimulationMessage);
    return () => window.removeEventListener('message', handleSimulationMessage);
  }, []);

  if (!media || !isVisible) return null;

  // Convert local paths to proper URLs or clean Supabase URLs
  let cleanUrl = media.url;
  
  if (cleanUrl.startsWith('/media/')) {
    // Legacy local path - will fail to load
    cleanUrl = media.url;
  } else if (cleanUrl.endsWith('?')) {
    cleanUrl = cleanUrl.slice(0, -1);
  }

  const simulationHtml = media.type === 'simulation' ? buildSimulationHtml(cleanUrl) : null;
  const prevSimUrlRef = useRef<string | null>(null);
  if (media.type === 'simulation' && cleanUrl !== prevSimUrlRef.current) {
    prevSimUrlRef.current = cleanUrl;
    console.log('[SessionMediaDisplay] Simulation URL starts with:', cleanUrl.substring(0, 80));
    console.log('[SessionMediaDisplay] Bridge injected (srcDoc):', !!simulationHtml);
    if (!simulationHtml) {
      console.warn('[SessionMediaDisplay] WARNING: No srcDoc — simulation will load via src= (no bridge!)');
    }
  }

  const handleSimulationLoad = () => {
    if (media.type !== 'simulation' || !iframeRef.current?.contentWindow) return;
    console.log('[SessionMediaDisplay] Simulation iframe loaded, bridge will auto-start');
    
    // Fallback: if bridge postMessage doesn't reach parent, actively poll for manifest
    let manifestSent = false;
    const pollForManifest = () => {
      if (manifestSent) return;
      try {
        const iframeWin = iframeRef.current?.contentWindow as any;
        if (!iframeWin) return;
        
        // Try to read SIMULATION_CONFIG from iframe
        let simConfig: any = null;
        try { simConfig = iframeWin.SIMULATION_CONFIG; } catch(e) { /* cross-origin */ }
        if (!simConfig) {
          try { simConfig = iframeWin.eval?.('typeof SIMULATION_CONFIG !== "undefined" ? SIMULATION_CONFIG : null'); } catch(e) {}
        }
        
        if (simConfig && simConfig.id) {
          console.log('[SessionMediaDisplay] Fallback: Read SIMULATION_CONFIG from iframe:', simConfig.id);
          // Build manifest and send it
          const caps: any = { commands: ['start','reset','click_button','call_function','set_variant'], buttons: [], globals: [] };
          try { caps.config = JSON.parse(JSON.stringify(simConfig)); } catch(e) {}
          // Check for known functions
          ['executeAICommand','simulate','startSimulation','resetSimulation','runVariant'].forEach(fn => {
            try { if (typeof iframeWin[fn] === 'function') caps.globals.push(fn); } catch(e) {}
          });
          const manifestData = {
            type: 'simulation_manifest',
            simulation_id: simConfig.id,
            capabilities: caps,
            page_text: ''
          };
          console.log('[SessionMediaDisplay] Fallback: Sending manifest for', simConfig.id);
          manifestSent = true;
          if (onSimulationUpdate) {
            onSimulationUpdate(manifestData);
          }
          return; // success
        }
      } catch(e) {
        console.warn('[SessionMediaDisplay] Fallback manifest poll error:', e);
      }
    };
    
    // Poll after delays to give the iframe time to initialize
    setTimeout(pollForManifest, 1200);
    setTimeout(pollForManifest, 3000);
  };

  return (
    <div className="h-full w-full p-2 bg-blue-50 rounded-lg border-2 border-blue-200 overflow-hidden">
      {media.type === 'image' && (
        <div className="h-full flex flex-col gap-2">
          <div className="flex items-center gap-2 text-blue-700 font-medium">
            <span>📸</span>
            <span>Regarde cette image :</span>
          </div>
          {imageError ? (
            <div className="text-center py-4">
              <p className="text-red-600 text-sm">❌ Erreur de chargement</p>
              {cleanUrl.startsWith('/media/') ? (
                <p className="text-xs text-blue-600 mt-1">💡 Ressource locale obsolète - veuillez la re-uploader</p>
              ) : (
                <p className="text-xs text-gray-500 mt-1">{cleanUrl}</p>
              )}
            </div>
          ) : (
            <img
              src={cleanUrl}
              alt={media.caption || 'Image explicative'}
              className="flex-1 min-h-0 max-h-full w-auto max-w-full mx-auto rounded-lg shadow-md object-contain"
              onError={() => {
                setImageError(true);
                console.error('[SessionMediaDisplay] Failed to load image:', cleanUrl);
              }}
            />
          )}
          {media.caption && !imageError && (
            <p className="text-sm text-gray-600 text-center italic">{media.caption}</p>
          )}
        </div>
      )}

      {media.type === 'simulation' && (
        <div className="h-full w-full overflow-hidden rounded-lg border bg-white">
          <div className="w-[145%] h-[145%] origin-top-left scale-[0.68]">
            <iframe
              ref={iframeRef}
              src={simulationHtml ? undefined : media.url}
              srcDoc={simulationHtml ?? undefined}
              className="w-full h-full border-0"
              scrolling="no"
              title="Simulation"
              allowFullScreen
              onLoad={handleSimulationLoad}
            />
          </div>
        </div>
      )}

      {media.type === 'video' && (
        <div className="h-full flex flex-col gap-2">
          <div className="flex items-center gap-2 text-blue-700 font-medium">
            <span>🎥</span>
            <span>Regarde cette vidéo :</span>
          </div>
          <video
            src={media.url}
            controls
            className="flex-1 min-h-0 w-full rounded-lg shadow-md object-contain"
          >
            Votre navigateur ne supporte pas la lecture de vidéos.
          </video>
          {media.caption && (
            <p className="text-sm text-gray-600 text-center italic">{media.caption}</p>
          )}
        </div>
      )}
    </div>
  );
}
