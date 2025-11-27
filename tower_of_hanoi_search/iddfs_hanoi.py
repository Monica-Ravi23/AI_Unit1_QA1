PEG_NAMES = ['A', 'B', 'C']
INITIAL_STATE = ((3, 2, 1), (), ())
GOAL_STATE = ((), (), (3, 2, 1))

class Node:
    def __init__(self, state, parent=None, move=None):
        self.state = state
        self.parent = parent
        self.move = move

def get_successors(state):
    successors = []
    pegs = [list(p) for p in state]

    for i in range(3):
        if not pegs[i]:
            continue
        disk = pegs[i][-1]

        for j in range(3):
            if i != j and (not pegs[j] or pegs[j][-1] > disk):
                np = [list(p) for p in pegs]
                np[i].pop()
                np[j].append(disk)
                new_state = tuple(tuple(p) for p in np)
                successors.append((new_state, (i, j, disk)))

    return successors

def reconstruct(node):
    moves = []
    while node.parent:
        frm, to, d = node.move
        moves.append((PEG_NAMES[frm], PEG_NAMES[to], d))
        node = node.parent
    return list(reversed(moves))

def dls(node, goal, depth, visited):
    if node.state == goal:
        return node
    if depth == 0:
        return None

    visited.add(node.state)

    for nxt, move in get_successors(node.state):
        if nxt not in visited:
            child = Node(nxt, node, move)
            res = dls(child, goal, depth - 1, visited)
            if res:
                return res

    return None

def iddfs(start, goal, max_depth=20):
    for depth in range(max_depth):
        visited = set()
        result = dls(Node(start), goal, depth, visited)
        if result:
            return result
    return None

if __name__ == "__main__":
    result = iddfs(INITIAL_STATE, GOAL_STATE)
    moves = reconstruct(result)

    print("\n=== IDDFS Solution ===")
    print("Total moves:", len(moves))
    for i, (frm, to, disk) in enumerate(moves, 1):
        print(f"Move {i}: Move disk {disk} from {frm} to {to}")
