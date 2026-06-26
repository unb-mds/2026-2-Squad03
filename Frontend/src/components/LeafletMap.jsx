import {
  MapContainer,
  TileLayer,
  Marker,
  Popup,
  Polygon,
} from "react-leaflet";
import "leaflet/dist/leaflet.css";
import { noticias } from "../data/noticias";
console.log(noticias);
import { useNavigate } from "react-router-dom";

const coordenadas = {
  SP: [-23.5505, -46.6333],
  RJ: [-22.9068, -43.1729],
  MG: [-19.9167, -43.9345],
  DF: [-15.7801, -47.9292],
  BA: [-12.9714, -38.5014],
  RS: [-30.0346, -51.2177],
  CE: [-3.7319, -38.5267],
};

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
          position={coordenadas[noticia.estado]}>
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