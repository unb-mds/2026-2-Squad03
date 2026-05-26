function RegionChart() {
  const regions = [
    { name: "Sudeste", value: 420, percent: "90%" },
    { name: "Nordeste", value: 310, percent: "70%" },
    { name: "Sul", value: 210, percent: "50%" },
    { name: "Centro-Oeste", value: 160, percent: "38%" },
    { name: "Norte", value: 120, percent: "28%" },
  ];

  return (
    <div className="region-list">
      {regions.map((region, index) => (
        <div key={index}>
          <span>{region.name}</span>
          <div className="bar">
            <div style={{ width: region.percent }}></div>
          </div>
          <strong>{region.value}</strong>
        </div>
      ))}
    </div>
  );
}

export default RegionChart;
