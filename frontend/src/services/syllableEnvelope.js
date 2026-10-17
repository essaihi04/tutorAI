/**
 * Ouverture de bouche (0 → 1) qui suit les syllabes d'une voix, à partir du RMS du signal joué.
 *
 * - Contraste syllabique : le RMS instantané est comparé à sa moyenne glissante (~120 ms). Le noyau
 *   vocalique d'une syllabe dépasse cette moyenne, les consonnes et les pauses retombent dessous :
 *   la bouche s'ouvre et se referme à chaque syllabe au lieu de rester ouverte pendant toute la phrase.
 * - Porte de niveau : rapportée au pic récent de la voix, elle ferme la bouche dans les silences
 *   et le souffle, quel que soit le volume de l'enregistrement.
 * - Compensation de latence : l'analyse voit le son avant qu'il ne sorte du haut-parleur
 *   (`AudioContext.outputLatency` + `baseLatency`) ; la valeur rendue est retardée d'autant.
 * - Attaque rapide, fermeture un peu plus lente, comme une mâchoire.
 *
 * Réglages choisis sur les enregistrements des cours : environ 3 ouvertures par seconde de parole,
 * contre 0,6 à 0,9 pour l'ancienne enveloppe, qui restait au maximum 70 à 80 % du temps.
 */
const smooth = (a, b, x) => { const t = Math.min(1, Math.max(0, (x - a) / (b - a))); return t * t * (3 - 2 * t); };

export class SyllableEnvelope {
  constructor({ floor = 0.006, slowTau = 0.12, low = 0.9, high = 1.5, attack = 0.015, release = 0.05, window = 0.6 } = {}) {
    Object.assign(this, { floor, slowTau, low, high, attack, release, window });
    this.reset();
  }

  /**
   * @param {number} rms       RMS instantané du signal (non écrêté)
   * @param {number} dt        secondes écoulées depuis l'appel précédent
   * @param {number} now       horloge en secondes
   * @param {number} latency   latence de sortie audio en secondes
   * @returns {number} ouverture 0…1, alignée sur le son entendu
   */
  push(rms, dt, now, latency = 0) {
    this.slow += (rms - this.slow) * (1 - Math.exp(-dt / this.slowTau));
    this.peak = Math.max(rms, this.peak * Math.exp(-dt / 1.4), 0.02);
    const gate = smooth(0.05, 0.25, rms / this.peak);
    const target = rms < this.floor ? 0 : gate * smooth(this.low, this.high, rms / Math.max(this.slow, 0.004));
    this.trail.push([now, target]);
    while (this.trail.length > 2 && this.trail[0][0] < now - this.window) this.trail.shift();
    const wanted = now - Math.min(this.window * 0.8, Math.max(0, latency));
    let delayed = this.trail[0][1];
    for (const [t, v] of this.trail) { if (t <= wanted) delayed = v; else break; }
    const tau = delayed > this.open ? this.attack : this.release;
    this.open += (delayed - this.open) * (1 - Math.exp(-dt / tau));
    return this.open;
  }

  reset() { this.open = 0; this.trail = []; this.peak = 0.02; this.slow = 0.02; }
}
