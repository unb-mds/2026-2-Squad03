import "../App.css";
import { useState, useEffect } from "react";
import Sidebar from "../components/Sidebar";
import StatCard from "../components/StatCard";
import NewsChart from "../components/NewsChart";
import TopVehicles from "../components/TopVehicles";
import RegionChart from "../components/RegionChart";
import LatestNews from "../components/LatestNews";
import AuthPrompt from "../components/AuthPrompt";
import BrazilMap from "../components/BrazilMap";

function Dashboard() {
  const [showModal, setShowModal] = useState(() => {
    return localStorage.getItem("veritas-auth-modal") !== "closed";
  });

  // Estado para armazenar os dados vindo do backend
  const [info, setInfo] = useState(null);

  useEffect(() => {
    async function fetchDashboard() {
      try {
        const resposta = await fetch('https://two026-2-veritasia.onrender.com/dashboard/');
        if (!resposta.ok) throw new Error('Erro ao buscar estatísticas');
        const dados = await resposta.json();
        setInfo(dados);
      } catch (err) {
        console.error("Erro no Dashboard:", err);
      }
    }
    fetchDashboard();
  }, []);

  // Dados dos cards consumindo o estado 'info'
  const stats = [
    {
      title: "Total de Notícias",
      value: info?.total_atual?.toLocaleString() || "0",
      description: "Total acumulado na base",
    },
    {
      title: "Média por dia",
      value: info?.media_diaria?.toString() || "0",
      description: "Média da última semana",
    },
    {
      title: "Crescimento",
      value: `${info?.crescimento_percentual || 0}%`,
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
              <span>Últimos 14 dias</span>
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

        {showModal && (
          <AuthPrompt
            onClose={() => {
              localStorage.setItem("veritas-auth-modal", "closed");
              setShowModal(false);
            }}
          />
        )}

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