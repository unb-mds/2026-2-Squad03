import { useState, useEffect, useMemo } from "react";
import { ComposableMap, Geographies, Geography } from "react-simple-maps";
import { scaleLinear } from "d3-scale";

const geoUrl = "https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson";

function BrazilMap({ data }) {
  const [geoData, setGeoData] = useState(null);

  useEffect(() => {
    fetch(geoUrl)
      .then((res) => res.json())
      .then((json) => setGeoData(json));
  }, []);

  const maxNoticias = useMemo(() => {
    if (!data) return 0;
    return Math.max(...Object.values(data), 1);
  }, [data]);

  const colorScale = scaleLinear()
    .domain([0, maxNoticias])
    .range(["#d1d5db", "#4338ca"]);

  if (!geoData) return <div>Carregando...</div>;

  return (
    <div className="brazil-map-container">
      <ComposableMap projection="geoMercator" projectionConfig={{ scale: 700, center: [-54, -15] }}>
        <Geographies geography={geoData}>
          {({ geographies }) =>
            geographies.map((geo) => {
              const mapNomeParaSigla = {
                "Acre": "AC", "Alagoas": "AL", "Amapá": "AP", "Amazonas": "AM", "Bahia": "BA",
                "Ceará": "CE", "Distrito Federal": "DF", "Espírito Santo": "ES", "Goiás": "GO",
                "Maranhão": "MA", "Mato Grosso": "MT", "Mato Grosso do Sul": "MS", "Minas Gerais": "MG",
                "Pará": "PA", "Paraíba": "PB", "Paraná": "PR", "Pernambuco": "PE", "Piauí": "PI",
                "Rio de Janeiro": "RJ", "Rio Grande do Norte": "RN", "Rio Grande do Sul": "RS",
                "Rondônia": "RO", "Roraima": "RR", "Santa Catarina": "SC", "São Paulo": "SP",
                "Sergipe": "SE", "Tocantins": "TO"
              };
              
              const uf = mapNomeParaSigla[geo.properties.name] || "";
              const value = data ? (data[uf] || 0) : 0;

              return (
                <Geography
                  key={geo.rsmKey}
                  geography={geo}
                  style={{
                    default: { 
                      fill: value === 0 ? "#b7b6b6" : colorScale(value), 
                      stroke: "#ffffff", 
                      strokeWidth: 1 
                    },
                    hover: { 
                      fill: "#1e1b4b", 
                      stroke: "#ffffff",
                      strokeWidth: 1.5,
                      cursor: "pointer" 
                    }
                  }}
                />
              );
            })
          }
        </Geographies>
      </ComposableMap>

      <div className="map-legend-gradient">
        <div className="legend-labels">
          <span>Menos notícias</span>
          <span>Mais notícias</span>
        </div>
        <div className="gradient-bar"></div>
      </div>
    </div>
  );
}

export default BrazilMap;