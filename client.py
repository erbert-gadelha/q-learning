import connection as cn
import random
import sys

def stringify(platform):
    '''
    Coloca os bits da plataforma em uma linguagem mais legível
    '''
    match platform[7:]:
            case '00':
                dir_s = "Norte"
            case '01':
                dir_s = "Leste"
            case '10':
                dir_s = "Sul"
            case '11':
                dir_s = "Oeste"
            case _:
                dir_s = "What"
        
    platform_i = int(platform[2:7], 2)
    return (platform_i, dir_s) 

def createf(initial = 0, jump_bonus=0) -> list:
    '''
    Cria uma nova Q-table, com todos os valores zerados ou com um inicial predefinido
    Jump_bonus encoraja pulos ao invés de giros
    '''
    rtrn = []
    for i in range(0, 96):
        
        rtrn.append({
            "left": initial,
            "right": initial,
            "jump": initial+jump_bonus,
        })

    return rtrn

def loadf() -> list:
    '''
    Carrega a Q-table do arquivo resultado.txt
    '''
    f = open("resultado.txt", "r")
    s = f.read()
    f.close()

    rtrn = []
    for line in s.split('\n'):
        split = line.split(' ')
        if len(split) < 3:
            continue
        
        rtrn.append({
            "left": float(split[0]),
            "right": float(split[1]),
            "jump": float(split[2]),
        })
    
    if len(rtrn) != 96:
        print(f"Esperado: (96) estados. Lidos: ({len(rtrn)}) estados.\nArquivo foi carregado com ({len(rtrn)}) estados.")

    return rtrn

def savef(result: list) -> None:
    ''' 
    Salva a Q-table atual no arquivo resultado.txt
    '''
    if len(result) != 96:
        print(f"Esperado: (96) estados. Recebido: ({len(result)}) estados.\nArquivo foi salvo com ({len(result)}) estados.")


    s = ""
    for state in result:
        s += "{0} {1} {2}\n".format(
            '{0:.6f}'.format(state['left']),
            '{0:.6f}'.format(state['right']),
            '{0:.6f}'.format(state['jump']))

    f = open("resultado.txt", "w")
    f.write(s)
    f.close()
    return 0

class qLearning():
    def __init__(self, port:int = 2037, state = '0b0', reward = -14, load=True, save=True, alpha=0.1, gamma=0.9, loops=90, initial=0, jump_bonus=0): #alpha=1e-1, gamma=0.99
        '''
        Inicializa a conexão e os parâmetros do algoritmo
        '''
        self.state = state
        self.reward = reward
        self.alpha = alpha
        self.gamma = gamma
        self.save = save
        self.loops = loops

        if load:
            self.result = loadf()
        else:
            self.result = createf(initial, jump_bonus)

        self.s = cn.connect(port)
        

    def test(self) -> None:
        '''
        Testa o resultado, sem treinar
        '''
        for i in range(0, 1000):
            action = self.__most_valued__(self.state)
            self.s.recv(1024).decode()
            new_state, new_reward = cn.get_state_reward(self.s, action)
            old_state=self.state
            self.state  = new_state
            print(f'{i:03} [state/reward]: [{stringify(old_state)} -> {action}')
    def train(self) -> None:
        '''
        Realiza o treinamento do algoritmo
        '''
        if(self.save):
            savef(self.result)
        for j in range(0,self.loops):
            for i in range(0, 99):
                # Corrigir erro de dados incorretos vindos do jogo
                # Sem isso, get_state_reward pode retornar os dados do movimento anterior (penúltimo movimento)
                self.s.recv(1024).decode()
                
                # Política exploratória
                my_list = [0] * 7 + [1] * 2 + [2] * 1
                action = self.__most_valued__(self.state, random.choice(my_list))
                
                new_state, new_reward = cn.get_state_reward(self.s, action)
                
                new_reward_mod = new_reward
                
                # Reduzir punição por falha, para evitar vícios de ficar 'preso'
                if new_reward_mod == -100:
                    new_reward_mod = -20
                
                # Evitar distorções do reset
                if self.reward == -20:
                    self.reward = -14
                elif self.reward == 300:
                    self.reward = -14
                
                # Usar a diferença de recompensas na fórmula
                reward_received = new_reward_mod - self.reward
                if reward_received == 0:
                    # Punir a ação de ficar no mesmo quadrado
                    reward_received = -0.5
                
                # Função Q
                reward = (1-self.alpha) * self.result[int(self.state, 2)][action] + self.alpha * (reward_received + self.gamma*self.result[int(new_state, 2)][self.__most_valued__(new_state)])
                
                # Atualizar tabela
                self.result[int(self.state, 2)][action] = reward
                
                # Atualizar estado atual
                old_state = self.state
                self.state = new_state
                self.reward = new_reward_mod
                print(f'{j:02}{i:03} [state/reward]: [{stringify(old_state)} -> {action} | {reward_received}]\t~\t{reward}')

            if(self.save):
                savef(self.result)
    
    def __most_valued__(self, state, rank=0) -> str:
        states = self.result[int(state, 2)]
        states = dict(sorted(states.items(), key=lambda item: item[1], reverse=True))
        # print(states)
        return str(list(states.keys())[rank])

if "zerado" in sys.argv:
    ql = qLearning(load=False, save=True, alpha=0.2, gamma=0.2, loops=30, initial=20)
    ql.train()
    ql = qLearning(load=True, save=True, alpha=0.1, gamma=0.7, loops=50)
    ql.train()
    while True:
        ql = qLearning(load=True, save=True, alpha=0.05, gamma=0.9, loops=999)
        ql.train()
elif "teste" in sys.argv:
    ql = qLearning(load=True, save=True, alpha=0.05, gamma=0.9, loops=299)
    ql.test()
else:
    ql = qLearning(load=True, save=True, alpha=0.05, gamma=0.9, loops=299)
    ql.train()

