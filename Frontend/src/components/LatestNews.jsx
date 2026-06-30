/**
 * ============================================================================
 * Componente: LatestNews
 * ----------------------------------------------------------------------------
 * Exibe a lista das notícias mais recentes
 * retornadas pelo backend.
 *
 * Funcionalidades:
 * - Formata a data de publicação.
 * - Permite navegar para a página de detalhes.
 *
 * Props:
 * - data: lista de notícias recentes.
 * ============================================================================
 */

//Navigate: Utilizado para navegar até a página de detalhes da notícia.

/** FormatarData
 * Converte a data recebida da API
 * para o formato brasileiro.
 *
 * @param {string} dataString
 * @returns {string}
 */



import { useNavigate } from "react-router-dom";

function LatestNews({ data }) {
  const navigate = useNavigate();

  const formatarData = (dataString) => {
    if (!dataString) return "";
    return new Date(dataString).toLocaleDateString("pt-BR");
  };

  if (!data || data.length === 0) {
    return (
      <div className="latest-news">
        <p>Nenhuma notícia recente.</p>
      </div>
    );
  }

  return (
    <div className="latest-news">
      {data.map((item) => (
        <div
          key={item.id}
          className="news-item clickable-news"
          onClick={() => navigate(`/noticias/${item.id}`)}
        >
          <div>
            <h4>{item.titulo}</h4>

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