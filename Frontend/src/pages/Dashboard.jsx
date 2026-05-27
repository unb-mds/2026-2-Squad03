import "../App.css";
import { useState } from "react";
import Sidebar from "../components/Sidebar";
import StatCard from "../components/StatCard";
import NewsChart from "../components/NewsChart";
import TopVehicles from "../components/TopVehicles";
import RegionChart from "../components/RegionChart";
import LatestNews from "../components/LatestNews";
import AuthPrompt from "../components/AuthPrompt";
import BrazilMap from "../components/BrazilMap";

function Dashboard() {
  const [showModal, setShowModal] = useState(true);

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
            <button className="date-button">
              <span>📅</span>
              <span>01/05/2024 - 31/05/2024</span>
            </button>
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

        {showModal && <AuthPrompt onClose={() => setShowModal(false)} />}

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
        <section className="dashboard-grid">
          <div className="chart-box">
            <h3>Evolução temporal das publicações</h3>

            <NewsChart />
          </div>

          <div className="map-box">
            <h3>Distribuição por estado</h3>

            <BrazilMap />
          </div>
        </section>
        <section className="dashboard-grid bottom-grid">
          <div className="chart-box">
            <h3>Top Veículos</h3>

            <TopVehicles />
          </div>

          <div className="map-box">
            <h3>Notícias por região</h3>

            <div className="fake-map">
              <RegionChart />
            </div>
          </div>
        </section>
        <section className="full-box">
          <h3>Últimas Notícias</h3>
          <LatestNews />
        </section>
      </main>
    </div>
  );
}

export default Dashboard;
