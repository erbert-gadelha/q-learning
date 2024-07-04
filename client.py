import connection as cn
import result as rs


class qLearning():
    def __init__(self, port:int = 2037, state:int = 0, load=True, save=True, alpha=0.1, gamma=0.9): #alpha=1e-1, gamma=0.99
        self.state = state
        self.alpha = alpha
        self.gamma = gamma

        if load:
            self.result = rs.load()
        else:
            self.result = rs.create()

        self.s = cn.connect(port)

    


    def test(self) -> None:
        for i in range(0, 1000):
            action = self.__most_valued__(self.state)
            new_state, new_reward = cn.get_state_reward(self.s, action)
            self.state  = int(new_state, 2)

    def train(self) -> None:
        for i in range(0, 1000):
            action = self.__most_valued__(self.state)

            new_state, new_reward = cn.get_state_reward(self.s, action)
            new_state = int(new_state, 2)


            reward = (1-self.alpha) * self.result[self.state][action] + self.alpha * (new_reward + self.gamma*self.result[new_state][self.__most_valued__(new_state)])

            self.result[self.state][action] = reward
            self.state = new_state

            print(f'{i:03} [state/reward]: [{self.state:02}|{new_reward}]\t~\t{reward}')

        if(self.save):
            rs.save(self.result)
    
        
        

    def __most_valued__(self, state) -> str:
        states = self.result[self.state]
        states = dict(sorted(states.items(), key=lambda item: item[1], reverse=True))
        #print(states)
        return str(list(states.keys())[0])
    
    def save(self) -> None:
        rs.save(self.result)

    def load(self) -> None:
        self.result = rs.load()


ql = qLearning(load=True, save=True)
ql.train()

