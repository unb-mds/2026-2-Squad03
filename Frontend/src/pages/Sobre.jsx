import Sidebar from "../components/Sidebar";
import "../App.css";
import "./Sobre.css";

const STACK = [
  { grupo: "Frontend", icone: "🎨", itens: ["React"] },
  { grupo: "Backend", icone: "⚙️", itens: ["Scrapy", "Playwright", "FastAPI"] },
  { grupo: "Banco de dados", icone: "🗄️", itens: ["PostgreSQL"] },
];

const PORTAIS = ["G1", "Metrópoles", "R7", "CNN"];

const FLUXO = [
  { titulo: "Portais de notícias", desc: "Fontes públicas: G1, Metrópoles, R7 e CNN." },
  { titulo: "Scrapy / Playwright", desc: "Robôs de coleta navegam e capturam o conteúdo." },
  { titulo: "Coleta automatizada", desc: "Execução contínua, sem intervenção manual." },
  { titulo: "Tratamento dos dados", desc: "Limpeza, padronização e filtragem por tema." },
  { titulo: "Arquivos JSON", desc: "Dados estruturados, prontos para consumo." },
  { titulo: "API FastAPI", desc: "Camada que organiza e expõe os dados." },
  { titulo: "Frontend React", desc: "Visualização final — aqui, neste painel." },
];

const FUNCIONALIDADES = [
  "Coleta automatizada de notícias",
  "Filtragem por tema relacionado a feminicídio",
  "Consolidação de dados em JSON",
  "Monitoramento contínuo",
  "Estrutura modular para expansão futura",
  "Compatibilidade com análise de dados e Machine Learning",
];

const ROADMAP = [
  "Dashboard estatístico",
  "Análise temporal",
  "Visualização gráfica",
  "Sistema de busca",
  "Análise de sentimento",
  "Classificação automática de notícias",
  "API pública para consulta de dados",
];

const EQUIPE = [
  {
    nome: "Vitor Barreto Gomes",
    funcao: "Frontend",
    github: "https://github.com/TheBagomes",

  },

  
];

export default function Sobre() {
  return (
    <div className="app">
      <Sidebar />
      <main className="content">
        <header className="header">
          <div>
            <h2>Sobre</h2>
            <p>O projeto e os dados por trás do VeritasIA</p>
          </div>
          <div className="header-actions">
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

        <div className="sobre-page">
          <section className="sobre-hero">
            <span className="section-eyebrow">Sobre o projeto</span>
            <h3 className="sobre-quote">Transformar números em consciência.</h3>
            <p>
              O VeritasIA reúne, analisa e divulga dados sobre feminicídio no
              Brasil, construindo uma visão clara e fundamentada sobre a
              violência contra a mulher no país.
            </p>
            <p>
              A partir de notícias e dados públicos de fontes oficiais e
              veículos de comunicação confiáveis, transformamos informação
              dispersa em um painel único, acessível e centralizado.
            </p>
          </section>

          <div className="sobre-row">
            <section className="sobre-card">
              <span className="section-eyebrow">Tecnologia</span>
              <h3 className="section-title">Como construímos</h3>
              <div className="stack-list">
                {STACK.map((s) => (
                  <div className="stack-group" key={s.grupo}>
                    <div className="stack-icon">{s.icone}</div>
                    <div>
                      <p className="stack-label">{s.grupo}</p>
                      <div className="stack-pills">
                        {s.itens.map((item) => (
                          <span className="stack-pill" key={item}>
                            {item}
                          </span>
                        ))}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </section>

            <section className="sobre-card">
              <span className="section-eyebrow">Fontes</span>
              <h3 className="section-title">Portais monitorados</h3>
              <p className="section-sub">Coleta contínua, sem intervenção manual.</p>
              <div className="portal-list">
                {PORTAIS.map((p) => (
                  <span className="portal-chip" key={p}>
                    <span className="portal-dot"></span>
                    {p}
                  </span>
                ))}
              </div>
            </section>
          </div>

          <section className="sobre-card fluxo-card">
            <span className="section-eyebrow">Arquitetura</span>
            <h3 className="section-title">Da notícia ao painel</h3>
            <p className="section-sub">
              Sete etapas, da coleta bruta até a visualização final.
            </p>
            <div className="fluxo-list">
              {FLUXO.map((f, i) => (
                <div className="fluxo-item" key={f.titulo}>
                  <div className="fluxo-num">{i + 1}</div>
                  <p className="fluxo-title">{f.titulo}</p>
                  <p className="fluxo-desc">{f.desc}</p>
                </div>
              ))}
            </div>
          </section>

          <div className="sobre-row">
            <section className="sobre-card">
              <span className="section-eyebrow">Hoje</span>
              <h3 className="section-title">O que já existe</h3>
              <ul className="feature-list">
                {FUNCIONALIDADES.map((f) => (
                  <li className="feature-item" key={f}>
                    <span className="feature-check">✓</span>
                    {f}
                  </li>
                ))}
              </ul>
            </section>

            <section className="sobre-card roadmap-card">
              <span className="section-eyebrow">Em breve</span>
              <h3 className="section-title">O que vem por aí</h3>
              <ul className="feature-list">
                {ROADMAP.map((f) => (
                  <li className="feature-item roadmap-item" key={f}>
                    <span className="feature-circle"></span>
                    {f}
                  </li>
                ))}
              </ul>
            </section>
          </div>

          <section className="aviso-box">
            <div className="aviso-icon">⚖️</div>
            <p className="aviso-text">
              Este projeto utiliza exclusivamente informações públicas
              provenientes de portais jornalísticos e fontes abertas,
              respeitando limites éticos de coleta de dados e sem contornar
              mecanismos de proteção ou autenticação.
            </p>
          </section>
        </div>
      </main>
    </div>
  );
}
