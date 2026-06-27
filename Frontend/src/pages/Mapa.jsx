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
        <PageHeader title="Mapa" subtitle="Visualização geográfica das notícias">
          <div className="view-selector">
            <button className={`view-btn ${viewType === 'markers' ? 'active' : ''}`} onClick={() => setViewType("markers")}>📍 Marcadores</button>
            <button className={`view-btn ${viewType === 'heat' ? 'active' : ''}`} onClick={() => setViewType("heat")}>🔥 Calor</button>
          </div>
        </PageHeader>

        <section className="full-box">
          <div className="map-page-container">
            <LeafletMap viewType={viewType} />
          </div>
        </section>
      </main>
    </div>
  );
}

export default Mapa;