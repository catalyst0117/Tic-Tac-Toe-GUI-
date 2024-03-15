import socket
from gameboard import Boardclass


def get_host_info():
    """get the host name and port"""
    serverAddress = input("Please enter server address:\n")
    serverPort = input("Please enter server port\n")
    return serverAddress, int(serverPort)

def connect_to_socket():
    """create a socket object and connect to the server"""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((get_host_info()))
    except:
        continue_connect = input("connection failed, do you want to try again:(y/n)\n")
        while continue_connect == 'y':
            try:
                s.connect((input('new server address\n'),int(input('new serverPort\n'))))
            except:
                continue_connect = input("connection failed, do you want to try again:(y/n)\n")
        if continue_connect == 'n':
            quit()
    return s


def play(s):
    """basically execute the game：
       The user can input the coordinate of the TicTacToe by x(horizontal, range from 0-2) and y (vertical, range from 0-2).
    """
    clientname = 'player1'
    #since in piazza the professor say the username is up to us, I just name it player1
    s.send(clientname.encode()) 
    continue_play = 'y'
    player1 = Boardclass(name = clientname)
    serverName = s.recv(7).decode()
    while continue_play == 'y' or continue_play == 'Y':
        player1.resetGameBoard()
        while not player1.isWinner() and not player1.isLosser() and not player1.BoardisFull():
            player1.print_board()
            x,y = int(input("Please enter x coordinate:(from 0-2)\n")), int(input("Please enter y coordinate:(from 0-2)\n"))
            player1.setplayer_symbol('X')
            player1.updateGameBoard(x, y)
            player1.setlast_player_name(clientname)
            player1.print_board()
            if player1.isWinner() or player1.BoardisFull():
                s.send(str(x).encode())
                s.send(str(y).encode())
                break
            print('Waiting for the opponent to take the step...')
            s.send(str(x).encode())
            s.send(str(y).encode())
            x2 = s.recv(1).decode()
            y2 = s.recv(1).decode()
            player1.setplayer_symbol('O')
            player1.updateGameBoard(int(x2), int(y2))
            player1.setlast_player_name(serverName)
            if player1.isLosser():
                player1.print_board()
                break 
        continue_play = input('Do you want to play again? (y/Y)(n/N)\n')
        s.send(continue_play.encode())
    if continue_play == 'n' or continue_play == 'N':
        print('Fun Times')
        player1.printStats()
        s.close()

if __name__ == "__main__":
    play(connect_to_socket())
