// Phrases que le tableau des cours prononcera, calculées avec le code même de la page
// (slideVersScript + toSpokenText) : les clés du cache vocal sont alors identiques.
//   node scripts/phrases_cours.cjs decks.json phrases_cours.json
// decks.json : export des cours publiés (scripts/exporter_decks.py, sur le serveur).
// Puis : python -m scripts.kaggle_tts cours phrases_cours.json
const fs = require('fs');
const path = require('path');
const FRONT = path.resolve(__dirname, '../../frontend');
const ts = require(path.join(FRONT, 'node_modules/typescript'));
const [entree = 'decks.json', sortie = 'phrases_cours.json'] = process.argv.slice(2);

function charger(rel) {
  const src = fs.readFileSync(path.join(FRONT, 'src', rel), 'utf8');
  const js = ts.transpileModule(src, { compilerOptions: { module: ts.ModuleKind.CommonJS, target: ts.ScriptTarget.ES2020 } }).outputText;
  const m = { exports: {} };
  new Function('module', 'exports', 'require', js)(m, m.exports, require);
  return m.exports;
}

const { toSpokenText } = charger('utils/mathSpeech.ts');
const { slideVersScript } = charger('components/course/slideVersScript.ts');
const decks = JSON.parse(fs.readFileSync(entree, 'utf8'));

const vues = new Map();   // clé lang|texte -> {lang, texte}
const ajouter = (lang, brut) => {
  const t = toSpokenText(brut || '');
  if (t && t.trim()) vues.set(`${lang}|${t}`, { lang, texte: t });
};
let diapos = 0;
for (const deck of decks) {
  for (const activite of deck.activities || []) {
    for (const slide of activite.slides || []) {
      diapos += 1;
      for (const langue of ['fr', 'mixed']) {
        const { steps } = slideVersScript(slide, langue);
        for (const step of steps) {
          if (step.action === 'write' && step.line && step.line.content) ajouter('fr', step.line.content);  // LANGUE_DU_TABLEAU
          if (step.action === 'ask') ajouter(langue, (step.say && step.say.trim()) || step.text);
          if ((step.action === 'figure' || step.action === 'bloc') && typeof step.say === 'string') ajouter(langue, step.say);
        }
      }
    }
  }
}
const liste = [...vues.values()];
fs.writeFileSync(sortie, JSON.stringify(liste, null, 1));
const car = liste.reduce((n, p) => n + p.texte.length, 0);
console.log(`${diapos} diapositives -> ${liste.length} phrases (${liste.filter(p => p.lang === 'fr').length} fr, ${liste.filter(p => p.lang === 'mixed').length} darija), ${car} caractères`);
console.log(liste.slice(0, 6).map(p => `${p.lang}: ${p.texte.slice(0, 80)}`).join('\n'));
