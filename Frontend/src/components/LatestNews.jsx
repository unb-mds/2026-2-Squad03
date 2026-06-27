import { useNavigate } from "react-router-dom";

function LatestNews({ data }) {
  const navigate = useNavigate();

  // Função utilitária para formatar a data
  const formatarData = (dataString) => {
    if (!dataString) return "";
    return new Date(dataString).toLocaleDateString('pt-BR');
  };

  // Verificação de segurança: se não houver dados, exibe mensagem ou vazio
  if (!data || data.length === 0) {
    return <div className="latest-news"><p>Nenhuma notícia recente.</p></div>;
  }

  return (
    <div className="latest-news">
      {data.map((item) => (
        <div className="news-item" key={item.id}>
          <div>
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
          <div className="news-right">
            <span>{formatarData(item.data_publicacao)}</span>
            <span className="news-arrow">→</span>
          </div>
        </div>
      ))}
    </div>
  );
}

export default LatestNews;