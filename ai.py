"""AI algorithms for learning how to solve the maze"""
from random import randint,choice

from state import State, Q
class AI:
    def __init__(self,window):
        self.window = window
        self.starting_state = self.window.cell_dict[self.window.starting_state_coord]

        self.states = self.window.cell_dict
        self.actions = [(right,down) for right in range(-1,2) for down in range(-1,2) if (right,down) != (0,0)]
        
        self.qs = {}
        self.create_qs()

        self.alpha = 0.15
        self.gamma = 0.8
        self.epsilon = 0.15

        self.episode_num = 0            #to keep track of what episode we are currently on while training

    def run_episode(self):
        steps = 0
        state = self.starting_state
        while True:
            if state.purpose == 'finish':    #end episode if on the terminal state
                break
            steps += 1
            state = self.algorithm(state)
        self.episode_num += 1
        print(f'Episode {self.episode_num} took {steps} steps')

    def algorithm(self,state):
        """preforms the ML algorithm, returning the next state"""
        action = self.get_action(state)
        q = self.get_q(state,action)

        state_prime, reward = self.next_state_reward(state,action)
        q_prime = self.get_q(state,action)

        q.value = q.value + self.alpha*(reward + self.gamma*q_prime.value - q.value)

        return state_prime

    def create_qs(self):
        """fill the qs dict with the state;s coord and the action as a Q's key"""
        for s_coord, state in self.states.items():
            for action in self.actions:
                self.qs[(s_coord,action)] = Q(state,action)

    def get_action(self,state):
        """checks all qs accessible from state and returns best one unless chooses randomly"""
        actions = self.actions[:]
        action_values = [self.qs[(state.coord,action)].value for action in actions]

        max_value = max(action_values)
        ind = action_values.index(max_value)

        max_action = actions.pop(ind)

        if randint(0,1) > self.epsilon:
            return max_action
        else:
            return choice(actions)

    def get_q(self,state,action):
        return self.qs[(state.coord,action)]

    def next_state_reward(self,state,action):
        """returns (next state, reward) given a state-action pair"""
        next_coord = (state.coord[0]+action[0], state.coord[1]+action[1])
        try:
            state_prime = self.states[next_coord]
            reward = state_prime.reward
            if state_prime.purpose == 'wall':       #agent can't enter wall so sends back to in front of wall
                return state, reward
            else:
                return state_prime, reward
        except:
            return state, -1            #assign -1 reward when goes off map, essentially surroounded by walls

class Knowledge:
    """will use for saving the AI's knowledge of a specific map"""
    def __init__(self,qs,episode):
        self.qs = qs
        self.episode = episode