import { useParams } from 'react-router-dom';
import { useState, useMemo, useEffect } from "react";
import { Link } from 'react-router-dom';
import Sidebar from "../components/Sidebar";
import "../App.css";
import "./Noticias.css";

export default function DetalhesNoticia() {
  const { id } = useParams(); // Captura o ID da URL
  const [noticia, setNoticia] = useState(null);
  const [carregando, setCarregando] = useState(true);

  useEffect(() => {
    async function carregarNoticia() {
      try {
        // Agora sim, o fetch aponta para a porta 8000 (FastAPI)
        const resposta = await fetch(`https://two026-2-veritasia.onrender.com//noticias/${id}`);
        
        if (!resposta.ok) throw new Error("Erro ao buscar notícia");
        
        const dados = await resposta.json();
        setNoticia(dados);
      } catch (err) {
        console.error(err);
      } finally {
        setCarregando(false);
      }
    }

    carregarNoticia();
  }, [id]); // O ID no array de dependências garante que o fetch ocorra se o ID mudar

  if (carregando) return <p>Carregando...</p>;
  if (!noticia) return <p>Notícia não encontrada.</p>;

  return (
    <div>
      <h1>{noticia.titulo}</h1>
      <p>{noticia.conteudo}</p>
      {/* Restante do seu layout */}
    </div>
  );
}