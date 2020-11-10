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
        if self.iter == 100 or self.env.dirty_porcent() >= 60 or (self.env.dirty_porcent() == 0 and self.env.all_childs_in_guard()):
            return True
        return False

    def run(self):
        while (not self.end_simulation()):
            print("---Iteration #", self.iter, "---")
            print("all_childs_in_guard: ", self.env.all_childs_in_guard())
            print("-> Bot Turn")
            self.bot.do_action(self.env)
            print("-> Childs turn")
            for c in self.childs.values():
                if c.is_active:
                    c.do_action(self.env)
            self.iter = self.iter + 1
            print(self.env)
            # input()
        return self.end_simulation()
         

if __name__ == '__main__':
    for i in range (100):
        sim = Simulator()
        sim.init_world(2, 5, 5, 10, 10, 4)
        print(sim.env)
        print("START SIMULATION")
        sim.run()