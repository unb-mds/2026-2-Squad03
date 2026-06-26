import { useNavigate } from "react-router-dom";
import { noticias } from "../data/noticias";

function LatestNews() {
  const navigate = useNavigate();

  return (
    <div className="latest-news">
      {noticias.slice(0, 5).map((item) => (
        <div
          className="news-item clickable-news"
          key={item.id}
          onClick={() => navigate(`/noticias/${item.id}`)}
        >
          <div>
            <h4>{item.titulo}</h4>

            <p>
              {item.fonte} • {item.estado}
            </p>
          </div>

          <div className="news-right">
            <span>{item.data}</span>

            <span className="news-arrow">→</span>
          </div>
        </div>
      ))}
    </div>
  );
}

export default LatestNews;