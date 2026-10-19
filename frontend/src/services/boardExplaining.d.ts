declare class BoardExplaining {
  /** Le tableau commence à expliquer ; la fonction rendue l'arrête (idempotente). */
  begin(): () => void;
  readonly active: boolean;
  subscribe(fn: (explaining: boolean) => void): () => void;
}
export const boardExplaining: BoardExplaining;
