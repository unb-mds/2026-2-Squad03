
import {
  MapContainer,
  TileLayer,
  Marker,
  Popup,
  Polygon,
  GeoJSON,
} from "react-leaflet";
import "leaflet/dist/leaflet.css";

import L from 'leaflet';
import markerIcon from 'leaflet/dist/images/marker-icon.png';
import markerShadow from 'leaflet/dist/images/marker-shadow.png';

let DefaultIcon = L.icon({
    iconUrl: markerIcon,
    shadowUrl: markerShadow,
    iconSize: [25, 41],
    iconAnchor: [12, 41]
});
L.Marker.prototype.options.icon = DefaultIcon;

export default function LeafletMap({ data }) {
  // data aqui é o seu objeto FeatureCollection vindo da API
  
  return (
    <MapContainer
      center={[-15.7801, -47.9292]} 
      zoom={4}
      style={{ height: "600px", width: "100%" }}
    >
      <TileLayer
        attribution="&copy; OpenStreetMap contributors"
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        maxZoom={13}
        minZoom={4}
        opacity={1}
      />

      {data && (
        <GeoJSON 
          key={JSON.stringify(data)} // O 'key' força a atualização se o dado mudar
          data={data} 
          onEachFeature={(feature, layer) => {
            if (feature.properties) {
              layer.bindPopup(`
                <b>${feature.properties.titulo}</b><br>
                <a href="#/noticias/${feature.properties.id}">Ver detalhes</a>
              `);
            }
          }}
        />
      )}
    </MapContainer>
  );
}