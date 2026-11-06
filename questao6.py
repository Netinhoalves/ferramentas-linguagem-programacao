# Questão 6 - Cálculo de Horas Trabalhadas

# datetime trabalha com datas e horários, e timedelta representa uma duração de tempo.
from datetime import datetime, timedelta

EXEMPLO = ["08:00;12:00", "13:30;17:45", "22:00;06:00"]


def ler_turnos():
    print("Digite um turno por linha, no formato hh:mm;hh:mm (linha vazia para terminar).")
    print("Se der Enter logo de início, o programa usa o exemplo do enunciado.")
    linhas = []
    while True:
        try:
            linha = input().strip()
        except EOFError:
            break
        if not linha:
            break
        linhas.append(linha)
    return linhas or EXEMPLO


def duracao_do_turno(linha):
    entrada_texto, saida_texto = linha.split(";")
    # strptime transforma "hh:mm" em um horário e gera ValueError em casos como 25:10 ou 8h30.
    entrada = datetime.strptime(entrada_texto.strip(), "%H:%M")
    saida = datetime.strptime(saida_texto.strip(), "%H:%M")
    # Saída menor que a entrada: ela pertence ao dia seguinte, então soma um dia com timedelta.
    if saida < entrada:
        saida += timedelta(days=1)
    # Subtrair dois horários gera um timedelta com a duração do turno.
    return saida - entrada


def formatar_duracao(duracao):
    # Dividir um timedelta por outro com // diz quantas vezes o segundo cabe no primeiro,
    # e % dá o que sobra. Assim as contas ficam com a biblioteca, sem converter na mão.
    horas = duracao // timedelta(hours=1)
    minutos = (duracao % timedelta(hours=1)) // timedelta(minutes=1)
    return f"{horas}h{minutos:02d}min"


def main():
    linhas = ler_turnos()
    print()

    total = timedelta()
    for numero, linha in enumerate(linhas, start=1):
        try:
            duracao = duracao_do_turno(linha)
        except ValueError:  # horário inválido ou linha sem os dois horários
            print(f"Linha {numero}: horário em formato inválido ({linha})")
            continue
        print(f"Turno {numero}: {formatar_duracao(duracao)}")
        total += duracao

    print(f"Total: {formatar_duracao(total)}")


if __name__ == "__main__":
    main()
