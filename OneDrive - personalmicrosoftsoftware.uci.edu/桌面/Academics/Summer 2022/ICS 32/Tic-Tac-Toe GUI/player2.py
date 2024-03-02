import tkinter as tk
import socket
from gameboard import Boardclass


def connect_to_socket(a, b):
   """establish a socket connection"""
   s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   s.bind((a, b))
   s.listen(5)
   conn,clientAddress = s.accept()
   return conn

class game():
    master = 0

    """#Define my tkinter class variables
    server = '127.0.0.1'
    port = 8000
    user = 'player2'
    operation = 0
    result = 0
    #Define my class constructor"""
    def __init__(self):
        #intializing my calculator class variable
        '''self.myCalc = calc.Calculator()'''

        #call my method to create my canvas and add my widgets
        self.canvasSetup()
        self.initTKVariables()
        
        self.createserverLabel()
        self.createserverEntry()
        
        self.createportLabel()
        self.createportEntry()
        self.createSubmitButton()
        self.runUI()
        

    #define a method that initalizes my tk variables
    def initTKVariables(self):
        self.server = tk.StringVar()
        self.port = tk.IntVar()
        self.user = tk.StringVar()
        self.operation = tk.StringVar()
        self.result = tk.IntVar()
    def canvasSetup(self):
        #initialize my tkinter canvas
        self.master  = tk.Tk()
        self.master.title("Tic-Tac-Toe") #sets the window title
        self.master.geometry('600x600') #sets the default size of the window
        self.master.configure(background='green')#set the background colorof the window
        self.master.resizable(0,0)#setting the x(horizontal) and y (vertical) to not be resizable.

    def createserverLabel(self):
        self.serverLabel = tk.Label(self.master, text='Enter server name:', width=25)
        self.serverLabel.grid(row=1)
          
    #define a method that creates a number entry field
    def createserverEntry(self):
        self.serverEntry = tk.Entry(self.master,textvariable=self.server, width=25)
        self.serverEntry.grid(row=2)

    #define a method that creates a number entry field
    def createportLabel(self):
        self.portLabel = tk.Label(self.master, text='Enter port number:', width=25)
        self.portLabel.grid(row=3)

    def createportEntry(self):
        self.portEntry = tk.Entry(self.master, textvariable=self.port, width=25)
        self.portEntry.grid(row=4)

    def createuserLabel(self):
        self.userLabel = tk.Label(self.master, text='Enter user name:', width=25)
        self.userLabel.grid(row=6)

    def createuserEntry(self):
        self.userEntry = tk.Entry(self.master, textvariable=self.user, width=25)
        self.userEntry.grid(row=7)

    def createSubmitButton(self):
        self.ConnectButton = tk.Button(self.master,text="Submit",command=self.connect).grid(row=5)

    def createSendButton(self):
        self.SendButton = tk.Button(self.master,text="Send username",command=self.send).grid(row=8)
    
    def connect(self, event=None):
        self.serverName = self.server.get()
        self.portnumber = self.port.get()
        self.soc = connect_to_socket(self.serverName, self.portnumber)
        self.createuserLabel()
        self.createuserEntry()
        self.clientName = self.soc.recv(15).decode()
        self.createSendButton()

    def send(self, event=None):
        self.soc.send(self.user.get().encode())
        self.player2 = Boardclass(name = self.user.get())
        self.print_Board()
        
        
        
        
    def print_Board(self):     
        self.statusLabel = tk.Label(self.master, text='game taking place', width=25)
        self.statusLabel.grid(row=15)
        self.turnLabel = tk.Label(self.master, text=f'turn:{self.clientName}', width=25)
        self.turnLabel.grid(row=16)
        self.grid_frame = tk.Frame(self.master)
        self.grid_frame.grid(row=9)
        self.b = [[0,0,0],[0,0,0],[0,0,0]]
        for self.i in range(3):
            for self.j in range(3):                         
                self.b[self.i][self.j] = tk.Button(self.grid_frame,text='', height = 4, width = 8)
                self.b[self.i][self.j].bind("<ButtonPress-1>", self.update)
                self.b[self.i][self.j].grid(row=self.i, column=self.j)
        self.grid_frame.update()
        self.x2 = int(self.soc.recv(1).decode())
        self.y2 = int(self.soc.recv(1).decode())
        self.b[self.y2][self.x2]['text'] = 'X'

        self.b[self.y2][self.x2]['state'] = 'disabled'
        
        self.b[self.y2][self.x2].update()
        self.player2.setplayer_symbol('X')

        self.player2.updateGameBoard(int(self.x2), int(self.y2))
           
        self.player2.setlast_player_name(self.clientName)
        self.turnLabel['text'] = f'turn:{self.user.get()}'
        self.turnLabel.update()

    def update(self, event):
        clicked_btn = event.widget
        clicked_btn['text'] = 'O'

        clicked_btn['state'] = 'disabled'

        clicked_btn.update()
        self.x = clicked_btn.grid_info()['column']
        self.y = clicked_btn.grid_info()['row']
        self.player2.setlast_player_name(self.user.get())
        self.player2.setplayer_symbol('O')
        self.player2.updateGameBoard(self.x, self.y)
        
        if self.player2.isWinner():
           self.statusLabel['text'] = 'You win!'
           self.statusLabel.update()
           self.soc.send(str(self.x).encode())
           self.soc.send(str(self.y).encode())
           self.continue_message()
           return
        if self.player2.BoardisFull():
           self.statusLabel['text'] = 'It is a tie!'
           self.statusLabel.update()
           self.soc.send(str(self.x).encode())
           self.soc.send(str(self.y).encode())
           self.continue_message()
           return

        

        self.soc.send(str(self.x).encode())
        self.soc.send(str(self.y).encode())
        
        self.turnLabel['text'] = f'turn:{self.clientName}'
        self.turnLabel.update()

        self.wait_for_message()
        
    def wait_for_message(self):
       
        self.x2 = int(self.soc.recv(1).decode()) 
        self.y2 = int(self.soc.recv(1).decode())
        self.b[self.y2][self.x2]['text'] = 'X'

        self.b[self.y2][self.x2]['state'] = 'disabled'

        self.b[self.y2][self.x2].update()
        self.player2.setplayer_symbol('X')
        self.player2.updateGameBoard(int(self.x2), int(self.y2))
        self.player2.setlast_player_name(self.clientName)

        if self.player2.isLosser():
            self.statusLabel['text'] = 'You loss!'
            self.statusLabel.update()
            self.continue_message()
            return
        if self.player2.BoardisFull():
            self.statusLabel['text'] = 'It is a tie!'
            self.statusLabel.update()
            self.continue_message()
            return
        self.turnLabel['text'] = f'turn:{self.user.get()}'
        self.turnLabel.update()
    def continue_message(self):
        continue_message = self.soc.recv(1).decode()
        if continue_message == 'y':
            self.player2.resetGameBoard()
            self.statusLabel.grid_forget()
            self.statusLabel.update()
            self.grid_frame.grid_forget()
            self.grid_frame.update()
            self.print_Board()
        if continue_message == 'n':
            self.StatsLabel = tk.Label(self.master, text=self.player2.printStats())
            self.StatsLabel.grid(row=20)
            self.soc.close()
    def runUI(self):
        #starts my UI - event handler
        self.master.mainloop()
if __name__ == "__main__":
    game()
