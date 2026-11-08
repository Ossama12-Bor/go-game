# -*- coding: utf-8 -*-
''' This is the file you have to modify for the tournament. Your default AI player must be called by this module, in the
myPlayer class.

Right now, this class contains the copy of the randomPlayer. But you have to change this!
'''

import time
import Goban 
from random import choice
from playerInterface import *
from theory import tree_black , tree_white
from model import *
import numpy as np
import torch

class myPlayer(PlayerInterface):
    ''' Example of a random player for the go. The only tricky part is to be able to handle
    the internal representation of moves given by legal_moves() and used by push() and 
    to translate them to the GO-move strings "A1", ..., "J8", "PASS". Easy!

    '''

    def __init__(self):
        self._board = Goban.Board()
        self._mycolor = None
        self._theoric = True
        self.tree = tree_black if self._mycolor == Goban.Board._BLACK else tree_white

    def getPlayerName(self):
        return "Procrastinator" 

    #def getPlayerMove(self):
    #    if self._board.is_game_over():
    #        print("Referee told me to play but the game is over!")
    #        return "PASS" 
    #    moves = self._board.legal_moves() # Dont use weak_legal_moves() here!
    
    def getPlayerMove(self):
        if self._board.is_game_over():
            print("Referee told me to play but the game is over!")
            return "PASS" 
        if self._board._lastPlayerHasPassed:
            diff_stones = self._board._nbBLACK - self._board._nbWHITE
            if (self._mycolor == self._board._BLACK and diff_stones > 0) or \
               (self._mycolor == self._board._WHITE and diff_stones < 0):
                #print("L'adversaire a passé et nous avons l'avantage, on passe aussi")
                return "PASS"
        
        capturable, at = self.can_capture_group()
        if capturable:
            move = Board.flat_to_name(at)
    
        else :
            if self._theoric:
                theoric , move = self.theoric_moves()
                self._theoric = theoric 
            if not self._theoric:
                move = self.alpha_beta_search(3)  # Use the alpha-beta search to find the best move
        self._board.push(self._board.str_to_move(move))

        # New here: allows to consider internal representations of moves
        print("I am playing ", move)
        print("My current board :")
        self._board.prettyPrint()
        # move is an internal representation. To communicate with the interface I need to change if to a string
        return move 
    def playOpponentMove(self, move):
        print("Opponent played ", move) # New here
        # the board needs an internal represetation to push the move.  Not a string
        self._board.push(Goban.Board.name_to_flat(move)) 
        self.tree.traverse(move)

    def newGame(self, color):
        self._mycolor = color
        self._opponent = Goban.Board.flip(color)

    def endGame(self, winner):
        if self._mycolor == winner:
            print("I won!!!")
        else:
            print("I lost :(!!")

    def alpha_beta_search(self, depth):
        def max_value(board, alpha, beta, d):
            if d == 0 or board.is_game_over():
                return self.evaluate_board(board)
            v = -float("inf")
            for move in board.legal_moves():
                board.push(move)
                v = max(v, min_value(board, alpha, beta, d-1))
                board.pop()
                if v >= beta:
                    return v
                alpha = max(alpha, v)
            return v

        def min_value(board, alpha, beta, d):
            if d == 0 or board.is_game_over():
                return self.evaluate_board(board)
            v = float("inf")
            for move in board.legal_moves():
                board.push(move)
                v = min(v, max_value(board, alpha, beta, d-1))
                board.pop()
                if v <= alpha:
                    return v
                beta = min(beta, v)
            return v

        best_score = -float("inf")
        best_action = "PASS"
        moves = self._board.legal_moves()
        for move in moves:
            self._board.push(move)
            score = min_value(self._board, -float("inf"), float("inf"), depth - 1)
            #print(f"Evaluating move {Goban.Board.flat_to_name(move)}: score = {score}")
            self._board.pop()
            if score > best_score:
                best_score = score
                best_action = Board.flat_to_name(move)
        return best_action 
 
        

    def evaluate_board(self, board):
        
        history = board._historyMoveNames
        array = array_data(history)
        with torch.no_grad():
            model_pred = model(torch.tensor(array, dtype=torch.float32).unsqueeze(0)).item()
        model_pred = model_pred if self._mycolor == Board._BLACK else 1 - model_pred

    
        def get_connected_groups(color):
            chains = {}
            for i in range(Board._BOARDSIZE**2):
                if self._board[i] == color:
                    root = self._board._getStringOfStone(i)
                    if root not in chains:
                        chains[root] = []
                    chains[root].append(i)
            return chains 
                
        my_groups = get_connected_groups(self._mycolor)



        

        # Score final
        final_score = model_pred
        return final_score

    def can_capture_group(self):
        opponent = Board.flip(self._mycolor)
        already_seen = set()
    
        for i in range(Board._BOARDSIZE ** 2):
            if self._board[i] != opponent:
                continue
    
            root = self._board._getStringOfStone(i)
            if root in already_seen:
                continue
            already_seen.add(root)
    
            liberties = self._board._stringLiberties[root]
            if liberties == 1:
                neighbors = self._board._neighbors[self._board._neighborsEntries[i]:]
                for n in neighbors:
                    if n == -1:
                        break
                    if n in self._board.legal_moves():
                        return True, n  
        return False, None

    def theoric_moves(self):
        theory_moves = [n.move for n in self.tree.current]
        
        # Premier coup en noir -> centre
        if len(self._board._historyMoveNames) == 0 and self._mycolor == self._board._BLACK:
            move = Goban.Board.name_to_flat("E5")
            self.tree.traverse("E5")
            return True , "E5"
        moves = self._board.legal_moves()
        # Évaluation des coups théoriques avec evaluate_board
        if theory_moves:
            move_flat = None
            for tmove in theory_moves:
                if tmove == "PASS":
                    continue
                
                move_flat = self._board.name_to_flat(tmove)
                if move_flat in moves:
                   break
            if  move_flat in moves : 
                self.tree.traverse(tmove)
                return True , tmove
    
        return False , "PASS"  # No valid theoretical moves, return PASS
    