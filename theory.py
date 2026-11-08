import json

class Node:
    def __init__(self, move=None):
        self.move = move
        self.children = []
        self.parent = None

    def add_child(self, child_node):
        child_node.parent = self
        self.children.append(child_node)

    def get_child_by_move(self, move):
        for child in self.children:
            if child.move == move:
                return child
        return None


class GameTree:
    def __init__(self):
        self.roots = []
        self.current = []

    def add_root(self, node):
        if node not in self.roots:
            self.roots.append(node)
            node.parent = None

    def traverse(self, move):
        for node in self.current:
            if node.move == move:
                self.current = node.children
                return True
        return False
    
    def add_child(self, move, child_move):
        for node in self.current:
            if node.move == move:
                node.add_child(child_move)
                return True
        return False

    def get_children(self, move):
        self.traverse(move)
        return self.current

def build_tree_from_plays(plays):
    tree = GameTree()
    for play in plays:
        moves = play.get("moves", [])
        if not moves:
            continue
        # Cherche ou crée la racine
        root = None
        for r in tree.roots:
            if r.move == moves[0]:
                root = r
                break
        if not root:
            root = Node(moves[0])
            tree.add_root(root)
        current = root
        for move in moves[1:]:
            child = current.get_child_by_move(move)
            if not child:
                child = Node(move)
                current.add_child(child)
            current = child
    tree.current = tree.roots[:]  # Initialise current avec toutes les racines
    return tree

def load_plays(filepath):
    with open(filepath, "r") as f:
        data = json.load(f)
    return data

plays = load_plays("plays-8x8.json")
plays_black = [play for play in plays if play.get("winner") == "black"]
plays_white = [play for play in plays if play.get("winner") == "white"]
tree = build_tree_from_plays(plays)
tree_black = build_tree_from_plays(plays)
tree_white = build_tree_from_plays(plays)
   

