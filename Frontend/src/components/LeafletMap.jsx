import {
  MapContainer,
  TileLayer,
  Marker,
  Popup,
  Polygon,
} from "react-leaflet";

import "leaflet/dist/leaflet.css";

import { noticias } from "../data/noticias";

import { useNavigate } from "react-router-dom";

import L from "leaflet";

import { renderToStaticMarkup } from "react-dom/server";

import { FaMapMarkerAlt } from "react-icons/fa";

const coordenadas = {
  SP: [-23.5505, -46.6333],
  RJ: [-22.9068, -43.1729],
  MG: [-19.9167, -43.9345],
  DF: [-15.7801, -47.9292],
  BA: [-12.9714, -38.5014],
  RS: [-30.0346, -51.2177],
  CE: [-3.7319, -38.5267],
};

function criarIcone(cor) {
  return new L.DivIcon({
    html: renderToStaticMarkup(
      <FaMapMarkerAlt
        size={36}
        color={cor}
        style={{
          filter:"drop-shadow(0px 4px 8px rgba(0, 0, 0, 0.35))",
        }}
      />
    ),
    className: "",
    iconSize: [34, 34],
    iconAnchor: [17, 34],
    popupAnchor: [0, -30],
  });
}

const markerRed = criarIcone("#dc2626");

const markerOrange = criarIcone("#ea580c");

const markerBlue = criarIcone("#2563eb");

function getMarker(tipo) {

  switch(tipo){

    case "feminicidio":
      return markerRed;

    case "violencia":
      return markerOrange;

    default:
      return markerBlue;

  }

}

function LeafletMap() {
  const navigate = useNavigate();
  
  const regioesMonitoradas = [
    {
      nome: "Distrito Federal",
      coordenadas: [
        [-15.5, -48.2],
        [-15.5, -47.6],
        [-16.0, -47.6],
        [-16.0, -48.2],
      ],
    },
  ];

  return (
    <MapContainer
      center={[-15.7801, -47.9292]}
      zoom={4}
      style={{ height: "600px", width: "100%" }}
    >
      
      <TileLayer
        attribution="&copy; OpenStreetMap contributors"
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />

      {noticias.map((noticia) => (
        <Marker 
          key={noticia.id}
          position={coordenadas[noticia.estado]}
          icon={getMarker(noticia.tipo)}>
        <Popup>
          <div className="popup-card">

            <img
              src="https://placehold.co/320x180?text=Notícia"
              alt={noticia.titulo}
              className="popup-image"
            />

          <h4>{noticia.titulo}</h4>

          <button
            className="popup-btn"
            onClick={() => navigate(`/noticias/${noticia.id}`)}
          >
            Ler notícia →
          </button>

          </div>
        </Popup>
        </Marker>
      ))}

      {regioesMonitoradas.map((regiao, index) => (
        <Polygon
          key={index}
          positions={regiao.coordenadas}
          pathOptions={{
            color: "#4338ca",
            fillColor: "#6366f1",
            fillOpacity: 0.3,
          }}
        >
          <Popup>
            <div>
              <strong>{regiao.nome}</strong>
              <p>Região monitorada pelo sistema.</p>
            </div>
          </Popup>
        </Polygon>
      ))}
    </MapContainer>
  );
}

export default LeafletMap;