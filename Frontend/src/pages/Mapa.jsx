import { useState, useEffect } from "react";
import Sidebar from "../components/Sidebar";
import LeafletMap from "../components/LeafletMap";
import "../App.css";

export default function Mapa() {
  const [noticias, setNoticias] = useState(null);
  const [carregando, setCarregando] = useState(true);
  const [erro, setErro] = useState(null);

  useEffect(() => {
    async function buscarNoticiasMapa() {
      try {
        const resposta = await fetch('https://two026-2-veritasia.onrender.com/mapa');
        
        if (!resposta.ok) {
          throw new Error('Não foi possível carregar os dados geográficos.');
        }

        const dadosGeo = await resposta.json();
        setNoticias(dadosGeo);
      } catch (err) {
        console.error("Erro no fetch do mapa:", err);
        setErro(err.message);
      } finally {
        setCarregando(false);
      }
    }

    buscarNoticiasMapa();
  }, []);

  return (
    <div className="app">
      <Sidebar />

      <main className="content">
        <header className="header">
          <div>
            <h2>Mapa</h2>
            <p>Visualização geográfica das notícias monitoradas</p>
          </div>
        </header>

        <section className="full-box">
          <h3>Distribuição das notícias pelo Brasil</h3>

          <div className="map-page-container">
            {carregando ? (
              <div className="map-loading">Carregando mapa e notícias...</div>
            ) : erro ? (
              <div className="map-error">Erro: {erro}</div>
            ) : (
              // Aqui passamos os dados recebidos via API como prop 'data'
              <LeafletMap data={noticias} />
            )}
          </div>
        </section>
      </main>
    </div>
  );
}