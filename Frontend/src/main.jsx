/**
============================================================================
 Arquivo: main.jsx
 
 Ponto de entrada da aplicação React.
 
 Responsabilidades:
 - Inicializar a aplicação.
 - Renderizar o componente principal (App).
 - Aplicar o StrictMode durante o desenvolvimento para auxiliar na
 - identificação de possíveis problemas e boas práticas.
 - Importar os estilos globais da aplicação.
============================================================================
 */


import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import App from './App.jsx'
import './index.css'

// Renderiza a aplicação dentro da div "root" definida no index.html.

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>,
)