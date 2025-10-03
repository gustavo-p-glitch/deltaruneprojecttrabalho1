from atitude import Atitude

class Poupar(Atitude):
    def __init__(self):
        super().__init__("Poupar")

    def executar(self, jogador_usando, alvo):
        jogador_usando.poupar(alvo)
