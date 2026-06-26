import "../App.css";
import "./Mapa.css";
import Sidebar from "../components/Sidebar";
import LeafletMap from "../components/LeafletMap";

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
    <LeafletMap />
  </div>

  <div className="map-legend">

    <div className="legend-header">
      <span className="legend-icon">🗺️</span>
      <h4>Legenda do mapa</h4>
    </div>

    <div className="legend-items">

      <div className="legend-item">
        <span className="legend-dot red"></span>
        <span>Feminicídio</span>
      </div>

      <div className="legend-item">
        <span className="legend-dot orange"></span>
        <span>Violência Doméstica</span>
      </div>

      <div className="legend-item">
        <span className="legend-dot blue"></span>
        <span>Outros</span>
      </div>

    </div>

  </div>

</section>
      </main>
    </div>
  );
}

export default Mapa;