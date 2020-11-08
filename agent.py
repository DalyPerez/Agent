import random

### Directions ###
North = (-1, 0)
South = (1, 0)
East  = (0, 1)
West  = (0, -1)

class Agent:
    def __init__(self, name, position, direction):
        self.name = name
        self.position = position
        r = random.Random()
        self.direction = direction

    def update_location(self, new_pos, new_dir):
        self.change_position(new_pos)
        self.change_direction(new_dir)

    def change_direction(self, new_dir):
        self.direction = new_dir

    def change_position(self):
        x1, y1 = self.position
        x2, y2 = self.direction
        self.position = (x1 + x2, y1 + y2)

    def do_action(self):
        raise Exception("Not implemented yet !!!")

class Robot (Agent):
    def __init__(self, position, estrategy, direction):
        self.e = estrategy
        self.child_carried = None
        super(Robot, self).__init__("R ", position, direction)

    def is_full(self):
        return self.child_carried != None

    def do_action(self, env):
        print ("do actio from robot")

class Child (Agent):
    def __init__(self, name, position, direction):
        super(Child, self).__init__(name, position, direction)

    def do_action(self, env):
        print ("do actio from child")

