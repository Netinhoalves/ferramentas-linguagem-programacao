# Questão 3 - Arquivos e Tratamento de Exceções

# csv lê arquivos com campos separados por um delimitador.
# pathlib facilita montar o caminho dos arquivos.
import csv
from pathlib import Path

# Path(__file__).parent é a pasta do programa, assim os arquivos são achados de onde ele for executado.
PASTA = Path(__file__).parent
TOTAL_CAMPOS = 4
MEDIA_MINIMA = 6.0


class NotaForaDoIntervaloException(Exception):
    """Exceção própria para nota menor que 0 ou maior que 10."""

    def __init__(self, nota):
        super().__init__(f"nota {nota} fora do intervalo 0–10")


def converter_nota(texto):
    # float gera ValueError quando o texto não é um número, como "dez".
    nota = float(texto)
    if not 0 <= nota <= 10:
        raise NotaForaDoIntervaloException(nota)
    return nota


def ler_notas():
    relatorio = []
    erros = []

    # newline="" é a forma recomendada de abrir um arquivo para usar com o módulo csv.
    with open(PASTA / "notas.csv", encoding="utf-8", newline="") as arquivo:
        # csv.reader entrega cada linha como uma lista de campos, separados aqui por ponto e vírgula.
        leitor = csv.reader(arquivo, delimiter=";")
        next(leitor, None)  # pula o cabeçalho

        for campos in leitor:
            if not campos:  # linha em branco
                continue

            nome = campos[0].strip()
            # line_num é o número da linha atual do arquivo, contando o cabeçalho.
            origem = f"Linha {leitor.line_num} ({nome})"

            if len(campos) != TOTAL_CAMPOS:
                erros.append(f"{origem}: esperados {TOTAL_CAMPOS} campos, encontrados {len(campos)}")
                continue

            notas = []
            try:
                for texto in campos[1:]:
                    notas.append(converter_nota(texto))
            except ValueError:
                erros.append(f'{origem}: nota inválida "{texto.strip()}"')
                continue
            except NotaForaDoIntervaloException as erro:
                erros.append(f"{origem}: {erro}")
                continue

            media = sum(notas) / len(notas)
            situacao = "Aprovado" if media >= MEDIA_MINIMA else "Reprovado"
            media_texto = f"{media:.2f}".replace(".", ",")
            relatorio.append(f"{nome} | média {media_texto} | {situacao}")

    return relatorio, erros


def gravar(nome_arquivo, linhas):
    with open(PASTA / nome_arquivo, "w", encoding="utf-8") as arquivo:
        for linha in linhas:
            arquivo.write(linha + "\n")


def main():
    try:
        relatorio, erros = ler_notas()
    except FileNotFoundError:
        print("Arquivo notas.csv não encontrado. Coloque o arquivo na mesma pasta do programa e tente de novo.")
        return
    except UnicodeDecodeError:
        print("Não foi possível ler o arquivo notas.csv. Salve o arquivo em UTF-8 e tente de novo.")
        return

    gravar("relatorio.txt", relatorio)
    gravar("erros.txt", erros)
    print(f"relatorio.txt gravado com {len(relatorio)} estudante(s).")
    print(f"erros.txt gravado com {len(erros)} erro(s).")


if __name__ == "__main__":
    main()
