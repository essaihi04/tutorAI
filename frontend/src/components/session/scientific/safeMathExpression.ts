type Evaluator = (x: number) => number;

type Token =
  | { kind: 'number'; value: number }
  | { kind: 'identifier'; value: string }
  | { kind: 'operator'; value: '+' | '-' | '*' | '/' | '^' }
  | { kind: 'leftParen' | 'rightParen' | 'end' };

const FUNCTIONS: Record<string, (value: number) => number> = {
  sin: Math.sin,
  cos: Math.cos,
  tan: Math.tan,
  asin: Math.asin,
  acos: Math.acos,
  atan: Math.atan,
  sqrt: Math.sqrt,
  abs: Math.abs,
  exp: Math.exp,
  ln: Math.log,
  log: Math.log10,
  floor: Math.floor,
  ceil: Math.ceil,
  round: Math.round,
};

function tokenize(expression: string): Token[] | null {
  if (expression.length > 100) return null;
  const tokens: Token[] = [];
  let index = 0;

  while (index < expression.length) {
    const character = expression[index];
    if (/\s/.test(character)) {
      index += 1;
      continue;
    }

    const rest = expression.slice(index);
    const numberMatch = rest.match(/^(?:\d+(?:\.\d*)?|\.\d+)/);
    if (numberMatch) {
      const value = Number(numberMatch[0]);
      if (!Number.isFinite(value)) return null;
      tokens.push({ kind: 'number', value });
      index += numberMatch[0].length;
      continue;
    }

    const identifierMatch = rest.match(/^[A-Za-z]+/);
    if (identifierMatch) {
      tokens.push({ kind: 'identifier', value: identifierMatch[0].toLowerCase() });
      index += identifierMatch[0].length;
      continue;
    }

    if (character === '(') tokens.push({ kind: 'leftParen' });
    else if (character === ')') tokens.push({ kind: 'rightParen' });
    else if (character === '+' || character === '-' || character === '*' || character === '/' || character === '^') {
      tokens.push({ kind: 'operator', value: character });
    } else {
      return null;
    }
    index += 1;
    if (tokens.length > 80) return null;
  }

  tokens.push({ kind: 'end' });
  return tokens;
}

class ExpressionParser {
  private index = 0;
  private readonly tokens: Token[];

  constructor(tokens: Token[]) {
    this.tokens = tokens;
  }

  parse(): Evaluator | null {
    const evaluator = this.parseAdditive();
    return evaluator && this.peek().kind === 'end' ? evaluator : null;
  }

  private peek(): Token {
    return this.tokens[this.index] || { kind: 'end' };
  }

  private take(): Token {
    const token = this.peek();
    this.index += 1;
    return token;
  }

  private takeOperator(value: '+' | '-' | '*' | '/' | '^'): boolean {
    const token = this.peek();
    if (token.kind !== 'operator' || token.value !== value) return false;
    this.take();
    return true;
  }

  private parseAdditive(): Evaluator | null {
    let left = this.parseMultiplicative();
    if (!left) return null;

    while (true) {
      const operator = this.peek();
      if (operator.kind !== 'operator' || (operator.value !== '+' && operator.value !== '-')) break;
      this.take();
      const right = this.parseMultiplicative();
      if (!right) return null;
      const previous: Evaluator = left;
      const operand: Evaluator = right;
      left = operator.value === '+'
        ? (x: number): number => previous(x) + operand(x)
        : (x: number): number => previous(x) - operand(x);
    }
    return left;
  }

  private parseMultiplicative(): Evaluator | null {
    let left = this.parseUnary();
    if (!left) return null;

    while (true) {
      const operator = this.peek();
      if (operator.kind !== 'operator' || (operator.value !== '*' && operator.value !== '/')) break;
      this.take();
      const right = this.parseUnary();
      if (!right) return null;
      const previous: Evaluator = left;
      const operand: Evaluator = right;
      left = operator.value === '*'
        ? (x: number): number => previous(x) * operand(x)
        : (x: number): number => previous(x) / operand(x);
    }
    return left;
  }

  private parseUnary(): Evaluator | null {
    if (this.takeOperator('+')) return this.parseUnary();
    if (this.takeOperator('-')) {
      const value = this.parseUnary();
      return value ? x => -value(x) : null;
    }
    return this.parsePower();
  }

  private parsePower(): Evaluator | null {
    const base = this.parsePrimary();
    if (!base) return null;
    if (!this.takeOperator('^')) return base;
    const exponent = this.parseUnary();
    return exponent ? x => Math.pow(base(x), exponent(x)) : null;
  }

  private parsePrimary(): Evaluator | null {
    const token = this.take();
    if (token.kind === 'number') return () => token.value;

    if (token.kind === 'leftParen') {
      const value = this.parseAdditive();
      if (!value || this.take().kind !== 'rightParen') return null;
      return value;
    }

    if (token.kind !== 'identifier') return null;
    if (token.value === 'x') return x => x;
    if (token.value === 'pi') return () => Math.PI;
    if (token.value === 'e') return () => Math.E;

    const fn = FUNCTIONS[token.value];
    if (!fn || this.take().kind !== 'leftParen') return null;
    const argument = this.parseAdditive();
    if (!argument || this.take().kind !== 'rightParen') return null;
    return x => fn(argument(x));
  }
}

export function compileSafeMathExpression(expression: string): Evaluator | null {
  const tokens = tokenize(expression);
  if (!tokens) return null;
  const evaluator = new ExpressionParser(tokens).parse();
  if (!evaluator) return null;
  return x => {
    const value = evaluator(x);
    return Number.isFinite(value) ? value : Number.NaN;
  };
}
