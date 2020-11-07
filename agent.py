import random

### Directions ###
North = (-1, 0)
South = (1, 0)
East  = (0, 1)
West  = (0, -1)

class Agent:
    def __init__(self, name, position):
        self.name = name
        self.position = position
        r = random.Random()
        self.direction = r.choice([North, South, East, West])

    def update_location(self, new_pos, new_dir):
        self.change_position(new_pos)
        self.change_direction(new_dir)

    def change_direction(self, new_dir):
        self.direction = new_dir

    def change_position(self):
        self.position = self.position + self.direction

    def do_action(self):
        raise Exception("Not implemented yet !!!")

class Robot (Agent):
    def __init__(self, position, estrategy):
        self.e = estrategy
        self.child_carried = None
        super(Robot, self).__init__("R ", position)

    def is_full(self):
        return self.child_carried != None

    def do_action(self, env):
        print ("do actio from robot")

class Child (Agent):
    def __init__(self, name, position):
        super(Child, self).__init__(name, position)

    def do_action(self, env):
        print ("do actio from child")

