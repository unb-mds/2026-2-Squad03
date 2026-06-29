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