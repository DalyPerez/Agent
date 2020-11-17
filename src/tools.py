### Directions ###
North = (-1, 0)
South = (1, 0)
East  = (0, 1)
West  = (0, -1)

import random as rdm

def sum_positions(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return (x1 + x2, y1 + y2)

def get_adyacents( pos):
    ady = []
    for dir in [North, South, East, West]:
        p = sum_positions(pos, dir)
        yield p

def rest_positions(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return (x1 - x2, y1 - y2)

def bfs(env, i, j, bot, final_func):
    mx = env.map

    """
        mx: matrix of cell
        (i,j): origin pos
        final_func: final predicate that indicate when a cell is the target one
        :return: vector direction of the initial position to find the shortest path
    """
    q = [(i, j)]
    d = {(i,j): 0}
    pi = {(i, j): -1}
    target = None
    while len(q) > 0:
        x, y = q.pop(0)
        if(final_func(mx[x][y])):
            target = (x, y)
            break
        for nextp in env.get_adyacents((x, y)):
            nx, ny = nextp
            if env.robot_CanMoveAnyWhere(bot, (i,j), nextp) and d.get((nx, ny), None) == None:
                d[(nx, ny)] = d[(x, y)] + 1
                pi[(nx, ny)] = (x, y)
                q.append((nx, ny))
    if target == None:
        print ("not found anyone")
        return None
    while pi[target] != (i, j) and pi[target] != -1:
        target = pi[target]
    return rest_positions(target, (i, j))
        
def connect (n, m, obs):
    mx = [[0 for j in range(m)] for i in range(n)]
    used = [[0 for j in range(m)] for i in range(n)]
    
    for x in obs:
        i, j = x
        mx[i][j] = 1
    
    if len(obs) == n * m: return False
    i,j = [(i,j) for i in range(n) for j in range(m) if not mx[i][j]][0]    

    def inside(i, j):
        return i >= 0 and j >= 0 and i < n and j < m
    
    def dfs_e(p, mx, used):
        used[p[0]][p[1]] = 1
        for np in get_adyacents(p):
            x, y = np
            if inside(x, y) and not mx[x][y] and not used[x][y]:
                dfs_e(np, mx, used)

    dfs_e((i,j), mx, used)

    li = [(i,j) for i in range(n) for j in range(m) if not mx[i][j] and not used[i][j]]
   
    return len(li) == 0

if __name__ == "__main__":
    r = rdm.Random()
    n,m,k  = 8,8,25
    positions = [(i,j) for i in range(n) for j in range(m)]
    r.shuffle(positions)
    # print(connect(2,2,[(0,0), (0, 1)]))
    l = []

    for i in positions:
        if k == 0: break
        if connect(n, m, l + [i]):
            l.append(i)
            k -= 1
    print (l)
    mx = [[0 for j in range(m)] for i in range(n)]
    
    for x in l:
        i, j = x
        mx[i][j] = 1
    
    for i in range(n):
        print (mx[i])