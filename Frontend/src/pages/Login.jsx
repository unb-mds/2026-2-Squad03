import { useState } from "react";
import { Link } from "react-router-dom";
import logoVeritas from "../assets/logo.png";
import "../App.css";

function Login() {
  const [isRegister, setIsRegister] = useState(false);

  return (
    <main className="auth-container">
      <div className="auth-logo-area">
        <img src={logoVeritas} alt="VeritasIA" />
      </div>
      <section className={`login-card ${isRegister ? "active" : ""}`}>
        <div className="form-container register-form">
          <form>
            <h1>Criar Conta</h1>
            <span>Use seu email para se cadastrar</span>

            <input type="text" placeholder="Nome" />
            <input type="email" placeholder="Email" />
            <input type="password" placeholder="Senha" />

            <button type="button">Criar Conta</button>
          </form>
        </div>

        <div className="form-container login-form">
          <form>
            <h1>Acesse sua conta</h1>
            <span>Entre com suas credenciais para continuar</span>

            <input type="email" placeholder="Email" />
            <input type="password" placeholder="Senha" />

            <div className="login-options">
              <label>
                <input type="checkbox" />
                Lembrar-me
              </label>

              <a href="#">Esqueceu a senha?</a>
            </div>

            <button type="button">Entrar</button>

            <div className="divider">
              <span></span>
              <p>ou</p>
              <span></span>
            </div>

            <button type="button" className="google-button">
              Continuar com Google
            </button>

            <p className="auth-switch-text">
              Não tem uma conta?{" "}
              <button type="button" onClick={() => setIsRegister(true)}>
                Cadastre-se
              </button>
            </p>

            <Link to="/" className="back-link">
              Continuar sem login
            </Link>
          </form>
        </div>

        <div className="toggle-container">
          <div className="toggle">
            <div className="toggle-panel toggle-left">
              <h1>Bem-vindo de volta!</h1>
              <p>Já tem uma conta? Entre agora.</p>
              <button onClick={() => setIsRegister(false)}>Entrar</button>
            </div>

            <div className="toggle-panel toggle-right">
              <h1>Bem-vindo!</h1>
              <p>Cadastre-se para receber alertas e notificações.</p>
              <button onClick={() => setIsRegister(true)}>Cadastre-se</button>
            </div>
          </div>
        </div>
      </section>
    </main>
  );
}

export default Login;
