import "../App.css";
import Sidebar from "../components/Sidebar";
import BrazilMap from "../components/BrazilMap";

function Mapa() {
  return (
    <div className="app">
      <Sidebar />

      <main className="content">
        <header className="header">
          <div>
            <h2>Mapa</h2>
            <p>Visualização geográfica das notícias monitoradas</p>
          </div>
        </header>

        <section className="full-box">
          <h3>Distribuição das notícias pelo Brasil</h3>

          <div className="map-page-container">
            <BrazilMap />
          </div>
        </section>
      </main>
    </div>
  );
}

export default Mapa;