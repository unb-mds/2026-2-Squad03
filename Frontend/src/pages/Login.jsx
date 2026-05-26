import { useState } from "react";
import { Link } from "react-router-dom";
import "../App.css";

function Login() {
  const [isRegister, setIsRegister] = useState(false);

  return (
    <main className="auth-container">
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

            <a href="#">Esqueceu sua senha?</a>

            <button type="button">Entrar</button>

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
