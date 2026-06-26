function PageHeader({ title, subtitle, children }) {
  return (
    <header className="header">
      <div>
        <h2>{title}</h2>
        <p>{subtitle}</p>
      </div>

      <div className="header-actions">
        {children}
      </div>
    </header>
  );
}

export default PageHeader;