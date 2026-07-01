/**
 * ============================================================================
 * Componente: Mapa
 * ----------------------------------------------------------------------------
 * Página responsável pela visualização geográfica das notícias monitoradas
 * pelo sistema VeritasIA.
 *
 * Funcionalidades:
 * - Exibe o mapa interativo ocupando toda a área da aba.
 * - Permite alternar entre visualização por marcadores e mapa de calor
 *   através de um painel flutuante sobre o mapa.
 * - Apresenta uma legenda flutuante com as categorias monitoradas.
 *
 * Componentes utilizados:
 * - Sidebar
 * - LeafletMap
 *
 * Dependências:
 * - React
 * - React Leaflet
 * ============================================================================
 */

import { useState } from "react";
import "../App.css";
import "./Mapa.css";
import Sidebar from "../components/Sidebar";
import LeafletMap from "../components/LeafletMap";

/** UseState
 * Controla o tipo de visualização do mapa.
 *
 * Valores possíveis:
 * - "markers": exibe cada notícia como um marcador individual.
 * - "heat": exibe um mapa de calor baseado na concentração das ocorrências.
 */

function Mapa() {
  const [viewType, setViewType] = useState("markers");

  return (
    <div className="app">
      <Sidebar />

      <main className="content map-content">
        <div className="map-fullbleed">
          {/* Painel flutuante: título + seletor de visualização */}
          <div className="map-floating-header">
            <div>
              <h2>Mapa</h2>
              <p>Visualização geográfica das notícias</p>
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

          {/* Mapa ocupando 100% da área da aba */}
          <div className="map-fullbleed-container">
            <LeafletMap viewType={viewType} />
          </div>

          {/* Painel flutuante: legenda
          <div className="map-legend map-floating-legend">
            <div className="legend-header">
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
          */}
        </div>
      </main>
    </div>
  );
}

export default Mapa;
