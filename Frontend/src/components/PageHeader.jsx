/**
 * ============================================================================
 * Componente: PageHeader
 * ----------------------------------------------------------------------------
 * Cabeçalho reutilizável utilizado pelas páginas
 * principais da aplicação.
 *
 * Props:
 * - title: título principal.
 * - subtitle: descrição da página.
 * - children: elementos adicionais como botões,
 *   filtros ou ações.
 * ============================================================================
 */

/**
 * children permite que cada página personalize
 * as ações exibidas no lado direito do cabeçalho,
 * mantendo um layout consistente.
 */

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