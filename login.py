from tkinter import Tk, Canvas, Entry, Button
from PIL import Image, ImageTk
from window import *

class Login(Tk):
    def __init__(self):
        super().__init__()
        self.title("Methode du Simplexe")
        self.width = 950
        self.height = self.width - int(self.width / 3.46153846154)                                          # Proportionnelle
        self.geometry(f"{self.width}x{self.height}+0+0")                                                    # widthxheight+left+top    1440x1024+0+0
        self.resizable(False, False)
        self.iconphoto(False, ImageTk.PhotoImage(Image.open('icon.png')))
        self.configure(bg = "#D5D6DF")
        
        self.canvas = Canvas(
        self,
        bg = "#D5D6DF",
        height = self.height,                                                                   #1024
        width = self.width,                                                                     #1440
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
        )
        
        self.canvas.place(x = 0, y = 0)
        self.image_image_1 = ImageTk.PhotoImage(
        Image.open("./login_images/image_1.png").resize((int(self.height/1.14285714286), int(self.width/1.37931034483))))
        image_1 = self.canvas.create_image(
        self.width/3.29840408867,                                                     #436.57476806640625
        self.height/2.00391389432,                                                                  #511.0
        image=self.image_image_1
        )
       
        self.welcom = self.canvas.create_text(
        (self.width/1.31267092069),                                                                         #1097.0
        (self.height/34.1333333333),                                                                           #30.0
        anchor="nw",
        text="Welcome !",
        fill="#000000",
        font=("Inter Bold", 40 * -1)
        )

        self.canvas.create_text(
        self.width/1.4131501472,                                                 #1019.0,
        self.height/1.03329969728 - 7,                                                  #991.0,
        anchor="nw",
        text="by @gg and @alain",
        fill="#0F1B5C",
        font=("Inter Regular", 20 * -1)
        )

        self.canvas.create_text(
        self.width/1.4131501472,                                                 #1019.0,
        self.height/3.68345323741,                                               #278.0,
        anchor="nw",
        text="Login",
        fill="#000000",
        font=("Inter ExtraBold", 25 * -1)
        )

        self.canvas.create_rectangle(
        self.width/1.40625,                                         #1024.0,
        self.height/3.25079365079 + 7,                                  #315.0,
        self.width/1.17551020408,                                              #1225.0,
        self.height/3.24050632911 + 7,                                  #316.0,
        fill="#809AF6",
        outline="")

        # self.entry_image_1 = PhotoImage(
        # file= "./login_images/entry_1.png")
        self.Username = Entry(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0
        )
        self.Username.place(
        x=self.width/1.4201183432,                                                  #1014.0,
        y=self.height/2.61224489796,                                                    #392.0,
        width=self.width/5,                                                         #288.0
        height=self.height/31.0303030303                                            #33.0
        )
        self.Username.insert(0, 'Username')

        # self.entry_image_2 = PhotoImage(
        # file= "./login_images/entry_2.png")
        self.Password = Entry(
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0,
        show='*'
        )
        self.Password.place(
        x=self.width/1.4201183432,                                                  #1014.0,
        y=self.height/2.11570247934,                                                 #484.0,
        width=self.width/5,                                                         #288.0
        height=self.height/31.0303030303                                            #33.0
        )
        self.Password.insert(0, 'Password')

        def auth(username, password):
            if username=="Username" and password=="Password":                                   # definir ici le mot de passe et le username et l'action a faire si on a un bon mot de passe
                my_width = self.width
                x = self.winfo_x()
                y = self.winfo_y()
                self.destroy()
                app = window(my_width, x, y)
                app.mainloop()
                #print("True")

        self.button_image_1 = ImageTk.PhotoImage(
        Image.open("./login_images/button_1.png").resize((int(self.height/7.87692307692) + 1, int(self.width/22.8571428571) + 1)))
        self.login = Button(
        image=self.button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: auth(self.Username.get(), self.Password.get()),
        relief="flat"
        )
        self.login.place(
        x=self.width/1.31267092069,                                                                         #1097.0
        y=self.height/1.64895330113,                                                                         #621.0,
        width=self.width/13.0909090909,                                                                      #110.0,
        height=self.height/23.2727272727                                                                    #44.0
        )
