/**
 * ============================================================================
 * Componente: HeatmapLayer
 * ----------------------------------------------------------------------------
 * Responsável por adicionar uma camada de mapa de calor ao Leaflet.
 *
 * Funcionalidades:
 * - Recebe uma lista de coordenadas.
 * - Renderiza uma camada Heatmap.
 * - Remove automaticamente a camada quando o componente é desmontado.
 *
 * Props:
 * - points: lista de coordenadas no formato
 *   [latitude, longitude, intensidade].
 * ============================================================================
 */

/**
 * Obtém a instância do mapa Leaflet fornecida
 * pelo React Leaflet.
 
const map = useMap();*/

/** useEffect
 * Sempre que os pontos ou o mapa forem alterados,
 * a camada de calor é recriada para refletir os
 * novos dados.
 */

// Validação: Evita criar uma camada caso o mapa ainda não
// esteja disponível ou não existam pontos válidos.

/** Filtragem
 * Remove coordenadas inválidas para evitar erros
 * durante a criação da camada Heatmap.
 */

/**heatLayer
 * Configuração visual da camada de calor.
 *
 * Os parâmetros definem o raio de influência,
 * intensidade, opacidade e gradiente de cores.
 */

/** Cleanup
 * Remove a camada do mapa quando o componente
 * é desmontado ou quando os pontos são alterados.
 *
 * Evita sobreposição de múltiplas camadas
 * e vazamento de memória.
 */

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
    radius: 40,      // Aumentar o raio faz os pontos se "fundirem" mais rápido
    blur: 35,        // Aumentar o blur suaviza as manchas
    maxZoom: 20,
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