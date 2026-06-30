/**
 * ============================================================================
 * Componente: NewsChart
 * ----------------------------------------------------------------------------
 * Responsável por exibir a evolução temporal da quantidade de notícias
 * monitoradas pelo sistema.
 *
 * Funcionalidades:
 * - Obtém os dados estatísticos do Dashboard.
 * - Renderiza um gráfico de linhas utilizando Recharts.
 * - Exibe a quantidade de notícias publicadas por dia.
 *
 * Bibliotecas:
 * - Recharts
 * ============================================================================
 */

/** 
 * Armazena os dados utilizados pelo gráfico.
 
const [data, setData] = useState([]);

 * Controla o estado de carregamento da requisição.
 
const [loading, setLoading] = useState(true);*/

/**
 * Executado apenas durante a montagem do componente.
 *
 * Responsável por obter os dados necessários para
 * construção do gráfico temporal.
 
useEffect(() => { */

/**
 * Realiza a requisição das estatísticas utilizadas
 * pelo gráfico de evolução das notícias.
 
async function fetchData() { */

import { useState, useEffect } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

function NewsChart() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
      try {
        // Certifique-se de que a URL corresponde à rota que você criou
        const response = await fetch('https://two026-2-veritasia.onrender.com/dashboard');
        if (!response.ok) throw new Error("Erro ao buscar dados do gráfico");
        const json = await response.json();
        setData(json);
      } catch (err) {
        console.error("Erro no NewsChart:", err);
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, []);

  if (loading) return <p>Carregando gráfico...</p>;

  return (
    <ResponsiveContainer width="100%" height={300}>
      <LineChart data={data.noticias_semana}>
        <XAxis dataKey="dia" />
        <YAxis />
        <Tooltip />
        <Line
          type="monotone"
          dataKey="noticias"
          stroke="#0b4db3"
          strokeWidth={3}
          activeDot={{ r: 8 }}
        />
      </LineChart>
    </ResponsiveContainer>
  );
}

export default NewsChart;