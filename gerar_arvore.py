# gerar_arvore.py
from pathlib import Path

# Configuração: Pastas que NUNCA devem aparecer na documentação
PASTAS_IGNORADAS = {'.git', '.venv', 'node_modules', '__pycache__', '.next', '.pytest_cache'}

def mapear_diretorio(diretorio, prefixo=""):
    arquivos = sorted(list(diretorio.iterdir()), key=lambda x: (x.is_file(), x.name.lower()))
    # Filtra as pastas ignoradas
    arquivos = [f for f in arquivos if f.name not in PASTAS_IGNORADAS]
    
    for i, caminho in enumerate(arquivos):
        eh_ultimo = (i == len(arquivos) - 1)
        sinalizador = "└── " if eh_ultimo else "├── "
        
        # Printa o item atual
        print(f"{prefixo}{sinalizador}{caminho.name}")
        
        # Se for um diretório, faz a busca recursiva dentro dele
        if caminho.is_dir():
            proximo_prefixo = prefixo + ("    " if eh_ultimo else "│   ")
            mapear_diretorio(caminho, proximo_prefixo)

if __name__ == "__main__":
    raiz = Path(__file__).parent
    print(f"📁 {raiz.name}")
    mapear_diretorio(raiz)