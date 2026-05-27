import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

const data = [
  { dia: "Seg", noticias: 12 },
  { dia: "Ter", noticias: 19 },
  { dia: "Qua", noticias: 8 },
  { dia: "Qui", noticias: 22 },
  { dia: "Sex", noticias: 17 },
  { dia: "Sáb", noticias: 25 },
  { dia: "Dom", noticias: 15 },
];

function NewsChart() {
  return (
    <ResponsiveContainer width="100%" height={300}>
      <LineChart data={data}>
        <XAxis dataKey="dia" />

        <YAxis />

        <Tooltip />

        <Line
          type="monotone"
          dataKey="noticias"
          stroke="#0b4db3"
          strokeWidth={3}
        />
      </LineChart>
    </ResponsiveContainer>
  );
}

export default NewsChart;
