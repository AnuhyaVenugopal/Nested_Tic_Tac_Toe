from tkinter import Button, Tk, Frame, Menu, messagebox
import random

class NestedTicTacToe:
    def __init__(self):  
        self.board = [[self.create_game() for _ in range(3)] for _ in range(3)]
        self.big_board = [['' for _ in range(3)] for _ in range(3)]  # Keeps track of the main game
        self.player = 'X'
        self.game_over = False
        self.opponent_is_bot = self.ask_for_opponent()

        self.root = Tk()
        self.root.title("Nested Tic Tac Toe")
        menubar = Menu(self.root)
        self.root.config(menu=menubar)
        menubar.add_command(label="Reset Game", command=self.reset_game)

        self.frames = [[Frame(self.root, bd=2, relief='solid') for _ in range(3)] for _ in range(3)]
        self.buttons = [[[[Button(self.frames[big_row][big_col], text="", height=2, width=5, command=lambda big_row=big_row, big_col=big_col, small_row=small_row, small_col=small_col: self.on_click(big_row, big_col, small_row, small_col)) for small_col in range(3)] for small_row in range(3)] for big_col in range(3)] for big_row in range(3)]
        for big_row in range(3):
            for big_col in range(3):
                self.frames[big_row][big_col].grid(row=big_row, column=big_col, padx=5, pady=5)
                for small_row in range(3):
                    for small_col in range(3):
                        self.buttons[big_row][big_col][small_row][small_col].grid(row=small_row, column=small_col)
        self.root.mainloop()

       
    def create_game(self):
        return [[{'text': "", 'clicked': False} for _ in range(3)] for _ in range(3)]


    # Disabling the small game and highlighting the grid to indicate a win
    def disable_buttons(self, big_row, big_col, winner):
        """
        This method disables the buttons in the small game and highlights the grid to indicate a win.
        """
        for i in range(3):
            for j in range(3):
                self.buttons[big_row][big_col][i][j]['state'] = 'disabled'
        # Highlight the square
        if winner == 'X':
            self.frames[big_row][big_col].config(highlightbackground='green', highlightthickness=3)
        elif winner == 'O':
            self.frames[big_row][big_col].config(highlightbackground='blue', highlightthickness=3)


    def disable_all_buttons(self):
        """
        This method disables all the buttons when the main game is over.
        """
        for i in range(3):
            for j in range(3):
                self.disable_buttons(i, j, None)


    def check_for_winner(self, big_row, big_col):
        """
        This method checks for a win in the small game.
        """
        # Check rows and columns for a win in the small game
        for i in range(3):
            if self.board[big_row][big_col][i][0]['text'] == self.board[big_row][big_col][i][1]['text'] == self.board[big_row][big_col][i][2]['text'] != "":
                self.disable_buttons(big_row, big_col, self.board[big_row][big_col][i][0]['text'])
                return self.board[big_row][big_col][i][0]['text']
            if self.board[big_row][big_col][0][i]['text'] == self.board[big_row][big_col][1][i]['text'] == self.board[big_row][big_col][2][i]['text'] != "":
                self.disable_buttons(big_row, big_col, self.board[big_row][big_col][0][i]['text'])
                return self.board[big_row][big_col][0][i]['text']
        # Check diagonals
        if self.board[big_row][big_col][0][0]['text'] == self.board[big_row][big_col][1][1]['text'] == self.board[big_row][big_col][2][2]['text'] != "":
            self.disable_buttons(big_row, big_col,self.board[big_row][big_col][0][0]['text'])
            return self.board[big_row][big_col][0][0]['text']
        if self.board[big_row][big_col][0][2]['text'] == self.board[big_row][big_col][1][1]['text'] == self.board[big_row][big_col][2][0]['text'] != "":
            self.disable_buttons(big_row, big_col, self.board[big_row][big_col][0][2]['text'])
            return self.board[big_row][big_col][0][2]['text']
        # Check for tie
        for i in range(3):
            for j in range(3):
                if self.board[big_row][big_col][i][j]['text'] == "":
                    return None  # No winner and no tie
        return 'Tie'  # No winner, so it's a tie


    def check_for_big_winner(self):
        """
        This method checks for a win in the big game.
        """
        # Check rows and columns for a win in the big game
        for i in range(3):
            if self.big_board[i][0] == self.big_board[i][1] == self.big_board[i][2] != "":
               return self.big_board[i][0]
            if self.big_board[0][i] == self.big_board[1][i] == self.big_board[2][i] != "":
                return self.big_board[0][i]
        # Check diagonals
        if self.big_board[0][0] == self.big_board[1][1] == self.big_board[2][2] != "":
            return self.big_board[0][0]
        if self.big_board[0][2] == self.big_board[1][1] == self.big_board[2][0] != "":
            return self.big_board[0][2]
        for i in range(3):
            for j in range(3):
                if self.big_board[i][j] == "":
                    return None  # No winner and no tie
        return 'Tie'


    def on_click(self,big_row, big_col, small_row, small_col):
        """
        This method handles non-bot button clicks and checks for a winner or tie in small game and big game.
        """
        if self.board[big_row][big_col][small_row][small_col]['text'] == "" and self.buttons[big_row][big_col][small_row][small_col]['state'] != 'disabled':
            self.board[big_row][big_col][small_row][small_col]['text'] = self.player
            self.buttons[big_row][big_col][small_row][small_col]['text'] = self.player
            winner = self.check_for_winner(big_row, big_col)
            # Check for a tie
            if winner == 'Tie':
                # Reset small game
                messagebox.showinfo("Small Game Over", f"It's a Tie, resetting grid {big_row+1}, {big_col+1}!")
                for small_row in range(3):
                    for small_col in range(3):
                        self.board[big_row][big_col][small_row][small_col]['text'] = ""
                        self.buttons[big_row][big_col][small_row][small_col]['text'] = ""
                        self.buttons[big_row][big_col][small_row][small_col]['state'] = 'normal'
            # Check for a win in big game
            elif winner is not None:
                self.big_board[big_row][big_col] = winner
                big_winner = self.check_for_big_winner()
                if big_winner == 'Tie':
                    messagebox.showinfo("Game Over", f"It's a Tie, please reset grid to play again!")
                elif big_winner is not None:
                    self.game_over = True
                    self.disable_all_buttons()
                    messagebox.showinfo("Game Over", f"Player {big_winner} wins the big game!\nPlease reset grid to play again!")
                else:
                    messagebox.showinfo("Small Game Over", f"Player {winner} wins in grid {big_row+1}, {big_col+1}!")
            self.player = 'O' if self.player == 'X' else 'X'
            if self.opponent_is_bot and self.player == 'O' and not self.game_over:
                self.bot_turn()
                self.player = 'X'


    def ask_for_opponent(self):
        """
        This method asks the user if they want to play against a bot.
        """
        opponent = messagebox.askquestion("Choose Opponent", "Do you want to play against a bot?")
        return opponent == "yes"


    def bot_turn(self):
        """
        This method makes the bot's move. 
        It chooses a random move from the available moves.
        """
        # Get all available moves
        available_moves = [(big_row, big_col, small_row, small_col) for big_row in range(3) for big_col in range(3) for small_row in range(3) for small_col in range(3) if self.buttons[big_row][big_col][small_row][small_col]['text'] == "" and self.buttons[big_row][big_col][small_row][small_col]['state'] != 'disabled']
        # Choose a random move
        if available_moves:
            big_row, big_col, small_row, small_col = random.choice(available_moves)
            # Make the move
            self.buttons[big_row][big_col][small_row][small_col]['text'] = 'O'
            self.board[big_row][big_col][small_row][small_col]['text'] = 'O'
            # Check for a win in the small game
            winner = self.check_for_winner(big_row, big_col)
            if winner is not None:
                self.big_board[big_row][big_col] = winner
                big_winner = self.check_for_big_winner()
                # Check for a winner in big game
                if big_winner is not None:
                    self.game_over = True
                    self.disable_all_buttons()
                    messagebox.showinfo("Game Over", f"Player {big_winner} wins the big game!\nPlease reset grid to play again!")
                else:
                    messagebox.showinfo("Small Game Over", f"Player {winner} wins in grid {big_row+1}, {big_col+1}!")
            return

    
    def reset_game(self):
        """
        This method resets the game by clearing the board and buttons, 
        and resetting the player and game_over variables.
        """
        # Reset the board
        for big_row in range(3):
            for big_col in range(3):
                self.big_board[big_row][big_col] = ''
                for small_row in range(3):
                    for small_col in range(3):
                        self.board[big_row][big_col][small_row][small_col]['text'] = ""
                self.frames[big_row][big_col].config(highlightbackground='black', highlightthickness=0)
        # Reset buttons
        for big_row in range(3):
            for big_col in range(3):
                for small_row in range(3):
                    for small_col in range(3):
                        self.buttons[big_row][big_col][small_row][small_col]['text'] = ""
                        self.buttons[big_row][big_col][small_row][small_col]['state'] = 'normal'  
        # Reset player and game_over
        self.player = 'X'
        self.game_over = False
        #Ask for opponent again
        self.opponent_is_bot = self.ask_for_opponent()

if __name__ == "__main__":
    NestedTicTacToe()