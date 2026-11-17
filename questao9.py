# Questão 9 - Gerador e Validador de Senhas

# secrets gera números aleatórios próprios para segurança.
# string traz prontas as listas de letras e dígitos.
# re é a biblioteca de expressões regulares.
import re
import secrets
import string

ESPECIAIS = "!@#$%&*"

# Por que não usar o gerador comum (módulo random) para senhas: ele foi feito para
# simulações e jogos. Os números saem de uma fórmula previsível, então quem descobrir o
# estado interno do gerador consegue calcular os próximos valores e adivinhar as senhas.
# O módulo secrets usa a fonte de aleatoriedade do sistema operacional, própria para segurança.

# Expressão: (?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[!@#$%&*]).{12,}
#   (?=.*[A-Z])       confere se existe uma maiúscula em algum lugar da senha
#   (?=.*[a-z])       confere se existe uma minúscula
#   (?=.*[0-9])       confere se existe um dígito
#   (?=.*[!@#$%&*])   confere se existe um caractere especial do conjunto
#   .{12,}            exige no mínimo 12 caracteres
# O (?=...) só olha à frente sem consumir o texto, por isso as quatro conferências
# começam do início da senha.
REGEX_SENHA = r"(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[!@#$%&*]).{12,}"

# Usadas só para mostrar o que falta em uma senha inválida.
REGRAS = [
    ("maiúscula", r"[A-Z]"),
    ("minúscula", r"[a-z]"),
    ("dígito", r"[0-9]"),
    ("caractere especial", r"[!@#$%&*]"),
]


def gerar_senha(tamanho):
    if tamanho < 4:
        raise ValueError("A senha precisa de pelo menos 4 caracteres, um de cada tipo.")

    todos = string.ascii_letters + string.digits + ESPECIAIS
    # secrets.choice sorteia um item. A senha começa com um caractere de cada tipo para garantir as regras.
    senha = [
        secrets.choice(string.ascii_uppercase),
        secrets.choice(string.ascii_lowercase),
        secrets.choice(string.digits),
        secrets.choice(ESPECIAIS),
    ]
    while len(senha) < tamanho:
        senha.append(secrets.choice(todos))

    # SystemRandom usa a mesma fonte segura, e shuffle embaralha para os 4 primeiros
    # caracteres não seguirem sempre a mesma ordem.
    secrets.SystemRandom().shuffle(senha)
    return "".join(senha)


def validar_senha(senha):
    # fullmatch exige que a senha inteira combine com a expressão.
    return re.fullmatch(REGEX_SENHA, senha) is not None


def motivos_invalida(senha):
    motivos = []
    if len(senha) < 12:
        motivos.append("menos de 12 caracteres")

    # re.search procura o padrão em qualquer parte da senha.
    faltando = [nome for nome, padrao in REGRAS if not re.search(padrao, senha)]
    if len(faltando) > 1:
        motivos.append("falta " + ", ".join(faltando[:-1]) + " e " + faltando[-1])
    elif faltando:
        motivos.append("falta " + faltando[0])

    return "; ".join(motivos)


def descrever(senha):
    if validar_senha(senha):
        return "válida"
    return f"inválida ({motivos_invalida(senha)})"


def main():
    print("Teste do validador:")
    for senha in ["Abc123!@xyzW", "abc123456789", "ABCdef!@#$%&", "Ab1!"]:
        print(f"{senha:<13} -> {descrever(senha)}")

    print("\nSenhas geradas:")
    senhas = [gerar_senha(12) for _ in range(5)]
    for senha in senhas:
        print(f"{senha:<13} -> {descrever(senha)}")

    if all(validar_senha(senha) for senha in senhas):
        print("\nAs 5 senhas geradas são válidas.")
    else:
        print("\nAlguma senha gerada não passou no validador.")


if __name__ == "__main__":
    main()
