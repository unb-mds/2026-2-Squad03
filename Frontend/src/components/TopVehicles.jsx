function TopVehicles() {
  const vehicles = [
    { name: "G1", value: 312, percent: "95%" },
    { name: "UOL", value: 201, percent: "75%" },
    { name: "Folha de S.Paulo", value: 178, percent: "60%" },
  ];

  return (
    <div className="vehicle-list">
      {vehicles.map((vehicle, index) => (
        <div key={index}>
          <span>{vehicle.name}</span>
          <div className="bar">
            <div style={{ width: vehicle.percent }}></div>
          </div>
          <strong>{vehicle.value}</strong>
        </div>
      ))}
    </div>
  );
}

export default TopVehicles;
