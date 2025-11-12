import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.tsx'


createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <div className="min-h-screen bg-cover bg-center" style={{ backgroundImage: "url('/image/background.jpg')" }}>
      <App />
    </div>
  </StrictMode>,
)
