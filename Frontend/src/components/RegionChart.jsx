import { useState, useEffect } from "react";

function RegionChart() {
  const [regions, setRegions] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchRegions() {
      try {
        const response = await fetch('https://two026-2-veritasia.onrender.com/dashboard/');
        const data = await response.json();
        // Acessamos a chave 'top_regioes' que configuramos no backend
        setRegions(data.top_regioes || []);
      } catch (err) {
        console.error("Erro ao buscar dados de regiões:", err);
      } finally {
        setLoading(false);
      }
    }
    fetchRegions();
  }, []);

  if (loading) return <div className="region-list"><p>Carregando regiões...</p></div>;

  return (
    <div className="region-list">
      {regions.map((region, index) => (
        <div key={index} className="region-item">
          <div className="region-info">
            <span>{region.name}</span>
            <strong>{region.value}</strong>
          </div>
          <div className="bar">
            {/* O estilo width usa diretamente a string percent vinda do backend (ex: "45%") */}
            <div className="bar-fill" style={{ width: region.percent }}></div>
          </div>
        </div>
      ))}
    </div>
  );
}

export default RegionChart;