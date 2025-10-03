from inimigo import Inimigo

class Menu:
    def __init__(self):
        self.inimigos_disponiveis = {
            1: Inimigo(nome="Lancer", vida=250, magia=0, atk=10, defn=10, lootouro=20),
            2: Inimigo(nome="Jevil", vida=3500, magia=50, atk=15, defn=3, lootouro=500),
        }

    def iniciar_menu_batalha(self):
        print("--- Menu de Batalha ---")
        while True:
            print("Escolha seu oponente:")
            for key, inimigo in self.inimigos_disponiveis.items():
                print(f"[{key}] - {inimigo.nome} (Vida: {inimigo.vida})")

            escolha = input("Digite o número do inimigo: ")

            try:
                escolha = int(escolha)
                if escolha in self.inimigos_disponiveis:
                    return self.inimigos_disponiveis[escolha]
                else:
                    print("Escolha inválida. Tente novamente.")
            except ValueError:
                print("Entrada inválida. Digite um número.")
