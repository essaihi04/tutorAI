/*
 * Feuille d'examen — l'énoncé d'un exercice du national reproduit en code, comme la vraie feuille
 * (professeur, règle 46 ; logique-de-cours, règle 5). Pas la photo du sujet : une feuille blanche,
 * texte noir, l'en-tête officiel, le titre de l'exercice et ses points, les questions numérotées avec
 * leur barème dans la colonne de droite, les données, tableaux et figures redessinés.
 *
 * ── 1. Usage direct (aucun code) ───────────────────────────────────────────────────────────────
 *   /media/simulations/shared/examen/feuille.html?sujet=physique/2024-normale&exercice=2&questions=1-3
 *     sujet      <matière>/<année>-<session> (physique | svt | mathematiques ; normale | rattrapage)
 *     exercice   n° à plat dans le sujet (1, 2, …). Liste : python scripts/examens/copier_sujets.py --liste <sujet>
 *                (en SVT, une partie sans exercices — la restitution — compte pour un)
 *     questions  positions dans la liste des questions de l'exercice : « 1-3 », « 1,2,5 » (défaut : toutes).
 *                Règle 48 : une diapo d'énoncé ne montre que la partie qui va être répondue (1 à 3 questions).
 *     sous       dans la question gardée, les propositions / sous-questions montrées : « 2 », « 1,3 » (défaut : toutes).
 *                Allumer la question elle-même (q-iv) n'allume que sa consigne, pas ses propositions.
 *     partie     sur une page à soi (window.FEUILLE.blocs) : garde les blocs `partie: k` et ceux sans `partie`
 *     page       « 3/6 » : la case « الصفحة » de l'en-tête (défaut : vide)
 *     entete     complete (défaut : l'en-tête de la page 1 du sujet) | courte (pages 2 à N) | aucune
 *     bareme     droite (défaut) | gauche (sujets 2016-2019, maths) | inline (« (0,5pt) » en fin de question, 2020-2025)
 *     titre      bande (défaut, bande grise) | encadre (SVT) | souligne (maths)
 *   Le texte et les points viennent de exam.json, copié (sans corrigé) par scripts/examens/copier_sujets.py dans
 *   /media/examens/<matière>/<année>-<session>.json ; les figures découpées dans …/<année>-<session>/assets/.
 *
 * ── 2. Énoncé fidèle, figures redessinées (page d'une session de cours) ─────────────────────────
 *   exam.json n'est pas toujours fidèle (questions fusionnées, texte déplacé) : une page à soi donne l'énoncé exact
 *   dans l'ordre du scan (pages/sujet_pN.jpg sert de modèle) et ses figures en SVG/canvas.
 *     <link rel="stylesheet" href="/media/simulations/shared/examen/feuille.css">
 *     <script>
 *       window.FEUILLE = {
 *         sujet: 'physique/2024-normale', page: '3/6',        // l'en-tête vient de ce sujet (année, matière, durée…)
 *         id: 'examen-physique-2024-normale-ex2',              // simulation_id (défaut : dérivé du sujet)
 *         titre: 'EXERCICE 2 (2,5 points) : Propagation d’un signal à la surface de l’eau',
 *         blocs: [                                             // dans l'ordre de la feuille
 *           { texte: 'On se propose … (Markdown + $LaTeX$)' },
 *           { question: '1', points: 0.5, texte: 'Choisir la proposition juste …', choix: [['A', '…'], ['B', '…']] },
 *           { figure: 'fig-cuve', place: 'droite', svg: '<svg …>…</svg>' },   // ou html, src, ou dessiner(el)
 *           { question: '2-1', points: 0.5, texte: 'Déterminer la valeur de la célérité $v$ de l’onde.' },
 *           { html: '<div class="clair"></div>' },
 *         ],
 *       };
 *     </script>
 *     <script src="/media/simulations/shared/examen/feuille.js"></script>
 *   Sans `blocs`, la page peut garder exam.json et seulement remplacer les figures :
 *     window.FEUILLE = { sujet, exercice: 2, figures: { doc_ex2_1: { svg: '…', place: 'droite' } } }
 *   Markdown : paragraphes, **gras**, *italique*, tableaux « | a | b | », $…$ et $$…$$ (KaTeX local, katex/).
 *   Une donnée pointable : [$r_1 = 14$]{#donnee-r1} → <span id="donnee-r1"> (marche aussi dans une case de tableau).
 *
 * ── 3. Repères pour le tuteur ──────────────────────────────────────────────────────────────────
 *   Chaque question a un id `q-<numéro>` (« 2-1 » → q-2.1, « 1) a) » → q-1.a), le titre `titre-exo`, le texte
 *   d'introduction `contexte`, chaque figure `fig-<id>`, chaque tableau `tab-<n>`, chaque donnée marquée `donnee-…`.
 *   Messages reçus (postMessage du lecteur) :
 *     { type:'simulation_control', command:'surligner', parameters:{ id:'q-2.1', garder:false } }  surligne et amène
 *     { … command:'highlight', parameters:{ target:'q-2.1' } }                                    même chose
 *     { … command:'allume', parameters:{ cible } } / { … command:'eteins' }                       démonstration (règle 17)
 *     { … command:'effacer' }                                                                     retire les surlignages
 *     { … command:'defiler', parameters:{ id } | { fraction: 0..1 } }                            défilement doux
 *     { type:'simulation_manifest_request' }                                                      renvoie le manifeste
 *   Messages envoyés : simulation_ready, simulation_manifest (commandes, repères {id: libellé}, page_text = le texte
 *   de la feuille, que le tuteur lit), simulation_state (current_state : surligne, reperes, defilement).
 *   window.Feuille = { rendre(config), surligner(id), effacer(), md(texte) } ; window.executeAICommand(cmd, params).
 *
 * Mise à l'échelle : la feuille prend la largeur du cadre (≤ 1000 px), le texte courant vaut largeur/54 sans
 * descendre sous 15 px ; un énoncé long défile (jamais coupé). Vérifié à 1366×560 et 724×350.
 */
(function () {
  'use strict';
  if (window.Feuille) return;

  const ICI = (document.currentScript && document.currentScript.src) ? document.currentScript.src.replace(/[^/]*$/, '') : '/media/simulations/shared/examen/';
  const P = new URLSearchParams(location.search);

  // ── KaTeX local ───────────────────────────────────────────────────────────
  function chargerKatex() {
    if (window.katex) return Promise.resolve();
    return new Promise((ok) => {
      if (!document.querySelector('link[data-katex]')) {
        const l = document.createElement('link'); l.rel = 'stylesheet'; l.href = ICI + 'katex/katex.min.css'; l.dataset.katex = '1';
        document.head.appendChild(l);
      }
      const s = document.createElement('script'); s.src = ICI + 'katex/katex.min.js'; s.onload = ok; s.onerror = ok;
      document.head.appendChild(s);
    });
  }
  function tex(src, display) {
    if (!window.katex) return esc(display ? `$$${src}$$` : `$${src}$`);
    src = src.replace(/(\d),(?=\d)/g, '$1{,}');   // 9,8 et non « 9, 8 »
    try { return window.katex.renderToString(src, { displayMode: !!display, throwOnError: false, strict: false, trust: false }); }
    catch (_) { return esc(src); }
  }

  // ── Markdown minimal + LaTeX ──────────────────────────────────────────────
  const esc = (s) => String(s ?? '').replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  let nTableau = 0;
  function md(src) {
    const maths = [];
    let s = String(src ?? '').replace(/\r/g, '');
    s = s.replace(/\$\$([\s\S]+?)\$\$/g, (_, t) => `\u0000${maths.push([t, true]) - 1}\u0000`);
    s = s.replace(/(^|[^\\])\$([^$\n]+?)\$/g, (_, a, t) => `${a}\u0000${maths.push([t, false]) - 1}\u0000`);
    s = s.replace(/\[([^\]\n]+)\]\{#([a-z0-9_.-]+)\}/gi, (_, t, id) => `\u0001${id}\u0002${t}\u0003`);
    s = esc(s);
    const inline = (t) => t
      .replace(/\*\*([\s\S]+?)\*\*/g, '<b>$1</b>')
      .replace(/(^|[^*\w])\*([^*\n]+?)\*/g, '$1<i>$2</i>')
      .replace(/(^|\s)_([^_\n]+?)_(?=[\s.,;:!?)]|$)/g, '$1<i>$2</i>')
      .replace(/!\[([^\]]*)\]\(([^)\s]+)\)/g, '<img alt="$1" src="$2">');
    const blocs = s.split(/\n\s*\n/).map((b) => {
      const lignes = b.split('\n').filter((l) => l.trim() !== '');
      if (!lignes.length) return '';
      if (lignes.every((l) => /^\s*\|/.test(l))) {
        const rangs = lignes.filter((l) => !/^\s*\|?\s*:?-{2,}/.test(l))
          .map((l) => l.trim().replace(/^\|/, '').replace(/\|$/, '').split('|').map((c) => c.trim()));
        const id = `tab-${++nTableau}`;
        return `<table class="t" id="${id}" data-repere="${id}" data-professor-point="${id}" data-professor-label="Tableau ${nTableau}">` +
          rangs.map((r) => `<tr>${r.map((c) => `<td>${inline(c)}</td>`).join('')}</tr>`).join('') + '</table>';
      }
      return `<p>${lignes.map(inline).join('<br>')}</p>`;
    }).join('');
    return blocs
      .replace(/\u0001([^\u0002]+)\u0002([\s\S]*?)\u0003/g, (_, id, t) => `<span class="donnee" id="${id}" data-repere="${id}" data-professor-point="${id}">${t}</span>`)
      .replace(/\u0000(\d+)\u0000/g, (_, i) => tex(maths[+i][0], maths[+i][1]));
  }

  // ── Données d'en-tête ─────────────────────────────────────────────────────
  const MATIERES = {
    physique: { ar: 'الفيزياء والكيمياء', fr: 'Physique-Chimie', code: '28' },
    svt: { ar: 'علوم الحياة والأرض', fr: 'Sciences de la vie et de la Terre', code: '34' },
    mathematiques: { ar: 'الرياضيات', fr: 'Mathématiques', code: '22' },
  };
  const ministere = (annee) => (annee >= 2022
    ? ['وزارة التربية الوطنية', 'والتعليم الأولي والرياضة']
    : ['وزارة التربية الوطنية والتكوين المهني', 'والتعليم العالي والبحث العلمي']);
  const ministereFr = (annee) => (annee >= 2022
    ? 'Ministère de l’Éducation nationale, du Préscolaire et des Sports'
    : 'Ministère de l’Éducation nationale, de la Formation professionnelle, de l’Enseignement supérieur et de la Recherche scientifique');
  const nbFr = (v) => (v == null || v === '' ? '' : String(+v === +v ? +v : v).replace('.', ','));
  // Pas de blason dessiné (19/11/2026, l'utilisateur : « le drapeau est mal fait ; l'annuler si on ne le met pas comme le
  // vrai ») : un dessin approximatif des armoiries du Royaume est pire que rien.
  const EMBLEME = '';

  function infos(exam, cfg) {
    const sujet = cfg.sujet || exam.sujet || '';
    const [matiere = '', cle = ''] = sujet.split('/');
    const annee = +(exam.year || cle.slice(0, 4)) || 2024;
    const ratt = /ratt|ratr/i.test(String(exam.session || cle));
    const m = MATIERES[matiere] || { ar: '', fr: exam.subject || '', code: '' };
    return {
      sujet, matiere, annee, ratt, m,
      code: cfg.code || exam.code || `${ratt ? 'RS' : 'NS'} ${m.code}F`,
      duree: cfg.duree || (exam.duration_minutes ? `${Math.round(exam.duration_minutes / 60 * 10) / 10}h`.replace('.', ',') : '3h'),
      coef: cfg.coefficient ?? exam.coefficient ?? '',
      page: String(cfg.page || P.get('page') || ''),
    };
  }
  function caseFraction(page) {
    const [n = '', N = ''] = page.split('/');
    return `<div class="page-boite"><div class="lib ar">الصفحة</div><div class="frac"><svg viewBox="0 0 100 100" preserveAspectRatio="none"><line x1="0" y1="0" x2="100" y2="100" stroke="#000" stroke-width="3" vector-effect="non-scaling-stroke"/></svg><span class="num">${esc(n)}</span><span class="den">${esc(N)}</span></div></div>`;
  }
  function entete(i, mode) {
    if (mode === 'aucune') return '';
    const session = i.ratt ? 'الدورة الاستدراكية' : 'الدورة العادية';
    const sessionFr = i.ratt ? 'Session de rattrapage' : 'Session normale';
    const filiere = 'شعبة العلوم التجريبية مسلك العلوم الفيزيائية (خيار فرنسية)';
    const fr = `<div class="entete-fr">Royaume du Maroc — ${ministereFr(i.annee)} — Centre national de l’évaluation et des examens<br>` +
      `Examen national unifié du baccalauréat — ${sessionFr} ${i.annee} — Sujet — ${esc(i.m.fr)} — Sciences expérimentales, filière Sciences physiques (option française) — Durée ${esc(i.duree)} — Coefficient ${esc(nbFr(i.coef))}</div>`;
    if (mode === 'courte') {
      return `<table class="entete courte" id="entete" data-repere="entete" data-professor-point="entete" data-professor-label="En-tête"><tr>` +
        `<td class="page">${caseFraction(i.page)}</td><td class="code">${esc(i.code)}</td>` +
        `<td class="titre-ar ar"><div>الامتحان الوطني الموحد للبكالوريا - ${session} ${i.annee} – الموضوع</div><div>- مادة: ${esc(i.m.ar)} -</div><div>${filiere}</div></td>` +
        `<td class="vide"></td></tr></table>${fr}`;
    }
    const [m1, m2] = ministere(i.annee);
    return `<div id="entete" data-repere="entete" data-professor-point="entete" data-professor-label="En-tête">` +
      `<table class="entete"><tr>` +
      `<td class="page" rowspan="2">${caseFraction(i.page)}</td>` +
      `<td class="titre-ar ar"><div class="l1">الامتحان الوطني الموحد للبكالوريا</div><div class="l1">${session} ${i.annee}</div><div>- الموضوع -</div></td>` +
      `<td class="royaume ar" rowspan="2"><div class="ligne-emb"><div>المملكة المغربية<br>${m1}<br>${m2}</div>${EMBLEME}</div><div class="centre">المركز الوطني للتقويم والامتحانات</div></td>` +
      `</tr><tr><td class="code">${esc(i.code)}</td></tr></table>` +
      `<table class="entete2"><tr><td class="val">${esc(i.duree)}</td><td class="lib ar">مدة الإنجاز</td><td class="mat ar">${esc(i.m.ar)}</td><td class="cle ar">المادة</td></tr>` +
      `<tr><td class="val">${esc(nbFr(i.coef))}</td><td class="lib ar">المعامل</td><td class="fil ar">${filiere}</td><td class="cle ar">الشعبة أو المسلك</td></tr></table>` +
      `${fr}</div>`;
  }

  // ── Exercice : de exam.json aux blocs de la feuille ───────────────────────
  function exercicesAPlat(exam) {
    const out = [];
    for (const p of exam.parts || []) { if (p.exercises && p.exercises.length) out.push(...p.exercises); else out.push(p); }
    return out;
  }
  function plage(spec, n) {
    if (!spec) return null;
    const set = new Set();
    for (const morceau of String(spec).split(',')) {
      const [a, b] = morceau.split('-').map((x) => parseInt(x, 10));
      if (!Number.isFinite(a)) continue;
      for (let k = a; k <= (Number.isFinite(b) ? b : a) && k <= n; k++) set.add(k);
    }
    return set;
  }
  /** « 2-1. Déterminer … » → { parts: ['2','1'], reste: 'Déterminer …' } */
  function numeroEnTete(texte) {
    const m = /^\s*((?:\d+|[IVX]+|[a-z])(?:\s*[-.)]\s*(?:\d+|[a-z])(?![a-zà-ÿ]))*)\s*[-.)]\s+/i.exec(texte || '');
    if (!m) return null;
    return { parts: m[1].split(/\s*[-.)]\s*/).filter(Boolean), reste: texte.slice(m[0].length) };
  }
  function titreDepuisNom(nom, points) {
    const m = /^\s*Exercice\s+([^\s—–:-]+)\s*[—–:-]?\s*(?:(?:Physique|Chimie|Physique-chimie)\s*:\s*)?(.*)$/i.exec(nom || '');
    const pts = points != null ? ` (${nbFr(points)} points)` : '';
    if (m) return `EXERCICE ${m[1]}${pts}${m[2] ? ' : ' + m[2] : ''}`;
    return `${nom || ''}${pts}`;
  }
  function blocsDepuisExam(ex, cfg) {
    const blocs = [];
    const garde = plage(cfg.questions ?? P.get('questions'), (ex.questions || []).length);
    // Dans une partie (règle 48), une figure sans place flotte à droite, à 42 % de la largeur : la partie garde un texte
    // lisible au lieu d'être réduite (19/11/2026, l'utilisateur : réduire les figures des parties, cadre réel ~1126×460).
    const docs = Object.fromEntries((ex.documents || []).filter((d) => d && d.id)
      .map((d) => [d.id, garde && !d.place ? { ...d, place: 'droite', largeur: d.largeur || '42%' } : d]));
    const vus = new Set();
    const figure = (id) => {
      if (vus.has(id) || !docs[id]) return;
      vus.add(id);
      const d = docs[id]; const surcharge = (cfg.figures || {})[id] || {};
      blocs.push({ figure: id, src: d.src, legende: d.title && !/^figure suivante$/i.test(d.title) ? d.title : '', place: d.place, largeur: d.largeur, ...surcharge });
    };
    // Le contexte de l'exercice n'est montré qu'à la partie 1 : les parties suivantes (entete=courte) ne le répètent pas,
    // le tuteur le rappelle en une phrase (règle 48 ; 19/11/2026, l'utilisateur).
    const suite = !!garde && (cfg.entete || P.get('entete')) === 'courte';
    if (ex.context && !suite) blocs.push({ texte: ex.context, id: 'contexte' });
    // L'introduction annonce la figure du montage (« figure 1 », « figure ci-contre », « document 1 », « le montage
    // schématisé ») : dans une partie qui montre cette introduction, la première figure de l'exercice est là aussi, même
    // si seule une question plus loin la cite (22/11/2026, l'utilisateur, 2025 R ex. 2 : « figure ci-contre » annoncée,
    // figure absente de la partie 1 ; même défaut sur 9 diapositives d'énoncé de 5 cours).
    if (garde && ex.context && !suite && /figure|document|sch[ée]ma|montage|ci-contre|ci-dessous/i.test(ex.context)) {
      const premiere = (ex.documents || []).find((d) => d && d.id);
      if (premiere) figure(premiere.id);
    }
    const refs = new Set((ex.questions || []).flatMap((q) => q.documents || []));
    // Un document qu'aucune question ne cite n'apparaît dans une partie (questions=…) que s'il est marqué `commun: true`
    // (19/11/2026, l'utilisateur, 2022 R ex. 2 : la figure de l'onde restait affichée dans la partie radioactivité —
    // « pas la peine de mettre la figure du périodique alors qu'on est dans la radioactivité »).
    for (const id of Object.keys(docs)) if (!refs.has(id) && (!garde || docs[id].commun)) figure(id);
    // Texte d'une partie de l'exercice (« Partie 2 : … », ses données ; « 3. On injecte… ») : ex.intros[clé], placé une
    // fois, juste avant la première question gardée qui le cite (q.intro_cles) — une partie montrée seule garde son texte.
    const introsVues = new Set();
    const cote = (id) => /^(droite|gauche)$/.test(((cfg.figures || {})[id] || {}).place || (docs[id] || {}).place || '');
    (ex.questions || []).forEach((q, k) => {
      if (garde && !garde.has(k + 1)) return;
      // dans une partie, la figure à droite passe avant les textes de partie et flotte à côté d'eux (2016 N, 2018 N
      // ex. 1 : la courbe pH = f(V) sous les longs textes faisait tomber la partie à 0,56)
      if (garde) for (const id of q.documents || []) if (cote(id)) figure(id);
      for (const c of q.intro_cles || []) {
        if (introsVues.has(c) || !(ex.intros || {})[c]) continue;
        introsVues.add(c);
        blocs.push({ texte: ex.intros[c], id: 'intro-' + String(c).replace(/[^a-z0-9_-]/gi, '-') });
      }
      // une figure à droite (ou à gauche) se place AVANT sa question, pour flotter à côté d'elle comme sur le sujet
      for (const id of q.documents || []) if (cote(id)) figure(id);
      blocs.push({ q });
      for (const id of q.documents || []) figure(id);
    });
    blocs.push({ html: '<div class="clair"></div>' });
    return blocs;
  }

  // ── Rendu des blocs ───────────────────────────────────────────────────────
  const IDS = new Set();
  const idUnique = (base) => { let id = base, k = 2; while (IDS.has(id)) id = `${base}-${k++}`; IDS.add(id); return id; };
  function blocQuestion(b, modeBareme, sous) {
    // b : { question:'2-1', points, texte, choix:[[l,t]], sous:[…] } ou { q: <question exam.json> }
    const q = b.q || {};
    let texte = b.texte ?? q.content ?? '';
    let parts;
    if (b.question != null) parts = String(b.question).split(/\s*[-.)]\s*/).filter(Boolean);
    else {
      const t = numeroEnTete(texte);
      if (t) { parts = t.parts; texte = t.reste; } else parts = String(q.number ?? '').split(/\s*[-.)]\s*/).filter(Boolean);
    }
    const id = b.id || idUnique('q-' + (parts.join('.') || 'x').toLowerCase());
    const label = parts.length ? parts.join('-') + '- ' : '';
    const points = b.points ?? q.points;
    const pts = points != null && points !== '' ? nbFr(points) : '';
    const choix = b.choix || (q.choices || []).map((c) => [c.letter, c.text]);
    // `sous=2` (21/11/2026, l'utilisateur) : d'une question à propositions (« IV- Pour chacune des propositions
    // numérotées de 1 à 4… »), seules les propositions traitées juste après sont montrées, comme la règle 48.
    const toutesSous = b.sous || (q.sub_questions || []).map((s) => ({ q: s }));
    const garderSous = !sous && SOUS && toutesSous.length ? toutesSous.filter((_, k) => SOUS.has(k + 1)) : toutesSous;
    const sousQ = garderSous.length ? garderSous : toutesSous;
    let corps = md(texte);
    // Le numéro en gras se colle au premier paragraphe, comme sur la feuille.
    corps = corps.replace(/^<p>/, `<p><span class="num">${esc(label)}</span>`);
    if (!/^<p>/.test(corps)) corps = `<span class="num">${esc(label)}</span>` + corps;
    if (pts && modeBareme === 'inline') corps = corps.replace(/<\/p>$/, ` <span class="pts-inline">(${pts}pt)</span></p>`);
    const tableChoix = choix.length ? `<table class="choix">${choix.map(([l, t]) => `<tr><td class="lettre">${esc(l)}</td><td>${md(t).replace(/^<p>|<\/p>$/g, '')}</td></tr>`).join('')}</table>` : '';
    const enfants = sousQ.map((s) => blocQuestion(s, modeBareme, true)).join('');
    const lib = `Question ${parts.join('-')}`;
    return `<div class="q${sous ? ' sous' : ''}" id="${id}" data-repere="${id}" data-professor-point="${id}" data-professor-label="${esc(lib)}">` +
      `${pts && modeBareme !== 'inline' ? `<div class="pts">${pts}</div>` : ''}${corps}${tableChoix}${enfants}</div>`;
  }
  function blocFigure(b) {
    const id = b.id || idUnique('fig-' + String(b.figure).replace(/^doc_/, '').replace(/[^a-z0-9_-]/gi, '-'));
    const place = b.place ? ` ${b.place}` : '';
    const style = b.largeur ? ` style="width:${esc(b.largeur)}"` : '';
    b._id = id;
    let dedans = b.svg || b.html || (b.src ? `<img src="${esc(b.src)}" alt="${esc(b.legende || 'Figure')}">` : '');
    return `<figure class="fig${place}" id="${id}" data-repere="${id}" data-professor-point="${id}" data-professor-label="${esc(b.legende || 'Figure')}"${style} data-dessin="${b.dessiner ? '1' : ''}">` +
      `${dedans}${b.legende ? `<figcaption>${md(b.legende).replace(/^<p>|<\/p>$/g, '')}</figcaption>` : ''}</figure>`;
  }

  // ── Mise à l'échelle ──────────────────────────────────────────────────────
  function taille() {
    const W = document.documentElement.clientWidth || innerWidth;
    const marge = W < 800 ? 8 : 24;
    const largeur = Math.max(280, Math.min(1000, W - 2 * marge));
    const pt = Math.max(15, Math.min(20, largeur / 54));
    document.documentElement.style.setProperty('--largeur', largeur + 'px');
    document.documentElement.style.setProperty('--pt', pt.toFixed(2) + 'px');
  }

  // ── Repères et pont avec le tuteur ────────────────────────────────────────
  let CFG = {}; let SURLIGNE = [];
  /** les propositions gardées d'une question (`sous=`), null : toutes */
  let SOUS = null;
  const simId = () => CFG.id || `examen-${String(CFG.sujet || 'sujet').replace(/[^a-z0-9]+/gi, '-')}-ex${CFG.exercice || ''}`;
  const envoyer = (msg) => { try { if (parent !== window) parent.postMessage({ simulation_id: simId(), ...msg }, '*'); } catch (_) { /* hors iframe */ } };
  function reperes() {
    const out = {};
    document.querySelectorAll('[data-repere]').forEach((el) => {
      const lib = el.dataset.professorLabel || (el.textContent || '').trim().slice(0, 60);
      out[el.dataset.repere] = lib;
    });
    return out;
  }
  function etat() {
    const h = document.documentElement.scrollHeight - innerHeight;
    return { sujet: CFG.sujet || '', exercice: CFG.exercice || '', surligne: SURLIGNE.slice(), reperes: Object.keys(reperes()), defilement: h > 0 ? +(scrollY / h).toFixed(3) : 0, page: PAGE, pages: NPAGES };
  }
  const emettre = () => envoyer({ type: 'simulation_state', current_state: etat(), timestamp: Date.now() });
  function manifeste() {
    window.__SIMULATION_MANIFEST_SENT__ = true;
    const r = reperes();
    envoyer({
      type: 'simulation_manifest',
      capabilities: {
        commands: ['surligner', 'highlight', 'allume', 'eteins', 'effacer', 'defiler', 'page'], globals: ['executeAICommand'],
        command_schema: { surligner: { id: Object.keys(r).join(' | '), garder: 'bool' }, highlight: { target: Object.keys(r).join(' | ') }, allume: { cible: Object.keys(r).join(' | ') }, eteins: {}, effacer: {}, defiler: { id: 'repère', fraction: '0..1' } },
        reperes: r, state_schema: { surligne: 'ids', defilement: '0..1' },
      },
      page_text: texteALire(),
    });
  }
  /** Une formule LaTeX en texte lisible : \\mathrm{t_1} → t1, \\sqrt{g.h} → √(g.h), 10^{-2} → 10^-2. */
  function lisible(t) {
    let s = String(t).replace(/\{,\}/g, ',');
    for (let k = 0; k < 5; k++) {
      s = s.replace(/\\sqrt\{([^{}]*)\}/g, '√($1)').replace(/\\frac\{([^{}]*)\}\{([^{}]*)\}/g, '($1)/($2)')
        .replace(/_\{([^{}]*)\}/g, '$1').replace(/\^\{([^{}]*)\}/g, '^$1')
        .replace(/\\(?:mathrm|text|mathbf|mathit|operatorname|boxed)\{([^{}]*)\}/g, '$1');
    }
    return s.replace(/_(\w)/g, '$1').replace(/\\[,;! ]/g, ' ').replace(/\\times/g, '×').replace(/\\cdot/g, '·')
      .replace(/\\(alpha|beta|gamma|delta|Delta|lambda|theta|tau|omega|pi|mu|rho|sigma)/g, (_, g) => ({ alpha: 'α', beta: 'β', gamma: 'γ', delta: 'δ', Delta: 'Δ', lambda: 'λ', theta: 'θ', tau: 'τ', omega: 'ω', pi: 'π', mu: 'µ', rho: 'ρ', sigma: 'σ' }[g]))
      .replace(/[{}]/g, '').replace(/\s+/g, ' ').trim();
  }
  /** Le texte que le tuteur lit : l'en-tête en français puis l'énoncé, le barème dit après chaque question. */
  function texteALire() {
    const corps = document.querySelector('.feuille .corps');
    if (!corps) return '';
    const c = corps.cloneNode(true);
    c.querySelectorAll('.tete-bareme').forEach((e) => e.remove());
    c.querySelectorAll('.katex').forEach((e) => {
      const tex = e.querySelector('annotation')?.textContent || e.textContent;
      e.replaceWith(lisible(tex));
    });
    c.querySelectorAll('figure').forEach((e) => e.replaceWith(`[Figure${e.querySelector('figcaption') ? ' : ' + e.querySelector('figcaption').textContent : ''}]`));
    c.querySelectorAll('.pts').forEach((e) => {
      const p = e.textContent.trim(); const q = e.parentElement; e.remove();
      (q.querySelector(':scope > p') || q).append(` (${p} pt)`);
    });
    c.style.cssText = 'position:absolute;left:-9999px;width:800px'; document.body.appendChild(c);
    const t = c.innerText; c.remove();
    const fr = document.querySelector('.entete-fr')?.textContent || '';
    return `${fr}\n\n${t}`.replace(/[ \t]+\n/g, '\n').replace(/\n{3,}/g, '\n\n').trim();
  }
  function amener(el) {
    const r = el.getBoundingClientRect();
    const bloc = r.height > innerHeight * 0.8 ? 'start' : 'center';
    el.scrollIntoView({ behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth', block: bloc });
  }
  function effacer() { document.querySelectorAll('.surligne').forEach((e) => e.classList.remove('surligne')); SURLIGNE = []; }
  function surligner(id, garder) {
    const el = id && (document.querySelector(`[data-repere="${CSS.escape(id)}"]`) || document.getElementById(id));
    if (!el) return false;
    if (!garder) effacer();
    const pg = pageDe(el); if (pg !== PAGE) montrerPage(pg);
    el.classList.add('surligne'); SURLIGNE.push(id); amener(el);
    return true;
  }
  window.executeAICommand = (cmd, p = {}) => {
    p = p || {};
    if (cmd === 'surligner' || cmd === 'highlight' || cmd === 'montrer' || cmd === 'point' || cmd === 'show' || cmd === 'allume') surligner(p.id || p.target || p.cible || p.repere, !!p.garder);
    else if (cmd === 'effacer' || cmd === 'eteins' || cmd === 'reset') effacer();
    else if (cmd === 'page') montrerPage(+(p.n || p.page) || 1);
    else if (cmd === 'defiler') {
      if (p.id) { const el = document.querySelector(`[data-repere="${CSS.escape(p.id)}"]`); if (el) amener(el); }
      else if (p.fraction != null) scrollTo({ top: (document.documentElement.scrollHeight - innerHeight) * +p.fraction, behavior: 'smooth' });
    }
    setTimeout(emettre, 50);
  };
  addEventListener('message', (e) => {
    const d = e.data;
    if (!d || typeof d !== 'object') return;
    if (d.type === 'simulation_control' && (!d.simulation_id || d.simulation_id === simId())) window.executeAICommand(d.command, d.parameters || {});
    if (d.type === 'simulation_manifest_request') manifeste();
  });
  let attente = 0;
  addEventListener('scroll', () => { clearTimeout(attente); attente = setTimeout(emettre, 200); }, { passive: true });
  addEventListener('resize', () => { taille(); paginer(); });

  // ── Rendu ─────────────────────────────────────────────────────────────────
  async function rendre(config = {}) {
    CFG = { ...config };
    CFG.sujet = CFG.sujet || P.get('sujet') || '';
    CFG.exercice = CFG.exercice ?? P.get('exercice') ?? '';
    const modeBareme = CFG.bareme || P.get('bareme') || 'droite';
    const modeTitre = CFG.style_titre || P.get('titre') || 'bande';
    const modeEntete = CFG.entete || P.get('entete') || 'complete';
    taille();
    const racine = CFG.racine || document.getElementById('feuille') || document.body.appendChild(Object.assign(document.createElement('div'), { id: 'feuille' }));
    const [, exam] = await Promise.all([
      chargerKatex(),
      CFG.exam ? Promise.resolve(CFG.exam) : (CFG.sujet ? fetch(`/media/examens/${CFG.sujet}.json`).then((r) => { if (!r.ok) throw new Error(`/media/examens/${CFG.sujet}.json : ${r.status}`); return r.json(); }) : Promise.resolve({})),
    ]).catch((e) => { racine.innerHTML = `<div class="erreur">Feuille d’examen : ${esc(e.message)}. Lancer python scripts/examens/copier_sujets.py ${esc(CFG.sujet)}</div>`; throw e; });
    IDS.clear(); nTableau = 0;
    SOUS = plage(CFG.sous ?? P.get('sous'), 99);
    let ex = null;
    if (!CFG.blocs) {
      const liste = exercicesAPlat(exam);
      ex = liste[(parseInt(CFG.exercice, 10) || 1) - 1];
      if (!ex) { racine.innerHTML = `<div class="erreur">Exercice ${esc(CFG.exercice)} introuvable (${liste.length} exercices dans ${esc(CFG.sujet)}).</div>`; return; }
    }
    // Une partie de l'exercice (professeur, règle 48) : sur une page à soi, `partie=<k>` (URL ou config) garde les blocs
    // `partie: k` (ou [k, m]) et ceux sans `partie` (le contexte, un document commun).
    const partie = CFG.partie ?? P.get('partie');
    const dansPartie = (b) => partie == null || partie === '' || b.partie == null || [].concat(b.partie).map(String).includes(String(partie));
    const blocs = CFG.blocs ? CFG.blocs.filter(dansPartie) : blocsDepuisExam(ex, CFG);
    const titre = CFG.titre || (ex ? titreDepuisNom(ex.name, ex.points) : '');
    const morceaux = blocs.map((b) => {
      if (b.q || b.question != null) return blocQuestion(b, modeBareme, false);
      if (b.figure != null) return blocFigure(b);
      if (b.texte != null) { const id = b.id || idUnique('texte'); return `<div class="contexte" id="${id}" data-repere="${id}" data-professor-point="${id}" data-professor-label="${esc(b.libelle || 'Énoncé')}">${md(b.texte)}</div>`; }
      if (b.html != null) return b.html;
      return '';
    }).join('');
    const i = infos(exam, CFG);
    racine.innerHTML = `<div class="feuille-zone"><article class="feuille" lang="fr"><div class="feuille-cadre">` +
      (modeEntete === 'aucune' ? '' : `<div class="entete-complete">${entete(i, modeEntete)}</div>` + `<div class="entete-courte" style="display:none">${entete(i, 'courte')}</div>`) +
      `<div class="corps${modeBareme === 'gauche' ? ' bareme-gauche' : ''}">` +
      (modeBareme === 'inline' ? '' : '<div class="tete-bareme">Barème</div>') +
      (titre ? `<div class="titre-exo ${modeTitre === 'bande' ? '' : modeTitre}" id="titre-exo" data-repere="titre-exo" data-professor-point="titre-exo" data-professor-label="Titre de l’exercice">${md(titre).replace(/^<p>|<\/p>$/g, '')}</div>` : '') +
      morceaux + `</div></div></article>` +
      `<div class="pages-nav"><button type="button" class="prec">◀ page précédente</button><span class="num"></span>` +
      `<button type="button" class="suiv">page suivante ▶</button></div></div>`;
    // Figures dessinées par la page (canvas, SVG construit en JS).
    blocs.forEach((b) => {
      if (b.figure != null && typeof b.dessiner === 'function') {
        const el = document.getElementById(b._id);
        if (el) b.dessiner(el);
      }
    });
    PAGE = 1; paginer();
    racine.querySelector('.pages-nav .prec').onclick = () => { montrerPage(PAGE - 1); emettre(); };
    racine.querySelector('.pages-nav .suiv').onclick = () => { montrerPage(PAGE + 1); emettre(); };
    racine.querySelectorAll('img').forEach((im) => { if (!im.complete) im.addEventListener('load', paginer, { once: true }); });
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(paginer);
    document.title = `${i.m.fr || 'Examen'} ${i.annee}${i.ratt ? ' rattrapage' : ' normale'} — ${titre.replace(/<[^>]+>/g, '')}`;
    envoyer({ type: 'simulation_ready' });
    manifeste(); emettre();
    setTimeout(manifeste, 400);
    window.__feuillePrete = true;
  }


  // ── Pages (19/11/2026, l'utilisateur : « l'exercice n'est pas totalement affiché ; l'afficher comme deux pages,
  // l'une après l'autre, pour garantir que tout l'exercice s'affiche ») ────────────────────────────────────────────
  // La feuille est coupée entre deux blocs (titre, texte, question, figure) pour que chaque page tienne en entier dans
  // le cadre, sans défiler. Page 1 : l'en-tête complet, le titre et le premier texte ; pages suivantes : l'en-tête
  // court, comme sur le vrai sujet. Une page encore trop haute (un bloc très long) est réduite pour tenir (≥ 0,72).
  // On passe d'une page à l'autre avec les boutons ◀ ▶ ; le tuteur qui surligne une question amène sa page.
  let PAGE = 1, NPAGES = 1, BESOIN = {}, DISPO = {}, COURTE1 = false;
  function montrerPage(n) {
    const corps = document.querySelector('.feuille .corps');
    if (!corps) return;
    PAGE = Math.max(1, Math.min(NPAGES, n));
    const vus = [];
    corps.querySelectorAll(':scope > [data-page]').forEach((el) => {
      const ici = +el.dataset.page === PAGE; el.style.display = ici ? '' : 'none'; if (ici) vus.push(el);
    });
    corps.classList.toggle('sans-titre', !!vus.length && !vus[0].classList.contains('titre-exo'));
    const ec = document.querySelector('.feuille .entete-complete'), ek = document.querySelector('.feuille .entete-courte');
    if (ec) ec.style.display = PAGE === 1 && !COURTE1 ? '' : 'none';
    if (ek) ek.style.display = (PAGE === 1 && !COURTE1) || !NPAGES || (NPAGES === 1 && !COURTE1) ? 'none' : '';
    const zone = document.querySelector('.feuille-zone');
    // une partie (règle 48) n'est jamais coupée en bas : elle peut descendre un peu plus bas (0,44) qu'une feuille entière
    const zPlancher = (CFG.questions ?? P.get('questions')) || (CFG.partie ?? P.get('partie')) ? 0.44 : 0.5;
    let z = BESOIN[PAGE] > DISPO[PAGE] ? Math.max(zPlancher, DISPO[PAGE] / BESOIN[PAGE]) : 1;
    if (zone) zone.style.zoom = z < 1 ? z.toFixed(3) : '';
    // la mesure par blocs sous-estime parfois (figures flottantes) : on resserre tant que la page déborde réellement
    while (zone && z > zPlancher && document.documentElement.scrollHeight > innerHeight + 2) {
      z = Math.max(zPlancher, z - 0.02); zone.style.zoom = z.toFixed(3);
    }
    const nav = document.querySelector('.pages-nav');
    if (nav) {
      nav.style.display = NPAGES > 1 ? '' : 'none';
      nav.querySelector('.num').textContent = `page ${PAGE} / ${NPAGES}`;
      nav.querySelector('.prec').disabled = PAGE === 1;
      nav.querySelector('.suiv').disabled = PAGE === NPAGES;
    }
    scrollTo({ top: 0 });
  }
  function paginer() {
    const corps = document.querySelector('.feuille .corps');
    if (!corps) return;
    const zone = document.querySelector('.feuille-zone'), feuille = document.querySelector('.feuille');
    const cadre = document.querySelector('.feuille-cadre'), nav = document.querySelector('.pages-nav');
    if (zone) zone.style.zoom = '';
    corps.classList.remove('sans-titre');
    const blocs = [...corps.children].filter((el) => getComputedStyle(el).position !== 'absolute');
    blocs.forEach((el) => { el.style.display = ''; delete el.dataset.page; });
    const ec = document.querySelector('.feuille .entete-complete'), ek = document.querySelector('.feuille .entete-courte');
    if (ec) ec.style.display = ''; if (ek) ek.style.display = '';
    if (nav) nav.style.display = '';
    document.documentElement.classList.add('en-pages');
    const px = (el, ...p) => p.reduce((s, k) => s + (parseFloat(getComputedStyle(el)[k]) || 0), 0);
    const hauteur = (el) => el.offsetHeight + px(el, 'marginTop', 'marginBottom');
    const fixe = px(zone, 'paddingTop', 'paddingBottom') + px(feuille, 'paddingTop', 'paddingBottom')
      + px(cadre, 'paddingTop', 'paddingBottom', 'borderTopWidth', 'borderBottomWidth')
      + (nav ? hauteur(nav) : 0) + 4;
    let hC = ec ? hauteur(ec) : 0; const hK = ek ? hauteur(ek) : 0;
    COURTE1 = false;
    const dispo = (p) => innerHeight - fixe - (p === 1 ? hC : hK);
    BESOIN = {}; DISPO = {};
    // Positions réelles (une figure flottante est à côté du texte, pas en dessous) : haut et bas de chaque bloc.
    const y0 = corps.getBoundingClientRect().top;
    const haut = (el) => el.getBoundingClientRect().top - y0 - (parseFloat(getComputedStyle(el).marginTop) || 0);
    const bas = (el) => el.getBoundingClientRect().bottom - y0 + (parseFloat(getComputedStyle(el).marginBottom) || 0);
    const visibles = blocs.filter((el) => el.offsetHeight > 0);
    const total = visibles.length ? Math.max(...visibles.map(bas)) - Math.min(...visibles.map(haut)) : 0;
    // 1. Tout tient sur UNE page en réduisant (≥ 0,6) : une seule page, sans passer à une autre (19/11/2026,
    //    l'utilisateur : « tout mettre dans une seule vue, une seule page suffit »).
    // La réduction s'applique à toute la feuille (en-tête compris) : on compare la hauteur de la page entière à l'écran.
    const pleine = (p, contenu) => fixe + (p === 1 ? hC : hK) + contenu;
    // Le grand en-tête n'est gardé que si la feuille reste presque à sa taille (≥ 0,9) ; sinon la page 1 prend l'en-tête
    // court, comme les suivantes, et le texte garde sa place (19/11/2026, l'utilisateur, captures 2020 R ex. 3 :
    // « c'est mieux de détailler pour prendre de l'espace, comme la deuxième page »).
    if (ec && ek && pleine(1, total) * 0.9 > innerHeight) { COURTE1 = true; hC = hK; }
    // Jamais plus petit que 0,75 : une partie trop longue pour une page passe à deux pages (règle 48 : la diapo d'énoncé
    // ne montre que les 1 à 3 questions traitées juste après, ce qui tient d'habitude sur une page).
    // Une PARTIE (questions= ou partie=, règle 48) se rassemble toujours sur une seule page, quitte à réduire jusqu'à
    // 0,5 (19/11/2026, l'utilisateur, capture 2022 N ex. 2 « 3-2 » seule en page 2/2 : « veuillez rassembler à une
    // seule page » ; le cadre réel du lecteur fait ~1126×460 à 1366 px de large).
    const enPartie = !!(CFG.questions ?? P.get('questions')) || !!(CFG.partie ?? P.get('partie'));
    const ZMIN = enPartie ? 0.5 : 0.75;
    if (pleine(1, total) * ZMIN <= innerHeight) {
      blocs.forEach((el) => { el.dataset.page = 1; });
      NPAGES = 1; DISPO[1] = innerHeight; BESOIN[1] = pleine(1, total);
      montrerPage(1);
      return;
    }
    // 2. Sinon, des pages faites d'« unités » qu'on ne coupe jamais (19/11/2026, l'utilisateur : « mettre tous les
    //    documents dans une seule page avec leur question ») : le titre et le texte d'ouverture ; puis chaque question
    //    avec tous les documents et textes qui la précèdent (ou, pour la question d'exam.json, la suivent : sa figure).
    //    Chaque page se remplit d'unités et se réduit au besoin (jusqu'à 0,62 ; 0,5 pour une unité seule très haute).
    const unites = []; let u = [];
    const fin = () => { if (u.length) unites.push(u); u = []; };
    const estQ = (b) => b.classList.contains('q');
    // un document : une figure, une grille (propositions d'un QCM), ou un texte qui est un document (id « doc… », ou un tableau de données)
    const estFig = (b) => b.classList.contains('fig') || b.classList.contains('grille') || /^doc/i.test(b.id || '') || (b.classList.contains('contexte') && !!b.querySelector('table'));
    blocs.forEach((el, k) => {
      const q = estQ(el), fig = estFig(el);
      if (!unites.length && u.length && (q || fig) && !u.some((b) => estQ(b) || estFig(b))) fin();   // l'ouverture
      u.push(el);
      const suivFig = blocs[k + 1] && estFig(blocs[k + 1]);
      if (q && !suivFig) fin();                              // une question ferme son unité…
      else if (fig && u.some(estQ) && !suivFig) fin();       // …ou la figure d'exam.json qui la suit
    });
    fin();
    // l'ouverture (titre, texte d'introduction) ne reste jamais seule : elle part avec la première question
    // (19/11/2026, captures SVT 2024 R et 2022 N : la page 1 n'avait que l'en-tête et le titre)
    if (unites.length > 1 && !unites[0].some((b) => estQ(b))) unites.splice(0, 2, unites[0].concat(unites[1]));
    const hU = (un) => { const v = un.filter((el) => el.offsetHeight > 0); return v.length ? Math.max(...v.map(bas)) - Math.min(...v.map(haut)) : 0; };
    let page = 1, plein = 0;
    unites.forEach((un, i) => {
      const h = hU(un);
      // une unité sans hauteur (le <div class="clair"> de fin) ne commence jamais une page à elle seule
      if (i > 0 && plein > 0 && h > 2 && pleine(page, plein + h) * ZMIN > innerHeight) { BESOIN[page] = pleine(page, plein); page += 1; plein = 0; }
      un.forEach((el) => { el.dataset.page = page; });
      plein += h;
    });
    BESOIN[page] = pleine(page, plein);
    NPAGES = page;
    for (let p = 1; p <= NPAGES; p++) DISPO[p] = innerHeight;
    if (NPAGES === 1) document.documentElement.classList.remove('en-pages');
    montrerPage(Math.min(PAGE, NPAGES));
  }
  function pageDe(el) {
    for (let e = el; e && e !== document.body; e = e.parentElement) if (e.dataset && e.dataset.page) return +e.dataset.page;
    return PAGE;
  }

  window.Feuille = { rendre, surligner, effacer, md, etat };
  // Démarrage : window.FEUILLE (page à soi) ou les paramètres de l'URL (feuille.html?sujet=…).
  const go = () => { if (window.FEUILLE_MANUELLE) return; if (window.FEUILLE || P.get('sujet')) rendre(window.FEUILLE || {}).catch((e) => console.error(e)); };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', go); else go();
})();
