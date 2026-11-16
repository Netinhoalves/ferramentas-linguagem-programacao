# Questão 4 - Biblioteca Matemática: Simulação de Financiamento

# math é a biblioteca matemática do Python.
# re é usada aqui para reconhecer números digitados com ponto de milhar.
import math
import re

EXEMPLO = (10000.0, 1.5, 12)  # valor financiado, taxa mensal em % e número de parcelas

# Por que o saldo do último mês pode não dar exatamente zero se arredondar a cada passo:
# a conta real tem mais de duas casas decimais, e cada arredondamento para centavos deixa
# uma pequena diferença. Essas diferenças vão se acumulando mês a mês. No exemplo do
# enunciado, arredondando os valores todo mês, o saldo terminaria em R$ 0,01 em vez de zero.
#
# Como resolvi: as contas usam os valores completos, e o arredondamento só acontece na hora
# de mostrar. Além disso, no último mês a amortização é o próprio saldo restante, o que
# elimina o resíduo mínimo que sobra porque o computador não guarda todas as casas decimais.


def converter_numero(texto):
    """Aceita números como 10000, 10000.50, 10.000 e 10.000,50."""
    texto = texto.strip()
    if "," in texto:
        texto = texto.replace(".", "").replace(",", ".")
    elif re.fullmatch(r"\d{1,3}(\.\d{3})+", texto):
        texto = texto.replace(".", "")
    return float(texto)


def formatar_moeda(valor):
    # round arredonda para 2 casas decimais, que são os centavos.
    # :,.2f usa o padrão americano (1,234.50); as trocas abaixo invertem a vírgula e o ponto.
    texto = f"{round(valor, 2):,.2f}"
    return texto.replace(",", "X").replace(".", ",").replace("X", ".")


def calcular_parcela(capital, taxa, parcelas):
    # math.pow calcula a potência: (1 + i) elevado a -n.
    denominador = 1 - math.pow(1 + taxa, -parcelas)
    if denominador == 0:  # taxa zero: sem juros, é só dividir o valor pelas parcelas
        return capital / parcelas
    return capital * taxa / denominador


def montar_tabela(capital, taxa, parcelas, parcela):
    tabela = []
    saldo = capital
    for mes in range(1, parcelas + 1):
        juros = saldo * taxa
        if mes == parcelas:
            amortizacao = saldo  # último mês: quita o que sobrou, como explicado no início
        else:
            amortizacao = parcela - juros
        saldo -= amortizacao
        tabela.append((mes, juros, amortizacao, saldo))
    return tabela


def ler_dados():
    try:
        capital_texto = input("Valor financiado em R$ (Enter usa o exemplo do enunciado): ").strip()
    except EOFError:
        capital_texto = ""
    if not capital_texto:
        return EXEMPLO

    capital = converter_numero(capital_texto)
    taxa = converter_numero(input("Taxa mensal em % (ex.: 1,5): "))
    parcelas = int(input("Número de parcelas: "))
    return capital, taxa, parcelas


def main():
    try:
        capital, taxa, parcelas = ler_dados()
    except (ValueError, EOFError):
        print("Valor inválido. Use números, como 10000,00 para o valor, 1,5 para a taxa e 12 para as parcelas.")
        return

    # math.isfinite recusa valores como "inf" e "nan", que o float aceita.
    if not (math.isfinite(capital) and math.isfinite(taxa)) or capital <= 0 or taxa < 0 or parcelas < 1:
        print("O valor precisa ser maior que zero, a taxa não pode ser negativa e deve haver pelo menos 1 parcela.")
        return

    taxa_mensal = taxa / 100
    parcela = calcular_parcela(capital, taxa_mensal, parcelas)
    tabela = montar_tabela(capital, taxa_mensal, parcelas, parcela)

    total_juros = sum(juros for _, juros, _, _ in tabela)
    total_pago = capital + total_juros

    print(f"\nParcela: R$ {formatar_moeda(parcela)}")
    print(f"Total pago: R$ {formatar_moeda(total_pago)}")
    print(f"Total de juros: R$ {formatar_moeda(total_juros)}")

    print(f"\n{'Mês':>3} | {'Juros':>10} | {'Amortização':>11} | {'Saldo':>12}")
    for mes, juros, amortizacao, saldo in tabela:
        print(f"{mes:>3} | {formatar_moeda(juros):>10} | {formatar_moeda(amortizacao):>11} | {formatar_moeda(saldo):>12}")


if __name__ == "__main__":
    main()
