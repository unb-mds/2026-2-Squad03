function StatCard({ title, value, description, icon }) {
  return (
    <div className="card">
      <div className="card-icon">
        {icon}
      </div>

      <p className="card-title">{title}</p>

      <h3 className="card-value">{value}</h3>

      <span className="card-description">
        {description}
      </span>
    </div>
  );
}

export default StatCard;