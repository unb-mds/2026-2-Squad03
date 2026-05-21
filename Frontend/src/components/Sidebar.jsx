import logoVeritas from "../assets/logo.png";

function Sidebar() {
  return (
    <aside className="sidebar">
      <img className="sidebar-logo" src={logoVeritas} alt="Logo Veritas IA" />

      <nav className="menu">
        <a className="active">Dashboard</a>
        <a>Mapa</a>
        <a>Notícias</a>
        <a>Sobre Nós</a>
      </nav>
    </aside>
  );
}

export default Sidebar;
