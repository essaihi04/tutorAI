import React from 'react';
import katex from 'katex';
import 'katex/dist/katex.min.css';

interface LatexRendererProps {
  content: string;
  display?: boolean;
}

const LatexRenderer: React.FC<LatexRendererProps> = ({ content, display = false }) => {
  if (!content) return null;

  // Split content into LaTeX and plain text parts
  // Supported delimiters: $...$ (inline), $$...$$ (display), \(...\) (inline), \[...\] (display)
  // NOTE: in a JS regex, the literal \( is written \\\( (escape \\ for backslash, escape \( for the paren),
  // and the literal \[ is written \\\[ (the [ must be escaped to avoid opening a character class).
  const parts: React.ReactNode[] = [];
  let lastIndex = 0;
  const regex = /(\$\$[\s\S]*?\$\$|\\\[[\s\S]*?\\\]|\$[\s\S]*?\$|\\\([\s\S]*?\\\))/g;
  let match;

  while ((match = regex.exec(content)) !== null) {
    // Add plain text before LaTeX
    if (match.index > lastIndex) {
      parts.push(<span key={`text-${lastIndex}`}>{content.slice(lastIndex, match.index)}</span>);
    }

    const latex = match[0];
    const isDisplay = latex.startsWith('$$') || latex.startsWith('\\[');
    // Strip the delimiters (in any of the 4 supported forms) — order matters: longest first.
    let innerLatex = latex;
    if (innerLatex.startsWith('$$') && innerLatex.endsWith('$$')) {
      innerLatex = innerLatex.slice(2, -2);
    } else if (innerLatex.startsWith('\\[') && innerLatex.endsWith('\\]')) {
      innerLatex = innerLatex.slice(2, -2);
    } else if (innerLatex.startsWith('\\(') && innerLatex.endsWith('\\)')) {
      innerLatex = innerLatex.slice(2, -2);
    } else if (innerLatex.startsWith('$') && innerLatex.endsWith('$')) {
      innerLatex = innerLatex.slice(1, -1);
    }

    try {
      const html = katex.renderToString(innerLatex, {
        displayMode: isDisplay || display,
        throwOnError: false,
        trust: true,
      });
      parts.push(
        <span
          key={`latex-${match.index}`}
          dangerouslySetInnerHTML={{ __html: html }}
          className={isDisplay || display ? 'block my-2' : 'inline'}
        />
      );
    } catch (e) {
      // Fallback to plain text if LaTeX parsing fails
      parts.push(<span key={`fallback-${match.index}`}>{latex}</span>);
    }

    lastIndex = match.index + match[0].length;
  }

  // Add remaining plain text
  if (lastIndex < content.length) {
    parts.push(<span key={`text-${lastIndex}`}>{content.slice(lastIndex)}</span>);
  }

  return <>{parts}</>;
};

export default LatexRenderer;
