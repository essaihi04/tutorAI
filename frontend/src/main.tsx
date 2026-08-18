import { createRoot } from 'react-dom/client'
import './index.css'
// Écoute le premier geste de l'élève dès le tout premier écran : c'est ce qui
// permet au professeur de parler tout seul à l'ouverture d'une session, sans
// réclamer un clic « activer le son » (voir services/audioUnlock.ts).
import './services/audioUnlock'
import App from './App.tsx'

createRoot(document.getElementById('root')!).render(
  <App />,
)
