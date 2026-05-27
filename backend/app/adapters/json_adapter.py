import json
import os

# Definindo os nomes dos arquivos na raiz do banco
ARQUIVO_LOCAIS = "banco_locais.json"
ARQUIVO_USUARIOS = "banco_usuarios.json"

class JsonRepositoryAdapter:
    
    # --- MÉTODOS PARA LOCAIS ---
    def salvar_local(self, regiao):
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

    def listar_todas(self):
        return self._ler(ARQUIVO_LOCAIS)

    # --- MÉTODOS PARA USUÁRIOS ---
    def salvar_usuario(self, user_data: dict):
        dados = self._ler(ARQUIVO_USUARIOS)
        # Verifica se o usuário já existe para evitar duplicatas (opcional)
        if any(u['email'] == user_data['email'] for u in dados):
            return False 
        
        dados.append(user_data)
        self._escrever(ARQUIVO_USUARIOS, dados)
        return True

    # --- MÉTODOS DE APOIO (PRIVADOS) ---
    def _ler(self, arquivo):
        """Lê o arquivo JSON ou retorna lista vazia se não existir."""
        if not os.path.exists(arquivo):
            return []
        try:
            with open(arquivo, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []

    def _escrever(self, arquivo, dados):
        """Escreve a lista de dados no arquivo JSON com formatação."""
        with open(arquivo, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)