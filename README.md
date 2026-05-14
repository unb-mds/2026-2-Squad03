<img width="2537" height="700" alt="LogoBlack" src="https://github.com/user-attachments/assets/f248a533-c998-46bd-97e2-1c97a966a261" />
---
# Sobre o Projeto
<p style="text-align: justify;">
Este projeto tem como objetivo reunir, analisar e divulgar dados e estatísticas sobre casos de feminicídio no Brasil, oferecendo uma visão clara e fundamentada sobre a realidade da violência contra a mulher no país. A partir de informações atualizadas e notícias provenientes de canais oficiais e veículos de comunicação confiáveis, buscamos transformar números em consciência, promovendo informação de qualidade e acessível à sociedade.
</p>
<p style="text-align: justify;">
Mais do que apresentar dados, o projeto se propõe a dar visibilidade a uma problemática urgente, incentivando o debate, a reflexão e a conscientização. Ao centralizar essas informações em um único espaço, pretendemos contribuir para o entendimento da dimensão do feminicídio no Brasil e reforçar a importância de ações de prevenção e combate a esse tipo de violência.
</p>

---

# Tecnologias Utilizadas

[Figma](https://www.figma.com/board/TERK5u1cdCHQBJgRb3m2x5/Squad-03?node-id=0-1&p=f&t=VAcCgipTLYa9FQ6e-0)

Frontend

- React

Backend

- Scrapy
- LangChain
- Playwright
- FastAPI

Banco de Dados

---

# Portais de Noticias escolhidos

- G1
- Metropoles
- R7

---

# Squad 03

- [Christian](https://github.com/christianrolim)
- [Daniel](https://github.com/Daniel241025)
- [Danilo](https://github.com/danilofns)
- [Henrique](https://github.com/SchneiderCode1)
- [Jadson](https://github.com/jadsonRleandro)
- [Vitor](https://github.com/TheBagomes)

---

# Como Executar o Backend (Ambiente de Desenvolvimento/Testes)

> ⚠️ **ATENÇÃO CRUCIAL PARA A EQUIPE:** Devido ao mapeamento estático e fixo dos caminhos do Frontend (`../../FrontEnd/app/static`), o servidor do Uvicorn **DEVE** ser executado obrigatoriamente de dentro do diretório interno `BackEnd/app`. 
>
> Se você tentar rodar o comando a partir da raiz do repositório ou de outra pasta, o FastAPI não localizará os arquivos de estilo (CSS) e scripts (JS), renderizando uma página em HTML puro ou disparando um erro de inicialização (`RuntimeError`).

# Passo a Passo para Execução:

1. Abra o seu terminal na raiz do repositório principal (`2026-2-VeritasIA`).
2. Navegue diretamente para a pasta interna onde está localizado o arquivo `main.py`:
   ```bash
   cd BackEnd/app