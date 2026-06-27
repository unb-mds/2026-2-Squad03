import { useState, useEffect, useMemo } from "react";
import { MapContainer, TileLayer, Marker, Popup, Polygon } from "react-leaflet";
import { useNavigate } from "react-router-dom";
import L from "leaflet";
import { renderToStaticMarkup } from "react-dom/server";
import { FaMapMarkerAlt } from "react-icons/fa";
import HeatmapLayer from "./HeatmapLayer";
import "leaflet/dist/leaflet.css";

const criarIcone = (cor) => new L.DivIcon({
  html: renderToStaticMarkup(<FaMapMarkerAlt size={36} color={cor} />),
  className: "", iconSize: [36, 36], iconAnchor: [18, 36], popupAnchor: [0, -32]
});

const icons = { feminicidio: criarIcone("#dc2626"), violencia: criarIcone("#ea580c"), outros: criarIcone("#2563eb") };

function LeafletMap({ viewType }) {
  const [geoJsonData, setGeoJsonData] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    fetch("https://two026-2-veritasia.onrender.com/mapa/")
      .then(res => res.json())
      .then(setGeoJsonData).catch(console.error);
  }, []);

  const heatPoints = useMemo(() => {
  if (!geoJsonData || !geoJsonData.features) return [];
  const points = geoJsonData.features
    .filter(f => f.geometry && f.geometry.type === "Point")
    .map(f => [
      f.geometry.coordinates[1], // Latitude
      f.geometry.coordinates[0], // Longitude
      0.8 // Intensidade fixa
    ]);
  
  console.log("Pontos processados para o mapa de calor:", points); 
  return points;
}, [geoJsonData]);

  if (!geoJsonData) return <div>Carregando mapa...</div>;

  return (
    <MapContainer center={[-15.7801, -47.9292]} zoom={4} minZoom={4} maxZoom={12} style={{ height: "600px", width: "100%" }}>
      <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
      
      {viewType === "heat" && (
        <HeatmapLayer 
          key="heatmap-unique-id" 
          points={heatPoints} 
        />
      )}
      
      {viewType === "markers" && geoJsonData.features.map((feature, i) => {
        if (feature.geometry.type === "Point") {
          const { id, titulo, tipo } = feature.properties;
          return (
            <Marker key={id || i} position={[feature.geometry.coordinates[1], feature.geometry.coordinates[0]]} icon={icons[tipo] || icons.outros}>
              <Popup><h4 onClick={() => navigate(`/noticias/${id}`)} style={{cursor: "pointer", color: "#4338ca"}}>{titulo}</h4></Popup>
            </Marker>
          );
        }
        return null;
      })}
    </MapContainer>
  );
}

export default LeafletMap;