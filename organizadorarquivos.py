import logging
from pathlib import Path

# Tarefa 3: Categorias globais
categorias = {
    "Imagens": [".jpg", ".jpeg", ".png", ".gif", ".bmp"],
    "PDFs": [".pdf"],
    "Word": [".docx", ".doc"],
    "Excel": [".xlsx", ".xls", ".csv"],
    "Audio": [".mp3", ".wav", ".flac"],
    "Videos": [".mp4", ".mkv", ".avi"],
    "Compactados": [".zip", ".rar", ".7z", ".tar.gz"]
}

# Configuração do Logging (Tarefa 10)
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

def obter_caminho_utilizador():
    """Tarefa 1 & 8: Pede o caminho e valida se a pasta existe."""
    caminho_digitado = input("Insira o caminho da pasta que deseja organizar: ").strip('"')
    pasta = Path(caminho_digitado)
    
    if not pasta.exists() or not pasta.is_dir():
        logging.error(f"O caminho '{caminho_digitado}' não é uma pasta válida!")
        return None
    return pasta

def gerir_conflito(pasta_destino, file):
    """Tarefa 7: Evita sobrepor ficheiros com o mesmo nome."""
    caminho_final_ficheiro = pasta_destino / file.name
    contador = 1
    nome_puro = file.stem      
    sufixo = file.suffix

    while caminho_final_ficheiro.exists():
        novo_nome = f"{nome_puro}_{contador}{sufixo}"
        caminho_final_ficheiro = pasta_destino / novo_nome
        contador += 1
    return caminho_final_ficheiro

def organizar_pasta(caminho_pasta, categorias):
    """Executa a organização e recolhe os dados para as estatísticas."""
    # Dicionário de estatísticas para a Tarefa 11
    estatisticas = {
        "analisados": 0,
        "organizados": 0,
        "outros": 0,
        "erros": 0
    }

    logging.info(f"A iniciar a análise da pasta: {caminho_pasta}")

    for file in caminho_pasta.iterdir():
        if file.is_file():
            estatisticas["analisados"] += 1
            try:
                extensao = file.suffix.lower()
                
                # Tarefa 4: Descobrir a categoria
                categoria_encontrada = "Outros"
                for pasta, extensoes_suportadas in categorias.items():
                    if extensao in extensoes_suportadas:
                        categoria_encontrada = pasta
                        break  
                
                if categoria_encontrada == "Outros":
                    estatisticas["outros"] += 1
                    # Tarefa 10: Registar um Aviso (Warning) para extensões desconhecidas
                    logging.warning(f"Ficheiro '{file.name}' com extensão desconhecida. Vai para 'Outros'.")
                        
                # Tarefa 5: Criar pasta destino
                pasta_destino = caminho_pasta / categoria_encontrada
                pasta_destino.mkdir(parents=True, exist_ok=True)  
                
                # Tarefa 7: Gerir conflitos de nomes
                caminho_final = gerir_conflito(pasta_destino, file)
                
                # Tarefa 6: Mover o ficheiro
                file.rename(caminho_final)
                estatisticas["organizados"] += 1
                
                # Tarefa 10: Registar Informação (Info) de sucesso
                logging.info(f"Movido: {file.name} -> {categoria_encontrada}/{caminho_final.name}")
                
            except Exception as e:
                estatisticas["erros"] += 1
                # Tarefa 10: Registar Erro (Error) se algo falhar
                logging.error(f"Não foi possível mover '{file.name}': {e}")

    return estatisticas

def exibir_relatorio(estatisticas):
    """Tarefa 11: Apresenta o painel final formatado no terminal."""
    print("\n================================")
    print("       FILE ORGANIZER V1.0      ")
    print("================================")
    print(f"Ficheiros analisados: {estatisticas['analisados']}")
    print(f"Ficheiros organizados: {estatisticas['organizados']}")
    print(f"Ficheiros em Outros: {estatisticas['outros']}")
    print(f"Erros encontrados: {estatisticas['erros']}")
    print("================================")
    print("Organização concluída.\n")

if __name__ == "__main__":
    # 1. Pede a pasta ao utilizador
    pasta_alvo = obter_caminho_utilizador()
    
    # 2. Se a pasta for válida, organiza e mostra o relatório
    if pasta_alvo:
        dados_finais = organizar_pasta(pasta_alvo, categorias)
        exibir_relatorio(dados_finais)
