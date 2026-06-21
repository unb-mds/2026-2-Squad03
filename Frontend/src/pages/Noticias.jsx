import { useState, useMemo } from "react";
import Sidebar from "../components/Sidebar";
import "../App.css";
import "./Noticias.css";

const MOCK_NEWS = [
  {
    id: 1,
    titulo: "Mulher é morta a facadas pelo ex-companheiro em SP",
    veiculo: "G1",
    data: "12/05/2026",
    estado: "SP",
  },
  {
    id: 2,
    titulo: "Feminicídio: mulher é assassinada dentro de casa em BH",
    veiculo: "UOL",
    data: "11/05/2026",
    estado: "MG",
  },
  {
    id: 3,
    titulo: "Polícia prende suspeito de feminicídio no Rio de Janeiro",
    veiculo: "Metrópoles",
    data: "11/05/2026",
    estado: "RJ",
  },
  {
    id: 4,
    titulo: "Dados apontam aumento de casos de feminicídio no país",
    veiculo: "Folha de S.Paulo",
    data: "10/05/2026",
    estado: "DF",
  },
  {
    id: 5,
    titulo: "Vítima de violência doméstica recebe medida protetiva em Brasília",
    veiculo: "R7",
    data: "10/05/2026",
    estado: "DF",
  },
  {
    id: 6,
    titulo: "Mulher é morta a facadas pelo ex-companheiro em SP",
    veiculo: "G1",
    data: "09/05/2026",
    estado: "SP",
  },
  {
    id: 7,
    titulo: "Caso de feminicídio é investigado pela polícia no Nordeste",
    veiculo: "G1",
    data: "09/05/2026",
    estado: "BA",
  },
  {
    id: 8,
    titulo: "Mulher sobrevive a tentativa de feminicídio em Porto Alegre",
    veiculo: "Metrópoles",
    data: "08/05/2026",
    estado: "RS",
  },
  {
    id: 9,
    titulo: "Delegacia da mulher recebe recorde de denúncias em maio",
    veiculo: "UOL",
    data: "08/05/2026",
    estado: "SP",
  },
  {
    id: 10,
    titulo: "Governo lança campanha de combate à violência doméstica",
    veiculo: "Folha de S.Paulo",
    data: "07/05/2026",
    estado: "DF",
  },
  {
    id: 11,
    titulo: "Mulher é assassinada pelo marido após pedir divórcio no CE",
    veiculo: "R7",
    data: "07/05/2026",
    estado: "CE",
  },
  {
    id: 12,
    titulo: "Feminicídio tentado: mulher escapa após vizinhos acionarem PM",
    veiculo: "G1",
    data: "06/05/2026",
    estado: "RJ",
  },
];

const ESTADOS = [...new Set(MOCK_NEWS.map((n) => n.estado))].sort();
const VEICULOS = [...new Set(MOCK_NEWS.map((n) => n.veiculo))].sort();

export default function Noticias() {
  const [busca, setBusca] = useState("");
  const [filtroEstado, setFiltroEstado] = useState("");
  const [filtroVeiculo, setFiltroVeiculo] = useState("");
  const [filtroPeriodo, setFiltroPeriodo] = useState("");
  const [pagina, setPagina] = useState(1);
  const POR_PAGINA = 8;

  function limparFiltros() {
    setBusca("");
    setFiltroEstado("");
    setFiltroVeiculo("");
    setFiltroPeriodo("");
    setPagina(1);
  }

  const noticiasFiltradas = useMemo(() => {
    return MOCK_NEWS.filter((n) => {
      const buscaOk =
        !busca ||
        n.titulo.toLowerCase().includes(busca.toLowerCase()) ||
        n.veiculo.toLowerCase().includes(busca.toLowerCase());
      const estadoOk = !filtroEstado || n.estado === filtroEstado;
      const veiculoOk = !filtroVeiculo || n.veiculo === filtroVeiculo;
      return buscaOk && estadoOk && veiculoOk;
    });
  }, [busca, filtroEstado, filtroVeiculo]);

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

          {/* Tabela */}
          <div className="noticias-table-wrap">
            <table className="noticias-table">
              <thead>
                <tr>
                  <th>Título</th>
                  <th>Veículo</th>
                  <th>Data</th>
                  <th>Estado</th>
                </tr>
              </thead>
              <tbody>
                {noticiasPagina.length === 0 ? (
                  <tr>
                    <td colSpan={4} className="noticias-empty">
                      Nenhuma notícia encontrada para os filtros selecionados.
                    </td>
                  </tr>
                ) : (
                  noticiasPagina.map((n) => (
                    <tr key={n.id}>
                      <td className="noticia-titulo">{n.titulo}</td>
                      <td>{n.veiculo}</td>
                      <td>{n.data}</td>
                      <td>
                        <span className="estado-badge">{n.estado}</span>
                      </td>
                    </tr>
                  ))
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
                  onClick={() =>
                    setPagina((p) => Math.min(totalPaginas, p + 1))
                  }
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
