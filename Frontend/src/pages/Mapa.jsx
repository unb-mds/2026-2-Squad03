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

            <div className="map-legend">
              <h4>Legenda</h4>

            <div className="legend-item">
              <span className="legend-dot red"></span>
                Feminicídio
            </div>

            <div className="legend-item">
              <span className="legend-dot orange"></span>
                Violência doméstica
            </div>

            <div className="legend-item">
              <span className="legend-dot blue"></span>
                Outros
            </div>
          </div>

          </div>

        </section>
      </main>
    </div>
  );
}

export default Mapa;