/**
 * ============================================================================
 * Componente: Sidebar
 * ----------------------------------------------------------------------------
 * Menu lateral utilizado para navegação entre
 * as principais páginas da aplicação.
 *
 * Funcionalidades:
 * - Exibe a identidade visual do sistema.
 * - Permite navegar entre Dashboard, Mapa,
 *   Notícias e Sobre.
 * - Disponibiliza acesso à documentação do projeto.
 * ============================================================================
 */

import logoVeritas from "../assets/logo_white.png";
import { Link } from "react-router-dom";

function Sidebar() {
  return (
    <aside className="sidebar">
      <img className="sidebar-logo" src={logoVeritas} alt="Logo Veritas IA" />
      
        <nav className="menu">
          <Link to="/dashboard">Dashboard</Link>

          <Link to="/mapa">Mapa</Link>

          <Link to="/noticias">Notícias</Link>

          <Link to="/sobre">Sobre Nós</Link>

          <a href="/2026-2-VeritasIA/docs/" target="_blank">
            Documentação
          </a>
        </nav>
        
    </aside>
  );
}

export default Sidebar;
