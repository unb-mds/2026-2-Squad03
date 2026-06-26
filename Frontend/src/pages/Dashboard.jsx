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
  // 1. Inicializa o estado lendo o localStorage. 
  // Se "modalDashboardFechado" existir, showModal começa como false.
  const [showModal, setShowModal] = useState(() => {
    const modalJaFechado = localStorage.getItem("modalDashboardFechado");
    return !modalJaFechado; 
  });
  
  const [info, setInfo] = useState(null);

  useEffect(() => {
      async function fetchDashboard() {
        try {
          const resposta = await fetch('https://two026-2-veritasia.onrender.com/dashboard');
          
          if (!resposta.ok) {
            throw new Error('Não foi possível obter os dados do servidor.');
          }

          const dadosDoBack = await resposta.json();
          setInfo(dadosDoBack); 
        } catch (err) {
          console.error("Erro na requisição:", err);
        } finally {
          console.log("Dados recebidos do servidor");
        }
      }

      fetchDashboard();
    }, []); 

  // 2. Cria a função que fecha o modal e salva a preferência no navegador
  const fecharEGravarModal = () => {
    setShowModal(false);
    localStorage.setItem("modalDashboardFechado", "true");
  };

  const stats = [
    {
      title: "Total de Notícias",
      value: info?.total_atual || 0, 
      description: "Desde o início do monitoramento",
    },
    {
      title: "Média por dia",
      value: info?.media_diaria || 0,
      description: "Hoje",
    },
    {
      title: "Comparação",
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

        {/* 3. Passa a nova função para o componente AuthPrompt */}
        {showModal && <AuthPrompt onClose={fecharEGravarModal} />}

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