# Questão 8 - Leitura e Gravação de JSON

# json lê e grava arquivos nesse formato.
# re é usada só para ajustar as casas decimais dos preços no arquivo gravado.
# pathlib facilita montar o caminho dos arquivos.
import json
import re
from pathlib import Path

# Path(__file__).parent é a pasta do programa, assim os arquivos são achados de onde ele for executado.
PASTA = Path(__file__).parent
PRECO_COM_DESCONTO = 200
DESCONTO = 0.10


def formatar_moeda(valor):
    # :,.2f usa o padrão americano (1,234.50); as trocas abaixo invertem a vírgula e o ponto.
    texto = f"{valor:,.2f}"
    return texto.replace(",", "X").replace(".", ",").replace("X", ".")


def carregar_produtos():
    with open(PASTA / "produtos.json", encoding="utf-8") as arquivo:
        # json.load transforma o conteúdo do arquivo em listas e dicionários do Python.
        return json.load(arquivo)


def listar_com_estoque(produtos):
    com_estoque = [produto for produto in produtos if produto["estoque"] > 0]
    # sorted ordena a lista: key diz qual campo comparar e reverse=True vai do maior para o menor.
    for produto in sorted(com_estoque, key=lambda item: item["preco"], reverse=True):
        print(f'{produto["nome"]} | R$ {formatar_moeda(produto["preco"])} | {produto["estoque"]} un.')


def aplicar_desconto(produtos):
    for produto in produtos:
        if produto["preco"] > PRECO_COM_DESCONTO:
            produto["preco"] = round(produto["preco"] * (1 - DESCONTO), 2)


def gravar_produtos(produtos):
    # json.dumps gera o texto em JSON: indent organiza as linhas e ensure_ascii=False mantém os acentos.
    texto = json.dumps(produtos, indent=4, ensure_ascii=False)
    # O JSON gravaria 809.1 e 189.0, então o re.sub deixa os preços com duas casas: 809.10 e 189.00.
    texto = re.sub(r'("preco": )(\d+\.\d+)', lambda item: f"{item.group(1)}{float(item.group(2)):.2f}", texto)
    with open(PASTA / "produtos_atualizados.json", "w", encoding="utf-8") as arquivo:
        arquivo.write(texto + "\n")


def main():
    try:
        produtos = carregar_produtos()
    except FileNotFoundError:
        print("Arquivo produtos.json não encontrado. Coloque o arquivo na mesma pasta do programa e tente de novo.")
        return
    except json.JSONDecodeError as erro:
        # lineno, colno e msg dizem onde está o erro de sintaxe e qual é o problema.
        print(f"O arquivo produtos.json tem um erro de sintaxe na linha {erro.lineno}, coluna {erro.colno}: {erro.msg}")
        return
    except UnicodeDecodeError:
        print("Não foi possível ler o arquivo produtos.json. Salve o arquivo em UTF-8 e tente de novo.")
        return

    try:
        listar_com_estoque(produtos)
        total = sum(produto["preco"] * produto["estoque"] for produto in produtos)
        print(f"Valor total em estoque: R$ {formatar_moeda(total)}")
        aplicar_desconto(produtos)
    except (KeyError, TypeError, ValueError):
        print("O arquivo produtos.json precisa ser uma lista de produtos com nome, preco e estoque.")
        return

    gravar_produtos(produtos)
    print("\nArquivo produtos_atualizados.json gravado.")


if __name__ == "__main__":
    main()
