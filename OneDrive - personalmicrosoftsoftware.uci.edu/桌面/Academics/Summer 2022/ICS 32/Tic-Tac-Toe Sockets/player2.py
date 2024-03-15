import socket
from gameboard import Boardclass

def get_host_info():
   """get the host name and port"""
   serverAddress = input("Please enter server address:\n")
   serverPort = input("Please enter server port\n")
   return serverAddress, int(serverPort)

def connect_to_socket():
   """establish a socket connection"""
   s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   s.bind((get_host_info()))
   s.listen(5)
   conn,clientAddress = s.accept()
   return conn

def play(conn):
   """basically execute the game:
      The user can input the coordinate of the TicTacToe by x(horizontal, range from 0-2) and y (vertical, range from 0-2).
   """
   serverName = 'player2'
   clientName = conn.recv(7).decode()
   conn.send(serverName.encode())
   player2 = Boardclass(name = serverName)
   while True:
      player2.resetGameBoard()
      while not player2.isWinner() and not player2.isLosser() and not player2.BoardisFull():
         x2 = conn.recv(1).decode()
         y2 = conn.recv(1).decode()
         player2.setplayer_symbol('X')
         try:
            player2.updateGameBoard(int(x2), int(y2))
         except:
            pass      
         player2.setlast_player_name(clientName)
         player2.print_board()
         if player2.isLosser() or player2.isWinner()or player2.BoardisFull():
            break 
         x,y = int(input("Please enter x coordinate:(from 0-2)\n")), int(input("Please enter y coordinate:(from 0-2)\n"))
         player2.setplayer_symbol('O')
         player2.updateGameBoard(x, y)
         player2.setlast_player_name(serverName)
         player2.print_board()
         
         print('Waiting for the opponent to take the step...')
         conn.send(str(x).encode())
         conn.send(str(y).encode())
      continue_message = conn.recv(1).decode()
      if continue_message == 'n':
         print('Fun Times')
         player2.printStats()
         break
   conn.close()

if __name__ == "__main__":
    play(connect_to_socket())
