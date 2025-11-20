import textwrap

# Variáveis globais de estado do sistema
AGENCIA = "0001"
LIMITE_SAQUES = 3

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
usuarios = []  # Lista para armazenar usuários (clientes)
contas = []    # Lista para armazenar contas correntes
numero_conta_sequencial = 1

def menu():
    """Exibe o menu principal do sistema."""
    menu_str = """\n
    ============== MENU ==============
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nu]\tNovo Usuário
    [nc]\tNova Conta
    [lc]\tListar Contas
    [q]\tSair
    => """
    return input(textwrap.dedent(menu_str))

# --- Funções das Operações Bancárias V1 ---

def depositar(saldo, valor, extrato, /):
    """
    Realiza um depósito na conta.
    Argumentos: Positional Only (saldo, valor, extrato)
    Retorno: Novo saldo e extrato atualizado.
    """
    if valor > 0:
        saldo += valor
        extrato += f"Depósito:\tR$ {valor:.2f}\n"
        print("\n=== Depósito realizado com sucesso! ===")
    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

    return saldo, extrato

def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    """
    Realiza um saque na conta.
    Argumentos: Keyword Only (saldo, valor, extrato, limite, numero_saques, limite_saques)
    Retorno: Novo saldo, extrato atualizado e número de saques.
    """
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")

    elif excedeu_limite:
        print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")

    elif excedeu_saques:
        print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")

    elif valor > 0:
        saldo -= valor
        extrato += f"Saque:\t\tR$ {valor:.2f}\n"
        numero_saques += 1
        print("\n=== Saque realizado com sucesso! ===")

    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

    return saldo, extrato, numero_saques

def exibir_extrato(saldo, /, *, extrato):
    """
    Exibe o extrato da conta.
    Argumentos: Positional Only (saldo), Keyword Only (extrato)
    """
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo:\t\tR$ {saldo:.2f}")
    print("==========================================")

# --- Funções da Versão 2 (Clientes e Contas) ---

def filtrar_usuario(cpf, usuarios):
    """Retorna o usuário com o CPF fornecido ou None se não encontrado."""
    cpf_limpo = cpf.replace(".", "").replace("-", "")
    for usuario in usuarios:
        if usuario["cpf"] == cpf_limpo:
            return usuario
    return None

def criar_usuario(usuarios):
    """
    Cria um novo usuário (cliente).
    Regras: Armazenar nome, data_nascimento, CPF (somente números) e endereço.
    Não permitir 2 usuários com o mesmo CPF.
    """
    cpf = input("Informe o CPF (somente números): ")
    
    # Limpa o CPF para garantir que só números sejam armazenados/comparados
    cpf_limpo = cpf.replace(".", "").replace("-", "")
    
    if filtrar_usuario(cpf_limpo, usuarios):
        print("\n@@@ Operação falhou! Já existe usuário com este CPF. @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    
    # Endereço: logradouro, nro - bairro - cidade/sigla estado
    logradouro = input("Logradouro (Ex: Rua Brasil): ")
    numero = input("Número: ")
    bairro = input("Bairro: ")
    cidade = input("Cidade: ")
    estado_sigla = input("Sigla do Estado (Ex: SP): ")
    
    endereco = f"{logradouro}, {numero} - {bairro} - {cidade}/{estado_sigla.upper()}"

    usuarios.append({
        "nome": nome, 
        "data_nascimento": data_nascimento, 
        "cpf": cpf_limpo, 
        "endereco": endereco
    })
    
    print("\n=== Usuário criado com sucesso! ===")

def criar_conta(contas, usuarios, numero_conta_sequencial):
    """
    Cria uma nova conta corrente e a vincula a um usuário existente.
    Regras: Agência fixa, Número da conta sequencial.
    """
    cpf = input("Informe o CPF do usuário: ")
    cpf_limpo = cpf.replace(".", "").replace("-", "")
    usuario = filtrar_usuario(cpf_limpo, usuarios)

    if not usuario:
        print("\n@@@ Usuário não encontrado, fluxo de criação de conta encerrado! @@@")
        return contas, numero_conta_sequencial

    contas.append({
        "agencia": AGENCIA, 
        "numero_conta": numero_conta_sequencial, 
        "usuario": usuario
    })
    
    print("\n=== Conta criada com sucesso! ===")
    print(f"Agência: {AGENCIA}, Conta: {numero_conta_sequencial}")
    
    # Incrementa o número sequencial da próxima conta
    numero_conta_sequencial += 1
    
    return contas, numero_conta_sequencial

def listar_contas(contas):
    """Exibe todas as contas cadastradas e seus respectivos usuários."""
    if not contas:
        print("\n@@@ Nenhuma conta cadastrada. @@@")
        return

    print("\n============== LISTA DE CONTAS ==============")
    for conta in contas:
        linha = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print("=" * 40)
        print(textwrap.dedent(linha))
    print("=============================================")

# --- Função Principal ---

def main():
    global saldo, extrato, numero_saques, contas, numero_conta_sequencial, usuarios
    
    while True:
        opcao = menu()

        if opcao == "d":
            valor = float(input("Informe o valor do depósito: "))
            # Chamada da função depositar (Positional Only)
            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == "s":
            valor = float(input("Informe o valor do saque: "))
            # Chamada da função sacar (Keyword Only)
            saldo, extrato, numero_saques = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES,
            )

        elif opcao == "e":
            # Chamada da função extrato (Positional + Keyword Only)
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == "nu":
            criar_usuario(usuarios)

        elif opcao == "nc":
            contas, numero_conta_sequencial = criar_conta(contas, usuarios, numero_conta_sequencial)
            
        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print("\n@@@ Operação inválida, por favor selecione novamente a operação desejada. @@@")

if __name__ == "__main__":
    main()