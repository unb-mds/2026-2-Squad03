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
import PageHeader from "../components/PageHeader";
import { FaNewspaper, FaCalendarAlt, FaChartLine } from "react-icons/fa";

function Dashboard() {
  const [showModal, setShowModal] = useState(() => {
    return localStorage.getItem("veritas-auth-modal") !== "closed";
  });

  const [info, setInfo] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchDashboard() {
      try {
        setLoading(true);
        const resposta = await fetch('https://two026-2-veritasia.onrender.com/dashboard/');
        if (!resposta.ok) throw new Error('Erro ao buscar estatísticas');
        const dados = await resposta.json();
        setInfo(dados);
      } catch (err) {
        console.error("Erro no Dashboard:", err);
      } finally {
        setLoading(false);
      }
    }
    fetchDashboard();
  }, []);

  if (loading) {
    return (
      <div className="app" style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
        <p>Carregando Dashboard...</p>
      </div>
    );
  }

  if (!info) {
    return <div className="latest-news"><p>Dados não disponíveis.</p></div>;
  }

  // Estatísticas preenchidas com dados da API e ícones importados
  const stats = [
    {
      title: "Total de Notícias",
      value: info?.estatisticas?.[0]?.total_atual?.toLocaleString() || "0",
      description: "Total acumulado na base",
      icon: <FaNewspaper />,
    },
    {
      title: "Média por dia",
      value: info?.estatisticas?.[0]?.media_diaria?.toString() || "0",
      description: "Média da última semana",
      icon: <FaCalendarAlt />,
    },
    {
      title: "Crescimento",
      value: `${info?.estatisticas?.[0]?.crescimento_percentual || 0}%`,
      description: "vs Semana anterior",
      icon: <FaChartLine />,
    },
  ];

  return (
    <div className="app">
      <Sidebar />

      <main className="content">
        {/* Cabeçalho centralizado via PageHeader */}
        <PageHeader title="Dashboard" subtitle="Visão geral do monitoramento de notícias">
          <button className="date-button">
            <span>📅</span> <span>Últimos 14 dias</span>
          </button>
          <span className="bell">🔔</span>
          <div className="user-box">
            <div className="avatar"></div>
            <div>
              <strong>Usuário</strong>
              <p>Analista</p>
            </div>
          </div>
        </PageHeader>

        {showModal && (
          <AuthPrompt onClose={() => {
            localStorage.setItem("veritas-auth-modal", "closed");
            setShowModal(false);
          }} />
        )}

        <section className="cards">
          {stats.map((stat, index) => (
            <StatCard
              key={index}
              title={stat.title}
              value={stat.value}
              description={stat.description}
              icon={stat.icon}
            />
          ))}
        </section>

        <section className="dashboard-grid">
          <div className="chart-box">
            <h3>Evolução temporal das publicações</h3>
            <NewsChart data={info.noticias_semana} />
          </div>

          <div className="map-box">
            <h3>Distribuição por estado</h3>
            <BrazilMap data={info.noticias_por_estado} />
          </div>
        </section>

        <section className="dashboard-grid bottom-grid">
          <div className="chart-box">
            <h3>Top Veículos</h3>
            <TopVehicles data={info.top_portais} />
          </div>

          <div className="map-box">
            <h3>Notícias por região</h3>
            <div className="fake-map">
              <RegionChart data={info.top_regioes} />
            </div>
          </div>
        </section>

        <section className="full-box">
          <h3>Últimas Notícias</h3>
          <LatestNews data={info.latest_news} />
        </section>
      </main>
    </div>
  );
}

export default Dashboard;