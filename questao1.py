# Questão 1 - Datas e Prazos

# datetime é a biblioteca de data e hora do Python.
from datetime import datetime

# Os nomes em português ficam em listas porque o strftime depende do locale pt_BR,
# que nem sempre está disponível no computador onde o programa roda.
MESES = [
    "janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho",
    "agosto", "setembro", "outubro", "novembro", "dezembro",
]
DIAS_SEMANA = [
    "segunda-feira", "terça-feira", "quarta-feira", "quinta-feira",
    "sexta-feira", "sábado", "domingo",
]

EXEMPLO_HOJE = "27/10/2026"
EXEMPLO_ATIVIDADES = ["Relatório;05/11/2026", "Prova;20/10/2026", "Seminário;03/12/2026"]


def ler_linha(mensagem=""):
    try:
        return input(mensagem).strip()
    except EOFError:
        return ""


def ler_atividades():
    print("Digite uma atividade por linha, no formato nome;dd/mm/aaaa (linha vazia para terminar):")
    linhas = []
    linha = ler_linha()
    while linha:
        linhas.append(linha)
        linha = ler_linha()
    return linhas


def converter_data(texto):
    # strptime transforma o texto em data seguindo o formato dia/mês/ano.
    # Se a data não existir no calendário (como 31/04/2026), ele gera ValueError.
    return datetime.strptime(texto.strip(), "%d/%m/%Y").date()


def data_por_extenso(data):
    return f"{data.day:02d} de {MESES[data.month - 1]} de {data.year}"


def situacao_do_prazo(data, hoje):
    # Subtrair duas datas gera um timedelta, e .days é a diferença em dias.
    dias = (data - hoje).days
    if dias == 0:
        return "vence hoje"
    if dias == 1:
        return "falta 1 dia"
    if dias > 1:
        return f"faltam {dias} dias"
    if dias == -1:
        return "atrasada há 1 dia"
    return f"atrasada há {-dias} dias"


def mostrar_atividades(linhas, hoje):
    # Alinha a coluna de nomes com base no nome mais comprido da lista.
    largura = max(len(linha.split(";")[0]) for linha in linhas) + 1

    for linha in linhas:
        partes = linha.split(";")
        if len(partes) != 2:
            print(f"Aviso: linha fora do formato nome;dd/mm/aaaa: {linha}")
            continue

        nome, data_texto = partes
        try:
            data = converter_data(data_texto)
        except ValueError:
            print(f"Aviso: data inválida em {nome}: {data_texto}")
            continue

        # weekday() devolve o dia da semana como número: 0 é segunda e 6 é domingo.
        dia_semana = DIAS_SEMANA[data.weekday()]
        print(f"{nome:<{largura}} | {data_por_extenso(data)} | {dia_semana} | {situacao_do_prazo(data, hoje)}")


def main():
    hoje_texto = ler_linha("Data de referência em dd/mm/aaaa (Enter usa o exemplo do enunciado): ")
    usar_exemplo = not hoje_texto

    try:
        hoje = converter_data(EXEMPLO_HOJE if usar_exemplo else hoje_texto)
    except ValueError:
        print(f"Data de referência inválida: {hoje_texto}")
        return

    linhas = EXEMPLO_ATIVIDADES if usar_exemplo else ler_atividades()
    if not linhas:
        print("Nenhuma atividade informada.")
        return

    print()
    mostrar_atividades(linhas, hoje)


if __name__ == "__main__":
    main()
