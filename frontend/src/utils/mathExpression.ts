/** Numeric expressions only. Never compile course or model text as JavaScript. */
const functions: Record<string, (...args: number[]) => number> = {
  sin: Math.sin, cos: Math.cos, tan: Math.tan, abs: Math.abs, sqrt: Math.sqrt,
  ln: Math.log, log: Math.log10, exp: Math.exp, min: Math.min, max: Math.max,
  pow: Math.pow,
};

export function evaluateMathExpression(source: string, x: number): number | null {
  if (source.length > 512 || !Number.isFinite(x)) return null;
  try {
    const input = source.replace(/\bMath\./g, '').toLowerCase();
    const tokens: string[] = [];
    const pattern = /\s*(\d+(?:\.\d*)?(?:e[+-]?\d+)?|\.\d+(?:e[+-]?\d+)?|[a-z]+|\*\*|[+\-*/^(),])/gy;
    let offset = 0;
    while (offset < input.trimEnd().length) {
      pattern.lastIndex = offset;
      const match = pattern.exec(input);
      if (!match) return null;
      tokens.push(match[1]);
      offset = pattern.lastIndex;
    }
    if (tokens.length > 256) return null;
    let pos = 0;
    const expression = (minimum = 0): number => {
      const token = tokens[pos++];
      let value: number;
      if (token === '+' || token === '-') {
        value = (token === '-' ? -1 : 1) * expression(30);
      } else if (token === '(') {
        value = expression();
        if (tokens[pos++] !== ')') throw new Error('Parenthesis');
      } else if (token === 'x') value = x;
      else if (token === 'pi') value = Math.PI;
      else if (token === 'e') value = Math.E;
      else if (Object.hasOwn(functions, token)) {
        if (tokens[pos++] !== '(') throw new Error('Function arguments');
        const args = [expression()];
        while (tokens[pos] === ',') { pos++; args.push(expression()); }
        if (tokens[pos++] !== ')' || args.length > 8) throw new Error('Function arguments');
        value = functions[token](...args);
      } else if (token && /^(?:\d|\.)/.test(token)) value = Number(token);
      else throw new Error('Unknown expression');

      while (pos < tokens.length) {
        const op = tokens[pos];
        const precedence = op === '+' || op === '-' ? 10 : op === '*' || op === '/' ? 20 : op === '^' || op === '**' ? 40 : 0;
        if (precedence <= minimum) break;
        pos++;
        const right = expression(precedence === 40 ? 39 : precedence);
        if (op === '+') value += right;
        else if (op === '-') value -= right;
        else if (op === '*') value *= right;
        else if (op === '/') value /= right;
        else value **= right;
      }
      return value;
    };
    const result = expression();
    return pos === tokens.length && Number.isFinite(result) ? result : null;
  } catch { return null; }
}
