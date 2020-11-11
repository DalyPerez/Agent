from environment import *

class Simulator:
    def __init__(self):
        self.t = None
        self.iter = 0
        self.env = None
        self.bot = None
        self.childs = {}

    def init_world(self, t, N, M, dirty_porcent, obstacle_porcent, num_childs):
        self.t = t
        self.env = Environment(t, N, M)
        num_of_dirty = int(N * M * dirty_porcent * 0.01)
        num_of_obs = int(N * M * obstacle_porcent * 0.01)
        r = random.Random()
        bot_pos = (r.choice(range(N)), r.choice(range(M)))
        
        self.bot, self.childs = self.env.restart_map(N, M, bot_pos, False, num_of_dirty, num_of_obs, num_childs, 0 )
    
    def random_variation_world(self):
        self.bot, self.childs = self.env.random_variation(self.bot.position)

    def end_simulation(self):
        if self.iter == 100 or self.env.dirty_porcent() >= 60 or (self.env.dirty_porcent() == 0 and self.env.all_childs_in_guard()):
            return True
        return False

    def run(self):
        while (True):
            if self.end_simulation():
                break
            print("---Iteration #", self.iter, "---")
            
            print("-> Bot Turn")
            self.bot.do_action(self.env)
            
            print("-> Childs turn")
            for c in self.childs.values():
                if c.is_active:
                    c.do_action(self.env)
            

            if (self.iter % self.t) == 0:
                print("-------------Random Variation----------")
                print(self.env)
                # input()
                self.random_variation_world()
                print(self.env)
                # input()

            self.iter = self.iter + 1
            print(self.env)
            # input()
        return self.end_simulation()
         
    def simulate(self):
        pass

if __name__ == '__main__':
    for i in range (100):
        sim = Simulator()
        sim.init_world(40, 5, 5, 10, 10, 2)
        print(sim.env)
        print("START SIMULATION")
        sim.run()
