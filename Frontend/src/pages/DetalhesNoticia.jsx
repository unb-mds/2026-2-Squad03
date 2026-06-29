import "../App.css";
import "./DetalhesNoticia.css";
import { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import Sidebar from "../components/Sidebar";
import PageHeader from "../components/PageHeader";

export default function Detalhes_Noticia() {
  const navigate = useNavigate();
  const { id } = useParams();
  
  // Estados para o aviso de conteúdo sensível
  const [naoMostrarNovamente, setNaoMostrarNovamente] = useState(false);
  const [mostrarAviso, setMostrarAviso] = useState(() => {
    return localStorage.getItem("veritas-aviso-sensivel") !== "true";
  });

  const [noticia, setNoticia] = useState(null);
  const [loading, setLoading] = useState(true);
  const [erro, setErro] = useState(false);

  useEffect(() => {
    async function fetchNoticiaDetalhada() {
      try {
        setLoading(true);
        const resposta = await fetch(`https://two026-2-veritasia.onrender.com/noticias/${id}`);
        if (!resposta.ok) throw new Error("Notícia não encontrada");
        
        const n = await resposta.json();
        
        const noticiaFormatada = {
          id: n.id,
          titulo: n.titulo || "Título Indisponível",
          resumo: n.resumo_raw || "Resumo não disponível",
          conteudo: n.conteudo_raw || n.texto || n.resumo_raw || "Conteúdo completo indisponível.",
          fonte: n.Portal || n.portal || n.veiculo || n.fonte || "Desconhecido",
          data: n.data_publicacao ? new Date(n.data_publicacao).toLocaleDateString('pt-BR') : "Data não informada",
          estado: n.regiao?.nome || "N/A",
          cidade: "N/A",
          link: n.fonte_url || "#", 
          imagem: n.imagem_url || "https://via.placeholder.com/300x150?text=Sem+Imagem",
          categoria: "Geral",
          status: "Analisada",
        };

        setNoticia(noticiaFormatada);
      } catch (err) {
        console.error("Erro ao carregar detalhes:", err);
        setErro(true);
      } finally {
        setLoading(false);
      }
    }
    fetchNoticiaDetalhada();
  }, [id]);

  if (loading) return <div className="app"><Sidebar /><main className="content"><div style={{padding:'2rem'}}><h2>Carregando...</h2></div></main></div>;
  if (erro || !noticia) return (
    <div className="app"><Sidebar /><main className="content"><div style={{padding:'2rem'}}>
      <h2>Notícia não encontrada.</h2>
      <button className="voltar-btn" onClick={() => navigate("/noticias")}>← Voltar</button>
    </div></main></div>
  );

  return (
    <div className="app">
      <Sidebar />
      <main className="content">
        
        <PageHeader title="Notícia" subtitle="Visualização detalhada da notícia coletada">
            <button className="date-button">📅 <span>01/05/2024 - 31/05/2024</span></button>
            <span className="bell">🔔</span>
        </PageHeader>

        {mostrarAviso && (
          <div className="overlay-aviso">
            <div className="modal-aviso">
              <div className="icone-aviso">⚠️</div>
              <h2>Aviso de conteúdo sensível</h2>
              <p>Esta seção apresenta dados e informações detalhadas sobre casos de <strong>feminicídio e violência doméstica</strong>.</p>
              
              <label style={{ display: "center", alignItems: "center", gap: "8px", marginBottom: "20px", cursor: "pointer" }}>
                <input 
                  type="checkbox" 
                  checked={naoMostrarNovamente}
                  onChange={(e) => setNaoMostrarNovamente(e.target.checked)}
                />
                <span> Não mostrar este aviso novamente.</span>
              </label>

              <div className="botoes-aviso">
                <button className="btn-continuar" onClick={() => {
                  if (naoMostrarNovamente) {
                    localStorage.setItem("veritas-aviso-sensivel", "true");
                  }
                  setMostrarAviso(false);
                }}>Continuar para a página</button>
                <button className="btn-voltar" onClick={() => navigate("/noticias")}>Voltar</button>
              </div>
            </div>
          </div>
        )}

        <button className="voltar-btn" onClick={() => navigate("/noticias")}>← Voltar para Notícias</button>

        <div className="noticia-layout">
          <section className="noticia-card">
            <div className="noticia-top">
              <span className="categoria">{noticia.categoria}</span>
              <span className="status verificado">✔ {noticia.status}</span>
            </div>

            <h1>{noticia.titulo}</h1>

            <div className="metadados">
              <span>📰 {noticia.fonte}</span>
              <span>📅 {noticia.data}</span>
              <span>📍 {noticia.cidade} - {noticia.estado}</span>
            </div>

            <div className="imagem-placeholder">
              <img src={noticia.imagem} alt={noticia.titulo} style={{width: '100%', borderRadius: '8px'}} />
            </div>

            <div className="bloco">
              <h3>Resumo</h3>
              <p>{noticia.resumo}</p>
            </div>

            <a href={noticia.link} target="_blank" rel="noreferrer" className="fonte-btn">Acessar notícia original</a>
          </section>

          <aside className="info-card">
            <h3>Informações</h3>
            <div className="info-item"><strong>Categoria</strong><span>{noticia.categoria}</span></div>
            <div className="info-item"><strong>Status</strong><span>✔ {noticia.status}</span></div>
            <div className="info-item"><strong>Fonte</strong><span>{noticia.fonte}</span></div>
            <div className="info-item"><strong>Data</strong><span>{noticia.data}</span></div>
            <div className="info-item"><strong>Local</strong><span>{noticia.estado}</span></div>
          </aside>
        </div>
      </main>
    </div>
  );
}