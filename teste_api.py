import requests


CATEGORIAS = ["familiar", "pessoal", "comercial"]
TIPOS = ["movel", "fixo", "comercial"]


def escolher_enum(msg, opcoes):
    """Função para escolher uma opção de enumeração."""
    while True:
        print(f"{msg}:")
        for idx, opc in enumerate(opcoes, 1):
            print(f"{idx}. {opc}")
        escolha = input("Digite o número da opção: ").strip()
        if escolha.isdigit() and 1 <= int(escolha) <= len(opcoes):
            return opcoes[int(escolha)-1]
        else:
            print("Opção inválida, tente novamente.\n")


def incluir_contato(base_url):
    """Função para incluir um novo contato via API."""
    nome = input("Nome do contato: ").strip()
    categoria = escolher_enum("Escolha a categoria", CATEGORIAS)

    telefones = []
    while True:
        numero = input("Telefone (apenas números): ").strip()
        tipo = escolher_enum("Escolha o tipo de telefone", TIPOS)
        telefones.append({"numero": numero, "tipo": tipo})
        mais = input("Adicionar outro telefone? (s/n): ").strip().lower()
        if mais != "s":
            break

    contato = {
        "nome": nome,
        "categoria": categoria,
        "telefones": telefones
    }

    resp = requests.post(base_url, json=contato)
    print("Status:", resp.status_code)
    print("Resposta:", resp.json())


def consultar_contato(base_url):
    """Função para consultar um contato pelo ID via API."""
    contato_id = input("Digite o ID do contato: ").strip()
    resp = requests.get(f"{base_url}{contato_id}")
    print("Status:", resp.status_code)
    if resp.status_code == 200:
        contato = resp.json()
        print(f"ID: {contato['id']}\nNome: {contato['nome']}\nCategoria: {contato['categoria']}")
        print("Telefones:")
        for tel in contato['telefones']:
            print(f"  - {tel['numero']} ({tel['tipo']})")
    else:
        print("Contato não encontrado.")


def listar_contatos(base_url):
    """Função para listar todos os contatos via API."""
    resp = requests.get(base_url)
    print("Status:", resp.status_code)
    contatos = resp.json()
    if contatos:
        for contato in contatos:
            print(f"ID: {contato['id']} | Nome: {contato['nome']} | Categoria: {contato['categoria']}")
            for tel in contato['telefones']:
                print(f"   - {tel['numero']} ({tel['tipo']})")
            print()
    else:
        print("Nenhum contato cadastrado.")


def main():
    base_url = "http://localhost:8000/contatos/"
    while True:
        print("\nMenu:")
        print("1. Incluir contato")
        print("2. Consultar contato por ID")
        print("3. Listar todos os contatos")
        print("4. Sair")
        opcao = input("Escolha uma opção: ").strip()
        if opcao == "1":
            incluir_contato(base_url)
        elif opcao == "2":
            consultar_contato(base_url)
        elif opcao == "3":
            listar_contatos(base_url)
        elif opcao == "4":
            print("Saindo...")
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()
