from collections import deque

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
    pegs = [list(peg) for peg in state]

    for i in range(3):
        if not pegs[i]:
            continue
        disk = pegs[i][-1]

        for j in range(3):
            if i != j and (not pegs[j] or pegs[j][-1] > disk):
                new_pegs = [list(peg) for peg in pegs]
                new_pegs[i].pop()
                new_pegs[j].append(disk)
                new_state = tuple(tuple(p) for p in new_pegs)
                successors.append((new_state, (i, j, disk)))
    return successors

def reconstruct_path(node):
    moves = []
    while node.parent:
        from_i, to_i, disk = node.move
        moves.append((PEG_NAMES[from_i], PEG_NAMES[to_i], disk))
        node = node.parent
    moves.reverse()
    return moves

def dfs(start, goal):
    stack = [Node(start)]
    visited = set()

    while stack:
        node = stack.pop()
        if node.state in visited:
            continue
        visited.add(node.state)

        if node.state == goal:
            return node

        for nxt, move in reversed(get_successors(node.state)):
            stack.append(Node(nxt, node, move))

    return None

if __name__ == "__main__":
    result = dfs(INITIAL_STATE, GOAL_STATE)
    moves = reconstruct_path(result)

    print("\n=== DFS Solution ===")
    print("Total moves:", len(moves))
    for i, (frm, to, disk) in enumerate(moves, 1):
        print(f"Move {i}: Move disk {disk} from {frm} to {to}")
