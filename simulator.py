from environment import *

class Simulator:
    def __init__(self):
        self.t = 0
        self.turn = 0
        self.iter = 0
        self.env = None
        self.bot = None
        self.childs = {}

    def init_world(self, t, N, M, dirty_porcent, obstacle_porcent, num_childs):
        self.t = t
        self.env = Environment(t, N, M)
        self.bot, self.childs = self.env.create_map(N, M, dirty_porcent, obstacle_porcent, num_childs)
        
    def end_simulation(self):
        pass
    
    def run(self):
        while (self.iter < 10):
            print("---Iteration #", self.iter, "---")
            print("-> Bot Turn")
            self.bot.do_action(self.env)
            print("-> Childs turn")
            for c in self.childs.values():
                c.do_action(self.env)
            self.iter = self.iter + 1
            print(self.env)

if __name__ == '__main__':
    sim = Simulator()
    sim.init_world(2, 5, 5, 15, 15, 1)
    print(sim.env)
    sim.run()