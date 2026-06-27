"""
Adaptador de repositório baseado em arquivos JSON.

Este módulo fornece uma implementação simples de repositório que utiliza arquivos 
JSON locais como armazenamento persistente. É ideal para ambientes de desenvolvimento, 
testes locais ou cenários onde um banco de dados completo (como PostgreSQL) ainda 
não está disponível ou não é necessário.
"""

import json
import os

#+-------------------------------------------++-------------------------------------------++-------------------------------------------+

# Definindo os nomes dos arquivos na raiz do banco
ARQUIVO_LOCAIS = "banco_locais.json"
"""Nome do arquivo JSON utilizado para persistir os dados de locais/regiões."""

ARQUIVO_USUARIOS = "banco_usuarios.json"
"""Nome do arquivo JSON utilizado para persistir os dados de usuários."""

class JsonRepositoryAdapter:
    """
    Classe adaptadora para manipulação de dados em arquivos JSON.

    Encapsula as operações de leitura e escrita em arquivos `.json`, atuando 
    como um banco de dados em memória persistido em disco. Contém métodos 
    para salvar e listar dados de locais e usuários.
    """
    
    # --- MÉTODOS PARA LOCAIS ---
    def salvar_local(self, regiao) -> bool:
        """
        Salva uma nova região/local no arquivo JSON correspondente.

        Lê o estado atual do arquivo de locais, gera um ID sequencial baseado 
        no tamanho da lista existente e adiciona o novo registro.

        Args:
            regiao (Any): Objeto representando a região. Espera-se que possua os 
                atributos `nome`, `latitude` e `longitude`.

        Returns:
            bool: Retorna True após a operação de escrita ser concluída com sucesso.
        """
        dados = self._ler(ARQUIVO_LOCAIS)
        # Adiciona um ID baseado no tamanho da lista
        dados.append({
            "id": len(dados) + 1, 
            "nome": regiao.nome, 
            "latitude": regiao.latitude, 
            "longitude": regiao.longitude
        })
        self._escrever(ARQUIVO_LOCAIS, dados)
        return True
    
#+-------------------------------------------++-------------------------------------------++-------------------------------------------+

    def listar_todas(self) -> list:
        """
        Recupera todos os locais armazenados.

        Returns:
            list: Uma lista de dicionários contendo os dados de todos os locais salvos.
        """
        return self._ler(ARQUIVO_LOCAIS)

#+-------------------------------------------++-------------------------------------------++-------------------------------------------+

    # --- MÉTODOS PARA USUÁRIOS ---
    def salvar_usuario(self, user_data: dict) -> bool:
        """
        Salva um novo usuário no arquivo JSON, prevenindo duplicatas.

        Lê o arquivo de usuários e verifica se já existe um registro com o mesmo
        email fornecido. Se existir, a inserção é bloqueada. Caso contrário, 
        o usuário é adicionado à lista e salvo no disco.

        Args:
            user_data (dict): Dicionário contendo os dados do usuário a ser salvo.
                Deve conter obrigatoriamente a chave 'email'.

        Returns:
            bool: Retorna True se o usuário foi salvo com sucesso, ou False se o 
                email já estiver cadastrado (duplicata).
        """
        dados = self._ler(ARQUIVO_USUARIOS)
        # Verifica se o usuário já existe para evitar duplicatas (opcional)
        if any(u['email'] == user_data['email'] for u in dados):
            return False 
        
        dados.append(user_data)
        self._escrever(ARQUIVO_USUARIOS, dados)
        return True
    
#+-------------------------------------------++-------------------------------------------++-------------------------------------------+

    # --- MÉTODOS DE APOIO (PRIVADOS) ---
    def _ler(self, arquivo: str) -> list:
        """
        Lê e decodifica o conteúdo de um arquivo JSON.

        Args:
            arquivo (str): O nome ou caminho do arquivo JSON a ser lido.

        Returns:
            list: A lista de dicionários lida do arquivo, ou uma lista vazia `[]` 
                caso o arquivo não exista ou o JSON seja inválido.
        """
        if not os.path.exists(arquivo):
            return []
        try:
            with open(arquivo, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []

#+-------------------------------------------++-------------------------------------------++-------------------------------------------+

    def _escrever(self, arquivo: str, dados: list) -> None:
        """
        Escreve uma lista de dados formatados em um arquivo JSON.

        Utiliza indentação de 4 espaços e garante o suporte adequado a 
        caracteres especiais (UTF-8) desativando o `ensure_ascii`.

        Args:
            arquivo (str): O nome ou caminho do arquivo JSON de destino.
            dados (list): Lista contendo os dados a serem serializados e salvos.
        """
        with open(arquivo, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)
            
#+-------------------------------------------++-------------------------------------------++-------------------------------------------+