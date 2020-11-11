import random
from tools import *

rnd = random.Random()

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
        pass

class Robot (Agent):
    FIND  = "F"
    SAVE  = "S"
    ClEAN = "C"
    def __init__(self, position):
        self.child_carried = None
        super(Robot, self).__init__("R ", position)

    def has_child(self):
        return self.child_carried != None

    def posible_movements(self, env):
        ady = env.get_adyacents(self.position)
        choices = []
        for p in ady:
            direction = rest_positions(p, self.position)
            if env.robot_CanMove(self, self.position, direction):
                choices.append(direction)
        return choices
    
    def select_direction(self, env):
        posible_choices = self.posible_movements(env)
        r = random.Random()
        return r.choice(posible_choices)

    def move(self, env):
        posible_step = [1, 2] if self.has_child() else [1]
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
        env.clean(self.position)

    def do_action(self, env):
        bot_cell = env.get_position(self.position)
        posible_action = [ self.move ]
        if bot_cell.is_dirty():
            posible_action.append(self.clean_cell)
        if self.has_child() and bot_cell.is_guard():
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
        if len(posible_choices) == 0:
            posible_choices = [(0, 0)]
        r = random.Random()
        return r.choice(posible_choices)

    def move(self, env):
        direction = self.select_direction(env)
        new_pos = sum_positions(self.position, direction)
        print("Child", self.name,  " moved from position ", self.position, "to ", new_pos )
        env.move_child(self, direction)

    def pollute(self, env):
        env.generate_dirt(self)
    
    def do_action(self, env):
        do = self.move(env)
        env.generate_dirt(self)
       
class ProtectRobot(Robot):
    """
    This robot prioritizes taking children to the corral
    """
    def __init__(self, position):
        super(ProtectRobot, self).__init__(position)
        self.state = Robot.FIND
    
    def select_direction(self, env):
        print ('select direction from protect robot')
        f = None
        if self.state == Robot.ClEAN:
            print('cleaning')
            f = lambda x: x.is_dirty()
        elif self.state == Robot.SAVE:
            print('saving a boy')
            f = lambda x: x.is_guard() and (not x.is_full())
        else:
            print ('finding a boy')
            f = lambda x : x.is_full() and isinstance(x.obj, Child) and not x.is_guard()
        d = bfs(env, self.position[0], self.position[1], self, f)
        if d == None:
            posible_choices = self.posible_movements(env)
            if len(posible_choices) == 0: #state in place
                posible_choices = [(0, 0)]
            d = rnd.choice(posible_choices)
        return d

    def move(self, env):
        step = 2 if self.has_child() else 1
        for _ in range(step):
            direction = self.select_direction(env)
            new_pos = sum_positions(self.position, direction)
            print("Bot moved from position ", self.position, "to ", new_pos )
            env.move_robot(self, direction)
            if env.get_position(new_pos).is_guard():
                break

    def do_action(self, env):
        if env.all_childs_in_guard():
            self.state = Robot.ClEAN
        elif self.has_child():
            self.state = Robot.SAVE
        else:
            self.state = Robot.FIND
        bot_cell = env.get_position(self.position)
        posible_action = []
        action = None
        if not (self.state == Robot.ClEAN and bot_cell.is_dirty()):
            action = self.move
        if (not self.state == Robot.SAVE) and bot_cell.is_dirty():
            action = self.clean_cell
        if self.state == Robot.SAVE and bot_cell.is_guard():
            action = self.drop_child
        return action(env)
    
class CleanerRobot(Robot):
    """
    This robot prioritizes clean the house
    """
    def __init__(self, position):
        super(CleanerRobot, self).__init__(position)
        self.state = Robot.ClEAN
    
    def select_direction(self, env):
        print ('select direction from cleaner robot')
        f = None
        if self.state == Robot.SAVE:
            print('saving a boy')
            f = lambda x: x.is_guard() and (not x.is_full())
        elif self.state == Robot.ClEAN: # by default clean
            print('cleaning')
            f = lambda x: x.is_dirty()
        
        d = bfs(env, self.position[0], self.position[1], self, f)
        if d == None:
            posible_choices = self.posible_movements(env)
            if len(posible_choices) == 0:
                posible_choices = [(0, 0)]
            d = rnd.choice(posible_choices)
        return d

    def move(self, env):
        step = 2 if self.has_child() else 1
        for _ in range(step):
            direction = self.select_direction(env)
            new_pos = sum_positions(self.position, direction)
            print("Bot moved from position ", self.position, "to ", new_pos )
            env.move_robot(self, direction)
            if env.get_position(new_pos).is_guard():
                break

    def do_action(self, env):
        if self.has_child():
            self.state = Robot.SAVE
        else:
            self.state = Robot.CLEAN
        bot_cell = env.get_position(self.position)
        action = None
        if not (self.state == Robot.ClEAN and bot_cell.is_dirty()):
            action = self.move
        if (not self.state == Robot.SAVE) and bot_cell.is_dirty():
            action = self.clean_cell
        if self.state == Robot.SAVE and bot_cell.is_guard():
            action = self.drop_child
        return action(env)
    


   

