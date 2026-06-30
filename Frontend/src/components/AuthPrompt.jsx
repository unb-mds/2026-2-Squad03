/**
 ============================================================================
 Componente: AuthPrompt
 ----------------------------------------------------------------------------
 Modal responsável por incentivar a autenticação do usuário.

 Funcionalidades:
 - Permite acessar a página de login.
 - Permite acessar a tela de cadastro.
 - Possibilita continuar utilizando o sistema sem autenticação.

 Props:
 - onClose: função responsável por fechar o modal.
 ============================================================================
 */

/* Overlay responsável por fechar o modal ao clicar fora dele. */

/* Impede que cliques dentro do modal fechem a janela. */

/* Fecha o modal mantendo o usuário na página atual. */

/* Opções de autenticação disponíveis para o usuário. */

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

        {/* Disclaimer de funcionalidade */}
        <div style={{ 
          backgroundColor: "#fff3cd", 
          padding: "10px", 
          borderRadius: "5px", 
          marginBottom: "15px", 
          border: "1px solid #ffeeba",
          fontSize: "0.85rem",
          color: "#856404",
          textAlign: "center"
        }}>
          ⚠️ <strong>Aviso:</strong> A função de cadastro ainda não está implementada.
        </div>

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