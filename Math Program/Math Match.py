import tkinter as tk
from tkinter.constants import FALSE
from typing import Text
import BetterShadows as bsha
import math, random
from functools import partial

#Should probably include colour constants here


class MathMatch():
    def __init__(self):

        #Main window for game to be in
        window = tk.Tk()
        window.geometry('809x500')
        window.resizable(False,False)
        window.title('Math Match')

        #Container to hold the other frames
        container = tk.Frame(window)
        container.pack(side = "top", fill = "both", expand = True)

        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)


        #Initialize the array of frames
        self.frames = {}


        #Iterate through frames, initialize them and put them in array
        for F in (MainMenu, HelpScreen, GameScreen):

            frame = F(container, self)
            self.frames[F] = frame

            frame.grid(row = 0, column = 0, sticky ="nsew")


        #Make Main Menu the first frame to be seen
        self.show_frame(MainMenu)


    #Function to show the desired frame
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


#Main menu and the frame the game starts up with
class MainMenu(tk.Frame):
    def __init__(self, container, controller):
        tk.Frame.__init__(self, container, bg='#E8E8E8') #F8F8F8 #E1E1E1 ##E8E8E8

        #Configure columns
        self.grid_columnconfigure((0,1,2), weight = 1)

        #Create three buttons
        self.play_button = bsha.BetterShadow(200, 100, self, "PLAY")
        self.help_button = bsha.BetterShadow(200, 100, self, "HELP")
        self.quit_button = bsha.BetterShadow(200, 100, self, "QUIT")
        
        #Put each button in the right place
        for B in ((0,self.play_button), (1,self.help_button), (2,self.quit_button)):
            B[1].grid(row=1,column=B[0],padx=10,pady=50)
            B[1].grid_propagate(False)
        
        #Set button commands
        self.play_button.button.configure(command = lambda : controller.show_frame(GameScreen))
        self.help_button.button.configure(command = lambda : controller.show_frame(HelpScreen))
        self.quit_button.button.configure(command = quit)

        #Create title object
        self.titleimage = tk.PhotoImage(file = 'assets/Titles/Title-Montserrat-Blue.png')
        self.title = tk.Label(self, image = self.titleimage, width = 800, height = 100, bg = '#E8E8E8')
        self.title.grid(row = 0, column = 0, columnspan=3, pady=50)


#Help menu frame, currently only here for testing
class HelpScreen(tk.Frame):
    def __init__(self, container, controller):
        tk.Frame.__init__(self, container, bg = 'green')

#Main gameplay screen
class GameScreen(tk.Frame):
    def __init__(self, container, controller):
        tk.Frame.__init__(self, container, bg = '#E8E8E8')
        self.grid_columnconfigure((0,1,2,3), weight = 1)

        #Create a container for the back button
        self.back_container = tk.Frame(self,bg = 'red')
        self.back_container.grid()

        #Create a back button
        self.back_button = bsha.BetterShadow(90, 40, self, "BACK")
        self.back_button.grid(row = 0, column = 0, pady = 0)

        #Create list of equations for the buttons to display
        self.eqs = []

        self.operations = ["add", "subtract","divide","multiply"]
        for i in range(4):
            x = random.randint(1,10) #Inclusive
            for i in range(2):
                self.eqs.append(self.algebra_create(random.choice(self.operations), x) + [False])
        random.shuffle(self.eqs)

        #Tuples in self.eqs are in the form of (Equation, X Value, Answered?)

        #Initialise buttons array
        self.buttons = []

        #Create 8 buttons
        for i in range(8):
            self.buttons.append(bsha.BetterShadow(190, 120, self, self.eqs[i][0]))
            self.buttons[i].grid(row = math.floor(i/4)+2, column = i%4)
            self.buttons[i].button.configure(command = partial(self.press,i))

        #Initialise whether a button is pressed or not
        self.pressed = False

        #Create container to hold the text widget
        self.text_container = tk.Frame(self, bg = 'red', width = 800, height=190)
        self.text_container.grid(column = 0, row = 1, columnspan=8, pady=(0,10))

        self.text_container.grid_rowconfigure(0, weight = 1)
        self.text_container.grid_columnconfigure(0, weight = 1)
        self.text_container.grid_propagate(False)

        #Create text widget
        self.text = tk.Text(self.text_container, bg = '#E8E8E8', height = 1, bd = 0, takefocus = 0, font = ("Open Sans Semibold","56"), fg = "black")
        self.text.grid(column = 0, row = 0, sticky = 'NESW')
        self.text.insert('end', "Time:\nScore:")
        self.text.configure(selectbackground=self.text.cget('bg'), selectforeground=self.text.cget('fg'))

        self.text.configure(state = tk.DISABLED)

    #Function to run when a button is clicked
    def press(self, idx):
        # if self.eqs[idx][2] == False:
        if self.pressed == False:
            self.buttons[idx].button.configure(bg = '#F0F0F0')
            self.pressed = True
            self.button_down = idx
        elif self.pressed == True and self.button_down != idx:
            if self.eqs[idx][1] == self.eqs[self.button_down][1]: #If buttons have the same value
                colour = '#03fc8c'
                self.eqs[idx][2] = True
                self.eqs[self.button_down][2] = True
            else: 
                colour = '#e32222'
            self.buttons[idx].button.configure(bg = colour)
            self.buttons[self.button_down].button.configure(bg = colour)
            self.pressed = False
        print(self.eqs[idx])
        
    #Function for creating the equations on the buttons
    def algebra_create(self, operation, x):
        if operation == "subtract":
            ans = random.randint(1,20-x) #Inclusive
            return([str(ans+x)+"−X="+str(ans), x])
        elif operation == "add":
            ans = random.randint(x+1,20) #Inclusive
            return([str(ans-x)+"+X="+str(ans), x])
        elif operation == "divide":
            ans = random.choice(list(range(2,math.floor(20/x)+1)))
            return([str(ans*x)+"÷X="+str(ans), x])
        elif operation == "multiply":
            num = random.choice(list(range(2,math.floor(20/x)+1)))
            return([str(num)+"×X="+str(num*x), x])

MathMatch()
tk.mainloop()