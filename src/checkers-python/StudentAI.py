from random import randint
from BoardClasses import Move
from BoardClasses import Board
import math
#The following part should be completed by students.
#Students can modify anything except the class name and exisiting functions and varibles.
class StudentAI():
    class Node():
        def __init__(self, parent):
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

        self.tree = self.Node(None, None)
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

        moves = self.board.get_all_possible_moves(self.color)

        # Initialize tree, begin with the root node representing the current state of the board
                
        # Selection Phase:
        #     Start from the root and repeatedly select child
        #     On the first iteration, select each child once
        #     After the first iteration, select each child based on some heuristic
        #     Heuristic can be either
        #         1.Upper Confidence Bound formula
        #         2. Random (Apparently this is not as effective)

        # Expansion Phase:
        #     If the selected node doesn't end the game and has unexplored moves, expand it by creating a new child node of this selected node
        #     The choice of which child node to choose can be:
        #         1. Random
        #         2. Based on whichever is not explored yet
        #         3. Random and based on whichever is not explored yet (Apparently this is effective)

        # Simulation Phase:
        #     Simulate ONE game until completion starting from the expanded node by choosing moves for both players
        #     The choice of which moves to choose can be
        #         1. Random
        #         2. Idk

        # Backpropagation Phase:
        #     After the simulation reaches a terminal state, backpropagate the result up through the tree along the path taken during the selection phase. Update the win/loss statistics and visit count of each node on this path
        #     Repeat process for a predetermined number of iterations
        #     Calculate the best Upper Confidence Bound score and choose the highest


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