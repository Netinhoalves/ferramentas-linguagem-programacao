# Questão 2 - Expressões Regulares em Texto

# re é a biblioteca de expressões regulares do Python.
# sys dá acesso aos argumentos passados na linha de comando.
import re
import sys
from datetime import datetime

TEXTO_EXEMPLO = """Contato: maria.souza@ifms.edu.br, tel (67) 99876-5432. Reunião em 12/11/2026.
Outro contato: joao_silva@gmail.com / (67) 3521-1234. E-mail com erro: carlos@@site.
Prazo final: 30/02/2026."""

# E-mail: \b[\w.+-]+@[\w-]+(?:\.[\w-]+)+\b
#   \b              começa no início de uma palavra
#   [\w.+-]+        usuário: letras, números, _, ponto, + ou -, com pelo menos um caractere
#   @               uma única arroba, por isso carlos@@site não passa
#   [\w-]+          primeira parte do domínio
#   (?:\.[\w-]+)+   um ou mais trechos começando com ponto, como .com ou .edu.br
#   \b              termina no fim de uma palavra, deixando de fora o ponto final da frase
REGEX_EMAIL = r"\b[\w.+-]+@[\w-]+(?:\.[\w-]+)+\b"

# Telefone: \(\d{2}\)\s?\d{4,5}-?\d{4}\b
#   \(\d{2}\)       DDD com dois dígitos entre parênteses
#   \s?             espaço opcional depois do DDD
#   \d{4,5}         primeira parte do número: 4 dígitos no fixo e 5 no celular
#   -?              hífen opcional
#   \d{4}\b         últimos 4 dígitos, sem outro dígito colado depois
REGEX_TELEFONE = r"\(\d{2}\)\s?\d{4,5}-?\d{4}\b"

# Data: \b\d{2}/\d{2}/\d{4}\b
#   \b ... \b       a data precisa estar separada do resto do texto
#   \d{2}/\d{2}     dia e mês com dois dígitos, separados por barra
#   /\d{4}          barra e ano com quatro dígitos
# A expressão só confere o formato. Quem diz se a data existe é o strptime.
REGEX_DATA = r"\b\d{2}/\d{2}/\d{4}\b"


def tipo_telefone(telefone):
    # \D representa tudo que não é dígito; o re.sub apaga esses caracteres e sobra só o número.
    digitos = re.sub(r"\D", "", telefone)
    # Tirando os 2 dígitos do DDD, o celular tem 9 e o fixo tem 8.
    return "celular" if len(digitos) - 2 == 9 else "fixo"


def data_existe(data_texto):
    # strptime gera ValueError quando a data não existe no calendário, como 30/02/2026.
    try:
        datetime.strptime(data_texto, "%d/%m/%Y")
        return True
    except ValueError:
        return False


def mascarar_email(encontrado):
    usuario, dominio = encontrado.group().split("@")
    return f"{usuario[0]}****@{dominio}"


def juntar(itens):
    return ", ".join(itens) if itens else "nenhum"


def carregar_texto():
    # Sem argumento, usa o texto do enunciado. Para testar outro texto: python questao2.py arquivo.txt
    if len(sys.argv) < 2:
        return TEXTO_EXEMPLO
    with open(sys.argv[1], encoding="utf-8") as arquivo:
        return arquivo.read()


def main():
    try:
        texto = carregar_texto()
    except (OSError, UnicodeDecodeError):
        print(f"Não foi possível ler o arquivo {sys.argv[1]}.")
        return

    # findall devolve uma lista com todos os trechos que combinam com a expressão.
    emails = re.findall(REGEX_EMAIL, texto)
    telefones = [f"{telefone} [{tipo_telefone(telefone)}]" for telefone in re.findall(REGEX_TELEFONE, texto)]
    datas = [
        f"{data} [{'válida' if data_existe(data) else 'inválida'}]"
        for data in re.findall(REGEX_DATA, texto)
    ]

    print(f"E-mails: {juntar(emails)}")
    print(f"Telefones: {juntar(telefones)}")
    print(f"Datas: {juntar(datas)}")

    # Aqui o re.sub recebe uma função, que é chamada para cada e-mail encontrado no texto.
    print("\nTexto com os e-mails mascarados:")
    print(re.sub(REGEX_EMAIL, mascarar_email, texto))


if __name__ == "__main__":
    main()
