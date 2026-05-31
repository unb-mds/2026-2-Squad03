function StatCard({ title, value, description }) {
  return (
    <div className="card">
      <p>{title}</p>
      <h3>{value}</h3>
      <span>{description}</span>
    </div>
  );
}

export default StatCard;