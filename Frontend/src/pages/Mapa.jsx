/**
 * ============================================================================
 * Componente: Mapa
 * ----------------------------------------------------------------------------
 * Página responsável pela visualização geográfica das notícias monitoradas
 * pelo sistema VeritasIA.
 *
 * Funcionalidades:
 * - Exibe o mapa interativo da aplicação.
 * - Permite alternar entre visualização por marcadores e mapa de calor.
 * - Apresenta uma legenda com as categorias monitoradas.
 *
 * Componentes utilizados:
 * - Sidebar
 * - PageHeader
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

/* JSX antes do Seletor 
  Seleciona o modo de visualização do mapa. */
/* Antes do mapa:
Componente responsável pela renderização do mapa interativo. */
/* Antes da legenda
  Legenda utilizada para identificar as categorias das notícias. */

function Mapa() {
  const [viewType, setViewType] = useState("markers");

  return (
    <div className="app">
      <Sidebar />

      <main className="content">
        <section className="full-box">
          <header className="header map-header">
            <div>
              <h2>Mapa</h2>
              <p>Visualização geográfica das notícias</p>
            </div>

            <div className="header-actions">
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
          </header>

          <h3 className="map-section-title">
            Distribuição das notícias pelo Brasil
          </h3>

          <div className="map-page-container">
            <LeafletMap viewType={viewType} />
          </div>

          <div className="map-legend">
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
        </section>
      </main>
    </div>
  );
}

export default Mapa;
