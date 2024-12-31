import os
from PIL import Image

def recortar_imagens(pasta_origem, pasta_destino):
    # Cria a pasta de destino, se não existir
    if not os.path.exists(pasta_destino):
        os.makedirs(pasta_destino)

    # Percorre os arquivos na pasta de origem
    for arquivo in os.listdir(pasta_origem):
        caminho_arquivo = os.path.join(pasta_origem, arquivo)

        # Verifica se é uma imagem suportada
        if arquivo.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            try:
                # Abre a imagem
                imagem = Image.open(caminho_arquivo)

                # Obtém as dimensões da imagem
                largura, altura = imagem.size

                # Verifica se a largura da imagem é maior ou igual a 40 pixels
                if largura >= 50:
                    # Recorta os primeiros 40 pixels da esquerda
                    area_recorte = (0, 0, 50, altura)  # (esquerda, topo, direita, base)
                    imagem_recortada = imagem.crop(area_recorte)

                    # Salva a imagem recortada na pasta de destino
                    caminho_destino = os.path.join(pasta_destino, arquivo)
                    imagem_recortada.save(caminho_destino)

                    print(f"Imagem recortada e salva: {caminho_destino}")
                else:
                    print(f"Ignorado: {arquivo} (largura menor que 40 pixels)")
            except Exception as e:
                print(f"Erro ao processar {arquivo}: {e}")
        else:
            print(f"Ignorado (não é uma imagem): {arquivo}")

# Caminhos para a pasta de origem e destino
pasta_origem = "E:\Programacao\Python\Finished\PokeView\icons"  # Substitua pelo caminho da pasta com as imagens
pasta_destino = "E:\Programacao\Python\Finished\PokeView\iconsCORTADOS"  # Substitua pelo caminho da pasta onde salvar os recortes

# Chama a função para processar as imagens
recortar_imagens(pasta_origem, pasta_destino)