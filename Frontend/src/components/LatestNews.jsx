import { useState, useEffect } from "react";


function LatestNews() {
  // Inicialize com null para identificar que os dados ainda não foram carregados
  const [info, setInfo] = useState(null); 

  useEffect(() => {
    async function fetchDashboard() {
      try {
        const resposta = await fetch('http://127.0.0.1:8000/dashboard');
        if (!resposta.ok) throw new Error('Erro ao buscar dados');
        const dadosDoBack = await resposta.json();
        setInfo(dadosDoBack); 
      } catch (err) {
        console.error("Erro na requisição:", err);
      }
    }
    fetchDashboard();
  }, []); 

  // --- AQUI ESTÁ A CORREÇÃO ---
  // Se 'info' for null ou se 'latest_news' ainda não existir, exibe um carregando
  if (!info || !info.latest_news) {
    return <div className="latest-news"><p>Carregando notícias...</p></div>;
  }

  return (
    <div className="latest-news">
      {info.latest_news.map((item, index) => (
        <div className="news-item" key={index}>
          <div>
            <h4>{item.titulo}</h4>
            <p>
              {item.Portal} • {item.regiao}
            </p>
          </div>
          <span>{item.data_publicacao}</span>
        </div>
      ))}
    </div>
  );
}

export default LatestNews;