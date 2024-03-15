class Boardclass:
    """A simple class to store and handle information about the board.

    Attributes:
        
        name (str): The name of the user in current move.
        last_player_name (str): The name of the user in the last move.
        player_symbol (str): The symbol 'X' or 'O'
        board (list): A list represent a 2D picture of Tic-Tac-Toe
        wins (int): number of wins
        ties (int): number of draws
        losses (int): number of losses
    """
    def __init__(self,  name: str = "", last_player_name: str = "", player_symbol = 'X', board: list = [[0, 0, 0], [0, 0, 0], [0, 0, 0]], wins: int= 0, ties: int= 0, losses: int = 0) -> None:
        """Make a Board object.

        """
        self.setname(name)
        self.setlast_player_name(last_player_name)
        self.player_symbol = player_symbol
        self.board = board
        self.wins = wins
        self.ties = ties
        self.losses = losses

    def setname(self, name: str) -> None:
        """Set the name in the Board.

        Args:
            name: Name of the the user in current move.
        """
        self.name = name

    def setlast_player_name(self, last_player_name: str) -> None:
        """Set the last name in the Board.

        Args:
            name: Name of the the user in the last move.
        """
        self.last_player_name = last_player_name

    def setplayer_symbol(self, player_symbol) -> None:
        """Set the symbol in the Board

        Args:
            player_symbol:The symbol 'X' or 'O'
        """

        self.player_symbol = player_symbol


    def getname(self) -> str:
        """Get the name of the Board.

        Returns:
            name: Name of the the user in current move.
        """
        return self.name
    
   
    def getlast_player_name(self)-> str:
        """Get the last name in the Board.

        Returns:
            name: Name of the the user in the last move.
        """
        return self.last_player_name

    def getplayer_symbol(self)-> str:
        """Get the symbol in the Board.

         Returns:
            player_symbol: The symbol 'X' or 'O'.
        """
        return self.player_symbol
        
    def getwins(self)-> int:
        """Get the total times of wins.

        Returns:
            the number of wins
        """
        return self.wins

    def getties(self)-> int:
        """Get the total times of draws.

        Returns:
            the number of draws
        """
        return self.ties

    def getlosses(self)-> int:
        """Get the total times of losses.

        Returns:
            the number of losses
        """
        return self.losses

    def incrementwins(self) -> None:
        """Increment the times of wins by 1
        """
        self.wins += 1

    def incrementties(self) -> None:
        """Increment the times of draws by 1.
        """
        self.ties += 1
        
    def incrementlosses(self) -> None:
        """Increment the times of losses by 1.
        """
        self.losses += 1

    def print_board(self)-> None:
        """print the 2D picture of Tic-Tac-Toe.
        """
        for row in self.board:
            print("+---+" * 3)        
            print(''.join(f"|{cell if cell else '':^3}|" for cell in row))
            print("+---+" * 3)

    def updateGamesPlayed(self)-> int:
        """Keeps track how many games have started.
        """
        return (self.getwins() + self.getties()+ self.getlosses())

    def resetGameBoard(self)-> None:
        """Clear all the moves from game board
        """
        self.board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    def updateGameBoard(self, hor, ver)-> None:
        """Updates the game board with the player's move.
           Will raise value error if input wrong coordinates.
        """
        if self.board[ver][hor] != 0 or not(0 <= hor <= 2) or not(0 <= ver <= 2):
            raise ValueError
        self.board[ver][hor] = self.player_symbol

    def isWinner(self)-> bool:
        """Checks if the latest move resulted in a win
           Updating the wins count step is made in player module
        """
        for y in self.board:  
            if y[0] == y[1] == y[2] != 0 and self.name == self.last_player_name:
                self.incrementwins()
                print('You win!')
                return True            
        for i in range(3):
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != 0 and self.name == self.last_player_name:
                self.incrementwins()
                print('You win!')
                return True
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != 0 and self.name == self.last_player_name:
            self.incrementwins()
            print('You win!')
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != 0 and self.name == self.last_player_name:
            self.incrementwins()
            print('You win!')
            return True
        return False

    def isLosser(self)-> bool:
        """Checks if the latest move resulted in a losses
           Updating the losses count step is made in player module
        """
        for y in self.board:
            if y[0] == y[1] == y[2] != 0 and self.name != self.last_player_name:
                self.incrementlosses()
                print('You lost!')
                return True
        for i in range(3):
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != 0 and self.name != self.last_player_name:
                self.incrementlosses()
                print('You lost!')
                return True
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != 0 and self.name != self.last_player_name:
            self.incrementlosses()
            print('You lost!')
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != 0 and self.name != self.last_player_name:
            self.incrementlosses()
            print('You lost!')
            return True
        return False

    def BoardisFull(self)-> bool:
        """Checks if the board is full (I.e. no more moves to make - tie)
           Updates the ties count
        """
        for element in self.board:
            if 0 in element:
                return False
        self.incrementties()
        print('It is a draw!')
        return True

    def printStats(self)-> None:
        """Prints the following each on a new line:
            Prints the players user name
            Prints the user name of the last person to make a move
            prints the number of games
            Prints the number of wins
            Prints the number of losses
            Prints the number of ties
        """
        print("players user name:", self.getname())
        print("user name of the last person to make a move:", self.getlast_player_name())
        print("number of games:", self.updateGamesPlayed())
        print("number of wins", self.getwins())
        print("number of losses", self.getlosses())
        print("number of ties", self.getties())



