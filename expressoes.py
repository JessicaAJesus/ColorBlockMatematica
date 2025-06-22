import random #biblioteca que gera os valores aleatorios

#função para gerar
def gerarOperacao(operador):
    tentativa = 0 #contador
    while tentativa < 10: #tenta gerar expressão válida
        if operador == '+':
            a = random.randint(5, 20) #evitar numeros pequenos
            b = random.randint(5, 20)
            if a == b or a + b <= 10: #evita somas muito pequenas ou com números iguais
                tentativa += 1
                continue
            resultado = a + b

        elif operador == '-':
            a = random.randint(5, 20)
            b = random.randint(1, a)
            if a - b <= 3 or a == b:
                tentativa += 1
                continue
            resultado = a - b

        elif operador == '*':
            a = random.randint(2, 10)
            b = random.randint(2, 10)
            if a == b == 1:
                tentativa += 1
                continue
            resultado = a * b

        elif operador == '/':
            b = random.randint(2, 10)
            resultado = random.randint(2, 10)
            a = b * resultado
            if resultado == 1:
                tentativa += 1
                continue
            operador = '÷'
        else:
            return None

        expressao = f"{a} {operador} {b}"
        return expressao, resultado

    return None 

def variasOperacoes(qtd=5):
    operadores = ['+', '-', '*', '/']
    contador = {'+': 0, '-': 0, '*': 0, '/': 0}
    expressoes = [] #lista para armazenar expressões validas

    while len(expressoes) < qtd:
        op = random.choice(operadores) #escolhe um operador aleatório
        if contador[op] >= 2:
            continue #pula se esse operador já foi usado 2 vezes

        resultado = gerarOperacao(op) #gera a operação com esse operador
        if resultado: #se a operação for válida
            expressao, valor = resultado
            expressoes.append((expressao, valor)) #adiciona na lista de expressões
            contador[op] += 1 

    return expressoes

# teste
if __name__ == "__main__":
    expressoes = variasOperacoes(5)
    for expr, res in expressoes:
        print(f"{expr} = {res}")
