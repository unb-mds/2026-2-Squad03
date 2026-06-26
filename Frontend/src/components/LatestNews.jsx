import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

function LatestNews() {
  const [info, setInfo] = useState(null); 
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    async function fetchDashboard() {
      try {
        setLoading(true);
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

  const formatarData = (dataString) => {
    if (!dataString) return "";
    return new Date(dataString).toLocaleDateString('pt-BR');
  };

  if (loading) return <div className="latest-news"><p>Carregando notícias...</p></div>;
  if (!info || !info.latest_news) return null;

  return (
    <div className="latest-news">
      {info.latest_news.map((item) => (
        <div className="news-item" key={item.id}>
          <div>
            {/* O título agora é clicável e dispara a navegação */}
            <h4 
              onClick={() => navigate(`/noticias/${item.id}`)}
              style={{ cursor: "pointer", color: "#4338ca", textDecoration: "underline" }}
            >
              {item.titulo}
            </h4>
            <p>
              {item.Portal} • {item.regiao}
            </p>
          </div>
          <span>{formatarData(item.data_publicacao)}</span>
        </div>
      ))}
    </div>
  );
}

export default LatestNews;