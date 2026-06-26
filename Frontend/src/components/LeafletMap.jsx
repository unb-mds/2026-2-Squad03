import { useState, useEffect } from "react";
import {
  MapContainer,
  TileLayer,
  Marker,
  Popup,
  Polygon,
} from "react-leaflet";
import { useNavigate } from "react-router-dom"; // 1. Importe o useNavigate
import "leaflet/dist/leaflet.css";
import L from "leaflet";

import icon from 'leaflet/dist/images/marker-icon.png';
import iconShadow from 'leaflet/dist/images/marker-shadow.png';
let DefaultIcon = L.icon({
    iconUrl: icon,
    shadowUrl: iconShadow,
    iconSize: [25, 41],
    iconAnchor: [12, 41]
});
L.Marker.prototype.options.icon = DefaultIcon;

function LeafletMap() {
  const [geoJsonData, setGeoJsonData] = useState(null);
  const navigate = useNavigate(); // 2. Inicialize o navigate

  useEffect(() => {
    async function fetchMapaData() {
      try {
        const resposta = await fetch("https://two026-2-veritasia.onrender.com/mapa/");
        if (!resposta.ok) throw new Error("Erro ao buscar dados do mapa.");
        const dados = await resposta.json();
        setGeoJsonData(dados);
      } catch (err) {
        console.error("Erro ao carregar dados geográficos:", err);
      }
    }
    fetchMapaData();
  }, []);

  if (!geoJsonData) {
    return <div style={{ height: "600px" }}><p>Carregando mapa...</p></div>;
  }

  return (
    <MapContainer
      center={[-15.7801, -47.9292]}
      zoom={4}
      style={{ height: "600px", width: "100%" }}
    >
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />

      {geoJsonData.features.map((feature, index) => {
        const { type, coordinates } = feature.geometry;
        const { id, titulo, resumo, veiculo } = feature.properties;

        // Função interna para navegar ao clicar no título
        const irParaNoticia = () => navigate(`/noticias/${id}`);

        if (type === "Point") {
          const posicao = [coordinates[1], coordinates[0]];
          return (
            <Marker key={id || index} position={posicao}>
              <Popup>
                <div>
                  {/* 3. Título como link clicável */}
                  <h4 
                    onClick={irParaNoticia} 
                    style={{ cursor: "pointer", color: "#4338ca", textDecoration: "underline" }}
                  >
                    {titulo}
                  </h4>
                  <p>{resumo.substring(0, 120).trim() + "..."}</p>
                  <p><em>Portal: {veiculo}</em></p>
                </div>
              </Popup>
            </Marker>
          );
        }

        if (type === "Polygon") {
          const posicoes = coordinates[0].map((coord) => [coord[1], coord[0]]);
          return (
            <Polygon
              key={id || index}
              positions={posicoes}
              pathOptions={{
                color: "#4338ca",
                fillColor: "#6366f1",
                fillOpacity: 0.3,
              }}
            >
              <Popup>
                <div>
                  {/* 3. Título como link clicável */}
                  <strong 
                    onClick={irParaNoticia} 
                    style={{ cursor: "pointer", color: "#4338ca", textDecoration: "underline" }}
                  >
                    {titulo}
                  </strong>
                  <p>{resumo.substring(0, 120).trim() + "..."}</p>
                </div>
              </Popup>
            </Polygon>
          );
        }
        return null;
      })}
    </MapContainer>
  );
}

export default LeafletMap;