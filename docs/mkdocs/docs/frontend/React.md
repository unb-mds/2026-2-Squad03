# React
é uma biblioteca mas na prática atua como framework quando utilizado com outras ferramentas, é uma biblioteca JavaScript criada pelo Meta (antigo Facebook) e também utilizado no Instagram, e em aplicativos como a Netflix para construir interfaces de usuário, principalmente para aplicações web. (É importante entender que o react é uma biblioteca pois assim temos em mente que podemos e em determinados momentos vamos precisar de outras bibliotecas que possam nos ajudar ao utilizar o react) 

O React serve para criar telas interativas e tem a praticidade de mudar e fazer atualizações de forma mais prática pois utiliza do conceito de "Componentes": 
Um componente é como um “bloco” da interface.
Exemplo:
-botão
-menu
-card de produto
-barra de navegação
Você monta a aplicação juntando esses blocos.

Podemos utilizar quando utilizamos os componentes por classes ou por função, a partir da versão 16.8 quando usamos com classes podemos ter acesso a  funcionalidades como hooks e estados. (as duas vão funcionar de forma igual para o usuário, então varia mais do gosto de cada desenvolvedor)

### Componetização

1. Componetização

Você divide a interface em partes reutilizáveis.

2. Virtual DOM

React cria uma versão “virtual” da tela para atualizar só o que mudou → deixa tudo mais rápido.

3. JSX

É uma forma de escrever HTML dentro do JavaScript: 

### O que é Virtual DOM?
O Virtual DOM é uma cópia virtual da tela (DOM real).

Como funciona:
DOM real (normal)

Sem React:

Qualquer mudança → atualiza a página inteira ou partes pesadas
Isso é lento
Com Virtual DOM (React)

React faz assim:

- Cria uma cópia da interface na memória (Virtual DOM)
- Quando algo muda:
- compara o antes vs depois (diff)
- Atualiza só o que mudou de verdade

Exemplo simples:

Imagina uma lista com 100 itens.

 Você muda só 1 item

Sem React: pode reprocessar tudo 
Com React: atualiza só aquele item 
Dentro do React usamos **O Babel** que é um compilador de JavaScript.

Pra que ele serve?

Ele “traduz” código moderno para código que o navegador entende.

Exemplo:

Você escreve isso (JSX do React):

`const elemento = <h1>Olá</h1>;`

O Babel transforma em algo assim:

`const elemento = React.createElement("h1", null, "Olá");`

 Ou seja:

Navegador não entende JSX
Babel converte JSX em JavaScript puro
 
Fluxo simplificado:

- Você escreve código React (JSX)
- Babel traduz esse código
- React usa o Virtual DOM
- Só atualiza o necessário na tela_ 

### Next.js

_Framework moderno baseado em React, focado em performance, escalabilidade e melhor experiência de desenvolvimento.

---

Sobre
O Next.js é um framework desenvolvido pela Vercel, criado para suprir limitações do React puro, principalmente em SEO, renderização e estrutura de aplicações.

---

### Principais Features

- Framework baseado em React
- Alta escalabilidade
- Sistema de roteamento automático
- Server-Side Rendering (SSR) com Node.js
- Renderização híbrida (cliente + servidor)
- Pré-renderização para melhor performance
- Code Splitting automático
- Roteamento do lado do cliente
- Suporte a CSS, Sass e CSS-in-JS
- Fast Refresh no desenvolvimento
- API Routes (backend integrado)
- Totalmente extensível

---

### Arquitetura
Construção isomórfica: combina renderização no cliente e no servidor ao mesmo tempo.

---

### Casos de Sucesso
Empresas que utilizam Next.js:

- Docker
- Twitch
- Nubank
- Uber
- Netflix
- GitHub
- 

---

### Desvantagens

- Algumas bibliotecas exigem configuração extra (ex: Redux, Styled Components)
- Dependência do ambiente Node.js
- Alto tráfego pode exigir mais carga de servidor
- Necessita mais atenção na arquitetura

---
### Conclusão
O Next.js é uma evolução do React que resolve problemas reais de desenvolvimento moderno, oferecendo melhor performance, SEO e organização. Apesar de exigir mais cuidado técnico, é uma das melhores opções para aplicações web escaláveis.

---

Pesquisa feita por Daniel Rodrigues e Vitor Barreto Gomes_