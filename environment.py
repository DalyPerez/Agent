import random
from agent import Agent, Child, Robot, North, South, East, West

######## Env set ########
GUARD    = "G"
EMPTY    = "E"
DIRTY    = "D"
OBSTACLE = "O"

class Cell:
    def __init__(self, i, j, floor):
        self.floor = floor
        self.p     = (i, j)
        self.obj   = None

    def is_full(self):
        return self.obj != None

    def release(self):
        self.obj = None

    def acquire(self, obj):
        self.obj = obj

    def set_dirty(self):
        self.floor = DIRTY
    
    def is_dirty(self):
        return self.floor == DIRTY

    def clean(self):
        self.floor = EMPTY

    def create_obstacle(self):
        self.floor = OBSTACLE
    
    def is_obstacle(self):
        return self.floor == OBSTACLE

    def is_empty(self):
        return self.floor == EMPTY

    def is_guard(self):
        return self.floor == GUARD

    def __str__(self):
        if self.is_full():
            return self.obj.name
        else:
            return self.floor + ' '

class Environment:
    def __init__(self, t, N, M):
        self.t = t
        self.map = [[None for j in range(M)] for i in range(N)]
        self.time = 0
        self.total = N * M
        self.N = N
        self.M = M
        self.empty_cells = []
        self.childs = {}
        self.bot = None
 

    def create_map(self, N, M, dirty_porcent, obstacle_porcent, num_childs):
        num_of_dirty = int(self.total * dirty_porcent * 0.01)
        num_of_obs = int(self.total * obstacle_porcent * 0.01)
        r = random.Random()
        
        # set cell for creation map
        cell = set([(i,j) for i in range(N) for j in range(M)])
        
        # dirty cell
        dirty_cell = r.sample(cell, num_of_dirty)
        cell = cell.difference(dirty_cell)

        # obs cell
        obs_cell = r.sample(cell, num_of_obs)
        cell = cell.difference(obs_cell)

        # guard cell
        guard_cell = r.sample(cell, num_of_obs)
        cell = cell.difference(guard_cell)

        # create cells for each type
        types = [EMPTY, DIRTY, OBSTACLE, GUARD]
        creation_cell = [cell, dirty_cell, obs_cell, guard_cell]
        for i in range(len(types)):
            for p in creation_cell[i]:
                x, y = p
                self.map[x][y] = Cell(x, y, types[i])

        # set child location
        childs_pos = r.sample(cell, num_childs)
        cell = cell.difference(childs_pos)

        for i in range(len(childs_pos)):
            name = f'C{i}' 
            pos = childs_pos[i]
            c_dir = r.choice([North, South, East, West])
            c = Child(name, pos, c_dir)
            self.childs[name] = c
            self.get_position(pos).acquire(c)
        
        # set robot position
        bot_pos = r.sample(cell, 1)[0]
        bot_dir = r.choice([North, South, East, West])
        self.bot = Robot(bot_pos, None, bot_dir)
        self.get_position(bot_pos).acquire(self.bot)

    def load_map(self, board):
        self.N = len(board)
        self.M = len(board[0])
        self.map = [[None for j in range(self.M)] for i in range(self.N)]

        for i in range(self.N):
            for j in range(self.M):
                item = board[i][j]
                if item == 'E':
                    cell = Cell(i, j, EMPTY)
                elif item == 'O':
                    cell = Cell(i, j, OBSTACLE)
                elif item == 'G':
                    cell = Cell(i, j, GUARD)
                elif item == 'R':
                    cell = Cell(i, j, EMPTY)
                    self.bot = Robot((i, j), None,  (0, 1) )
                    cell.acquire(self.bot)
                else:
                    cell = Cell(i, j, EMPTY)
                    child = Child(item, (i, j), (1, 0))
                    self.childs[item] = child
                    cell.acquire(child)
                self.map[i][j] = cell

    def inc_time(self):
        self.time = self.time + 1

    def set_position(self, p, obj):
        x, y = p
        self.map[x][y] = obj

    def get_position(self, p):
        x, y = p
        return self.map[x][y]

    def is_valid_position(self, p):
        x, y = p
        return 0 <= x < self.N and 0 <= y < self.M
    
    def sum_positions(self, p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        return (x1 + x2, y1 + y2)

    def robot_CanMove(self, bot):
        p = self.sum_positions(bot.position, bot.direction)
        if self.is_valid_position(p):
            cell = self.get_position(p)
            if cell.is_obstacle() or (cell.is_guard() and cell.is_full()):
                return False
            return True
        return False

    def child_CanMove(self, child):
        p = self.sum_positions(child.position, child.direction)
        if self.is_valid_position(p):
            cell = self.get_position(p)
            if (cell.is_empty() and not cell.is_full()) or cell.is_obstacle():
                return True
            else:
                return False
        return False

    def move_robot(self, bot):
        bot_cell = self.get_position(bot.position)
        bot_cell.release()
        bot.change_position()
        if bot.is_full():
            bot.child_carried.update_location(bot.position, bot.direction)
        new_cell = self.get_position(bot.position)
        new_cell.acquire(bot)
    
    def move_child(self, child):
        child_cell = self.get_position(child.position)
        new_cell = self.get_position(self.sum_positions(child.position, child.direction))
        if new_cell.is_empty():
            child_cell.release()
            child.change_position()
            new_cell.acquire(child)
        elif new_cell.is_obstacle():
            can_push = False
            next_p = self.sum_positions(new_cell.p, child.direction)
            while self.is_valid_position(next_p):
                next_cell = self.get_position(next_p)
                if next_cell.is_empty():
                    can_push = True
                    break
                elif next_cell.is_obstacle():
                    next_p = self.sum_positions(next_cell.p, child.direction)
                else:
                    break
            if can_push:
                child.change_position()
                child_cell.floor = EMPTY
                child_cell.release()
                new_cell.floor = EMPTY
                new_cell.acquire(child)
                next_p = self.sum_positions(new_cell.p, child.direction)
                while True:
                    last_cell = self.get_position(next_p)
                    if last_cell.is_empty():
                        last_cell.floor = OBSTACLE
                        break
                    next_p = self.sum_positions(last_cell.p, child.direction)

    def __str__(self):
        s = ""
        for i in range(self.N):
            s += str(([ str(self.map[i][j]) for j in range(self.M) ])) + "\n"
        return s

board = [['E'], ['R'], ['G'], ['O'], ['E']]
env = Environment(2, 5, 1)
env.load_map(board)
print(env)

if env.robot_CanMove(env.bot):
    env.move_robot(env.bot)
    print(env)
else:
    print(False)



