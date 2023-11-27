from random import randint
from BoardClasses import Move
from BoardClasses import Board

import math

from copy import deepcopy
import logging

# Basic configuration of the logging system
logging.basicConfig(level=logging.DEBUG, filename='myapp.log', filemode='w',
                    format='%(name)s - %(levelname)s - %(message)s')

#The following part should be completed by students.
#Students can modify anything except the class name and exisiting functions and varibles.
class StudentAI():
    class Node():
        def __init__(self, move, player, parent = None):
            self.move = move
            self.children = []
            self.parent = parent
            self.win_count = 0
            self.visit_count = 0
            # need to keep track of which player the node is for
            self.player = player
            

        def add_child(self, child_node):
            """ Adds a child node to this node. """
            self.children.append(child_node)

        def update_stats(self, outcome):
            """ Updates the win/loss statistics of the node."""
            self.visit_count += 1
            if outcome == self.player: # need to update correctly while backtracking given player who won
                self.win_count += 1
            elif outcome == -1:
                self.win_count += 0.5

        def calculate_winrate(self):
            """ Calculates the win rate of the node. """
            if self.visit_count == 0:
                return 0
            return self.win_count / self.visit_count

        def calculate_ucb(self, exploration_param=math.sqrt(2)):
            """ Calculates the UCB1 value for the node. """
            if self.visit_count == 0:
                return float('inf')

            ucb = self.calculate_winrate() + exploration_param * math.sqrt(math.log(self.parent.visit_count) / self.visit_count)
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

        # added root node for MCTS
        self.root = self.Node(None, None)
        self.board_copy = self.board
    
    def select_node(self, node):
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

        # If all children are visited, select the one with the highest UCB1 value
        # i = 0
        current_node = node
        while current_node.children != []:
            best_node = None
            # if current_node.player == self.color:
            best_ucb_value = float('-inf')
            for child in current_node.children:
                ucb_value = child.calculate_ucb()
                if ucb_value > best_ucb_value:
                    best_ucb_value = ucb_value
                    best_node = child
            # else:
            #     best_ucb_value = float('inf')
            #     for child in current_node.children:
            #         ucb_value = child.calculate_ucb()
            #         if ucb_value <= best_ucb_value:
            #             best_ucb_value = ucb_value
            #             best_node = child
            current_node = best_node

            # self.board_copy.make_move(current_node.move[0], self.opponent[self.color])
            # self.board_copy.make_move(current_node.move[1], self.color)
            self.board_copy.make_move(current_node.move, current_node.player)
            # i += 1
            
        return current_node
    

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


        # Get all possible moves from the selected move
        expanded_moves = self.board_copy.get_all_possible_moves(self.opponent[selected_node.player])
        # expanded_moves = self.board_copy.get_all_possible_moves(self.opponent[self.color])

        if not expanded_moves: return selected_node

        # # Filter out moves that have already been explored from the selected node
        # explored_moves = {str(child.move) for child in selected_node.children}
        # unexplored_moves = [move for sublist in expanded_moves for move in sublist if str(move) not in explored_moves]

        # existing_moves = set()
        # for child in self.root.children:
        #     existing_moves.add(str(child.move))
        # for piece in moves:
        #     for move in piece:
        #         if str(move) not in existing_moves: # Note: child.move and move must be compared in their string representation as they have different addresses
        #             self.root.add_child(self.Node(move, self.root, player = self.color))
        
        for piece in expanded_moves:
            for move in piece:
                # self.board_copy.make_move(move, self.opponent[self.color])
                # next_next_moves = self.board_copy.get_all_possible_moves(self.color)
                selected_node.add_child(self.Node(move, self.opponent[selected_node.player], selected_node ))
                # if not next_next_moves: continue
                # for next_piece in next_next_moves:
                #     for next_move in next_piece:
                #         selected_node.add_child(self.Node([move, next_move], self.color, selected_node ))
                # self.board_copy.undo()
        
        # if not selected_node.children: return selected_node


        # # No moves left to explore from this node
        # if not unexplored_moves:
        #     return None

        # # Randomly select one of the unexplored moves
        # move_to_expand = unexplored_moves[randint(0, len(unexplored_moves) - 1)]

        # best_ucb_value = float('-inf')
        # best_node = None
        # for child in selected_node.children:
        #     ucb_value = child.calculate_ucb()
        #     if ucb_value > best_ucb_value:
        #         best_ucb_value = ucb_value
        #         best_node = child

        # # Create a new node for this move and add it to the selected node
        # new_node = self.Node(move_to_expand, selected_node)
        # selected_node.add_child(new_node)

        index = randint(0, len(selected_node.children) - 1)
        best_node = selected_node.children[index]

        self.board_copy.make_move(best_node.move, best_node.player)
        # self.board_copy.make_move(best_node.move[0], self.opponent[self.color])
        # self.board_copy.make_move(best_node.move[1], self.color)

        return best_node
        
    # def simulate_game(self, current_node):
    def simulate_game(self, current_player):
        """
        Simulates a game starting from the given node until a terminal state is reached.

        Parameters:
            current_node (Node): The node from which the game simulation starts.

        Returns:
            Node: The last node of the simulation
            win(bool): Returns true if choosing expanded node resulted in a win
        """
        # if current_node.move:
        #     self.board_copy.make_move(current_node.move, current_node.player)

        # current_player = self.opponent[current_node.player]
        
        while True:
            moves = self.board_copy.get_all_possible_moves(current_player)
            if not moves:  # No more moves available
                break

            # Randomly select a move
            index = randint(0, len(moves) - 1)
            inner_index = randint(0, len(moves[index]) - 1)
            move = moves[index][inner_index]
            self.board_copy.make_move(move, current_player)

            # # Create a new node for this move and link it to the current node
            # new_node = self.Node(move, new_node.player, current_node)
            # current_node.add_child(new_node)
            # current_node = new_node  # Update current node

            # Check for win/lose/tie condition
            if self.board_copy.is_win(current_player) != 0:
                return self.board_copy.is_win(current_player)

            # Switch player
            current_player = self.opponent[current_player]
        # win = True if current_player == self.color else False
        # return win
        
    def propagate_back(self, start_node, outcome):
        """
        Backpropagates the simulation result through the tree.

        After the simulation reaches a terminal state, backpropagate the result up through the tree along the path taken during the selection phase.
        Update the win/loss statistics and visit count of each node on this path.
        win_counter is updated for both wins and ties
        visit_counter is also updated
        Repeat process for a predetermined number of iterations

        Parameters:
            start_node (Node): The node in the tree to begin updating values from.
            outcome (int): The outcome of the game for the AI player.
        """
        # make sure to undo moves so we get back to original board state
        current_node = start_node
        
        while current_node is not None:
            current_node.update_stats(outcome)
            current_node = current_node.parent
        
    def choose_move(self, children):
        """
        Chooses the best move to play from the given list of child nodes.

        Calculate ucb of each root's child nodes and choose the largest.
        Move the tree root to its subtree to reflect current board state and prune unreachable tree board states.
        Submit move.

        Parameters:
            children (list): A list of child nodes to choose the best move from.

        Returns:
            Move: The move chosen as the best move to play.
        """
        if not children:
            return None

        best_ucb_value = float('-inf')
        best_node = None

        # Iterate through each child to find the one with the highest UCB value
        for child in children:
            ucb_value = child.calculate_ucb()
            if ucb_value > best_ucb_value:
                best_ucb_value = ucb_value
                best_node = child

        # Return the move associated with the node having the highest UCB value
        logging.info("Selected Node Win Rate: %s", best_node.calculate_winrate())
        logging.info("Selected Node UCB Value: %s", best_node.calculate_ucb())
        logging.info("Selected Node visited Value: %s", best_node.visit_count)
        return best_node.move

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
            # make root node based off oponent's move
            self.board.make_move(move,self.opponent[self.color])
            for child in self.root.children:
                if str(move) == str(child.move):
                    
                    self.root = child
                    
                    if self.root.parent: 
                        self.root.parent.children = []  # Clear children of the old root
                        self.root.parent = None  # Remove parent reference from the new root
                    break
        else:
            self.color = 1
        # logging.info("Initialized board")
        # Initialize tree, begin with the root node representing the current state of the board
        # Get all possible moves, get a set of root's current children, and add moves to tree only if it isn't already there
        moves = self.board.get_all_possible_moves(self.color)

        existing_moves = set()
        for child in self.root.children:
            existing_moves.add(str(child.move))
        for piece in moves:
            for move in piece:
                if str(move) not in existing_moves: # Note: child.move and move must be compared in their string representation as they have different addresses
                    self.root.add_child(self.Node(move, self.color, self.root))

    
        for i in range(100):
            # for attr in self.board.__dict__:
            #     self.board_copy.__dict__[attr] = self.board.__dict__[attr]
            self.board_copy = deepcopy(self.board)
            #logging.info(self.board.get_all_possible_moves(self.color))
            #logging.info(self.board_copy.get_all_possible_moves(self.color))

            # Selection Phase:
            # logging.info("Selection Phase")
            selected_node = self.select_node(self.root)

            # Expansion Phase: 
            expanded_node = self.expand_node(selected_node)

            # if not expanded_node: break

            # Simulation Phase:
            outcome = self.simulate_game(self.opponent[expanded_node.player])

            # Backpropagation Phase:
            self.propagate_back(expanded_node, outcome)
        
        # Finalize move choice:
        move = self.choose_move(self.root.children)

        for child in self.root.children:
            if str(move) == str(child.move):
                
                self.root = child
                
                if self.root.parent: 
                    self.root.parent.children = []  # Clear children of the old root
                    self.root.parent = None  # Remove parent reference from the new root
                break

        # logging.info(self.board.get_all_possible_moves(self.color))
        # logging.info("Making move:{}".format(move))
        self.board.make_move(move, self.color)
        # logging.info("All possible moves after choosing: {}".format(self.board.get_all_possible_moves(self.color)))
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