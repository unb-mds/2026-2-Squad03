/**
 ===========================================================================
 Arquivo: App.jsx
 
 Componente raiz da aplicação.
 
 Responsabilidades:
 - Configurar o sistema de roteamento da aplicação.
 - Definir as páginas disponíveis.
 - Controlar a navegação entre as telas utilizando React Router.
 
 Observação:
 É utilizado HashRouter para facilitar o deploy em ambientes estáticos,
 como o GitHub Pages, evitando problemas com atualização direta das rotas.
 =========================================================================
 */

import { HashRouter, Routes, Route } from "react-router-dom";

import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import Noticias from "./pages/Noticias";
import Sobre from "./pages/Sobre";
import Mapa from "./pages/Mapa";
import DetalhesNoticia from "./pages/DetalhesNoticia";

function App() {
  return (
    <HashRouter>
     <Routes>
      <Route path="/" element={<Dashboard />} />
      <Route path="/dashboard" element={<Dashboard />} />
      <Route path="/login" element={<Login />} />
      <Route path="/noticias" element={<Noticias />} />
      <Route path="/noticias/:id" element={<DetalhesNoticia />} />
      <Route path="/sobre" element={<Sobre />} />
      <Route path="/mapa" element={<Mapa />} />
</Routes>
    </HashRouter>
  );
}

export default App;
