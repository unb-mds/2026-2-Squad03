import { useEffect, useState } from "react";
import Sidebar from "../components/Sidebar";
import LeafletMap from "../components/LeafletMap";
import Calendario from "../components/Calendario";
import "../App.css";
import "./Mapa.css";

export default function Mapa() {
  const [viewType, setViewType] = useState("markers");

  const [geoJsonData, setGeoJsonData] = useState(null);
  const [noticiasFiltradas, setNoticiasFiltradas] = useState([]);

  useEffect(() => {
    fetch("https://two026-2-veritasia.onrender.com/mapa/")
      .then((res) => res.json())
      .then((data) => {
        setGeoJsonData(data);
        setNoticiasFiltradas(data.features);
      });
  }, []);
  

function filtrarPorPeriodo(inicio, fim) {
  if (!geoJsonData?.features) {
    return;
  }


  const filtradas = geoJsonData.features.filter((n) => {
    const data = new Date(n.properties.data);

    return (
      data >= new Date(inicio) &&
      data <= new Date(fim)
    );
  });

  setNoticiasFiltradas(filtradas);
}
  return (
    <div className="app">
      <Sidebar />

      <main className="content map-content">
        <div className="map-fullbleed">

          {/* HEADER */}
          <div className="map-floating-header">
            <div>
              <h2>Mapa</h2>
              <p>Visualização geográfica das notícias</p>
            </div>

            <div className="calendario-container">
              <Calendario onPeriodoChange={filtrarPorPeriodo} />
            </div>


            <div className="view-selector">

              <button
                className={`view-btn ${viewType === "markers" ? "active" : ""}`}
                onClick={() => setViewType("markers")}
              >
                Marcadores
              </button>

              <button
                className={`view-btn ${viewType === "heat" ? "active" : ""}`}
                onClick={() => setViewType("heat")}
              >
                Calor
              </button>
            </div>
          </div>

          {/* MAPA */}
          <div className="map-fullbleed-container">
            <LeafletMap
              viewType={viewType}
              noticias={noticiasFiltradas}
            />
          </div>

        </div>
      </main>
    </div>
  );
}