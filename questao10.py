# Questão 10 - Analisador de Log (Integração)

# ipaddress confere se o IP existe de verdade.
# re é a biblioteca de expressões regulares.
# Counter conta quantas vezes cada valor aparece.
# datetime e timedelta trabalham com data, hora e duração.
# pathlib facilita montar o caminho do arquivo.
import ipaddress
import re
from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path

# Path(__file__).parent é a pasta do programa, assim o arquivo é achado de onde ele for executado.
PASTA = Path(__file__).parent

# Cada (?P<nome>...) guarda um pedaço da linha com um nome:
#   ip       quatro números separados por ponto
#   data     dentro de colchetes, no formato dd/mm/aaaa:hh:mm:ss
#   metodo   letras maiúsculas dentro das aspas, como GET ou POST
#   caminho  texto sem espaços, logo depois do método
#   status   três dígitos no fim da linha
REGEX_LINHA = re.compile(
    r"(?P<ip>\d{1,3}(?:\.\d{1,3}){3}) - - "
    r"\[(?P<data>\d{2}/\d{2}/\d{4}:\d{2}:\d{2}:\d{2})\] "
    r'"(?P<metodo>[A-Z]+) (?P<caminho>\S+)" '
    r"(?P<status>\d{3})"
)


def interpretar_linha(linha):
    """Devolve os dados da linha, ou None se ela estiver fora do padrão."""
    # fullmatch exige que a linha inteira siga a expressão.
    encontrado = REGEX_LINHA.fullmatch(linha.strip())
    if encontrado is None:
        return None

    # groupdict devolve os pedaços em um dicionário, usando os nomes dos grupos.
    dados = encontrado.groupdict()
    try:
        # As duas chamadas geram ValueError para um IP como 300.1.1.1 ou uma data como 31/04/2026.
        ipaddress.ip_address(dados["ip"])
        dados["momento"] = datetime.strptime(dados["data"], "%d/%m/%Y:%H:%M:%S")
    except ValueError:
        return None
    return dados


def analisar_log():
    status = Counter()
    erros_404 = Counter()
    invalidas = []
    validas = 0
    primeira = None
    ultima = None

    # errors="replace" evita que um caractere estranho em uma linha corrompida derrube a leitura.
    with open(PASTA / "acesso.log", encoding="utf-8", errors="replace") as arquivo:
        # O arquivo é lido linha a linha, e enumerate numera as linhas a partir de 1.
        for numero, linha in enumerate(arquivo, start=1):
            if not linha.strip():  # linha em branco
                continue

            dados = interpretar_linha(linha)
            if dados is None:
                invalidas.append(numero)
                continue

            validas += 1
            status[dados["status"]] += 1
            if dados["status"] == "404":
                erros_404[dados["ip"]] += 1

            if primeira is None:
                primeira = dados["momento"]
            ultima = dados["momento"]

    return validas, invalidas, status, erros_404, primeira, ultima


def formatar_periodo(periodo):
    # Dividir um timedelta por outro com // diz quantas vezes o segundo cabe no primeiro,
    # e % dá o que sobra.
    horas = periodo // timedelta(hours=1)
    minutos = (periodo % timedelta(hours=1)) // timedelta(minutes=1)
    segundos = (periodo % timedelta(minutes=1)) // timedelta(seconds=1)
    if horas:
        return f"{horas}h{minutos:02d}min{segundos:02d}s"
    return f"{minutos}min{segundos:02d}s"


def main():
    try:
        validas, invalidas, status, erros_404, primeira, ultima = analisar_log()
    except FileNotFoundError:
        print("Arquivo acesso.log não encontrado. Coloque o arquivo na mesma pasta do programa e tente de novo.")
        return

    resumo_invalidas = str(len(invalidas))
    if invalidas:
        palavra = "linha" if len(invalidas) == 1 else "linhas"
        numeros = ", ".join(str(numero) for numero in invalidas)
        resumo_invalidas += f" ({palavra} {numeros})"
    print(f"Linhas válidas: {validas} | Linhas inválidas: {resumo_invalidas}")

    for codigo in sorted(status):
        print(f"Status {codigo}: {status[codigo]}")

    if erros_404:
        # most_common(1) devolve o valor que mais aparece, junto com a contagem.
        ip, quantidade = erros_404.most_common(1)[0]
        palavra = "ocorrência" if quantidade == 1 else "ocorrências"
        print(f"IP com mais erros 404: {ip} ({quantidade} {palavra})")
    else:
        print("IP com mais erros 404: nenhum")

    if primeira is None:
        print("Período analisado: nenhuma linha válida")
        return

    # Subtrair dois horários gera um timedelta; abs garante uma duração positiva se o log estiver fora de ordem.
    periodo = abs(ultima - primeira)
    # A data só aparece junto quando o log passa de um dia.
    formato = "%H:%M:%S" if primeira.date() == ultima.date() else "%d/%m/%Y %H:%M:%S"
    print(f"Período analisado: {formatar_periodo(periodo)} ({primeira.strftime(formato)} a {ultima.strftime(formato)})")


if __name__ == "__main__":
    main()
