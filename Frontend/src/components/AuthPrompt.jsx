import { Link } from "react-router-dom";

function AuthPrompt({ onClose }) {
  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="auth-modal" onClick={(e) => e.stopPropagation()}>
        <button className="close-button" onClick={onClose}>
          ✕
        </button>

        <h3>Receba alertas personalizados</h3>

        <p>
          Faça login ou crie uma conta para receber notificações sobre novas
          notícias e atualizações do VeritasIA.
        </p>

        <div className="auth-modal-actions">
          <Link to="/login">Entrar</Link>

          <Link to="/login" className="primary">
            Cadastrar
          </Link>

          <button onClick={onClose}>Continuar sem cadastro</button>
        </div>
      </div>
    </div>
  );
}

export default AuthPrompt;
