import random
from tools import *

rnd = random.Random()

### Directions ###
North = (-1, 0)
South = (1, 0)
East  = (0, 1)
West  = (0, -1)

class Agent:
    def __init__(self, name, position):
        self.name = name
        self.position = position
        self.is_active = True

    def update_location(self, new_pos):
        self.change_position(new_pos)

    def change_position(self, direction):
        x1, y1 = self.position
        x2, y2 = direction
        self.position = (x1 + x2, y1 + y2)
    
    def posible_movements(self, env):
        pass

    def select_direction(self, env):
        pass

    def do_action(self):
        raise Exception("Not implemented yet !!!")

class Robot (Agent):
    def __init__(self, position, estrategy):
        self.e = estrategy
        self.child_carried = None
        super(Robot, self).__init__("R ", position)

    def is_full(self):
        return self.child_carried != None

    def posible_movements(self, env):
        ady = env.get_adyacents(self.position)
        choices = []
        for p in ady:
            direction = rest_positions(p, self.position)
            if env.robot_CanMove(self.position, direction):
                choices.append(direction)
        return choices
    
    def select_direction(self, env):
        posible_choices = self.posible_movements(env)
        r = random.Random()
        return r.choice(posible_choices)

    def move(self, env):
        posible_step = [1, 2] if self.is_full() else [1]
        step = rnd.choice(posible_step)
        for _ in range(step):
            direction = self.select_direction(env)
            new_pos = sum_positions(self.position, direction)
            print("Bot moved from position ", self.position, "to ", new_pos )
            env.move_robot(self, direction)
          
        

    def drop_child(self, env):
        print("Bot drop child ", self.child_carried.name)
        guard_cell = env.get_position(self.position)
        guard_cell.obj = self.child_carried
        self.child_carried = None

    def clean_cell(self, env):
        print("Bot clean cell ", self.position)
        guard_cell = env.get_position(self.position)
        guard_cell.clean()

    def do_action(self, env):
        bot_cell = env.get_position(self.position)
        posible_action = [ self.move ]
        if bot_cell.is_dirty():
            posible_action.append(self.clean_cell)
        if self.is_full() and bot_cell.is_guard():
            posible_action.append(self.drop_child)
        action = rnd.choice(posible_action)
        return action(env)


class Child (Agent):
    def __init__(self, name, position):
        super(Child, self).__init__(name, position)
        self.is_carried = False 

    def posible_movements(self, env):
        ady = env.get_adyacents(self.position)
        choices = []
        for p in ady:
            direction = rest_positions(p, self.position)
            if env.child_CanMove(self.position, direction):
                choices.append(direction)
        return choices
    
    def select_direction(self, env):
        posible_choices = self.posible_movements(env)
        r = random.Random()
        return r.choice(posible_choices)

    def move(self, env):
        direction = self.select_direction(env)
        new_pos = sum_positions(self.position, direction)
        print("Child", self.name,  " moved from position ", self.position, "to ", new_pos )
        env.move_child(self, direction)
    
    def do_action(self, env):
        do = self.move(env)
       

   

