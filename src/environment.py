import random
from agent import Agent, Child, Robot, ProtectRobot, CleanerRobot, North, South, East, West
from tools import *

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
        self.total = N * M
        self.N = N
        self.M = M
        self.dirty_cells = 0
        self.obst_cells = 0
        self.guards = []
        self.final_state = None

    def restart_map(self, N, M, bot, bot_has_child, num_of_dirty, num_of_obst, num_childs, childs_in_guard):
        r = random.Random()
        self.guards = []
        self.dirty_cells = num_of_dirty
        self.obst_cells = num_of_obst
        
        # set cells for creation map
        cell = set([(i,j) for i in range(N) for j in range(M)])
        cell = cell.difference([bot.position])

        # ubicate guards
        first_guard = r.sample(cell, 1)[0]
        self.consecutive_guards(first_guard[0], first_guard[1], num_childs, self.guards, bot.position )
        cell = cell.difference(self.guards)

        # select the guards with childs
        guards_with_childs = []
        for c in range(childs_in_guard):
            child_cell = self.guards[c]
            guards_with_childs.append(child_cell)

        # dirty cell
        dirty_cell = r.sample(cell, num_of_dirty)
        cell = cell.difference(dirty_cell)

        # obs cell
        obs_cell = r.sample(cell, num_of_obst)
        cell = cell.difference(obs_cell)

        # create cells for each type
        types = [EMPTY, DIRTY, OBSTACLE, GUARD, EMPTY]
        creation_cell = [cell, dirty_cell, obs_cell, self.guards, [bot.position]]
        for i in range(len(types)):
            for p in creation_cell[i]:
                x, y = p
                self.map[x][y] = Cell(x, y, types[i])

        # set childs to the guards
        i = 0
        childs = {}
        for p in guards_with_childs:
            name = f'C{i}' 
            i += 1
            c = Child(name, p)
            self.get_position(p).acquire(c)
            childs[name] = c

        # set child location
        rest_childs = num_childs - childs_in_guard
        if bot_has_child:
            rest_childs -= 1
        childs_pos = r.sample(cell, rest_childs)
        cell = cell.difference(childs_pos)

        for j in range(rest_childs):
            name = f'C{i + j}' 
            pos = childs_pos[j]
            c = Child(name, pos)
            childs[name] = c
            self.get_position(pos).acquire(c)

        # set bot to the map 
        if bot_has_child:
            c = Child(f'C{len(self.guards)}', bot.position)
            bot.child_carried = c
        self.get_position(bot.position).acquire(bot)

        return bot, childs

    def load_map(self, board):
        self.N = len(board)
        self.M = len(board[0])
        self.map = [[None for j in range(self.M)] for i in range(self.N)]
        childs = {}

        for i in range(self.N):
            for j in range(self.M):
                item = board[i][j]
                if item == 'E':
                    cell = Cell(i, j, EMPTY)
                elif item == 'D':
                    cell = Cell(i, j, DIRTY)
                    self.dirty_cells += 1
                elif item == 'O':
                    cell = Cell(i, j, OBSTACLE)
                elif item == 'G':
                    cell = Cell(i, j, GUARD)
                elif item == 'R':
                    cell = Cell(i, j, EMPTY)
                    bot = Robot((i, j))
                    cell.acquire(bot)
                else:
                    cell = Cell(i, j, EMPTY)
                    child = Child(item, (i, j))
                    childs[item] = child
                    cell.acquire(child)
                self.map[i][j] = cell
        return bot, childs

    def ubicate_guard(self, num_childs, N):
        positions = []
        current_pos = (0, 0)
        direction = (1, 0)
        count = 0
        while num_childs > 0:
            positions.append(current_pos)
            num_childs -= 1
            count += 1
            if count == N:
                   direction = (0, 1)
            current_pos = sum_positions(current_pos, direction)
        return positions 

    def consecutive_guards(self, x, y, cant_childs, guards, bot_pos):
        guards.append((x, y))
        if cant_childs == 1:
            return 1
        cant_childs -= 1
        possible = []
        for d in [North, South, East, West]:
            p = sum_positions((x, y), d)
            if self.is_valid_position(p) and not (p in guards) and p != bot_pos:
                possible.append(p)
        r = random.Random()
        r.shuffle(possible)
        solve = 1
        for p in possible:
            c = self.consecutive_guards(p[0], p[1], cant_childs, guards, bot_pos)
            cant_childs -= c
            solve += c
            if cant_childs == 0: break
        return solve
        
    def dirty_porcent(self):
        return (self.dirty_cells * 100) / self.total

    def set_position(self, p, obj):
        x, y = p
        self.map[x][y] = obj

    def get_position(self, p):
        x, y = p
        return self.map[x][y]

    def is_valid_position(self, p):
        x, y = p
        return 0 <= x < self.N and 0 <= y < self.M
    
    def get_adyacents(self, pos):
        ady = []
        for dir in [North, South, East, West]:
            p = sum_positions(pos, dir)
            if self.is_valid_position(p):
                ady.append(p)
        return ady

    def all_childs_in_guard(self):
        for pos in self.guards:
            guard_cell = self.get_position(pos)
            if (not guard_cell.is_full()) or (not isinstance(guard_cell.obj, Child)):
                return False
        return True

    def cant_childs_in_guards(self):
        count = 0
        for pos in self.guards:
            guard_cell = self.get_position(pos)
            if guard_cell.is_full() and isinstance(guard_cell.obj, Child):
                count += 1
        return count

    def robot_CanMove(self, bot, p, direction):
        new_pos = sum_positions(p, direction)
        return self.robot_CanMoveAnyWhere(bot, p, new_pos)

    def robot_CanMoveAnyWhere(self, bot, p, new_pos):
        if self.is_valid_position(new_pos):
            cell = self.get_position(new_pos)
            # not move if the cell contain an obstacle or is a guard with child or is a child and the bot have another child 
            if cell.is_obstacle() or (cell.is_full() and (cell.is_guard() or bot.has_child())):
                return False
            return True
        return False

    def child_CanMove(self, p, direction):
        new_pos = sum_positions(p, direction)
        if self.is_valid_position(new_pos):
            cell = self.get_position(new_pos)
            if (cell.is_empty() and not cell.is_full()) or cell.is_obstacle():
                return True
            else:
                return False
        return False

    def move_robot(self, bot, direction):
        bot_cell = self.get_position(bot.position)
        if isinstance(bot_cell.obj, Robot):
            bot_cell.release()
        bot.change_position(direction)
        
        if bot.has_child():
            bot.child_carried.update_location(bot.position)
        new_cell = self.get_position(bot.position)
        
        if new_cell.is_full(): #load the child in new_cell
            new_cell.obj.is_active = False #the child will to be inactive
            bot.child_carried = new_cell.obj

        new_cell.acquire(bot)

    def move_child(self, child, direction):
        child_cell = self.get_position(child.position)
        new_cell = self.get_position(sum_positions(child.position, direction))
        if new_cell.is_guard(): #if child go to guard => this child disable their actions 
            child.is_active = False
        if new_cell.is_empty() and not new_cell.is_full():
            child_cell.release()
            child.change_position(direction)
            new_cell.acquire(child)
        elif new_cell.is_obstacle():
            can_push = False
            next_p = sum_positions(new_cell.p, direction)
            while self.is_valid_position(next_p):
                next_cell = self.get_position(next_p)
                if next_cell.is_empty() and not next_cell.is_full():
                    can_push = True
                    break
                elif next_cell.is_obstacle():
                    next_p = sum_positions(next_cell.p, direction)
                else:
                    break
            if can_push:
                child.change_position(direction)
                child_cell.floor = EMPTY
                child_cell.release()
                new_cell.floor = EMPTY
                new_cell.acquire(child)
                next_p = sum_positions(new_cell.p, direction)
                while True:
                    last_cell = self.get_position(next_p)
                    if last_cell.is_empty():
                        last_cell.floor = OBSTACLE
                        break
                    next_p = sum_positions(last_cell.p, direction)

    def clean(self, p):
        guard_cell = self.get_position(p)
        guard_cell.clean()
        self.dirty_cells -= 1

    def get_all_neighbors(self, pos):
        ady = []
        directions = [(-1,-1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]
        for d in directions:
            ady_p = sum_positions(pos, d)
            if self.is_valid_position(ady_p):
                ady.append(ady_p)
        return ady

    def childs_in_quadrant(self, positions):
        count = 0
        for p in positions:
            p_cell = self.get_position(p)
            if p_cell.is_full() and isinstance(p_cell.obj, Child):
                count += 1
        return count + 1

    def empty_neighbors(self, neighbors):
        positions = []
        for p in neighbors:
            p_cell = self.get_position(p)
            if p_cell.is_empty() and not p_cell.is_full():
                positions.append(p)
        return positions

    def generate_dirt(self, child):
        neighbors = self.get_all_neighbors(child.position)
        empty = self.empty_neighbors(neighbors)
        childs_count = self.childs_in_quadrant(neighbors)

        if childs_count == 2:
            max_to_dirt = 3
        elif childs_count > 3:
            max_to_dirt = 6
        else:
            max_to_dirt = 1
        
        r = random.Random()
        to_dirt = min(r.randint(0, max_to_dirt), len(empty))
        cells_dirt = r.sample(set(empty), to_dirt)
        print("Child ", child.name, "DIRT", cells_dirt)
        for p in cells_dirt:
            p_cell = self.get_position(p)
            p_cell.set_dirty()
            self.dirty_cells += 1
      
    def random_variation(self, bot_position):
        bot_cell = self.get_position(bot_position)
        bot_has_child = False
        if isinstance(bot_cell.obj, Robot) and bot_cell.obj.has_child():
            bot_has_child = True
        if isinstance(bot_cell.obj, ProtectRobot):
            bot_type = ProtectRobot
        else:
            print("44444444444444444444444444444444")
            input()
            bot_type = CleanerRobot
        bot = bot_type(bot_position)
        bot, childs = self.restart_map(self.N, self.M, bot, bot_has_child, self.dirty_cells, self.obst_cells, len(self.guards), self.cant_childs_in_guards() )
        return bot, childs

    def __str__(self):
        s = ""
        for i in range(self.N):
            s += str(([ str(self.map[i][j]) for j in range(self.M) ])) + "\n"
        return s

if __name__ == '__main__':
    r = random.Random()
    board = [['G', 'E', 'E'], ['R', 'C1', 'D'], ['D', 'D', 'E']]
    N = 5
    M = 5
    t = 10
    env = Environment(t, N, M)
    bot_pos = (r.choice(range(N)), r.choice(range(M)))
    env.restart_map(N, M, bot_pos, False, 3, 3, 4, 2 )
    print(env)
  
    env.random_variation(bot_pos)
    print(env)
  
    



