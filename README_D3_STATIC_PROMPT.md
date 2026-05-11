# Prompt (HTML + CSS + JS) para página estática com gráficos de produtividade (D3.js)

Copie/cole os arquivos abaixo (index.html, style.css, script.js) no projeto e abra o **index.html** no navegador.

---

## ✅ index.html

```html
<!DOCTYPE html>
<html lang="pt-BR">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Dashboard de Produtividade (D3.js)</title>
    <link rel="stylesheet" href="./style.css" />
  </head>
  <body>
    <header class="header">
      <div>
        <h1>Dashboard de Produtividade da Equipe</h1>
        <p class="subtitle">
          Gráficos estáticos usando <strong>D3.js</strong> para visualização
          rápida.
        </p>
      </div>

      <div class="meta">
        <div class="meta-card">
          <div class="meta-label">Período</div>
          <div class="meta-value" id="periodo">Últimos 30 dias</div>
        </div>
        <div class="meta-card">
          <div class="meta-label">Atualização</div>
          <div class="meta-value" id="atualizado">—</div>
        </div>
      </div>
    </header>

    <main class="grid">
      <!-- Card 1: Comits por integrante (bar chart) -->
      <section class="card">
        <div class="card-header">
          <h2>Comits por integrante</h2>
          <span class="card-hint">Ordenado do maior para o menor</span>
        </div>
        <div class="chart" id="chart-comits"></div>
        <div class="legend" id="legend-comits"></div>
      </section>

      <!-- Card 2: Produtividade semanal (line chart) -->
      <section class="card">
        <div class="card-header">
          <h2>Produtividade semanal</h2>
          <span class="card-hint">Tendência da equipe</span>
        </div>
        <div class="chart" id="chart-semana"></div>
      </section>

      <!-- Card 3: Distribuição (donut chart) -->
      <section class="card">
        <div class="card-header">
          <h2>Distribuição de tarefas</h2>
          <span class="card-hint">Ex.: commits/PRs/tickets</span>
        </div>
        <div class="chart donut-wrap" id="chart-distribuicao"></div>
        <div class="legend" id="legend-distribuicao"></div>
      </section>

      <!-- Card 4: Matriz / Heatmap simples -->
      <section class="card">
        <div class="card-header">
          <h2>Heatmap de atividade</h2>
          <span class="card-hint">Dia da semana × semanas</span>
        </div>
        <div class="chart" id="chart-heatmap"></div>
        <div class="heatmap-footer">Quanto mais escuro, maior a atividade.</div>
      </section>
    </main>

    <footer class="footer">
      <span
        >Dados de exemplo (mock). Edite em <code>script.js</code> para usar seus
        números reais.</span
      >
    </footer>

    <!-- D3.js (v7) -->
    <script src="https://cdn.jsdelivr.net/npm/d3@7/dist/d3.min.js"></script>
    <script src="./script.js"></script>
  </body>
</html>
```

---

## ✅ style.css

```css
:root {
  --bg: #0b1220;
  --card: rgba(255, 255, 255, 0.06);
  --card2: rgba(255, 255, 255, 0.09);
  --text: rgba(255, 255, 255, 0.92);
  --muted: rgba(255, 255, 255, 0.68);
  --grid: rgba(255, 255, 255, 0.08);
  --accent: #6ee7ff;
  --accent2: #a78bfa;
  --good: #34d399;
  --warn: #fbbf24;
  --bad: #fb7185;

  --radius: 16px;
  --shadow: 0 20px 50px rgba(0, 0, 0, 0.35);
}

* {
  box-sizing: border-box;
}

body {
  margin: 0;
  font-family:
    ui-sans-serif,
    system-ui,
    -apple-system,
    Segoe UI,
    Roboto,
    Helvetica,
    Arial;
  background:
    radial-gradient(
      1200px 600px at 20% 0%,
      rgba(110, 231, 255, 0.18),
      transparent 55%
    ),
    radial-gradient(
      1000px 520px at 90% 20%,
      rgba(167, 139, 250, 0.16),
      transparent 50%
    ),
    var(--bg);
  color: var(--text);
  min-height: 100vh;
}

.header {
  padding: 28px 22px 16px;
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 18px;
}

.header h1 {
  margin: 0;
  font-size: 24px;
  letter-spacing: 0.2px;
}

.subtitle {
  margin: 8px 0 0;
  color: var(--muted);
  max-width: 720px;
}

.meta {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
  min-width: 280px;
}

.meta-card {
  background: var(--card);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 12px;
  padding: 12px 14px;
}

.meta-label {
  color: var(--muted);
  font-size: 12px;
}

.meta-value {
  margin-top: 6px;
  font-size: 14px;
  font-weight: 700;
}

.grid {
  max-width: 1200px;
  margin: 0 auto;
  padding: 12px 22px 28px;
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: 14px;
}

.card {
  grid-column: span 6;
  background: linear-gradient(
    180deg,
    rgba(255, 255, 255, 0.08),
    rgba(255, 255, 255, 0.04)
  );
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
  padding: 14px 14px 12px;
  overflow: hidden;
}

.card:nth-child(1) {
  grid-column: span 6;
}
.card:nth-child(2) {
  grid-column: span 6;
}
.card:nth-child(3) {
  grid-column: span 6;
}
.card:nth-child(4) {
  grid-column: span 6;
}

.card-header {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 8px;
}

.card-header h2 {
  margin: 0;
  font-size: 16px;
}

.card-hint {
  color: var(--muted);
  font-size: 12px;
}

.chart {
  width: 100%;
  height: 320px;
  background: rgba(0, 0, 0, 0.12);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 12px;
  position: relative;
}

.donut-wrap {
  height: 320px;
}

.legend {
  display: flex;
  flex-wrap: wrap;
  gap: 8px 12px;
  padding: 10px 2px 2px;
  color: var(--muted);
  font-size: 12px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.swatch {
  width: 10px;
  height: 10px;
  border-radius: 3px;
  background: var(--accent);
  display: inline-block;
}

.heatmap-footer {
  margin-top: 8px;
  color: var(--muted);
  font-size: 12px;
}

.footer {
  max-width: 1200px;
  margin: 0 auto;
  padding: 8px 22px 24px;
  color: var(--muted);
  font-size: 12px;
}

code {
  padding: 2px 6px;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid rgba(255, 255, 255, 0.08);
}

@media (max-width: 980px) {
  .card {
    grid-column: span 12;
  }
  .meta {
    min-width: auto;
  }
}
```

---

## ✅ script.js

```js
// ==============================
// Mock data (edite conforme necessário)
// ==============================
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
```

---

## Como usar

1. Garanta que `index.html`, `style.css` e `script.js` estão no mesmo diretório.
2. Abra o `index.html` no navegador.
3. Edite os dados no início do `script.js`.

---

## Observação

- O D3 é carregado via CDN.
- Não depende de React/Node; é página estática.
- Os gráficos são: **bar**, **line+area**, **donut** e **heatmap**.
