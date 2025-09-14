from jogador import Jogador
from inimigo import Inimigo
class Batalha:
    def __init__(self, jogador: Jogador, inimigo: Inimigo):
        self.jogador = jogador
        self.inimigo = inimigo
    def iniciarbatalha(self):
        print(f"Uma batalha contra {self.inimigo.nome} começou!")
        while self.jogador.estouvivo() and self.inimigo.estouvivo():
            print("--------------------------")
            self.turnojogador()
            if not self.inimigo.estouvivo():
                break
            self.turnoinimigo()
            if not self.jogador.estouvivo():
                break
        self.fimbatalha()
    def turnojogador(self):
        print(f"É o turno de {self.jogador.nome}!")
        print(f"Sua vida: {self.jogador.vida} | Magia: {self.jogador.magia}")
        print("Escolha uma ação: (1) Atacar | (2) Usar Habilidade")
        escolha = input("> ")
        if escolha == '1':
            self.jogador.atacar(self.inimigo)
        elif escolha == '2':
            print("Suas habilidades:")
            for i, habilidade in enumerate(self.jogador.habilidades):
                print(f"({i + 1}) {habilidade.nome} - Custo: {habilidade.customagia}")
            try:
                escolhahab = int(input("Escolha a habilidade: ")) - 1
                if 0 <= escolhahab < len(self.jogador.habilidades):
                    habilidadeescolhida = self.jogador.habilidades[escolhahab]
                    habilidadeescolhida.usar(self.jogador, self.inimigo)
                else:
                    print("Escolha inválida. Você perdeu o turno.")
            except ValueError:
                print("Entrada inválida. Você perdeu o turno.")
        else:
            print("Ação inválida. Você perdeu o turno.")
    def turnoinimigo(self):
        print("--- É o turno do inimigo! ---")
        self.inimigo.agir(self.jogador)
    def fimbatalha(self):
        print("--- A batalha terminou! ---")
        if self.jogador.estouvivo():
            print(f"Você venceu! {self.jogador.nome} derrotou {self.inimigo.nome}!")
        else:
            print(f"Você foi derrotado por {self.inimigo.nome}. Game Over!")
