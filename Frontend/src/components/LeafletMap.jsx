/**
 * ============================================================================
 * Componente: LeafletMap
 * ----------------------------------------------------------------------------
 * Responsável pela renderização do mapa interativo utilizando React Leaflet.
 *
 * Funcionalidades:
 * - Busca os dados geográficos da API.
 * - Renderiza marcadores personalizados.
 * - Exibe mapa de calor.
 * - Permite navegar para a página de detalhes da notícia.
 *
 * Dependências:
 * - React Leaflet
 * - Leaflet
 * - React Router
 * ============================================================================
 */

/**
 * Cria um ícone personalizado para os marcadores do mapa.
 *
 * Utiliza um ícone React convertido em HTML através do
 * renderToStaticMarkup para integração com o Leaflet.
 *
 * @param {string} cor Cor utilizada no marcador.
 * @returns {L.DivIcon} Ícone personalizado do Leaflet.
 */

/**const icons = {
 *
 * Conjunto de ícones utilizados para representar
 * visualmente cada categoria de notícia.
 */

/** const [geoJsonData, setGeoJsonData] = useState(null);
 * Armazena os dados geográficos retornados pela API
 * no formato GeoJSON.
 */

// const navigate = useNavigate();
// Responsável pela navegação para a página de detalhes da notícia.

/**useEffect(() => {
 * Executado apenas durante a montagem do componente.
 *
 * Realiza a requisição dos dados geográficos utilizados
 * pelo mapa e armazena o resultado no estado geoJsonData.
 *
 * O array de dependências vazio garante apenas
 * uma chamada à API durante a inicialização.
 */

  /** const heatPoints = useMemo(() => {
 * Gera os pontos utilizados pelo mapa de calor.
 *
 * useMemo é utilizado para evitar que essa transformação
 * seja recalculada a cada renderização do componente.
 *
 * O cálculo será executado apenas quando geoJsonData
 * sofrer alguma alteração.
 */
// LOADING
// Enquanto os dados ainda não foram carregados,
// exibe uma mensagem de carregamento.

/*MAP CONTAINER
 Configuração principal do mapa Leaflet. */

/* TileLayer
 Camada base utilizando mapas do OpenStreetMap.*/

/*Heatmap
Exibe o mapa de calor quando selecionado pelo usuário. */

/*Marker
 Renderiza um marcador para cada notícia georreferenciada. */

/*Popup
 Informações resumidas da notícia selecionada. */

 import { useState, useEffect, useMemo } from "react";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import { useNavigate } from "react-router-dom";
import L from "leaflet";
import { renderToStaticMarkup } from "react-dom/server";
import { FaMapMarkerAlt } from "react-icons/fa";
import HeatmapLayer from "./HeatmapLayer";
import "leaflet/dist/leaflet.css";

function criarIcone(cor) {
  return new L.DivIcon({
    html: renderToStaticMarkup(
      <FaMapMarkerAlt
        size={36}
        color={cor}
        style={{
          filter: "drop-shadow(0px 4px 8px rgba(0,0,0,.35))",
        }}
      />
    ),
    className: "",
    iconSize: [34, 34],
    iconAnchor: [17, 34],
    popupAnchor: [0, -30],
  });
}

const icons = {
  feminicidio: criarIcone("#dc2626"),
  violencia: criarIcone("#ea580c"),
  outros: criarIcone("#2563eb"),
};

function LeafletMap({ viewType }) {
  const [geoJsonData, setGeoJsonData] = useState(null);

  const navigate = useNavigate();

  useEffect(() => {
    fetch("https://two026-2-veritasia.onrender.com/mapa/")
      .then((res) => res.json())
      .then(setGeoJsonData)
      .catch(console.error);
  }, []);

  const heatPoints = useMemo(() => {
    if (!geoJsonData?.features) return [];

    return geoJsonData.features
      .filter((feature) => feature.geometry?.type === "Point")
      .map((feature) => [
        feature.geometry.coordinates[1],
        feature.geometry.coordinates[0],
        0.8,
      ]);
  }, [geoJsonData]);

  if (!geoJsonData) {
    return <div>Carregando mapa...</div>;
  }

  return (
    <MapContainer
      center={[-15.7801, -47.9292]}
      zoom={4}
      minZoom={4}
      maxZoom={12}
      style={{ height: "600px", width: "100%" }}
    >
      <TileLayer
        attribution="&copy; OpenStreetMap contributors"
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />

      {viewType === "heat" && (
        <HeatmapLayer
          key="heatmap"
          points={heatPoints}
        />
      )}

      {viewType === "markers" &&
        geoJsonData.features.map((feature, index) => {
          if (feature.geometry?.type !== "Point") return null;

          const { id, titulo, tipo } = feature.properties;

          return (
            <Marker
              key={id || index}
              position={[
                feature.geometry.coordinates[1],
                feature.geometry.coordinates[0],
              ]}
              icon={icons[tipo] || icons.outros}
            >
              <Popup>
                <div className="popup-card">
                  <img
                    src="https://placehold.co/320x180?text=Notícia"
                    alt={titulo}
                    className="popup-image"
                  />

                  <h4>{titulo}</h4>

                  <button
                    className="popup-btn"
                    onClick={() => navigate(`/noticias/${id}`)}
                  >
                    Ler notícia →
                  </button>
                </div>
              </Popup>
            </Marker>
          );
        })}
    </MapContainer>
  );
}

export default LeafletMap;