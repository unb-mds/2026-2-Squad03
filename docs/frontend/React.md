# Frontend

O frontend do **VeritasIA** foi desenvolvido utilizando **React** com **Vite**, proporcionando uma aplicação moderna, rápida e organizada. A interface foi construída de forma componentizada, facilitando a manutenção, reutilização de código e evolução do sistema.

Além do React, o projeto utiliza diversas bibliotecas para atender às necessidades específicas da aplicação, como navegação entre páginas, visualização de mapas, gráficos estatísticos e estilização da interface.

---

# React

O **React** é uma biblioteca JavaScript desenvolvida pela Meta (Facebook) para construção de interfaces de usuário baseadas em componentes.

No VeritasIA, o React foi escolhido por permitir o desenvolvimento de uma interface dinâmica, reutilizável e de fácil manutenção, além de possibilitar atualizações eficientes da tela sem necessidade de recarregar toda a aplicação.

Sua arquitetura baseada em componentes facilita a divisão da interface em pequenas partes independentes, tornando o desenvolvimento mais organizado.

## Componentização

A interface do sistema foi dividida em componentes reutilizáveis, como:

- Barra lateral de navegação;
- Cabeçalho;
- Cards de notícias;
- Gráficos estatísticos;
- Mapa interativo;
- Filtros de pesquisa;
- Listagem de notícias.

Essa abordagem reduz duplicação de código e facilita futuras modificações.

---

## Virtual DOM

O React utiliza o **Virtual DOM**, uma representação virtual da interface.

Quando alguma informação é alterada, o React compara o estado anterior com o novo estado e atualiza apenas os elementos modificados, aumentando significativamente o desempenho da aplicação.

Esse processo reduz renderizações desnecessárias e melhora a experiência do usuário.

---

## JSX

O React utiliza **JSX (JavaScript XML)**, uma sintaxe que permite escrever estruturas semelhantes ao HTML dentro do JavaScript.

Exemplo:

```jsx
function Botao() {
  return <button>Pesquisar</button>;
}
```

O JSX é convertido para JavaScript durante o processo de compilação realizado pelo Vite e pelo Babel.

---

# Vite

O projeto utiliza **Vite** como ferramenta de desenvolvimento e build.

O Vite oferece diversas vantagens em relação a ferramentas tradicionais:

- Inicialização extremamente rápida;
- Atualização instantânea durante o desenvolvimento (Hot Module Replacement);
- Build otimizada para produção;
- Configuração simples;
- Excelente integração com React.

Sua utilização reduz significativamente o tempo de desenvolvimento e melhora a produtividade da equipe.

---

# React Router DOM

Para gerenciar a navegação entre as páginas da aplicação foi utilizado o **React Router DOM**.

Ele permite criar uma aplicação do tipo **SPA (Single Page Application)**, onde a navegação ocorre sem recarregar toda a página.

As principais rotas da aplicação incluem:

- Dashboard;
- Mapa;
- Notícias;
- Sobre Nós;
- Página de detalhes da notícia.

Essa abordagem proporciona uma navegação mais fluida e melhora a experiência do usuário.

---

# React Leaflet

A funcionalidade de visualização geográfica foi implementada utilizando **React Leaflet**, biblioteca baseada no Leaflet para aplicações React.

Ela permite:

- Exibir mapas interativos;
- Posicionar marcadores;
- Visualizar regiões do Brasil;
- Implementar mapas de calor (Heatmap).

Essa biblioteca é responsável pela funcionalidade de análise espacial das notícias presentes no sistema.

---

# Recharts

Para apresentar os indicadores estatísticos foi utilizada a biblioteca **Recharts**.

Ela possibilita a criação de gráficos responsivos de forma simples, incluindo:

- Evolução temporal das notícias;
- Distribuição por estados;
- Notícias por região;
- Comparações estatísticas.

Os gráficos são totalmente integrados aos componentes React, facilitando sua atualização conforme os dados são alterados.

---

# Tailwind CSS

A estilização da aplicação foi desenvolvida utilizando **Tailwind CSS**.

O framework fornece classes utilitárias que permitem construir interfaces modernas sem necessidade de escrever grandes arquivos CSS.

Entre suas vantagens destacam-se:

- Desenvolvimento mais rápido;
- Padronização visual;
- Responsividade;
- Fácil manutenção;
- Reutilização de estilos.

---

# Organização do Projeto

O frontend segue uma estrutura organizada em módulos.

```text
src/
│
├── assets/
├── components/
├── pages/
├── services/
├── utils/
├── App.jsx
└── main.jsx
```

Essa organização facilita a separação das responsabilidades e torna o projeto mais escalável.

---

# Principais Tecnologias Utilizadas

| Tecnologia       | Finalidade                          |
| ---------------- | ----------------------------------- |
| React            | Construção da interface             |
| Vite             | Ambiente de desenvolvimento e build |
| React Router DOM | Navegação entre páginas             |
| React Leaflet    | Mapas interativos                   |
| Recharts         | Gráficos estatísticos               |
| Tailwind CSS     | Estilização da interface            |

---

# Conclusão

A arquitetura do frontend foi construída utilizando tecnologias modernas do ecossistema React, proporcionando uma aplicação rápida, organizada e de fácil manutenção.

A combinação entre React, Vite, React Router DOM, React Leaflet, Recharts e Tailwind CSS permite que o VeritasIA ofereça uma interface responsiva, intuitiva e eficiente para visualização e análise das notícias monitoradas.
