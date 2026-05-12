import logo from "../assets/logo.png";

function Sidebar() {
  return (
    <aside className="sidebar">
      <img className="sidebar-logo" src={logo} alt="Logo Veritas IA" />

      <nav className="menu">
        <a className="active">Dashboard</a>
        <a>Notícias</a>
        <a>Mapa</a>
        <a>Análises</a>
        <a>Palavras-chave</a>
        <a>Relatórios</a>
        <a>Fontes</a>
        <a>Configurações</a>
      </nav>
    </aside>
  );
}

export default Sidebar;
