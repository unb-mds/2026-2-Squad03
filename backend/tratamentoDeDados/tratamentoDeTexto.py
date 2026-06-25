import emoji

#+-------------------------------------------++-------------------------------------------++-------------------------------------------+

def transformar_padrao_data(data_da_publicacao):
    dia_da_publicacao = data_da_publicacao[8:10]
    mes_da_publicacao = data_da_publicacao[5:7]
    ano_da_publicacao = data_da_publicacao[0:4]
    hora_da_publicacao = data_da_publicacao[11:13]
    minuto_da_publicacao = data_da_publicacao[14:16]

    return f"{ano_da_publicacao}-{mes_da_publicacao}-{dia_da_publicacao} {hora_da_publicacao}:{minuto_da_publicacao}:00"

#+-------------------------------------------++-------------------------------------------++-------------------------------------------+

def formatar_texto(texto):
    
    # Remove espaços em branco extras
    texto = ' '.join(texto.split())
    
    # Remove quebras de linha
    texto = texto.replace('\n', ' ')
    
    # Remove tabs
    texto = texto.replace('\t', ' ')
    
    # Remove emojis
    texto = emoji.replace_emoji(texto, replace='')

    return texto

#+-------------------------------------------++-------------------------------------------++-------------------------------------------+

def juntar_texto(alltext):
    news = ' '.join(
    t.strip()
    for t in alltext
        if t.strip() )
    
    return news

#+-------------------------------------------++-------------------------------------------++-------------------------------------------+