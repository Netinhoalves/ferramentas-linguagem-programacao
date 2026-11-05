# Questão 5 - Tratamento de Strings

# re é a biblioteca de expressões regulares.
# unicodedata traz funções para lidar com os caracteres e seus acentos.
import re
import unicodedata

PALAVRAS_MINUSCULAS = ["de", "da", "do", "das", "dos", "e"]


def titulo(texto):
    # split() sem argumento separa as palavras e já descarta os espaços que sobram.
    palavras = texto.split()
    resultado = []
    # enumerate devolve a posição junto com a palavra, para saber qual é a primeira.
    for posicao, palavra in enumerate(palavras):
        if posicao > 0 and palavra.lower() in PALAVRAS_MINUSCULAS:
            resultado.append(palavra.lower())
        else:
            # capitalize() deixa a primeira letra maiúscula e as demais minúsculas.
            resultado.append(palavra.capitalize())
    # join junta a lista em um texto só, com um espaço entre as palavras.
    return " ".join(resultado)


def remover_acentos(texto):
    # A forma NFD separa cada letra do seu acento: "á" vira "a" + acento.
    decomposto = unicodedata.normalize("NFD", texto)
    # combining() dá diferente de zero para os acentos, então eles ficam de fora.
    return "".join(caractere for caractere in decomposto if not unicodedata.combining(caractere))


def slug(texto):
    sem_acentos = remover_acentos(texto).lower()
    # re.sub troca cada sequência de caracteres que não são letras nem números por um hífen.
    # Assim a pontuação também sai, porque ela não combina com uma URL.
    # strip tira os hífens que sobrarem nas pontas.
    return re.sub(r"[^a-z0-9]+", "-", sem_acentos).strip("-")


def palindromo(texto):
    sem_acentos = remover_acentos(texto).lower()
    # isalnum() é verdadeiro só para letras e números, o que descarta espaços e pontuação.
    letras = "".join(caractere for caractere in sem_acentos if caractere.isalnum())
    # [::-1] inverte o texto. Um texto sem nenhuma letra não conta como palíndromo.
    return letras != "" and letras == letras[::-1]


def main():
    for texto in [" ANÁLISE e desenvolvimento DE sistemas ", "DE volta   PARA casa", "  maria DAS dores  "]:
        print(f'titulo("{texto}")')
        print(f"-> {titulo(texto)}\n")

    for texto in ["Análise e Desenvolvimento de Sistemas", "Programação em Python 3", "  Olá,   Mundo!  "]:
        print(f'slug("{texto}")')
        print(f"-> {slug(texto)}\n")

    for texto in ["Socorram-me, subi no ônibus em Marrocos", "A base do teto desaba", "Olá, mundo"]:
        print(f'palindromo("{texto}")')
        print(f"-> {'verdadeiro' if palindromo(texto) else 'falso'}\n")


if __name__ == "__main__":
    main()
