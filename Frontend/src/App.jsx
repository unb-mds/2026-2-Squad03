import "./App.css";
import StatCard from "./components/StatCard";
import Sidebar from "./components/Sidebar";

function App() {
  const stats = [
    {
      title: "Total de notícias",
      value: "1.248",
      description: "↑ 18,6% vs. período anterior",
    },

    {
      title: "Média por dia",
      value: "40,3",
      description: "↑ 12,4% vs. período anterior",
    },

    {
      title: "Estados afetados",
      value: "27",
      description: "— 0% vs. período anterior",
    },

    {
      title: "Classificadas como feminicídio",
      value: "842",
      description: "↑ 15,2% vs. período anterior",
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

          <button>01/05/2024 - 31/05/2024</button>
        </header>

        <section className="filters">
          <input placeholder="Buscar notícias, locais, veículos..." />
          <button>Período</button>
          <button>Estado</button>
          <button>Município</button>
          <button>Veículo</button>
          <button>Classificação</button>
          <button className="dark">Limpar filtros</button>
        </section>

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
