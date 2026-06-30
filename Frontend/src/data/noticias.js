/**
 * ============================================================================
 * Arquivo: noticias.js
 * ----------------------------------------------------------------------------
 * Base de dados utilizada durante o desenvolvimento
 * da aplicação.
 *
 * Objetivo:
 * - Simular notícias antes da integração completa
 *   com o backend.
 *
 * Observação:
 * Em ambiente de produção, os dados são obtidos
 * através da API do VeritasIA.
 * ============================================================================
 */

/**
 * Lista de notícias simuladas.
 *
 * Cada objeto representa uma notícia contendo
 * informações utilizadas pelas páginas de listagem,
 * detalhes e mapa.
 */

export const noticias = [
  {
    id: 1,
    titulo: "Mulher é morta a facadas pelo ex-companheiro em SP",

    categoria: "Feminicídio",

    resumo:
      "Uma mulher foi vítima de feminicídio na zona leste de São Paulo. O suspeito foi preso em flagrante após o crime.",

    conteudo: `Na manhã desta segunda-feira uma mulher foi morta a facadas pelo ex-companheiro em São Paulo.

Segundo informações da Polícia Civil, o suspeito aguardou a vítima sair de casa e iniciou as agressões em via pública.

Testemunhas acionaram a Polícia Militar e o SAMU, porém a vítima não resistiu aos ferimentos.

O agressor foi localizado poucas horas depois e encaminhado para a delegacia responsável.

O caso segue sendo investigado pelas autoridades.`,

    imagem: "/images/noticia-placeholder.jpg",
    fonte: "G1",
    data: "12/05/2026",
    estado: "SP",
    cidade: "São Paulo",
    posicao: [-23.5505, -46.6333],
    local: "São Paulo - SP",
    status: "Verificado",
    link: "https://g1.globo.com/",
    conteudoSensivel: true,
    tipo:"violencia"
    
  },

  {
    id: 2,
    titulo: "Feminicídio: mulher é assassinada dentro de casa em BH",
    resumo:
      "Crime ocorreu durante a madrugada e está sendo investigado pela Polícia Civil.",

    conteudo:
      "Conteúdo de exemplo da notícia. Posteriormente esses dados virão da API.",

    imagem: "/images/noticia-placeholder.jpg",
    fonte: "UOL",
    data: "11/05/2026",
    estado: "MG",
    cidade: "Belo Horizonte",
    posicao: [-19.9167, -43.9345],
    local: "Belo Horizonte - MG",
    categoria: "Feminicídio",
    status: "Em análise",
    link: "https://uol.com.br",
    conteudoSensivel: true,
    tipo:"violencia"
  },

  {
    id: 3,
    titulo: "Polícia prende suspeito de feminicídio no Rio de Janeiro",
    resumo:
      "Suspeito foi localizado poucas horas após o crime.",

    conteudo:
      "Conteúdo de exemplo da notícia.",

    imagem: "/images/noticia-placeholder.jpg",
    fonte: "Metrópoles",
    data: "11/05/2026",
    estado: "RJ",
    cidade: "Rio de Janeiro",
    posicao: [-22.9068, -43.1729],
    local: "Rio de Janeiro - RJ",
    categoria: "Prisão",
    status: "Verificado",
    link: "https://metropoles.com",
    conteudoSensivel: false,
    tipo:"outros"
  },
];