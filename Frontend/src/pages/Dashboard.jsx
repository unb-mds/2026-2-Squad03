/**
 ============================================================================
Componente: Dashboard
 
Página principal do sistema VeritasIA.

Responsabilidades:
- Buscar os dados estatísticos da API.
- Exibir indicadores gerais do monitoramento.
- Renderizar gráficos, mapa e notícias recentes.
- Exibir modal de autenticação na primeira visita.

Componentes utilizados:
- Sidebar
- PageHeader
- StatCard
- NewsChart
- BrazilMap
- RegionChart
- TopVehicles
- LatestNews
- AuthPrompt
 ============================================================================
 */

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
  /**
 * Controla a exibição do modal de autenticação.
 *
 * O estado inicial é obtido do localStorage para evitar
 * que o modal seja exibido novamente após o usuário fechá-lo.
 */

const [showModal, setShowModal] = useState(() => {
    return localStorage.getItem("veritas-auth-modal") !== "closed";
  });

/**
 * const [info, setInfo] = useState(null);
 * 
 * Armazena todas as informações retornadas pela API
 * necessárias para renderização do Dashboard.
*/

/**
 * const [loading, setLoading] = useState(true);
 * 
 * Indica se os dados ainda estão sendo carregados.
 * Enquanto verdadeiro, é exibida uma tela de carregamento.
 */

  const [info, setInfo] = useState(null);
  const [loading, setLoading] = useState(true);

  /**
   * useEffect(() => {
 * Executado apenas uma vez durante a montagem do componente.
 *
 * Responsável por realizar a chamada à API do Dashboard,
 * armazenar os dados recebidos e controlar o estado de carregamento.
 * O array de dependências vazio garante que a requisição
 * seja realizada apenas na inicialização da página.
 */

  /**
   * async function fetchDashboard() {
   * 
 * Realiza a requisição das informações estatísticas
 * utilizadas pelo Dashboard.
 * Em caso de sucesso:
 * - Atualiza o estado "info".
 * Em caso de erro:
 * - Registra o erro no console.
 * Independentemente do resultado,
 * o estado de carregamento é finalizado.
 */
async function fetchDashboard() {
  useEffect(() => {
  
    async function fetchDashboard() {
      try {
        setLoading(true);

        const resposta = await fetch(
          "https://two026-2-veritasia.onrender.com/dashboard/"
        );

        if (!resposta.ok)
          throw new Error("Erro ao buscar estatísticas");

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
      <div
        className="app"
        style={{
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          height: "100vh",
        }}
      >
        <p>Carregando Dashboard...</p>
      </div>
    );
  }

  if (!info) {
    return (
      <div className="latest-news">
        <p>Dados não disponíveis.</p>
      </div>
    );
  }

/**
 * Estrutura utilizada para alimentar os componentes StatCard.
 * Cada objeto representa um indicador exibido na parte
 * superior do Dashboard.
 */
{/* Modal:
  Modal apresentado apenas na primeira visita do usuário. */}

{/* Cards
   Indicadores principais do Dashboard */}  

{/* Grafico 
  Evolução temporal das notícias monitoradas */}

{/* Mapa
   Distribuição das notícias por estado brasileiro */} 

{/* Região 
  Distribuição por regiões do país */}

{/* Ultimas noticias
   Lista das notícias mais recentes disponibilizadas pela API */}
   
  const stats = [
    {
      title: "Total de Notícias",
      value:
        info?.estatisticas?.[0]?.total_atual?.toLocaleString() || "0",
      description: "Total acumulado na base",
      icon: <FaNewspaper />,
    },
    {
      title: "Média por dia",
      value:
        info?.estatisticas?.[0]?.media_diaria?.toString() || "0",
      description: "Média da última semana",
      icon: <FaCalendarAlt />,
    },
    {
      title: "Crescimento",
      value: `${
        info?.estatisticas?.[0]?.crescimento_percentual || 0
      }%`,
      description: "vs Semana anterior",
      icon: <FaChartLine />,
    },
  ];

  return (
    <div className="app">
      <Sidebar />

      <main className="content">
        <PageHeader
          title="Dashboard"
          subtitle="Visão geral do monitoramento de notícias"
        >
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
        </PageHeader>

        {showModal && (
          <AuthPrompt
            onClose={() => {
              localStorage.setItem(
                "veritas-auth-modal",
                "closed"
              );
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
}
export default Dashboard;