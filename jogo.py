from alma import Alma
from jogador import Jogador
from inimigo import Inimigo
from batalha import Batalha
from habilidade import Habilidade

if __name__ == "__main__":

    almakris = Alma(nome="Kris", vida=100, poder="Determinação")
    kris = Jogador(nome="Kris", magia=20, atk=15, defn=5, alma=almakris)


    rudebuster = Habilidade(nome="rudebuster", tipo="ataque", customagia=10, efeitos={'dano': 25})
    kris.aprenderhabilidade(rudebuster)


    lancer = Inimigo(nome="Lancer", vida=80, magia=0, atk=10, defn=5)

    print("--- Teste de Batalha ---")
    print(f"Seu personagem: {kris.nome} | Vida: {kris.vida}")
    print(f"Inimigo: {lancer.nome} | Vida: {lancer.vida}")


    batalha = Batalha(kris, lancer)
    batalha.iniciarbatalha()
