import { useState, useMemo, useEffect } from "react";
import { Link } from 'react-router-dom';
import Sidebar from "../components/Sidebar";
import "../App.css";
import "./Noticias.css";

export default function ListaNoticias() {
  // 1. Estados para gerenciar o ciclo de dados da API
  const [noticias, setNoticias] = useState([]);
  const [carregando, setCarregando] = useState(true);
  const [erro, setErro] = useState(null);

  // 2. Estados para manipulação de filtros e paginação da interface
  const [busca, setBusca] = useState("");
  const [filtroEstado, setFiltroEstado] = useState("");
  const [filtroVeiculo, setFiltroVeiculo] = useState("");
  const [filtroPeriodo, setFiltroPeriodo] = useState("");
  const [pagina, setPagina] = useState(1);
  const POR_PAGINA = 8;

  // Hook para buscar os dados reais do seu banco de dados via FastAPI
  useEffect(() => {
    async function buscarTodasAsNoticias() {
      try {
        const resposta = await fetch('https://two026-2-veritasia.onrender.com/noticias');
        
        if (!resposta.ok) {
          throw new Error('Não foi possível obter os dados do servidor.');
        }

        const dadosDoBanco = await resposta.json();
        setNoticias(dadosDoBanco); 
      } catch (err) {
        console.error("Erro na requisição:", err);
        setErro(err.message);
      } finally {
        setCarregando(false);
      }
    }

    buscarTodasAsNoticias();
  }, []); 

  // 3. Extração dinâmica de opções para os filtros baseada no que existe no banco
  const ESTADOS = useMemo(() => {
    const ufs = noticias.map((n) => n.estado).filter(Boolean);
    return [...new Set(ufs)].sort();
  }, [noticias]);

  const VEICULOS = useMemo(() => {
    const mídias = noticias.map((n) => n.veiculo).filter(Boolean);
    return [...new Set(mídias)].sort();
  }, [noticias]);

  // 4. Lógica de Filtro aplicada sobre as notícias reais do banco
  const noticiasFiltradas = useMemo(() => {
    return noticias.filter((n) => {
      const buscaOk =
        !busca ||
        (n.titulo && n.titulo.toLowerCase().includes(busca.toLowerCase())) ||
        (n.veiculo && n.veiculo.toLowerCase().includes(busca.toLowerCase()));
      const estadoOk = !filtroEstado || n.estado === filtroEstado;
      const veiculoOk = !filtroVeiculo || n.veiculo === filtroVeiculo;
      return buscaOk && estadoOk && veiculoOk;
    });
  }, [noticias, busca, filtroEstado, filtroVeiculo]);

  // 5. Cálculos de Paginação
  const totalPaginas = Math.ceil(noticiasFiltradas.length / POR_PAGINA);
  const noticiasPagina = useMemo(() => {
    return noticiasFiltradas.slice(
      (pagina - 1) * POR_PAGINA,
      pagina * POR_PAGINA,
    );
  }, [noticiasFiltradas, pagina]);

  const temFiltro = busca || filtroEstado || filtroVeiculo || filtroPeriodo;

  function limparFiltros() {
    setBusca("");
    setFiltroEstado("");
    setFiltroVeiculo("");
    setFiltroPeriodo("");
    setPagina(1);
  }

  // Renderizações condicionais para carregamento ou erro de rede


  return (
    <div className="app">
      <Sidebar />
      <main className="content">
        <header className="header">
          <div>
            <h2>Notícias</h2>
            <p>Monitoramento de notícias sobre desinformação no Brasil</p>
          </div>
          <div className="header-actions">
            <button className="date-button">
              <span>📅</span>
              <span>01/05/2026 - 31/05/2026</span>
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

          {/* Tabela Modificada para o Banco de Dados */}
          <div className="noticias-table-wrap">
            <table className="noticias-table">
              <thead>
                <tr>
                  <th>Título</th>
                  <th>Link Original</th>
                  <th>Resumo IA</th>
                  <th>ID Banco</th>
                </tr>
              </thead>
              <tbody>
              {carregando ? (
                // Caso esteja carregando
                <tr>
                  <td colSpan={4} className="noticias-empty">
                    Procurando notícias no banco de dados... <span className="loading-dots">⏳</span>
                  </td>
                </tr>
              ) : erro ? (
                // Caso tenha ocorrido um erro (opcional, mas recomendado)
                <tr>
                  <td colSpan={4} className="noticias-empty" style={{ color: 'red' }}>
                    Erro ao carregar: {erro}
                  </td>
                </tr>
              ) : noticiasPagina.length > 0 ? (
                // Caso tenha notícias
                noticiasPagina.map((n) => (
                  <tr key={n.id}>
                    <td className="noticia-titulo">
                      <Link to={`/noticias/${n.id}`} style={{ textDecoration: 'none', color: '#007acc', fontWeight: 'bold' }}>
                        {n.titulo}
                      </Link>
                    </td>
                    <td>
                      <a href={n.fonte_url} target="_blank" rel="noreferrer" style={{ color: '#555' }}>
                        Acessar Fonte
                      </a>
                    </td>
                    <td style={{ fontSize: '0.9em', color: '#666' }}>
                      {n.resumo_blur ? `${n.resumo_blur.substring()}...` : "Sem resumo"}
                    </td>
                    <td>
                      <span className="estado-badge" style={{ fontFamily: 'monospace' }}>#{n.id}</span>
                    </td>
                  </tr>
                ))
              ) : (
                // Caso a lista esteja vazia após os filtros
                <tr>
                  <td colSpan={4} className="noticias-empty">
                    Nenhuma notícia encontrada com os filtros atuais.
                  </td>
                </tr>
              )}
            </tbody>
            </table>
          </div>

          {/* Paginação */}
          {totalPaginas > 1 && (
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