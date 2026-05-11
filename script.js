const dadosComits = [
  { nome: "Ana", valor: 128, cor: "#6ee7ff" },
  { nome: "Bruno", valor: 96, cor: "#a78bfa" },
  { nome: "Carla", valor: 142, cor: "#34d399" },
  { nome: "Diego", valor: 74, cor: "#fbbf24" },
  { nome: "Edu", valor: 110, cor: "#fb7185" },
];

const dadosSemana = [
  { dia: "Seg", valor: 22 },
  { dia: "Ter", valor: 28 },
  { dia: "Qua", valor: 19 },
  { dia: "Qui", valor: 34 },
  { dia: "Sex", valor: 41 },
];

const dadosDistribuicao = [
  { label: "Commits", value: 54, color: "#6ee7ff" },
  { label: "PRs", value: 26, color: "#a78bfa" },
  { label: "Tickets", value: 20, color: "#34d399" },
];

// Heatmap: linhas = semanas, colunas = dias da semana
const dias = ["Seg", "Ter", "Qua", "Qui", "Sex"]; // 5 dias
const semanas = ["S1", "S2", "S3", "S4", "S5", "S6"]; // 6 semanas
const heatValues = [
  [1, 2, 3, 2, 4],
  [2, 1, 2, 3, 3],
  [3, 2, 4, 3, 5],
  [2, 3, 3, 2, 4],
  [4, 3, 2, 4, 5],
  [3, 4, 3, 5, 4],
];

// ==============================
// Helpers
// ==============================
function setUpdatedText() {
  const el = document.getElementById("atualizado");
  if (!el) return;
  const d = new Date();
  el.textContent = d.toLocaleString("pt-BR");
}

function clearEl(id) {
  const el = document.getElementById(id);
  if (!el) return;
  el.innerHTML = "";
}

function appendLegend(containerId, items) {
  const legend = document.getElementById(containerId);
  if (!legend) return;
  legend.innerHTML = "";

  for (const it of items) {
    const div = document.createElement("div");
    div.className = "legend-item";
    div.innerHTML = `<span class="swatch" style="background:${it.color}"></span><span>${it.nome || it.label}: ${it.valor ?? it.value}</span>`;
    legend.appendChild(div);
  }
}

// ==============================
// Chart 1: Bar chart (Comits)
// ==============================
function renderComits() {
  const id = "chart-comits";
  const wrap = document.getElementById(id);
  if (!wrap) return;

  clearEl(id);

  const width = wrap.clientWidth;
  const height = wrap.clientHeight;
  const margin = { top: 18, right: 14, bottom: 44, left: 52 };

  const svg = d3
    .select(wrap)
    .append("svg")
    .attr("width", width)
    .attr("height", height);

  const data = [...dadosComits].sort((a, b) => b.valor - a.valor);

  const x = d3
    .scaleBand()
    .domain(data.map((d) => d.nome))
    .range([margin.left, width - margin.right])
    .padding(0.2);

  const y = d3
    .scaleLinear()
    .domain([0, d3.max(data, (d) => d.valor) * 1.1])
    .nice()
    .range([height - margin.bottom, margin.top]);

  svg
    .append("g")
    .attr("transform", `translate(0,${height - margin.bottom})`)
    .call(d3.axisBottom(x).tickSize(0))
    .selectAll("text")
    .style("fill", "rgba(255,255,255,0.8)")
    .style("font-size", "12px");

  svg
    .append("g")
    .attr("transform", `translate(${margin.left},0)`)
    .call(d3.axisLeft(y).ticks(5).tickSize(0))
    .selectAll("text")
    .style("fill", "rgba(255,255,255,0.7)")
    .style("font-size", "12px");

  const grid = svg.append("g");
  grid
    .attr("transform", `translate(${margin.left},0)`)
    .call(
      d3
        .axisLeft(y)
        .ticks(5)
        .tickSize(-1 * (width - margin.left - margin.right))
        .tickFormat(""),
    )
    .selectAll("line")
    .attr("stroke", "rgba(255,255,255,0.08)");

  svg
    .append("g")
    .selectAll("rect")
    .data(data)
    .enter()
    .append("rect")
    .attr("x", (d) => x(d.nome))
    .attr("y", (d) => y(d.valor))
    .attr("width", x.bandwidth())
    .attr("height", (d) => height - margin.bottom - y(d.valor))
    .attr("rx", 8)
    .attr("fill", (d) => d.cor)
    .attr("opacity", 0.92);

  // Labels
  svg
    .append("g")
    .selectAll("text")
    .data(data)
    .enter()
    .append("text")
    .attr("x", (d) => x(d.nome) + x.bandwidth() / 2)
    .attr("y", (d) => y(d.valor) - 6)
    .attr("text-anchor", "middle")
    .text((d) => d.valor)
    .style("fill", "rgba(255,255,255,0.92)")
    .style("font-size", "12px")
    .style("font-weight", "700");

  appendLegend("legend-comits", data);
}

// ==============================
// Chart 2: Line chart (Produtividade semanal)
// ==============================
function renderSemana() {
  const id = "chart-semana";
  const wrap = document.getElementById(id);
  if (!wrap) return;

  clearEl(id);

  const width = wrap.clientWidth;
  const height = wrap.clientHeight;
  const margin = { top: 20, right: 20, bottom: 42, left: 52 };

  const svg = d3
    .select(wrap)
    .append("svg")
    .attr("width", width)
    .attr("height", height);

  const data = dadosSemana;

  const x = d3
    .scalePoint()
    .domain(data.map((d) => d.dia))
    .range([margin.left, width - margin.right]);

  const y = d3
    .scaleLinear()
    .domain([0, d3.max(data, (d) => d.valor) * 1.2])
    .nice()
    .range([height - margin.bottom, margin.top]);

  // Grid
  svg
    .append("g")
    .attr("transform", `translate(${margin.left},0)`)
    .call(
      d3
        .axisLeft(y)
        .ticks(5)
        .tickSize(-1 * (width - margin.left - margin.right))
        .tickFormat(""),
    )
    .selectAll("line")
    .attr("stroke", "rgba(255,255,255,0.08)");

  // Axes
  svg
    .append("g")
    .attr("transform", `translate(0,${height - margin.bottom})`)
    .call(d3.axisBottom(x))
    .selectAll("text")
    .style("fill", "rgba(255,255,255,0.8)")
    .style("font-size", "12px");

  svg
    .append("g")
    .attr("transform", `translate(${margin.left},0)`)
    .call(d3.axisLeft(y).ticks(5).tickSize(0))
    .selectAll("text")
    .style("fill", "rgba(255,255,255,0.7)")
    .style("font-size", "12px");

  const line = d3
    .line()
    .x((d) => x(d.dia))
    .y((d) => y(d.valor))
    .curve(d3.curveMonotoneX);

  svg
    .append("path")
    .datum(data)
    .attr("fill", "none")
    .attr("stroke", "#6ee7ff")
    .attr("stroke-width", 3)
    .attr("d", line);

  // Area fill
  svg
    .append("path")
    .datum(data)
    .attr("fill", "rgba(110,231,255,0.18)")
    .attr(
      "d",
      d3
        .area()
        .x((d) => x(d.dia))
        .y0(height - margin.bottom)
        .y1((d) => y(d.valor))
        .curve(d3.curveMonotoneX),
    );

  // Points
  svg
    .selectAll("circle")
    .data(data)
    .enter()
    .append("circle")
    .attr("cx", (d) => x(d.dia))
    .attr("cy", (d) => y(d.valor))
    .attr("r", 6)
    .attr("fill", "#a78bfa")
    .attr("opacity", 0.95);

  // Tooltip-ish labels (static)
  svg
    .selectAll("text.point")
    .data(data)
    .enter()
    .append("text")
    .attr("class", "point")
    .attr("x", (d) => x(d.dia))
    .attr("y", (d) => y(d.valor) - 10)
    .attr("text-anchor", "middle")
    .text((d) => d.valor)
    .style("fill", "rgba(255,255,255,0.9)")
    .style("font-size", "12px")
    .style("font-weight", "700");
}

// ==============================
// Chart 3: Donut chart (Distribuição)
// ==============================
function renderDistribuicao() {
  const id = "chart-distribuicao";
  const wrap = document.getElementById(id);
  if (!wrap) return;

  clearEl(id);

  const width = wrap.clientWidth;
  const height = wrap.clientHeight;
  const r = Math.min(width, height) * 0.28;

  const svg = d3
    .select(wrap)
    .append("svg")
    .attr("width", width)
    .attr("height", height);

  const g = svg
    .append("g")
    .attr("transform", `translate(${width / 2},${height / 2})`);

  const data = dadosDistribuicao;

  const pie = d3
    .pie()
    .value((d) => d.value)
    .sort(null);

  const arc = d3
    .arc()
    .innerRadius(r * 0.62)
    .outerRadius(r);

  const arcs = g
    .selectAll("path")
    .data(pie(data))
    .enter()
    .append("path")
    .attr("d", arc)
    .attr("fill", (d) => d.data.color)
    .attr("stroke", "rgba(0,0,0,0.35)")
    .attr("stroke-width", 1);

  // Center label
  const total = data.reduce((sum, d) => sum + d.value, 0);
  g.append("text")
    .attr("text-anchor", "middle")
    .attr("y", -4)
    .style("font-size", "22px")
    .style("font-weight", 900)
    .style("fill", "rgba(255,255,255,0.95)")
    .text(total);

  g.append("text")
    .attr("text-anchor", "middle")
    .attr("y", 18)
    .style("font-size", "12px")
    .style("fill", "rgba(255,255,255,0.7)")
    .text("total (mock)");

  appendLegend(
    "legend-distribuicao",
    data.map((d) => ({ label: d.label, value: d.value, color: d.color })),
  );
}

// ==============================
// Chart 4: Heatmap
// ==============================
function renderHeatmap() {
  const id = "chart-heatmap";
  const wrap = document.getElementById(id);
  if (!wrap) return;

  clearEl(id);

  const width = wrap.clientWidth;
  const height = wrap.clientHeight;
  const margin = { top: 28, right: 18, bottom: 30, left: 52 };

  const svg = d3
    .select(wrap)
    .append("svg")
    .attr("width", width)
    .attr("height", height);

  const maxVal = d3.max(heatValues.flat());

  const x = d3
    .scaleBand()
    .domain(dias)
    .range([margin.left, width - margin.right])
    .padding(0.08);

  const y = d3
    .scaleBand()
    .domain(semanas)
    .range([margin.top, height - margin.bottom])
    .padding(0.08);

  const color = d3
    .scaleSequential()
    .domain([0, maxVal])
    .interpolator(d3.interpolateRgbBasis(["#1f2937", "#34d399", "#6ee7ff"]));

  // Axes labels
  svg
    .append("g")
    .attr("transform", `translate(0,${height - margin.bottom})`)
    .call(d3.axisBottom(x).tickSize(0))
    .selectAll("text")
    .style("fill", "rgba(255,255,255,0.8)")
    .style("font-size", "12px");

  svg
    .append("g")
    .attr("transform", `translate(${margin.left},0)`)
    .call(d3.axisLeft(y).tickSize(0))
    .selectAll("text")
    .style("fill", "rgba(255,255,255,0.7)")
    .style("font-size", "12px");

  const cells = [];
  for (let i = 0; i < semanas.length; i++) {
    for (let j = 0; j < dias.length; j++) {
      cells.push({ semana: semanas[i], dia: dias[j], value: heatValues[i][j] });
    }
  }

  svg
    .append("g")
    .selectAll("rect")
    .data(cells)
    .enter()
    .append("rect")
    .attr("x", (d) => x(d.dia))
    .attr("y", (d) => y(d.semana))
    .attr("width", x.bandwidth())
    .attr("height", y.bandwidth())
    .attr("rx", 6)
    .attr("fill", (d) => color(d.value))
    .attr("opacity", 0.95);

  // Cell text (valor)
  svg
    .append("g")
    .selectAll("text")
    .data(cells)
    .enter()
    .append("text")
    .attr("x", (d) => x(d.dia) + x.bandwidth() / 2)
    .attr("y", (d) => y(d.semana) + y.bandwidth() / 2 + 4)
    .attr("text-anchor", "middle")
    .text((d) => d.value)
    .style("fill", "rgba(0,0,0,0.65)")
    .style("font-size", "11px")
    .style("font-weight", "800");
}

// ==============================
// Boot
// ==============================
function renderAll() {
  setUpdatedText();
  renderComits();
  renderSemana();
  renderDistribuicao();
  renderHeatmap();
}

renderAll();

// Re-render on resize (simples)
window.addEventListener("resize", () => {
  // debounce simples
  clearTimeout(window.__d3Timer);
  window.__d3Timer = setTimeout(renderAll, 150);
});
