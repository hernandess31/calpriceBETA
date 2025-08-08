import hashlib

pedidos = []  
receitas_salvas = []

def hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

def carregar_usuarios():
    try:
        with open("usuarios.txt", "r", encoding="utf-8") as f:
            return [linha.strip().split(":") for linha in f if ":" in linha]
    except FileNotFoundError:
        return []

def fazer_login():
    usuarios = carregar_usuarios()
    print("\n=== LOGIN CALPRICE ===")
    usuario = input("Usuário: ").strip()
    senha = input("Senha: ").strip()
    
    for user, senha_hash in usuarios:
        if user == usuario and hash_senha(senha) == senha_hash:
            print("Login bem-sucedido! ✅")
            return True
    
    print("Usuário ou senha incorretos. ❌")
    return False

def cadastrar_usuario():
    novo_usuario = input("Novo usuário: ").strip()
    nova_senha = input("Nova senha: ").strip()
    
    with open("usuarios.txt", "a", encoding="utf-8") as f:
        f.write(f"{novo_usuario}:{hash_senha(nova_senha)}\n")
    print("Usuário cadastrado com sucesso! ✅")

def carregar_dados():
    global receitas_salvas, pedidos
    try:
        with open("receitas.txt", "r", encoding="utf-8") as f:
            receitas_salvas = [linha.strip() for linha in f.readlines()]
    except FileNotFoundError:
        pass
    
    try:
        with open("pedidos.txt", "r", encoding="utf-8") as f:
            pedidos = [linha.strip() for linha in f.readlines()]
    except FileNotFoundError:
        pass

if __name__ == "__main__":
    carregar_dados()

    while True:
        print("\n=== BEM-VINDO AO CALPRICE ===")
        print("1. Fazer Login")
        print("2. Cadastrar Novo Usuário")
        print("3. Sair")
        
        opcao = input("Escolha uma opção: ").strip()
        
        if opcao == "1":
            if fazer_login():
                break 
        elif opcao == "2":
            cadastrar_usuario()
        elif opcao == "3":
            print("Encerrando...")
            exit()
        else:
            print("Opção inválida.")

    while True:
        print("\nOlá, seja bem-vindo ao Calprice.")
        print("1 - Calculadora de preço")
        print("2 - Receitas")
        print("3 - Controle de Pedidos")
        print("4 - Sair")

        try:
            opcao = int(input("Escolha uma opção digitando o número correspondente: "))
        except ValueError:
            print("Por favor, digite um número válido.")
            continue

        if opcao == 1:
            preco = float(input("Preço pago: "))
            pacote_fechado = float(input("Quantidade de embalagem: "))
            usado = float(input("Quantidade receita em gramas: "))
            conta = preco / pacote_fechado * usado
            print(f"O valor a ser cobrado é: R$ {conta:.2f}")

        elif opcao == 2:
            while True:
                print("\n####### RECEITAS #######")
                print("1 - Adicionar nova receita")
                print("2 - Ver receitas salvas")
                print("3 - Voltar ao menu principal")

                escolha = input("Escolha uma opção: ").strip()

                if escolha == "1":
                    receita = input("Escreva sua receita: ")
                    resposta = input(f"Sua receita está certa? {receita} (sim/não): ").strip().lower()

                    while resposta not in ["sim", "não", "nao"]:
                        print("Resposta inválida. Por favor, digite 'Sim' ou 'Não'.")
                        resposta = input(f"Sua receita está certa? {receita} (Sim/Não): ").strip().lower()

                    if resposta == "sim":
                        receitas_salvas.append(receita)
                        with open("receitas.txt", "a", encoding="utf-8") as arquivo:
                            arquivo.write(receita + "\n")
                        print("Receita salva com sucesso!")
                    else:
                        print("Vamos corrigir a receita então.")

                elif escolha == "2":
                    if receitas_salvas:
                        print("\n#### Lista de receitas Salvas ####")
                        for i, r in enumerate(receitas_salvas, 1):
                            print(f"{i}. {r}")
                    else:
                        print("Nenhuma receita salva ainda.")

                elif escolha == "3":
                    print("Voltando ao menu principal...")
                    break

                else:
                    print("Opção inválida. Tente novamente.")

        elif opcao == 3:
            print("Bem-vindo à Central de Pedidos!")

            while True:
                print("\n--- Central de Pedidos ---")
                print("1. Adicionar um pedido")
                print("2. Ver pedidos já realizados")
                print("3. Voltar ao menu principal")

                subopcao = input("Escolha uma opção: ")

                if subopcao == "1":
                    pedido = input("Digite o nome do pedido: ")
                    pedidos.append(pedido)
                    with open("pedidos.txt", "a", encoding="utf-8") as arquivo:
                        arquivo.write(pedido + "\n")
                    print("Pedido adicionado com sucesso!")

                elif subopcao == "2":
                    if not pedidos:
                        print("Nenhum pedido realizado ainda.")
                    else:
                        print("\n--- Pedidos Realizados ---")
                        for i, p in enumerate(pedidos, 1):
                            print(f"{i}. {p}")

                elif subopcao == "3":
                    print("Retornando ao menu principal...")
                    break
                else:
                    print("Opção inválida. Tente novamente.")

        elif opcao == 4:
            print("Encerrando o programa... Até logo!")
            break

        else:
            print("Opção inválida. Tente novamente.")