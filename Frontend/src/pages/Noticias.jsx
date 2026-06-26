import { useState, useMemo, useEffect } from "react";
import Sidebar from "../components/Sidebar";
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
  const POR_PAGINA = 8;

  // 2. Fetch dos dados
  useEffect(() => {
    async function fetchNoticias() {
      try {
        setLoading(true);
        // Busca usando a sua rota (com limite de 100 para permitir testes de filtros front-end)
        const resposta = await fetch("https://two026-2-veritasia.onrender.com/noticias/");
        if (!resposta.ok) throw new Error("Erro ao buscar notícias");
        
        const dadosDoBack = await resposta.json();

        // 3. Tradução e Limitação de Tamanho (AQUI ESTÁ A MÁGICA)
        const TAMANHO_MAXIMO_RESUMO = 120; // Defina aqui quantos caracteres você quer no máximo

        const noticiasFormatadas = dadosDoBack.map(n => {
          // Formata a data (se existir) para um formato mais legível
          let dataFormatada = "Data não informada";
          if (n.data_publicacao) {
             const dataObj = new Date(n.data_publicacao);
             dataFormatada = dataObj.toLocaleDateString('pt-BR');
          }

          // LÓGICA PARA LIMITAR O RESUMO
          const resumoRaw = n.resumo_raw || "Resumo não disponível";
          let resumoLimitado = resumoRaw;
          
          if (resumoRaw.length > TAMANHO_MAXIMO_RESUMO) {
            // Corta o texto no tamanho máximo e adiciona '...'
            resumoLimitado = resumoRaw.substring(0, TAMANHO_MAXIMO_RESUMO).trim() + "...";
          }

          return {
            id: n.id,
            titulo: n.titulo || "Título Indisponível",
            resumo: resumoLimitado, // Usa o resumo que acabamos de limitar
            
            // Tratamento do Portal à prova de falhas
            fonte: n.Portal || n.portal || n.veiculo || n.fonte || "Desconhecido",
            
            data: dataFormatada, 
            estado: n.regiao ? String(n.regiao.nome) : "N/A", // Correção: Puxa o nome de dentro do objeto aninhado
            cidade: "N/A",
            imagem: n.imagem_url || "https://via.placeholder.com/300x150?text=Sem+Imagem",
            categoria: "Geral",
            status: "Analisada",
            conteudoSensivel: false
          };
        });

        setNoticiasAPI(noticiasFormatadas);
      } catch (err) {
        console.error("Falha ao carregar as notícias:", err);
      } finally {
        setLoading(false);
      }
    }
    fetchNoticias();
  }, []);

  // 4. Listas dinâmicas para os Dropdowns
  const ESTADOS = useMemo(() => [...new Set(noticiasAPI.map((n) => n.estado))].filter(e => e !== "N/A").sort(), [noticiasAPI]);
  const VEICULOS = useMemo(() => [...new Set(noticiasAPI.map((n) => n.fonte))].filter(f => f !== "Desconhecido").sort(), [noticiasAPI]);

  function limparFiltros() {
    setBusca("");
    setFiltroEstado("");
    setFiltroVeiculo("");
    setFiltroPeriodo("");
    setPagina(1);
  }

  // 5. Filtro
  const noticiasFiltradas = useMemo(() => {
    return noticiasAPI.filter((n) => {
      const buscaOk =
        !busca ||
        n.titulo.toLowerCase().includes(busca.toLowerCase()) ||
        n.fonte.toLowerCase().includes(busca.toLowerCase());
      const estadoOk = !filtroEstado || n.estado === filtroEstado;
      const veiculoOk = !filtroVeiculo || n.fonte === filtroVeiculo;
      return buscaOk && estadoOk && veiculoOk;
    });
  }, [busca, filtroEstado, filtroVeiculo, noticiasAPI]);

  const totalPaginas = Math.ceil(noticiasFiltradas.length / POR_PAGINA);
  const noticiasPagina = noticiasFiltradas.slice(
    (pagina - 1) * POR_PAGINA,
    pagina * POR_PAGINA,
  );

  const temFiltro = busca || filtroEstado || filtroVeiculo || filtroPeriodo;

  return (
    <div className="app">
      <Sidebar />
      <main className="content">
        <header className="header">
          <div>
            <h2>Notícias</h2>
            <p>Monitoramento de notícias sobre feminicídio no Brasil</p>
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

        <div className="noticias-container">
          {/* Barra de busca e filtros */}
          <div className="noticias-toolbar">
            <div className="noticias-search-wrap">
              <span className="search-icon">🔍</span>
              <input
                className="noticias-search"
                type="text"
                placeholder="Buscar notícias, locais, veículos..."
                value={busca}
                onChange={(e) => {
                  setBusca(e.target.value);
                  setPagina(1);
                }}
              />
            </div>

            <div className="noticias-filters">
              <select
                className="filter-select"
                value={filtroPeriodo}
                onChange={(e) => {
                  setFiltroPeriodo(e.target.value);
                  setPagina(1);
                }}
              >
                <option value="">Período ▾</option>
                <option value="hoje">Hoje</option>
                <option value="semana">Esta semana</option>
                <option value="mes">Este mês</option>
              </select>

              <select
                className="filter-select"
                value={filtroEstado}
                onChange={(e) => {
                  setFiltroEstado(e.target.value);
                  setPagina(1);
                }}
              >
                <option value="">Estado ▾</option>
                {ESTADOS.map((uf) => (
                  <option key={uf} value={uf}>
                    {uf}
                  </option>
                ))}
              </select>

              <select
                className="filter-select"
                value={filtroVeiculo}
                onChange={(e) => {
                  setFiltroVeiculo(e.target.value);
                  setPagina(1);
                }}
              >
                <option value="">Veículo ▾</option>
                {VEICULOS.map((v) => (
                  <option key={v} value={v}>
                    {v}
                  </option>
                ))}
              </select>

              {temFiltro && (
                <button className="btn-limpar" onClick={limparFiltros}>
                  Limpar Filtros
                </button>
              )}
            </div>
          </div>

          {/* Tabela de Notícias */}
          <div className="news-grid">
            {loading ? (
              <div className="noticias-empty-card">Carregando notícias do banco de dados...</div>
            ) : noticiasPagina.length === 0 ? (
              <div className="noticias-empty-card">Nenhuma notícia encontrada.</div>
            ) : (
              noticiasPagina.map((n) => (
                <article
                  key={n.id}
                  className="news-card"
                  onClick={() => navigate(`/noticias/${n.id}`)}
                >
                  {n.conteudoSensivel && (
                    <div className="news-warning">⚠ Conteúdo Sensível</div>
                  )}
                  <h3>
                    <img
                      src={n.imagem}
                      alt={n.titulo}
                      className="news-image"
                    />
                  </h3>
                  <p className="news-summary">{n.resumo}</p>
                  
                  {/* Usa as variáveis já mapeadas no Passo 3 */}
                  <div className="news-meta">
                    <span>📰 {n.fonte}</span>
                    <span>📅 {n.data}</span>
                  </div>
                  <div className="news-meta">
                    <span>📍 {n.estado}</span>
                  </div>

                  <div className="news-tags">
                    <span className="categoria-badge">{n.categoria}</span>
                    <span
                      className={`status-badge ${n.status
                        .toLowerCase()
                        .normalize("NFD")
                        .replace(/[\u0300-\u036f]/g, "")
                        .replace(/\s+/g, "-")}`}
                    >
                      {n.status}
                    </span>
                  </div>
                  <button className="ler-btn">Ler notícia →</button>
                </article>
              ))
            )}
          </div>

          {/* Paginação */}
          {!loading && totalPaginas > 1 && (
            <div className="noticias-pagination">
              <span className="pagination-info">
                Mostrando {(pagina - 1) * POR_PAGINA + 1}–
                {Math.min(pagina * POR_PAGINA, noticiasFiltradas.length)} de{" "}
                {noticiasFiltradas.length} notícias
              </span>
              <div className="pagination-buttons">
                <button
                  onClick={() => setPagina((p) => Math.max(1, p - 1))}
                  disabled={pagina === 1}
                  className="page-btn"
                >
                  ‹
                </button>
                {Array.from({ length: totalPaginas }, (_, i) => i + 1).map(
                  (p) => (
                    <button
                      key={p}
                      onClick={() => setPagina(p)}
                      className={`page-btn ${pagina === p ? "active" : ""}`}
                    >
                      {p}
                    </button>
                    ),
                  )}
                  <button
                    onClick={() => setPagina((p) => Math.min(totalPaginas, p + 1))}
                    disabled={pagina === totalPaginas}
                    className="page-btn"
                  >
                    ›
                  </button>
                </div>
              </div>
            )}
          </div>
        </main>
      </div>
    );
  }