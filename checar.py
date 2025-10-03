from atitude import Atitude
class Checar(Atitude):
    def __init__(self, num: int):
        self.__num = num
        super().__init__("Checar")

    @property
    def num(self):
        return self.__num

    def executar(self, jogador_usando, alvo):
        print(f"{jogador_usando.nome} checa {alvo.nome}.")
        print(f"Informações de {alvo.nome}: Vida: {alvo.vida}, Magia: {alvo.magia}, Ataque: {alvo.atk}, Defesa: {alvo.defn}")
