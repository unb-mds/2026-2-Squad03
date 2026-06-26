import "../App.css";
import "./DetalhesNoticia.css";
import { noticias } from "../data/noticias";
import { useState } from "react";

import { useNavigate, useParams } from "react-router-dom";
import Sidebar from "../components/Sidebar";

export default function Detalhes_Noticia() {
  
  const navigate = useNavigate();
  const [mostrarAviso, setMostrarAviso] = useState(true);
  const { id } = useParams();

const noticia = noticias.find(
  (item) => item.id === Number(id)
);

if (!noticia) {
  return (
    <div className="app">
      <Sidebar />

      <main className="content">
        <h2>Notícia não encontrada.</h2>
      </main>
    </div>
  );
}

  return (
    <div className="app">
      <Sidebar />

      <main className="content">

        <header className="header">
          <div>
            <h2>Notícia</h2>
            <p>Visualização detalhada da notícia coletada</p>
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

        {mostrarAviso && (
  <div className="overlay-aviso">
    <div className="modal-aviso">

      <div className="icone-aviso">
        ⚠️
      </div>

      <h2>Conteúdo Sensível</h2>

      <p>
        Esta notícia contém informações relacionadas a
        <strong> feminicídio </strong>
        e violência contra a mulher.
      </p>

      <p>
        O conteúdo é apresentado para fins de
        conscientização, pesquisa e monitoramento.
      </p>

      <div className="botoes-aviso">

        <button
          className="btn-continuar"
          onClick={() => setMostrarAviso(false)}
        >
          Continuar leitura
        </button>

        <button
          className="btn-voltar"
          onClick={() => navigate("/noticias")}
        >
          Voltar
        </button>

      </div>

    </div>
  </div>
)}

        <button
          className="voltar-btn"
          onClick={() => navigate("/noticias")}
        >
          ← Voltar para Notícias
        </button>

        <div className="noticia-layout">

          <section className="noticia-card">

            <div className="noticia-top">

              <span className="categoria">
                {noticia.categoria}
              </span>

              <span className="status verificado">
                ✔ {noticia.status}
              </span>

            </div>

            <h1>{noticia.titulo}</h1>

            <div className="metadados">

              <span>📰 {noticia.fonte}</span>

              <span>📅 {noticia.data}</span>

              <span>📍 {noticia.cidade} - {noticia.estado}</span>

            </div>

            <div className="imagem-placeholder">

              <span>📰</span>

              <p>Imagem da notícia</p>

            </div>

            <div className="bloco">

              <h3>Resumo</h3>

              <p>{noticia.resumo}</p>

            </div>

            <div className="bloco">

              <h3>Conteúdo</h3>

              {noticia.conteudo
                .trim()
                .split("\n")
                .map((texto, index) => (
                  <p key={index}>{texto}</p>
                ))}

            </div>

            <a
              href={noticia.link}
              target="_blank"
              rel="noreferrer"
              className="fonte-btn"
            >
              Acessar notícia original
            </a>

          </section>

          <aside className="info-card">

            <h3>Informações</h3>

            <div className="info-item">
              <strong>Categoria</strong>
              <span>{noticia.categoria}</span>
            </div>

            <div className="info-item">
              <strong>Status</strong>
              <span className="status verificado">
                ✔ {noticia.status}
              </span>
            </div>

            <div className="info-item">
              <strong>Fonte</strong>
              <span>{noticia.fonte}</span>
            </div>

            <div className="info-item">
              <strong>Data da coleta</strong>
              <span>{noticia.data}</span>
            </div>

            <div className="info-item">
              <strong>Local geocodificado</strong>
              <span>{noticia.cidade} - {noticia.estado}</span>
            </div>

          </aside>

        </div>

      </main>
    </div>
  );
}