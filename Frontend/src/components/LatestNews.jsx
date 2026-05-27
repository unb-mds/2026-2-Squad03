function LatestNews() {
  const news = [
    {
      title: "Caso de feminicídio é investigado pela polícia",
      source: "G1",
      state: "SP",
      date: "12/05/2026",
    },
    {
      title: "Mulher vítima de violência doméstica recebe medida protetiva",
      source: "UOL",
      state: "RJ",
      date: "11/05/2026",
    },
    {
      title: "Dados apontam aumento de denúncias no país",
      source: "Folha",
      state: "DF",
      date: "10/05/2026",
    },
  ];

  return (
    <div className="latest-news">
      {news.map((item, index) => (
        <div className="news-item" key={index}>
          <div>
            <h4>{item.title}</h4>
            <p>
              {item.source} • {item.state}
            </p>
          </div>

          <span>{item.date}</span>
        </div>
      ))}
    </div>
  );
}

export default LatestNews;
