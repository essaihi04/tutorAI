const g = globalThis; g.window = g;
g.localStorage = { getItem() { return null; }, setItem() {}, removeItem() {} }; g.sessionStorage = g.localStorage;
g.document = { addEventListener() {}, removeEventListener() {}, createElement() { return { style: {}, getContext() { return null; } }; }, documentElement: { style: {} }, body: {} };
g.addEventListener = () => {}; g.location = { search: '', pathname: '/', href: '', origin: 'https://moalim.online' };
g.matchMedia = () => ({ matches: false, addEventListener() {} }); g.Audio = function () {};
require(__dirname + '/banc.cjs');
