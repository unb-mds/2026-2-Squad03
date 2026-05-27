import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import "../App.css";

function Login() {
  const [isRegister, setIsRegister] = useState(false);
  const [formData, setFormData] = useState({ email: "", senha: "", nome: "" });
  const navigate = useNavigate();

  // Esta função atualiza o estado conforme o usuário digita
  const handleInputChange = (e) => {
    // e.target.name pega o atributo 'name' do input
    // e.target.value pega o texto que o usuário digitou
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleAuth = async (e) => {
    e.preventDefault(); 

    const url = isRegister 
      ? "http://localhost:8000/api/auth/register" 
      : "http://localhost:8000/api/auth/login";

    try {
      const response = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData), 
      });

      const data = await response.json();

      if (response.ok) {
        alert(isRegister ? "Cadastro realizado!" : "Login bem-sucedido!");
        if (!isRegister) navigate("/dashboard");
      } else {
        alert("Erro: " + (data.detail || "Falha na requisição"));
      }
    } catch (error) {
      alert("Não foi possível conectar ao back-end.");
    }
  };

  return (
    <main className="auth-container">
      <section className={`login-card ${isRegister ? "active" : ""}`}>
        
        {/* Formulário de Registro */}
        <div className="form-container register-form">
          <form onSubmit={handleAuth}>
            <h1>Criar Conta</h1>
            {/* Adicionamos name e onChange para cada input */}
            <input name="nome" type="text" placeholder="Nome" onChange={handleInputChange} />
            <input name="email" type="email" placeholder="Email" onChange={handleInputChange} />
            <input name="senha" type="password" placeholder="Senha" onChange={handleInputChange} />
            <button type="submit">Criar Conta</button>
          </form>
        </div>

        {/* Formulário de Login */}
        <div className="form-container login-form">
          <form onSubmit={handleAuth}>
            <h1>Acesse sua conta</h1>
            <input name="email" type="email" placeholder="Email" onChange={handleInputChange} />
            <input name="senha" type="password" placeholder="Senha" onChange={handleInputChange} />
            <a href="#">Esqueceu sua senha?</a>
            <button type="submit">Entrar</button>
          </form>
        </div>

        {/* Painéis laterais permanecem iguais */}


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

