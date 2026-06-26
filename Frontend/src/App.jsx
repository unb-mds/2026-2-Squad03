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