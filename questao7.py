# Questão 7 - Estatística com Biblioteca Matemática

# statistics traz funções prontas de estatística.
# math traz os arredondamentos para cima e para baixo.
import math
import statistics

TEMPERATURAS = [22.5, 25.0, 19.8, 30.1, 27.4, 24.2, 21.0]

# Diferença entre os desvios-padrão: o populacional é usado quando temos todos os dados
# do grupo, e divide a soma dos quadrados das diferenças para a média por n. O amostral
# é usado quando temos só uma parte do grupo, e divide por n - 1, o que compensa a
# tendência de uma amostra mostrar menos variação do que o grupo inteiro.
#
# A função usada aqui, statistics.stdev, calcula o amostral.
# Para o populacional, a função seria statistics.pstdev.


def formatar(valor):
    return f"{valor:.2f}".replace(".", ",")


def ler_temperaturas():
    try:
        texto = input("Temperaturas separadas por vírgula, como 22.5, 25.0 (Enter usa o vetor do enunciado): ").strip()
    except EOFError:
        texto = ""
    if not texto:
        return TEMPERATURAS

    # float gera ValueError se algum valor não for número.
    valores = [float(parte) for parte in texto.split(",")]
    # O desvio-padrão amostral precisa de pelo menos dois valores, e math.isfinite recusa "inf" e "nan".
    if len(valores) < 2 or not all(math.isfinite(valor) for valor in valores):
        raise ValueError
    return valores


def main():
    try:
        temperaturas = ler_temperaturas()
    except ValueError:
        print("Digite pelo menos dois números separados por vírgula, como 22.5, 25.0.")
        return

    # mean calcula a média, median pega o valor do meio e stdev calcula o desvio-padrão amostral.
    media = statistics.mean(temperaturas)
    mediana = statistics.median(temperaturas)
    desvio = statistics.stdev(temperaturas)
    maior = max(temperaturas)
    menor = min(temperaturas)

    print(f"\nMédia: {formatar(media)}")
    print(f"Mediana: {formatar(mediana)}")
    print(f"Desvio-padrão (amostral): {formatar(desvio)}")
    print(f"Maior: {formatar(maior)} | Menor: {formatar(menor)} | Amplitude: {formatar(maior - menor)}")
    # ceil arredonda para cima e floor arredonda para baixo, sempre para um número inteiro.
    print(f"Média arredondada para cima: {math.ceil(media)} | para baixo: {math.floor(media)}")


if __name__ == "__main__":
    main()
