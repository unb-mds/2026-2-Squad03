import { useEffect } from "react";
import { useMap } from "react-leaflet";
import L from "leaflet";
import "leaflet.heat";

function HeatmapLayer({ points }) {
  const map = useMap();

  useEffect(() => {
    // Validação estrita: se não houver mapa ou pontos, não faz nada
    if (!map || !points || points.length === 0) return;

    // Filtra pontos inválidos (garante que latitude e longitude existam)
    const validPoints = points.filter(p => p[0] != null && p[1] != null);

    const heatLayer = L.heatLayer(validPoints, {
    radius: 50,      // Aumentar o raio faz os pontos se "fundirem" mais rápido
    blur: 35,        // Aumentar o blur suaviza as manchas
    maxZoom: 15,
    max: 0.5,        // Tente baixar de 1.0 para 0.5 ou 0.3 (isso torna o mapa muito mais "quente")
    minOpacity: 0.4, // Força os pontos a terem uma opacidade mínima
    gradient: { 
        0.2: '#ffffb2', 0.4: '#fd8d3c', 
        0.6: '#41ab5d', 0.8: '#084594', 1.0: '#4a1486' 
    }
    }).addTo(map);

    // Garante a remoção da camada ao desmontar ou trocar de modo
    return () => {
      if (map.hasLayer(heatLayer)) {
        map.removeLayer(heatLayer);
      }
    };
  }, [map, points]);

  return null;
}

export default HeatmapLayer;