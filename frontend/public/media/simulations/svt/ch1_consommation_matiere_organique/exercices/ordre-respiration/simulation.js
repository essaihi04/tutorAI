/* Teaching model: track only the two glycolytic NAD cofactors.
   Recycling is separated in time for observation; real reactions are coupled.
   Cytosolic reducing equivalents reach the respiratory chain via shuttles. */
(() => {
  'use strict';
  document.documentElement.classList.toggle('embedded', window.parent !== window);
  const $ = id => document.getElementById(id);
  const config = window.SIMULATION_CONFIG = {
    id: 'ordre_respiration_svt',
    commands: ['start', 'pause', 'next', 'recycle', 'reset', 'set_variant', 'highlight'],
    command_schema: { highlight: { target: 'repère pointable (voir reperes)' } },
    variants: [{id:'respiration',label:'O₂ + mitochondrie active'}, {id:'fermentation_lactique',label:'Sans O₂ : lactate'}, {id:'fermentation_alcoolique',label:'Sans O₂ : éthanol'}, {id:'mitochondrie_inactive',label:'O₂ présent, mitochondrie inactive'}],
    objectives: ['Identifier le pyruvate comme carrefour', 'Comparer les deux voies', 'Relier le recyclage du NAD⁺ à la poursuite de la glycolyse']
  };
  // Script d'explication par condition : le tuteur dit chaque phrase pendant que le professeur montre le repère.
  const EXPLICATION = {
    respiration: [
      { repere: 'glycolyse', texte: 'Dans le cytoplasme, la glycolyse coupe le glucose à 6 carbones en deux pyruvates et donne 2 ATP nets.' },
      { repere: 'carrefour_pyruvate', texte: 'Le pyruvate est un carrefour : son devenir dépend de l’O₂ et de la mitochondrie.' },
      { repere: 'porte_o2', texte: 'Avec du dioxygène et une mitochondrie active, la porte est ouverte.' },
      { repere: 'krebs', texte: 'Dans la matrice, le pyruvate est oxydé en acétyl-CoA, puis le cycle de Krebs libère du CO₂ et charge NADH et FADH₂.' },
      { repere: 'chaine_respiratoire', texte: 'La chaîne respiratoire transfère leurs électrons à l’O₂, forme de l’eau et produit beaucoup d’ATP ; le NAD⁺ régénéré retourne à la glycolyse.' },
    ],
    fermentation_lactique: [
      { repere: 'glycolyse', texte: 'La glycolyse a lieu quand même : 2 pyruvates, 2 ATP, et 2 NADH chargés.' },
      { repere: 'porte_o2', texte: 'Sans O₂, la mitochondrie ne peut pas prendre les pyruvates.' },
      { repere: 'fermentation', texte: 'Le pyruvate est alors réduit dans le cytoplasme : c’est la fermentation.' },
      { repere: 'produits_fermentation', texte: 'Ici, il devient du lactate ; le bilan reste de 2 ATP seulement.' },
      { repere: 'recyclage_nad', texte: 'L’intérêt : le NADH redevient NAD⁺, et la glycolyse peut continuer.' },
    ],
    fermentation_alcoolique: [
      { repere: 'glycolyse', texte: 'La glycolyse fournit 2 pyruvates, 2 ATP et 2 NADH.' },
      { repere: 'fermentation', texte: 'Sans O₂, la levure fait une fermentation alcoolique.' },
      { repere: 'produits_fermentation', texte: 'Chaque pyruvate perd un carbone sous forme de CO₂ et donne de l’éthanol à 2 carbones.' },
      { repere: 'recyclage_nad', texte: 'Le NADH est réoxydé en NAD⁺ : la glycolyse repart, avec 2 ATP par glucose.' },
    ],
    mitochondrie_inactive: [
      { repere: 'condition_mitochondrie', texte: 'Le dioxygène est présent, mais la mitochondrie est inactive.' },
      { repere: 'porte_o2', texte: 'L’O₂ seul ne suffit pas : sans chaîne respiratoire active, la porte reste fermée.' },
      { repere: 'fermentation', texte: 'Les pyruvates partent donc en fermentation, comme sans O₂.' },
      { repere: 'nad', texte: 'C’est la seule façon de régénérer le NAD⁺ et de continuer la glycolyse.' },
    ],
  };
  if (window.Tableau) window.Tableau.explication(EXPLICATION);
  let oxygen = true, mitochondria = true, alcoholic = false;
  let stage = 0, playing = false, timer = null, frame = null, generation = 0;
  const completed = new Set(), actions = [];
  const respiration = () => oxygen && mitochondria;
  const variant = () => respiration() ? 'respiration' : !mitochondria && oxygen ? 'mitochondrie_inactive' : alcoholic ? 'fermentation_alcoolique' : 'fermentation_lactique';
  function publish(action) {
    actions.push(action);
    const pathways = new Set([...completed].map(v => v === 'respiration' ? 'respiration' : 'fermentation'));
    $('explored').textContent = `${pathways.size} / 2 voies`;
    window.parent.postMessage({type:'simulation_state',simulation_id:config.id,student_actions:[...actions],current_state:{
      simulation_status:stage === 6 ? 'finished' : stage === 0 ? 'idle' : 'running',
      current_variant:variant(),variants_completed:[...completed],stage,paused:!playing,
      oxygen_present:oxygen,mitochondrion_functional:mitochondria,pathway:respiration()?'respiration':'fermentation',
      fermentation_type:alcoholic?'alcoolique':'lactique',glycolytic_nad_available:stage < 2 || stage >= 5 ? 2 : 0,
      glycolytic_nadh:stage >= 2 && stage < 5 ? 2 : 0,pyruvate_count:stage >= 2 ? 2 : 0,
      glycolysis_atp_net:stage >= 2 ? 2 : 0,second_glucose_unlocked:stage >= 5,second_glucose_started:stage === 6,
      skill:'pyruvate_carrefour_et_recyclage_nad',
    },objective_progress:pathways.size / 2,timestamp:Date.now()}, '*');
  }
  function stop() { playing = false; clearTimeout(timer); timer = null; }
  function cancelMotion() { generation++; cancelAnimationFrame(frame); ['traveller','nadTraveller','electronTraveller'].forEach(id=>$(id).setAttribute('visibility','hidden')); }
  function move(id, pathId, duration = 1600) {
    cancelMotion();
    const token = $(id), path = $(pathId), length = path.getTotalLength(), run = generation;
    token.setAttribute('visibility','visible');
    const start = performance.now(), reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
    const tick = now => {
      if (run !== generation) return;
      const progress = reduced ? 1 : Math.min(1, (now - start) / duration);
      const point = path.getPointAtLength(length * progress);
      token.setAttribute('transform', `translate(${point.x} ${point.y})`);
      if (progress < 1) frame = requestAnimationFrame(tick);
      else if (id !== 'traveller') token.setAttribute('visibility','hidden');
    };
    frame = requestAnimationFrame(tick);
  }
  function render(message) {
    const resp = respiration();
    $('oxygen').innerHTML = `O₂ <strong>${oxygen?'présent':'absent'}</strong>`;
    $('mitochondria').innerHTML = `Mitochondrie <strong>${mitochondria?'active':'inactive'}</strong>`;
    $('oxygen').setAttribute('aria-pressed',String(oxygen)); $('mitochondria').setAttribute('aria-pressed',String(mitochondria));
    $('lactate').setAttribute('aria-pressed',String(!alcoholic)); $('ethanol').setAttribute('aria-pressed',String(alcoholic));
    $('gateText').textContent = resp ? 'O₂ ✓' : '×';
    ['respirePath','matrix','chain','electronPath','respAtp'].forEach(id=>$(id).classList.toggle('dim',!resp));
    ['fermentPath','fermentationLabel','fermentProduct','fermentCondition'].forEach(id=>$(id).classList.toggle('dim',resp));
    $('productText').textContent = alcoholic ? '2 éthanols + 2 CO₂' : '2 lactates';
    $('lactateCarbons').setAttribute('visibility',alcoholic?'hidden':'visible');
    $('ethanolCarbons').setAttribute('visibility',alcoholic?'visible':'hidden');
    $('nadText').textContent = stage < 2 || stage >= 5 ? '2 NAD⁺ disponibles' : '2 NADH + 2 H⁺';
    $('nadSub').textContent = stage < 2 ? 'pour la glycolyse' : stage >= 5 ? 'prêts à resservir !' : 'à réoxyder en NAD⁺';
    ['glycolysis','junction','matrix','chain','fermentProduct','nadBadge'].forEach(id=>$(id).classList.remove('active'));
    const focus = ['glycolysis','glycolysis','junction',resp?'matrix':'fermentProduct',resp?'chain':'fermentProduct','nadBadge','glycolysis'][stage];
    $(focus).classList.add('active');
    $('recyclePath').classList.toggle('recycling',!resp && stage >= 5);
    $('respRecyclePath').classList.toggle('recycling',resp && stage >= 5);
    $('recycle').disabled = stage !== 4;
    $('start').textContent = playing ? 'Ⅱ Pause' : stage === 6 ? '↻ Rejouer' : stage === 4 || stage === 5 ? 'Glucose suivant →' : stage === 0 ? '▶ Lancer' : '▶ Continuer';
    $('next').disabled = stage >= 4;
    const messages = [
      'Change les conditions, puis lance le glucose.',
      'Dans le cytoplasme : 1 glucose entre dans la glycolyse.',
      '2 pyruvates : le carrefour ! Les NAD⁺ ont reçu des électrons.',
      resp ? 'Voie ouverte : les pyruvates entrent dans la mitochondrie.' : oxygen ? 'O₂ seul ne suffit pas : mitochondrie inactive → fermentation.' : 'Sans O₂ : les pyruvates suivent la fermentation.',
      resp ? 'La chaîne reçoit les électrons. Fais revenir le NAD⁺ !' : 'La fermentation réoxyde le NADH. Fais revenir le NAD⁺ !',
      'NAD⁺ régénéré : lance maintenant le glucose suivant.',
      'La glycolyse repart ! Essaie l’autre voie pour comparer.'
    ];
    window.Tableau ? window.Tableau.ecrire($('feedback'), message || messages[stage]) : ($('feedback').textContent = message || messages[stage]);
  }
  function reset(clear = false) {
    stop(); cancelMotion(); stage = 0;
    if (clear) { completed.clear(); actions.length = 0; }
    render(); publish(clear?'reset':'new_trial');
  }
  function schedule() { if (playing && stage < 4) timer = setTimeout(()=>{step();schedule();},2400); }
  function step() {
    if (stage >= 4) return;
    stage++;
    if (stage === 1) { $('travellerShape').setAttribute('href','#c6'); move('traveller','stem'); }
    if (stage === 2) cancelMotion();
    if (stage === 3) { $('travellerShape').setAttribute('href','#twoPyruvates'); move('traveller',respiration()?'respirePath':'fermentPath'); }
    if (stage === 4) { stop(); cancelMotion(); if(respiration())move('electronTraveller','electronPath'); }
    render(); publish('step_'+stage);
  }
  function start() {
    if (playing) { stop(); cancelMotion(); render(); publish('pause'); return; }
    if (stage === 4) { render('Glucose suivant en attente : régénère d’abord le NAD⁺.'); publish('next_glucose_blocked'); return; }
    if (stage === 5) {
      stage = 6; completed.add(variant()); $('travellerShape').setAttribute('href','#c6'); move('traveller','stem'); render(); publish('second_glucose_started'); return;
    }
    if (stage === 6) reset();
    playing = true; step(); schedule();
  }
  function recycle() {
    if (stage !== 4) return;
    stage = 5; move('nadTraveller',respiration()?'respRecyclePath':'recyclePath',2000); render(); publish('nad_regenerated');
  }
  function changeCondition(fn, name) { stop();cancelMotion();stage=0;fn();render();publish(name); }
  $('oxygen').onclick=()=>changeCondition(()=>oxygen=!oxygen,'toggle_oxygen');
  $('mitochondria').onclick=()=>changeCondition(()=>mitochondria=!mitochondria,'toggle_mitochondrion');
  $('lactate').onclick=()=>changeCondition(()=>alcoholic=false,'select_lactate');
  $('ethanol').onclick=()=>changeCondition(()=>alcoholic=true,'select_ethanol');
  $('start').onclick=start; $('next').onclick=()=>{stop();step();};
  // Le bouton principal vise aussi la commande `pause` du professeur quand la lecture est en cours.
  const majControle=()=>$('start').dataset.professorControl=playing?'pause start':'start pause';
  new MutationObserver(majControle).observe($('start'),{childList:true,characterData:true,subtree:true}); $('reset').onclick=()=>reset(true); $('recycle').onclick=recycle;
  function info(open) { $('enzymeInfo').hidden=!open; $('enzyme').setAttribute('aria-expanded',String(open)); if (open) { stop(); render(); $('closeInfo').focus(); } else $('enzyme').focus(); }
  $('enzyme').onclick=()=>info($('enzymeInfo').hidden); $('closeInfo').onclick=()=>info(false);
  document.addEventListener('keydown',event=>{if(event.key==='Escape'&&!$('enzymeInfo').hidden)info(false);});
  window.runVariant = id => {
    if (!config.variants.some(v=>v.id===id) && id!=='exercise') return;
    reset(); oxygen = id==='respiration'||id==='mitochondrie_inactive'||id==='exercise'; mitochondria=id!=='mitochondrie_inactive'; alcoholic=id==='fermentation_alcoolique'; render(); start();
  };
  window.executeAICommand = (command,params={}) => {
    if (command==='highlight') { if (window.Tableau) window.Tableau.surligner(params.target); return; }   // le professeur montre un repère
    if (window.Tableau) window.Tableau.appuyer(command);
    if(command==='start'&&!playing)start();
    else if(command==='pause'){stop();cancelMotion();render();publish('pause');}
    else if(command==='next'){stop();step();}
    else if(command==='recycle')recycle();
    else if(command==='reset')reset(true);
    else if(command==='set_variant')window.runVariant(params.variant_id);
  };
  window.addEventListener('message',event=>{const d=event.data;if(event.source===window.parent&&d&&d.type==='simulation_control'&&d.simulation_id===config.id)window.executeAICommand(d.command,d.parameters||{});});
  window.__SIMULATION_MANIFEST_SENT__=true;
  const manifeste = () => window.parent.postMessage({type:'simulation_manifest',simulation_id:config.id,capabilities:{commands:config.commands,config,command_schema:config.command_schema,buttons:['start','next','recycle','reset'],reperes:window.Tableau?window.Tableau.listeReperes():{},explication:EXPLICATION},page_text:'Pyruvate carrefour : comparer respiration et fermentation, puis recycler le NADH en NAD⁺ et lancer un deuxième glucose. Modèle simplifié suivant seulement les deux NAD⁺ de la glycolyse.'},'*');
  manifeste(); setTimeout(manifeste, 2000);
  render(); publish('ready');
})();
