import { useState } from "react";
import "../App.css";
import "./Mapa.css";
import Sidebar from "../components/Sidebar";
import LeafletMap from "../components/LeafletMap";
import PageHeader from "../components/PageHeader";

function Mapa() {
  const [viewType, setViewType] = useState("markers");

  return (
    <div className="app">
      <Sidebar />

      <main className="content">
        <PageHeader
          title="Mapa"
          subtitle="Visualização geográfica das notícias"
        >
          <div className="view-selector">
            <button
              className={`view-btn ${
                viewType === "markers" ? "active" : ""
              }`}
              onClick={() => setViewType("markers")}
            >
              📍 Marcadores
            </button>

            <button
              className={`view-btn ${
                viewType === "heat" ? "active" : ""
              }`}
              onClick={() => setViewType("heat")}
            >
              🔥 Calor
            </button>
          </div>
        </PageHeader>

        <section className="full-box">
          <h3>Distribuição das notícias pelo Brasil</h3>

          <div className="map-page-container">
            <LeafletMap viewType={viewType} />
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