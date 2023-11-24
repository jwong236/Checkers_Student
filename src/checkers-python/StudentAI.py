from random import randint
from BoardClasses import Move
from BoardClasses import Board
import math
#The following part should be completed by students.
#Students can modify anything except the class name and exisiting functions and varibles.
class StudentAI():
    class Node():
        def __init__(self, move, parent = None):
            self.move = move
            self.children = []
            self.parent = parent
            self.win_count = 0
            self.lose_count = 0
            self.visit_count = 0

        def add_child(self, child_node):
            """ Adds a child node to this node. """
            self.children.append(child_node)

        def update_stats(self, win):
            """ Updates the win/loss statistics of the node."""
            self.visit_count += 1
            if win:
                self.win_count += 1
            else:
                self.lose_count += 1

        def calculate_winrate(self):
            """ Calculates the win rate of the node. """
            if self.visit_count == 0:
                return 0
            return self.win_count / self.visit_count

        def calculate_ucb(self, exploration_param=math.sqrt(2)):
            """ Calculates the UCB1 value for the node. """
            if self.visit_count == 0:
                return float('inf')

            win_rate = self.calculate_winrate()
            if self.parent is None or self.parent.visit_count == 0:
                return win_rate

            ucb = win_rate + exploration_param * math.sqrt(math.log(self.parent.visit_count) / self.visit_count)
            return ucb
    def __init__(self,col,row,p):
        self.col = col
        self.row = row
        self.p = p
        self.board = Board(col,row,p)
        self.board.initialize_game()
        self.color = ''
        self.opponent = {1:2,2:1}
        self.color = 2

        self.root = self.Node(None)
    
    def select_node(self, children):
        """
        Selects a child node from the given list of children based on a specified heuristic.

        Start from the root and repeatedly select child
        On the first iteration, select each child once
        After the first iteration, select each child based on some heuristic
        Heuristic can be either
            1. Upper Confidence Bound formula
            2. Random (Apparently this is not as effective)

        Parameters:
            children (list): A list of child nodes to select from.

        Returns:
            Node: The selected child node.
        """
        return children(randint(0,len(children)-1))
    
    def expand_node(self, selected_node):
        """
        Expands the given node by adding a new child node to it.

        If the selected node doesn't end the game and has unexplored moves, expand it by creating a new child node of this selected node
        The choice of which child node to choose can be:
            1. Random
            2. Based on whichever is not explored yet
            3. Random and based on whichever is not explored yet (Apparently this is effective)

        Parameters:
            selected_node (Node): The node to be expanded.

        Returns:
            Node: The newly created child node.
        """
        expanded_node = self.Node(None, selected_node)
        selected_node.add_child(expanded_node)
        return expanded_node
        
    def simulate_game(self, expanded_node):
        """
        Simulates a game starting from the given node until a terminal state is reached.

        Simulate ONE game until completion starting from the expanded node by choosing moves for both players
        The choice of which moves to choose can be
            1. Random
            2. Idk

        Parameters:
            expanded_node (Node): The node from which the game simulation starts.

        Returns:
            list: A list representing the simulation route, containing tuples of nodes and their parents.
        """
        simulation_route = [(expanded_node, expanded_node.parent)]
        return simulation_route
        
    def propagate_back(self, simulation_route):
        """
        Backpropagates the simulation result through the tree.

        After the simulation reaches a terminal state, backpropagate the result up through the tree along the path taken during the selection phase. Update the win/loss statistics and visit count of each node on this path
        Repeat process for a predetermined number of iterations
        Calculate the best Upper Confidence Bound score and choose the highest

        Parameters:
            simulation_route (list): The path of nodes taken during the simulation, represented as a list.
        """
        return
        
    def choose_move(self, children):
        """
        Chooses the best move to play from the given list of child nodes.

        Calculate ucb of each root's child nodes and choose the largest
        Move the tree root to it's subtree to reflect current board state and prune unreachable tree board states
        Submit move

        Parameters:
            children (list): A list of child nodes to choose the best move from.

        Returns:
            Move: The move chosen as the best move to play.
        """
        return children[randint(0,len(children)-1)]


    def get_move(self,move):
        """
        Selects and executes a move for the AI player.

        After updating the board with the opponent's last move, this method fetches all possible moves
        for the AI player. These are stored in 'moves', a list of lists, where each sublist contains 
        Move objects for one piece. Each Move object contains a sequence of tuples representing 
        the path of the move from start to finish, with the first tuple representing the piece's initial position.

        Example of moves accounting for 4 pieces:
        moves = [
            [Move([(2, 2), (3, 3)])],  # First piece, 1 possible move
            [Move([(5, 1), (7, 3), (9, 5)])],  # Second piece, 1 possible move (with 2 jumps)
            [Move([(3, 4), (4, 3)]), Move([(3, 4), (5, 6)]), Move([(3, 4), (5, 6), (7, 4)])]  # Third piece, 3 possible moves
            [] # Fourth piece, no possible moves
        ]

        Parameters:
            move (Move): The opponent's last move or empty if no move has been made.

        Returns:
            Move: The move selected by the AI.
        """
        # Execute opponent's move onto the board, or initialize color for beginning of game
        if len(move) != 0:
            self.board.make_move(move,self.opponent[self.color])
        else:
            self.color = 1

        # Initialize tree, begin with the root node representing the current state of the board
        # Get all possible moves, get a set of root's current children, and add moves to tree only if it isn't already there
        moves = self.board.get_all_possible_moves(self.color)
        existing_moves = set()
        for child in self.root.children:
            existing_moves.add(str(child.move))
        for piece in moves:
            for move in piece:
                if str(move) not in existing_moves: # Note: child.move and move must be compared in their string representation as they have different addresses
                    self.root.add_child(self.Node(move, self.root))
    
        # Selection Phase:
        selected_node = self.select_node(self.root.children) # TODO

        # Expansion Phase:
        expanded_node = self.expand_node(selected_node) # TODO

        # Simulation Phase:
        simulation_route = self.simulate_game(expanded_node) # TODO

        # Backpropagation Phase:
        self.propagate_back(simulation_route) # TODO

        # Finalize move choice:
        move = self.choose_move(self.root.children) # TODO
        for child in self.root.children:
            if str(move) == str(child.move):
                self.root = child
                if self.root.parent:
                    self.root.parent.children = []  # Clear children of the old root
                    self.root.parent = None  # Remove parent reference from the new root
                break
        self.board.make_move(move, self.color)
        return move
    

    """
        # Execute opponent's move onto the board, but if 
        if len(move) != 0:
            self.board.make_move(move,self.opponent[self.color])
        else:
            self.color = 1
 
        
        moves = self.board.get_all_possible_moves(self.color)

        index = randint(0,len(moves)-1)
        inner_index =  randint(0,len(moves[index])-1)
        move = moves[index][inner_index]
        self.board.make_move(move,self.color)
        return move
"""