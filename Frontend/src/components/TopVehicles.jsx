import { useState, useEffect } from "react";

function TopVehicles() {
  const [info, setInfo] = useState(null); 
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchDashboard() {
      try {
        setLoading(true);
        // Lembre-se de ajustar a URL para a que está em produção (onrender)
        const resposta = await fetch('https://two026-2-veritasia.onrender.com/dashboard');
        if (!resposta.ok) throw new Error('Erro ao buscar dados');
        const dadosDoBack = await resposta.json();
        setInfo(dadosDoBack); 
      } catch (err) {
        console.error("Erro na requisição:", err);
      } finally {
        setLoading(false);
      }
    }
    fetchDashboard();
  }, []); 

  // 1. Tratamento de carregamento e erro
  if (loading) return <div>Carregando portais...</div>;
  if (!info || !info.top_portais) return <div>Nenhum dado disponível.</div>;

  return (
    <div className="vehicle-list">
      {info.top_portais.map((portal, index) => (
        <div key={index} className="vehicle-item">
          <span>{portal.name}</span>
          
          <div className="bar-container">
            {/* 2. Adicionamos a unidade '%' ao valor percentual */}
            <div 
              className="bar" 
              style={{ width: `${portal.percent}%` }} 
            ></div>
          </div>
          
          <strong>{portal.value}</strong>
        </div>
      ))}
    </div>
  );
}

export default TopVehicles;