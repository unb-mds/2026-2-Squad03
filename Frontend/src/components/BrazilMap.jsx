import { useState, useEffect } from "react";
import { ComposableMap, Geographies, Geography } from "react-simple-maps";

const geoUrl = "https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson";

function BrazilMap({ data }) {
  const [geoData, setGeoData] = useState(null);

  useEffect(() => {
    fetch(geoUrl)
      .then((res) => res.json())
      .then((json) => setGeoData(json))
      .catch((err) => console.error("Erro no GeoJSON:", err));
  }, []);

  if (!geoData) return <div>Carregando mapa...</div>;

  return (
    <div className="brazil-map">
      <ComposableMap 
        projection="geoMercator" 
        projectionConfig={{ scale: 700, center: [-54, -15] }}
      >
        <Geographies geography={geoData}>
          {({ geographies }) =>
            geographies
              // FILTRO DE SEGURANÇA: Remove qualquer item malformado antes do map
              .filter(geo => geo && geo.geometry && geo.properties)
              .map((geo) => {
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
                        fill: value > 0 ? "#6366f1" : "#e5e7eb", 
                        stroke: "#FFFFFF", 
                        strokeWidth: 0.5 
                      },
                      hover: { fill: "#4338ca", cursor: "pointer" }
                    }}
                  />
                );
              })
          }
        </Geographies>
      </ComposableMap>
    </div>
  );
}

export default BrazilMap;