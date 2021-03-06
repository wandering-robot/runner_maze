"""AI algorithms for learning how to solve the maze"""
from random import random,choice
import pygame as py

from state import State, Action, Q
class AI:
    """object that learns from trial and error using RL algorithms"""
    def __init__(self,window):
        self.window = window
        self.starting_state = self.window.cell_dict[self.window.starting_state_coord]

        self.states = self.window.cell_dict
        self.actions = self.create_actions()
        
        self.qs = {}
        self.create_qs()

        self.alpha = self.window.main.alpha
        self.gamma = self.window.main.gamma
        self.epsilon = self.window.main.epsilon
        self.lamda = self.window.main.lamda
        self.E_eq = self.window.main.E_eq
        self.eq = self.get_eq()

        self.episode_num = 0            #to keep track of what episode we are currently on while training

    def get_eq(self):
        """input is the q's eligibility, outputs q's new eligibility"""
        if self.E_eq == 'a':
            return lambda x: self.gamma*self.lamda*x + 1
        elif self.E_eq == 'r':
            return lambda x: 1
        elif self.E_eq == 'd':
            return lambda x: (1-self.alpha)*self.gamma*self.lamda*x +1

    def run_episode(self):
        """preforms algorithm based on which subclass is loaded in the window, stops once hits terminal, returns steps taken to hit terminal"""
        steps = 0
        state = self.starting_state
        while True:
            if state.purpose == 'finish':    #end episode if on the terminal state
                break
            steps += 1
            state = self.algo(state)
        self.episode_num += 1
        return steps

    def create_actions(self):
        """creates list of all actions that AI can take"""
        return [Action(del_row,del_col) for del_row in range(-1,2) for del_col in range(-1,2) if (del_row,del_col) != (0,0)]

    def get_similar_qs(self,state_coord,q):
        """returns a list other qs that would lead to that state, so
         that the reward can be destributed to all of them"""
        similar_qs = []
        for action in self.actions:
            try:
                pre_state = self.states[(state_coord[0] - action[0], state_coord[1] - action[1])]       #by subtracting action it goes backwards
                pre_q = self.get_q(pre_state,action)
                if pre_q != q and pre_state.purpose == None:
                    similar_qs.append(pre_q)
            except:
                continue
        return similar_qs

    def distribute2similar(self,state,state_prime,q,q_prime,action,reward):
        """uses get similar qs and distributes the reward to all similars"""
        if state != state_prime:
            similar_qs = self.get_similar_qs(state_prime.coord,q)   #should normally do this
        else:
            similar_qs = self.get_similar_qs((state.coord[0]+action[0],state.coord[1]+action[1]),q) #if hits something, state stays same. need to project out-of-map/into-wall 
        for pre_q in similar_qs:
            self.update_q_value(pre_q,q_prime,reward)

    def update_q_value(self,q,q_prime,reward):
        """Update rule derived from the Bellman Equation"""
        q.value = q.value + self.alpha*(reward + self.gamma*q_prime.value - q.value)

    def create_qs(self):
        """fill the qs dict with the state;s coord and the action as a Q's key"""
        for s_coord, state in self.states.items():
            for action in self.actions:
                self.qs[(s_coord,action.tup)] = Q(state,action)

    def get_action(self,state):
        """checks all qs accessible from state and returns best one unless chooses randomly"""
        actions = self.actions[:]
        action_values = [self.qs[(state.coord,action.tup)].value for action in actions]

        max_value = max(action_values)
        max_actions = []
        for ind in range(len(actions)):
            if action_values[ind] == max_value:
                max_actions.append(actions[ind])

        randnum = random()
        if randnum > self.epsilon:
            return choice(max_actions)
        else:
            return choice(actions)

    def get_best_action(self,state):
        """checks all qs accessible from state and returns best one unless chooses randomly"""
        actions = self.actions[:]
        action_values = [self.qs[(state.coord,action.tup)].value for action in actions]

        max_value = max(action_values)
        max_actions = []
        for ind in range(len(actions)):
            if action_values[ind] == max_value:
                max_actions.append(actions[ind])

        return choice(max_actions)

    def get_q(self,state,action):
        return self.qs[(state.coord,action.tup)]

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
            return state, -5            #assign -1 reward when goes off map, essentially surroounded by walls

class EligML(AI):
    def __init__(self,window):
        super().__init__(window)
        self.eligibles = []

    def algo(self,state):
        """preforms the td(lambda) algorithm, returning the next state"""
        action = self.get_action(state)
        q = self.get_q(state,action)
        self.make_eligible(q)

        state_prime, reward = self.next_state_reward(state,action)
        action_prime = self.get_best_action(state_prime)
        q_prime = self.get_q(state_prime,action_prime)

        self.distribute2similar(state,state_prime,q,q_prime,action,reward)
        delta = reward + self.gamma*q_prime.value - q.value
        q.elig = self.eq(q.elig)

        self.distribute_reward(delta)
        self.clean_eligibles()

        return state_prime

    def distribute_reward(self,delta):
        """distributes the reward to every eligible state action pair"""
        for q in self.eligibles:
            q.value += self.alpha*delta*q.elig
            q.elig = self.gamma*self.lamda*q.elig

    def clean_eligibles(self):
        """removes state action pairs form eligibles if their eligibilty drops below 0.005"""
        for q in self.eligibles.copy():
            if q.elig < 0.005:
                self.eligibles.remove(q)

    def make_eligible(self,q):
        """adds a q to the eligibles list"""
        self.eligibles.append(q)


class BasicML(AI):
    def __init__(self,window):
        super().__init__(window)

    def algo(self,state):
        """preforms the ML algorithm, returning the next state"""
        action = self.get_action(state)
        q = self.get_q(state,action)

        state_prime, reward = self.next_state_reward(state,action)
        action_prime = self.get_action(state_prime)
        q_prime = self.get_q(state_prime,action_prime)

        self.update_q_value(q,q_prime,reward)
        self.distribute2similar(state,state_prime,q,q_prime,action,reward)

        return state_prime

    def update_q_value(self,q,q_prime,reward):
        """Update rule derived from the Bellman Equation"""
        q.value = q.value + self.alpha*(reward + self.gamma*q_prime.value - q.value)


class Knowledge:
    """will use for saving the AI's knowledge of a specific map"""
    def __init__(self,qs,episode):
        self.qs = qs
        self.episode = episode

class Runner(AI):
    """object that solves a maze using previously generated knowledge"""
    def __init__(self,window):
        self.window = window
        self.knowledge_list = self.window.knowledge
        self.size = self.window.cell_size
        self.colour = (255,0,255)

        self.starting_state = self.window.starting_state
        self.states = self.window.cell_dict
        self.actions = super().create_actions()
        self.epsilon = 0

        py.init()
        self.body = py.Surface((self.size,self.size)).convert()
        self.body.fill(self.colour)

        self.pos = self.starting_state.coord
        self.i = 0
        self.knowledge = self.knowledge_list[self.i]
        self.qs = self.knowledge.qs
        self.re_green(self.qs,self.window.cell_dict)


    def is_terminal(self):
        """return true if the ai made it to the terminal state"""
        return self.states[self.pos].purpose == 'finish'

    def quit_iter(self):
        """quit this current iteration and move on to the next one"""
        self.pos = self.starting_state.coord
        self.next_knowledge()
    
    def next_knowledge(self):
        """move to next knowledge iteration, terminate if no more"""
        self.i += 1
        try:
            self.knowledge = self.knowledge_list[self.i]
            self.qs = self.knowledge.qs
            self.re_green(self.qs,self.window.cell_dict)
        except:
            py.quit()
            self.window.running = False
            self.window.grapher.data_terminate()

    def re_green(self,qs,cell_dict):
        """iterate through all states ascribing them values as determined by the Ai's 
        current state-action pair knowledge. Then change their green-ness based on value"""
        state_values = []
        for state in cell_dict.values():
            #skip all walls etc
            if state.purpose != None:
                continue
            actions = self.actions[:]
            action_values = [self.qs[(state.coord,action.tup)].value for action in actions]
            action_num = len(action_values)

            max_value = max(action_values)
            action_values.remove(max_value)

            #create state.value and incrementally increase it's expected value
            state.value = 0
            for value in action_values:
                state.value += value*(self.epsilon/action_num)
            state.value += max_value*(1 - self.epsilon)

            state_values.append(state.value)

        max_value = max(state_values)
        min_value = min(state_values)

        #go through and actually 
        for state in cell_dict.values():
            if state.purpose != None:
                continue
            state.re_green(max_value,min_value)

    def move(self):
        """process of moving avatar to next state based on it's current maze knowledge"""
        state = self.window.cell_dict[self.pos]
        if not self.is_terminal():
            action = self.get_best_action(state)
            state_prime, _ = super().next_state_reward(state,action)
            self.show_damage(state,state_prime)
            self.pos = state_prime.coord
        else:
            self.quit_iter()

    def show_damage(self,state,state_prime):
        """make the avatar red when it runs in to a wall"""
        if state == state_prime:
            self.colour = (255,0,0)
        else:
            self.colour = (255,0,255)
        self.body.fill(self.colour)