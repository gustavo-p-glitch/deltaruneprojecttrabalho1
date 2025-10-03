from jogador import Jogador
from inimigo import Inimigo
from habilidade import Habilidade
from acao import Acao
from checar import Checar
from poupar import Poupar
from defender import Defender
from atitude import Atitude


class InterfaceBatalha:
    ASCII_ARTS = {"Jevil": """CHAOS! CHAOS! I CAN DO ANYTHING!
                             ⠺⢳⠅⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣿⢹⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣤⣴⣾⣿⣿⠏⠆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⡰⢘⡂⣽⣿⣿⣿⣿⣿⢋⠎⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⢤⣲⣽⣿⣼⣿⣷⡙⠘⣿⣿⣿⡟⡥⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⣊⣴⣿⣿⣿⠟⠙⠉⠉⢃⢀⣿⣿⠷⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⣴⢿⣵⣿⣿⣿⡿⠁⢀⡀⠄⠀⢾⡶⠛⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣼⣿⣿⣿⡿⠋⢀⣤⠊⠁⠀⠀⠀⠀⢿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⣶⣶⣾⣶⣷⣦⣄⣀⠀⠀⢄⠀⠀⠀⣀⣤⣖⣮⣥⣦⣤⣌⣁⠒⠄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣰⣿⣿⣿⠿⡡⠂⠹⡇⠀⠀⠀⠀⠀⠀⢸⡆⠀⠀⠀⠀⠀⠀⠀⢀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⡀⡀⢀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⠲⣆⣀⠃⠀⠀⠀⣠⣄⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢠⣿⣿⣿⡫⢻⣅⠀⠀⠙⠀⠀⠀⠀⠀⠀⠀⣧⠘⠀⠀⠀⠀⠀⣰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣄⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠋⠀⠀⠀⠀⠀⢀⣤⣴⣾⡿⠟⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⣸⣿⣿⣿⡅⠀⠻⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⡄⠡⠀⠀⢀⢰⡿⠟⠛⠉⠛⢿⣿⣿⣿⣿⣿⣿⣿⣿⢿⡿⣽⣻⣿⣿⣿⣿⣿⣿⠋⣸⡟⠁⠀⠀⠀⠀⠀⠀⣾⣿⡿⠁⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⣿⣿⡟⠻⣧⠀⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢷⠀⠂⠀⣦⣼⠂⠀⠀⠀⠀⠈⢻⣿⣿⣿⣿⣻⣽⢾⢻⣭⣭⣟⢿⣿⣿⣿⣿⣿⠀⡟⠀⠀⠀⠀⡠⣔⣪⣿⣿⣿⣧⣌⠀⡀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢸⣿⡿⠁⠀⠙⢦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⡆⠈⡀⠀⠁⠀⠀⠀⠀⠀⠀⠈⣿⣿⣿⣛⢟⡱⢮⣿⣿⡿⢿⠷⣻⣿⣿⣿⣿⡛⠀⢠⣤⣶⣿⣿⣿⣿⣿⣿⣿⣿⠿⠿⠿⠷⠶⠶⠆⠀⠀
⠀⠀⠀⠀⢸⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⡀⠠⠀⠀⠀⠀⢄⠀⠀⠀⠰⣿⣿⣿⣯⢮⡱⢿⣿⣿⡧⢺⣿⣿⣹⣿⣿⣿⣷⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢸⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢷⠀⠀⠀⠀⠀⠀⠑⢞⡭⣿⣿⣿⣏⣨⠴⣩⢏⡿⣉⣶⢿⣿⣿⢽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠘⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣇⠀⠀⠀⠀⠀⠀⠀⠙⠛⡿⣿⣽⣺⣽⣧⣿⣞⣿⣿⣿⣿⢏⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⣤⠓⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣶⡆⠀⡀⠀⠀⠀⠀⣤⢷⢻⣿⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⢿⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠻⠿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⣿⣿⣧⣧⠈⢀⠀⠀⣠⣶⣿⣷⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣾⣱⣿⣿⣿⣿⣿⣿⣿⡟⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⣿⣿⣿⣿⣶⣿⣿⣿⣿⣿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡽⣞⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠰⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢯⡿⣿⣿⡿⣿⣿⣿⣿⣿⣽⣲⣽⣿⣿⣿⣿⣿⣿⣟⢧⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠆⢃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⢿⣷⡈⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⠸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢯⣿⣷⡀⠀⠈⠉⠙⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣿⣷⡀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣾⣿⣷⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣟⣿⣧⠀⠀⢹⣿⠁⢨⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠛⠻⠿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⣟⣿⣧⠀⢸⡏⠀⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⣿⣿⣿⣿⣿⣿⠿⡀⠀⠀⠀⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⡿⣿⣷⡀⠇⠘⠿⣿⣿⣿⣿⣿⣿⡿⠠⣿⣿⣿⣿⣿⣟⠎⠀⠈⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢳⡹⣿⣷⠀⠀⠀⠀⠉⠉⠉⢉⣿⣕⣠⣿⣿⣿⣿⣟⠎⠀⠀⠀⠀⠀⠑⠢⢁⠂⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠳⠽⠋⠀⠀⠀⠀⠀⠀⢀⣾⣟⣾⠻⢹⣿⣿⣟⠎⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢁⡀⠀⠀⠀⣀⣠⣀⠤⠤⠀⠐⠂⠀⠐⠒⠒⠃⠴⢂⡄⣀⠀⠀⣴⣿⣿⡿⠁⠀⢈⣿⣿⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠐⠠⣀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣤⠶⠛⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⢺⢋⣿⣿⡟⠀⠀⠀⣾⠆⠀⠆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢷⡄
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⣷⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⠾⠟⠉⠘⠦⢤⣼⡗⠇⠰⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⠇
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠗⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⣟⣿⠀⡦⢆⡄⢀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⠛⠀
⠄⠐⠀⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⣿⡿⠀⠁⠀⠈⠉⠐⠋⠴⢒⣠⠤⠄⣀⣀⣀⣀⣀⠠⣄⠮⠋⠁⠀⠀
⠀⠀⡀⠄⠀⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⢿⣿⣿⡇⢠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠁⠀⠀⠀⠈⠉⠀⠀⠀⠀⠀⠀
⠈⠀⠀⠀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⢯⣿⣿⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⡎⠐⠀⠀⡢⠀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
"""
        , "Lancer": """⠀⠀⠀⣠⡿⣇⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣶⢏⠱⡌⢽⣶⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⢠⣼⠛⡔⣊⣵⡎⢆⡜⡛⣤⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⣤⡾⢗⢢⡙⠔⣦⣿⣿⣿⣴⢡⢃⠿⣇⣄⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⣶⢍⠣⡍⢆⣱⣿⣿⣿⣿⣿⣿⣶⣏⡰⢩⢹⣶⣀⣀⣰⣶⣆⣀⠀
    ⠀⠀⠀⢀⣀⢿⡘⢇⣸⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⢇⠠⣿⣿⣇⢄⡸⢿⣀
    ⠀⠀⠀⢸⣿⠢⠜⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⢡⠛⣿⡏⢒⡜⠤⣿
    ⠀⠀⠀⢸⣿⢡⣯⣿⣿⣿⣿⣿⣿⡟⢻⡿⠛⣿⣿⣿⡟⢻⣦⢍⣿⡇⠘⢲⣽⠛
    ⠀⠀⠀⢸⣿⣿⠀⠉⠹⠿⠿⠿⠉⠹⠿⠗⠀⠉⣉⡉⠁⠀⠈⣿⣿⡇⠀⢸⣿⠀
    ⠀⠀⠀⠈⠉⣿⣶⡆⠀⠀⠀⣶⣶⣶⣶⣶⣶⣶⣿⡇⠀⢰⣶⣿⠉⠁⠀⢸⣿⠀
    ⠀⠀⠀⠀⠀⣤⣿⣿⣧⡄⠀⠀⠛⣧⡤⠄⡤⠄⣿⣧⣼⣟⠛⠀⠀⠀⢸⣇⠀⠀
    ⠀⢀⡸⠿⠿⠀⣀⣀⡀⠸⠿⣿⣿⣿⣧⣙⣼⣿⠿⠇⠀⠀⠀⠀⠀⢸⡇⠀⠀⠀
    ⣶⡋⠁⠀⠀⣶⢛⡛⢳⣶⣶⣿⠟⣿⣿⣿⣿⣿⣶⣶⣶⣆⠀⠀⣶⡏⠁⠀⠀⠀
    ⣿⡅⠀⠀⠀⠛⠦⡙⠤⢻⣿⠤⣋⠤⡙⢿⣿⣿⣿⣿⣿⣿⣿⣤⠛⠃⠀⠀⠀⠀
    ⠈⠲⢆⣀⣀⣀⣧⣹⣼⣿⠿⡱⢌⠲⢩⢌⡹⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀
    ⠀⠀⠈⠉⠙⣿⣿⣿⣿⣿⣶⠑⣾⣷⡇⣦⢹⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⣉⠿⢿⣿⣿⣿⣡⣿⣿⣿⣿⣾⣿⠿⠿⠿⢿⣿⠉⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⣿⠀⠙⢻⣿⣿⣿⣿⣿⣿⡟⠛⠛⠀⠀⠀⠘⠛⣤⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⣿⣤⣤⡄⠀⠀⣤⠛⠛⠛⠛⠛⣤⣤⡄⠀⠀⠀⣤⣿⣧⡄⠀⠀⠀
    ⠀⠀⢀⣰⣶⠭⢩⢿⣷⣶⣶⠉⠀⠀⠀⠀⠀⠉⠉⠱⢶⣶⣶⢩⡙⡍⢳⣆⣀⠀
    ⠀⢰⣾⣿⣶⣾⣷⣾⣶⡞⠛⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⢻⣶⣶⣷⣾⣷⣾⣿⣶"""
        , "cavaleiro": """⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣀⣸⣄⠀⠀⠠⢿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣦⡏⠈⢀⣴⣄⣁⣽⡷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⢀⠀⠀⠀⠻⢿⣿⣿⣿⣿⣿⡧⣤⡴⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠉⢷⣶⣦⣤⣤⣝⣯⣝⢫⣾⣷⡋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢀⣤⣮⣿⡿⢿⣿⣿⣿⣿⡟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⢀⣴⠿⠋⠉⠀⠀⢼⣍⣭⣟⠋⠙⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⣴⠶⣿⡇⠀⠀⠀⠀⠀⣰⣿⢿⣿⡓⠀⠘⣿⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⢻⣶⣿⠰⠆⠀⠀⠀⣴⣿⠃⢸⣿⠀⠀⠠⣼⢿⣷⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣼⣿⡇⠀⢸⡟⠀⠀⠀⠀⠈⠯⣾⣦⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠈⠻⣷⣀⣼⡇⠀⠀⠀⠀⠀⠀⠘⢿⣿⣶⡀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠳⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠙⢿⣿⣦⡀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⢿⣿⣦⣀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢈⣛⠿⣿⣦⣀"""}

    def __init__(self, jogadores: list[Jogador], inimigo: Inimigo):
        self.jogadores = jogadores
        self.inimigo = inimigo

    def mostrar_status(self):
        
        print("\n" + "=" * 60)
        print(f"| BATALHA CONTRA: {self.inimigo.nome.upper()} |")
        print("=" * 60)

        nome_inimigo = self.inimigo.nome
       
        ascii_art_inimigo = self.ASCII_ARTS.get(nome_inimigo, f"(Arte ASCII para '{nome_inimigo}' não encontrada)")
        print(ascii_art_inimigo)

        print("\n" + "=" * 60)

        
        print("--- Status da Batalha ---")
        for jogador in self.jogadores:
            if jogador.estouvivo():
               
                defesa_status = ""
                if hasattr(jogador, 'defesa_duracao') and jogador.defesa_duracao > 0:
                    defesa_status = f" (DEF +{jogador.defn - jogador.defn_base}, Turnos: {jogador.defesa_duracao})"

                print(
                    f"{jogador.nome}: Vida: {jogador.vida} | Magia: {jogador.magia} | Ataque: {jogador.atk} | Defesa: {jogador.defn}{defesa_status}")

        
        print(
            f"\n{self.inimigo.nome}: Vida: {self.inimigo.vida}| Contagem: {self.inimigo.contador}")
        print("--------------------------")

    
    def mostrar_opcoes_jogador(self, jogador: Jogador, acoes_disponiveis: list):
        """Mostra todas as opções (Ataque, Poupar, Habilidades, Atitudes e Item Condicional)."""

        print("\n" + "=" * 40)
        print(f"É o turno de {jogador.nome}!")
        print("Escolha sua ação:")

        for i, acao in enumerate(acoes_disponiveis):
            numero = i + 1

            # CORREÇÃO CRÍTICA: Checa se é uma função E diferencia as funções
            if callable(acao):
                # Usa acao.__name__ para distinguir entre jogador.atacar e jogador.poupar
                if acao.__name__ == 'atacar':
                    print(f"[{numero}] - Ataque Básico")
                elif acao.__name__ == 'poupar':
                    print(f"[{numero}] - Poupar")
                else:
                    # Fallback para outras funções (caso haja)
                    print(f"[{numero}] - Ação (Função)")

            # Para classes (Habilidade, Acao, Checar, Defender)
            elif hasattr(acao, 'nome'):
                if isinstance(acao, Habilidade):
                    print(f"[{numero}] - Habilidade: {acao.nome} (Custo: {acao.customagia})")
                else:
                    # Isso inclui Checar, Defender e outras Ações customizadas
                    print(f"[{numero}] - Ação: {acao.nome}")

        # Adiciona a opção de Item se o jogador tiver itens
        indice_item = len(acoes_disponiveis) + 1
        # Usamos a propriedade tem_itens (que assume que o jogador tem o inventário)
        if jogador.tem_itens:
            print(f"[{indice_item}] - Item (Inventário)")

        print("=" * 40)

        escolha = input("> ")
        return escolha

    def mostrar_menu_inventario(self, jogador: Jogador):
        # Este método não foi o foco, mas mantive a lógica de exibição para rodar
        print(f"\n--- Inventário de {jogador.nome} ---")

        itens_exibidos = []

        for i, item in enumerate(jogador.inventario):
            itens_exibidos.append(item)
            tipo_nome = item.tipo.nome if hasattr(item.tipo, 'nome') else str(item.tipo)
            status_equipado = " (Equipado)" if hasattr(jogador, 'equipamentos') and item in jogador.equipamentos else ""
            print(f"[{i + 1}] - {item.nome} ({tipo_nome}){status_equipado}")

        print("[0] - Voltar ao Menu Principal")
        print("-" * 30)

        escolha_item = input("Escolha o item a usar (ou 0 para voltar): ")

        try:
            escolha_int = int(escolha_item)
            if escolha_int == 0:
                return None, None

            indice = escolha_int - 1
            if 0 <= indice < len(itens_exibidos):
                item_escolhido = itens_exibidos[indice]
                tipo_nome = item_escolhido.tipo.nome if hasattr(item_escolhido.tipo, 'nome') else str(
                    item_escolhido.tipo)
                return item_escolhido, tipo_nome
            else:
                print("Escolha de item inválida.")
                return None, None
        except ValueError:
            print("Entrada inválida. Digite um número.")
            return None, None
