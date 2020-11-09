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

    def update_location(self, new_pos):
        self.change_position(new_pos)

    def select_direction(self):
        r = random.Random()
        return r.choice([North, South, East, West])

    def change_position(self, direction):
        x1, y1 = self.position
        x2, y2 = direction
        self.position = (x1 + x2, y1 + y2)

    def do_action(self):
        raise Exception("Not implemented yet !!!")

class Robot (Agent):
    def __init__(self, position, estrategy):
        self.e = estrategy
        self.child_carried = None
        super(Robot, self).__init__("R ", position)

    def is_full(self):
        return self.child_carried != None

    def move(self, env):
        direction = self.select_direction()
        if env.robot_CanMove(self.position, direction):
            env.move_robot(self, direction)
            return direction
        return None

    def do_action(self, env):
        do = self.move(env)
        if do != None:
            print("Robot change position")
        else:
            print("Robot dont move")

class Child (Agent):
    def __init__(self, name, position):
        super(Child, self).__init__(name, position)

    def move(self, env):
        direction = self.select_direction()
        if env.child_CanMove(self.position, direction):
            env.move_child(self, direction)
            return direction
        return None

    def do_action(self, env):
        do = self.move(env)
        if do != None:
            print("Child change position")
        else:
            print("Child dont move")

   

