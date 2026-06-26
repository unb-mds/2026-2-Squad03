import {
  MapContainer,
  TileLayer,
  Marker,
  Popup,
  Polygon,
} from "react-leaflet";
import "leaflet/dist/leaflet.css";

function LeafletMap() {
  const noticias = [
    {
      id: 1,
      titulo: "Operação contra fraude digital em São Paulo",
      resumo: "Investigação apura esquema de disseminação de notícias falsas.",
      link: "#/noticias",
      posicao: [-23.5505, -46.6333],
    },
    {
      id: 2,
      titulo: "Nova campanha de conscientização no Rio",
      resumo: "Projeto busca combater a desinformação em redes sociais.",
      link: "#/noticias",
      posicao: [-22.9068, -43.1729],
    },
    {
      id: 3,
      titulo: "Relatório aponta aumento de fake news",
      resumo: "Levantamento mostra crescimento da desinformação no DF.",
      link: "#/noticias",
      posicao: [-15.7801, -47.9292],
    },
  ];

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
        <Marker key={noticia.id} position={noticia.posicao}>
          <Popup>
            <div>
              <h4>{noticia.titulo}</h4>

              <p>{noticia.resumo}</p>

              <a href={noticia.link}>
                Ver notícia completa
              </a>
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