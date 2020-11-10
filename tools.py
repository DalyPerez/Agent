### Directions ###
North = (-1, 0)
South = (1, 0)
East  = (0, 1)
West  = (0, -1)

def sum_positions(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return (x1 + x2, y1 + y2)

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
        




