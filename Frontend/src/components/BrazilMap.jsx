import { ComposableMap, Geographies, Geography } from "react-simple-maps";

const geoUrl =
  "https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson";

const stateData = {
  SP: 320,
  RJ: 210,
  MG: 180,
  BA: 160,
  DF: 90,
  RS: 140,
};

function getColor(value) {
  if (value > 250) return "#312e81";
  if (value > 180) return "#4338ca";
  if (value > 120) return "#6366f1";
  if (value > 80) return "#8b5cf6";

  return "#c4b5fd";
}

function BrazilMap() {
  return (
    <div className="brazil-map">
      <ComposableMap
        projection="geoMercator"
        projectionConfig={{
          scale: 650,
          center: [-54, -15],
        }}
      >
        <Geographies geography={geoUrl}>
          {({ geographies }) =>
            geographies.map((geo) => {
              const uf = geo.properties.sigla;

              const value = stateData[uf] || 20;

              return (
                <Geography
                  key={geo.rsmKey}
                  geography={geo}
                  title={`${uf}: ${value} notícias`}
                  style={{
                    default: {
                      fill: getColor(value),
                      stroke: "#ffffff",
                      outline: "none",
                    },
                    hover: {
                      fill: "#111827",
                      stroke: "#ffffff",
                      outline: "none",
                    },
                    pressed: {
                      fill: "#1e1b4b",
                      stroke: "#ffffff",
                      outline: "none",
                    },
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
