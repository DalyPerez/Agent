from environment import *
from agent import CleanerRobot, ProtectRobot

class Simulator:
    def __init__(self):
        self.t = None
        self.N = None
        self.M = None
        self.iter = 0
        self.env = None
        self.bot = None
        self.childs = {}
        self.statistics = {"STOP": 0, "FIRE": 0, "DONE": 0, "DIRTY": 0}

    def init_world(self, t, N, M, dirty_porcent, obstacle_porcent, num_childs, bot_type):
        self.t = t
        self.N = N
        self.M = M
        self.iter = 0
        self.env = Environment(t, N, M)
        total = N * M - 2*num_childs - 1
        num_of_dirty = int(total * dirty_porcent * 0.01)
        num_of_obs = int(total * obstacle_porcent * 0.01)
        r = random.Random()
        bot_pos = (r.choice(range(N)), r.choice(range(M)))
        bot = bot_type(bot_pos)
        
        self.bot, self.childs = self.env.restart_map(N, M, bot, num_of_dirty, num_of_obs, num_childs )

    def random_variation_world(self):
        self.childs = self.env.random_variation(self.bot)

    def end_simulation(self):
        if self.iter == 100 * self.t :
            self.env.final_state = "STOP"
            self.statistics["STOP"] += 1
            self.statistics["DIRTY"] += self.env.dirty_porcent()
            return True
        elif self.env.dirty_porcent() >= 60:
            self.env.final_state = "FIRE"
            self.statistics["FIRE"] += 1
            self.statistics["DIRTY"] += self.env.dirty_porcent()
            return True
        elif self.env.dirty_porcent() == 0 and self.env.all_childs_in_guard():
            self.env.final_state = "DONE"
            self.statistics["DONE"] += 1
            self.statistics["DIRTY"] += self.env.dirty_porcent()
            return True
        return False

    def run(self):
        while (True):
            if self.end_simulation():
                print(self.env.final_state)
                print(self.statistics)
                break
            # print("---Iteration #", self.iter, "---")
            # print("-> Bot Turn")
            self.bot.do_action(self.env)
            
            # print("-> Childs turn")
            for c in self.childs.values():
                if c.is_active:
                    c.do_action(self.env)
            
            # print(self.env)
    
            if ((self.iter + 1 ) % self.t ) == 0:
                # print("-------------Random Variation----------")
                self.random_variation_world()
                # print(self.env)

            self.iter = self.iter + 1
 
         
def simulate(iterations, t, N, M, dirty_porcent, obst_porcent, num_childs, bot_type):
    s = Simulator()
    for i in range(iterations):
        s.init_world(t, N, M, dirty_porcent, obst_porcent, num_childs, bot_type)
        # print(s.env)
        print("START SIMULATION : ", i)
        s.run()
    "------------------SIMULATION RESULTS----------------"
    print("number of layoffs: ", s.statistics["FIRE"])
    print("number of stop in iteration 100 : ", s.statistics["STOP"])
    print("number of goal accomplished: ", s.statistics["DONE"])
    print("average percentage of dirt: ", s.statistics["DIRTY"] / iterations)
    
    

if __name__ == '__main__':
    t = 100
    N = 30
    M = 3
    D = 5
    O = 20
    C = 2
    # bot_type = Robot
    # simulate(30, t, N, M, D, O, C, bot_type)
    # input()

    # bot_type = ProtectRobot
    # simulate(30, t, N, M, D, O, C, bot_type)
    # input()

    bot_type = CleanerRobot
    simulate(30, t, N, M, D, O, C, bot_type)

    
