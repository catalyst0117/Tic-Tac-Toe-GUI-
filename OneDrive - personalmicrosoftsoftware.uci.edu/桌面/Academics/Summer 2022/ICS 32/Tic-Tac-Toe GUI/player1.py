import socket
from gameboard import Boardclass
import tkinter as tk
from tkinter import messagebox



def connect_to_socket(a, b):
    #create a socket object and connect to the server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((a, b))
        return s
    except:
        return False



    
class game():
    #Define my class constructor
    def __init__(self):
        self.canvasSetup()
        self.initTKVariables()
        self.createserverLabel()
        self.createserverEntry()
        self.createportLabel()
        self.createportEntry()
        self.createConnectButton()
        self.runUI()
        
        

    #define a method that initalizes my tk variables
    def initTKVariables(self):
        self.server = tk.StringVar()
        self.port = tk.IntVar()
        self.user = tk.StringVar()
        self.operation = tk.StringVar()
        self.result = tk.IntVar()
        self.continue_playVar = tk.StringVar()
    def canvasSetup(self):
        #initialize my tkinter canvas
        self.master  = tk.Tk()
        self.master.title("Tic-Tac-Toe") #sets the window title
        self.master.geometry('600x600') #sets the default size of the window
        self.master.configure(background='blue')#set the background colorof the window
        self.master.resizable(0,0)#setting the x(horizontal) and y (vertical) to not be resizable.
        self.master.columnconfigure(0, weight=1)
        self.master.columnconfigure(1, weight=1)
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

    def createConnectButton(self):
        self.ConnectButton = tk.Button(self.master,text="Connect to socket",command=self.connect).grid(row=5)
    def createSendButton(self):
        self.SendButton = tk.Button(self.master,text="Send username",command=self.send).grid(row=8)
    def connect(self, event=None):
        self.servername = self.server.get()
        self.portnumber = self.port.get()
        self.soc = connect_to_socket(self.servername, self.portnumber)
        if self.soc == False:
            self.again = tk.Label(self.master, text='Connection failed, do you want to try again?')
            self.again.grid()
            self.againyesButton = tk.Button(self.master,text="Yes", command=self.yes)
            self.againyesButton.grid()
            self.againnoButton = tk.Button(self.master,text="No", command=self.master.destroy)
            self.againnoButton.grid()
        else:
            self.createuserLabel()
            self.createuserEntry()
            self.createSendButton()

    def yes(self, event=None):
        self.server.set('')
        self.port.set(0)
        self.again.grid_forget()
        self.againyesButton.grid_forget()
        self.againnoButton.grid_forget()
    def send(self, event=None):
        self.soc.send(self.user.get().encode())
        self.serverName = self.soc.recv(15).decode()
        self.player1 = Boardclass(name = self.user.get())
        self.print_Board()
    
    def print_Board(self):



        self.statusLabel = tk.Label(self.master, text='game taking place', width=25)
        self.statusLabel.grid(row = 15)
        self.turnLabel = tk.Label(self.master, text=f'turn:{self.user.get()}', width=25)
        self.turnLabel.grid(row=16)
        self.grid_frame = tk.Frame(self.master)
        self.grid_frame.grid(row=9)
        self.b = [[0,0,0],[0,0,0],[0,0,0]]
        for self.i in range(3):
            for self.j in range(3):                         
                self.b[self.i][self.j] = tk.Button(self.grid_frame,text='', height = 4, width = 8)
                self.b[self.i][self.j].bind("<ButtonPress-1>", self.update)
                self.b[self.i][self.j].grid(row=self.i, column=self.j)
        
                
        
       
    def update(self, event):
        clicked_btn = event.widget
        clicked_btn['text'] = 'X'

        clicked_btn['state'] = 'disabled'

        clicked_btn.update()
        self.x = clicked_btn.grid_info()['column']
        self.y = clicked_btn.grid_info()['row']
        self.player1.setplayer_symbol('X')
        self.player1.updateGameBoard(self.x, self.y)
        self.player1.setlast_player_name(self.user.get())
        if self.player1.isWinner():
            self.statusLabel['text'] = 'You win!'
            self.soc.send(str(self.x).encode())
            self.soc.send(str(self.y).encode())
            self.master.after(1000, self.continue_play())
            return
        if self.player1.BoardisFull():
            self.statusLabel['text'] = 'It is a tie'
            self.soc.send(str(self.x).encode())
            self.soc.send(str(self.y).encode())
            self.master.after(1000, self.continue_play())
            return
        self.turnLabel['text'] = f'turn:{self.serverName}'
        self.turnLabel.update()
        self.soc.send(str(self.x).encode())
        self.soc.send(str(self.y).encode())
        self.master.after(1000, self.wait_for_message())
    def wait_for_message(self):
        x2 = int(self.soc.recv(1).decode())
        y2 = int(self.soc.recv(1).decode())
        self.b[y2][x2]['text'] = 'O'

        self.b[y2][x2]['state'] = 'disabled'
        self.b[y2][x2].update()

        self.player1.setplayer_symbol('O')
        self.player1.updateGameBoard(int(x2), int(y2))
        self.player1.setlast_player_name(self.serverName)
        if self.player1.isLosser():
            self.statusLabel['text'] = 'You lose!'
            
            self.master.after(1000, self.continue_play())
            return
        if self.player1.BoardisFull():
            self.statusLabel['text'] = 'It is a tie!'
            self.statusLabel.update()
            self.continue_message()
            return
        self.turnLabel['text'] = f'turn:{self.user.get()}'
            
    def continue_play(self):
        self.continue_playmessage = tk.messagebox.askyesno(message = 'Do you want to play again?')
        if self.continue_playmessage == True:
            self.soc.send('y'.encode())
            self.player1.resetGameBoard()
            self.statusLabel.grid_forget()
            self.grid_frame.grid_forget()
            self.print_Board()
        else:
            self.soc.send('n'.encode())
            self.continue_playLabel = tk.Label(self.master, text=self.player1.printStats())
            self.continue_playLabel.grid(row=20)
            self.soc.close()
    #define a method start UI
    def runUI(self):
        #starts my UI - event handler
        self.master.mainloop()
        
    

if __name__ == "__main__":
    game()
