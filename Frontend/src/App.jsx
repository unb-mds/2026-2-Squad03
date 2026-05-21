import "./App.css";
import StatCard from "./components/StatCard";
import Sidebar from "./components/Sidebar";

function App() {
  const stats = [
    {
      title: "Total de Notícias",
      value: "0.000",
      description: "00,00% vs período anterior",
    },
    {
      title: "Média por dia",
      value: "0.000",
      description: "00,00% vs período anterior",
    },
    {
      title: "Comparação",
      value: "00,00%",
      description: "vs Semana anterior",
    },
  ];

  return (
    <div className="app">
      <Sidebar />

      <main className="content">
        <header className="header">
          <div>
            <h2>Dashboard</h2>
            <p>Visão geral do monitoramento de notícias</p>
          </div>

          <div className="header-actions">
            <button className="date-button">01/05/2024 - 31/05/2024</button>
            <span className="bell">🔔</span>

            <div className="user-box">
              <div className="avatar"></div>
              <div>
                <strong>Usuário</strong>
                <p>Analista</p>
              </div>
            </div>
          </div>
        </header>

        <section className="cards">
          {stats.map((stat, index) => (
            <StatCard
              key={index}
              title={stat.title}
              value={stat.value}
              description={stat.description}
            />
          ))}
        </section>
      </main>
    </div>
  );
}

export default App;
