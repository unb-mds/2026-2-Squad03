import { useState, useMemo, useEffect } from "react";
import Sidebar from "../components/Sidebar";
import PageHeader from "../components/PageHeader";
import "../App.css";
import "./Noticias.css";
import { useNavigate } from "react-router-dom";

export default function Noticias() {
  const navigate = useNavigate();
  
  // 1. Estados
  const [noticiasAPI, setNoticiasAPI] = useState([]);
  const [loading, setLoading] = useState(true);
  const [busca, setBusca] = useState("");
  const [filtroEstado, setFiltroEstado] = useState("");
  const [filtroVeiculo, setFiltroVeiculo] = useState("");
  const [filtroPeriodo, setFiltroPeriodo] = useState("");
  const [pagina, setPagina] = useState(1);
  
  // 2. Estados do Aviso de Conteúdo Sensível
  const [naoMostrarNovamente, setNaoMostrarNovamente] = useState(false);
  const [mostrarAviso, setMostrarAviso] = useState(() => {
    return localStorage.getItem("veritas-aviso-sensivel") !== "true";
  });

  const POR_PAGINA = 8;

  // 3. Fetch dos dados
  useEffect(() => {
    async function fetchNoticias() {
      try {
        setLoading(true);
        const resposta = await fetch("https://two026-2-veritasia.onrender.com/noticias/");
        if (!resposta.ok) throw new Error("Erro ao buscar notícias");
        
        const dadosDoBack = await resposta.json();

        const noticiasFormatadas = dadosDoBack.map(n => ({
          id: n.id,
          titulo: n.titulo || "Título Indisponível",
          resumo: (n.resumo_blur || "Resumo não disponível").substring(0, 120).trim() + "...",
          fonte: n.Portal || n.portal || n.veiculo || n.fonte || "Desconhecido",
          data: n.data_publicacao ? new Date(n.data_publicacao).toLocaleDateString('pt-BR') : "Data indisponível",
          estado: n.regiao?.nome || "N/A",
          imagem: n.imagem_url || "https://via.placeholder.com/300x150?text=Sem+Imagem",
          categoria: "Geral",
          status: "Analisada",
          conteudoSensivel: false
        }));

        setNoticiasAPI(noticiasFormatadas);
      } catch (err) {
        console.error("Falha ao carregar as notícias:", err);
      } finally {
        setLoading(false);
      }
    }
    fetchNoticias();
  }, []);

  const ESTADOS = useMemo(() => [...new Set(noticiasAPI.map((n) => n.estado))].filter(e => e !== "N/A").sort(), [noticiasAPI]);
  const VEICULOS = useMemo(() => [...new Set(noticiasAPI.map((n) => n.fonte))].filter(f => f !== "Desconhecido").sort(), [noticiasAPI]);

  const noticiasFiltradas = useMemo(() => {
    return noticiasAPI.filter((n) => {
      const buscaOk = !busca || n.titulo.toLowerCase().includes(busca.toLowerCase()) || n.fonte.toLowerCase().includes(busca.toLowerCase());
      const estadoOk = !filtroEstado || n.estado === filtroEstado;
      const veiculoOk = !filtroVeiculo || n.fonte === filtroVeiculo;
      return buscaOk && estadoOk && veiculoOk;
    });
  }, [busca, filtroEstado, filtroVeiculo, noticiasAPI]);

  const totalPaginas = Math.ceil(noticiasFiltradas.length / POR_PAGINA);
  const noticiasPagina = noticiasFiltradas.slice((pagina - 1) * POR_PAGINA, pagina * POR_PAGINA);

  return (
    <div className="app">
      <Sidebar />
      <main className="content">
        
        <PageHeader 
          title="Notícias" 
          subtitle="Monitoramento de notícias sobre feminicídio no Brasil"
        >
          <button className="date-button">📅 <span>01/05/2024 - 31/05/2024</span></button>
          <span className="bell">🔔</span>
          <div className="user-box"><div className="avatar"></div><div><strong>Usuário</strong><p>Analista</p></div></div>
        </PageHeader>

        {mostrarAviso && (
          <div className="overlay-aviso">
            <div className="modal-aviso">
              <div className="icone-aviso">⚠️</div>
              <h2>Aviso de conteúdo sensível</h2>
              <p>
                Esta seção apresenta dados e informações detalhadas sobre casos de 
                <strong> feminicídio e violência doméstica</strong>.
              </p>

              <label style={{ display: "center", alignItems: "center", gap: "8px", marginBottom: "20px", cursor: "pointer" }}>
                <input 
                  type="checkbox" 
                  checked={naoMostrarNovamente}
                  onChange={(e) => setNaoMostrarNovamente(e.target.checked)}
                />
                <span> Não mostrar este aviso novamente.</span>
              </label>

              <div className="botoes-aviso">
                <button 
                  className="btn-continuar" 
                  onClick={() => {
                    if (naoMostrarNovamente) {
                      localStorage.setItem("veritas-aviso-sensivel", "true");
                    }
                    setMostrarAviso(false);
                  }}
                >
                  Continuar para a página
                </button>
                <button className="btn-voltar" onClick={() => navigate("/dashboard")}>
                  Voltar
                </button>
              </div>
            </div>
          </div>
        )}

        <div className="noticias-container">
          <div className="noticias-toolbar">
            <div className="noticias-search-wrap">
              <span className="search-icon">🔍</span>
              <input className="noticias-search" placeholder="Buscar..." value={busca} onChange={(e) => { setBusca(e.target.value); setPagina(1); }} />
            </div>

            <div className="noticias-filters">
              <select className="filter-select" value={filtroEstado} onChange={(e) => { setFiltroEstado(e.target.value); setPagina(1); }}>
                <option value="">Estado ▾</option>
                {ESTADOS.map(uf => <option key={uf} value={uf}>{uf}</option>)}
              </select>
              <select className="filter-select" value={filtroVeiculo} onChange={(e) => { setFiltroVeiculo(e.target.value); setPagina(1); }}>
                <option value="">Veículo ▾</option>
                {VEICULOS.map(v => <option key={v} value={v}>{v}</option>)}
              </select>
            </div>
          </div>

          <div className="news-grid">
            {loading ? <div className="noticias-empty-card">Carregando notícias...</div> : 
             noticiasPagina.length === 0 ? <div className="noticias-empty-card">Nenhuma notícia encontrada.</div> :
             noticiasPagina.map((n) => (
              <article key={n.id} className="news-card" onClick={() => navigate(`/noticias/${n.id}`)}>
                <h3><img src={n.imagem} alt={n.titulo} className="news-image" /></h3>
                <p className="news-summary">{n.resumo}</p>
                <div className="news-meta"><span>📰 {n.fonte}</span> <span>📅 {n.data}</span></div>
                <div className="news-meta"><span>📍 {n.estado}</span></div>
                <button className="ler-btn">Ler notícia →</button>
              </article>
            ))}
          </div>

          {!loading && totalPaginas > 1 && (
            <div className="noticias-pagination">
              <button onClick={() => setPagina(p => Math.max(1, p - 1))} disabled={pagina === 1}>‹</button>
              <span>{pagina} de {totalPaginas}</span>
              <button onClick={() => setPagina(p => Math.min(totalPaginas, p + 1))} disabled={pagina === totalPaginas}>›</button>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}