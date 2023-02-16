from tkinter import Tk, Canvas, Entry, Button, PhotoImage, Radiobutton, IntVar, messagebox
from PIL import Image, ImageTk
from Constraint import *
from traitements import my_main
#from simplexe import simplexe_main
import pysimplex as ps
from adapter import *
from afficher import *

class window(Tk):
    def __init__(self, my_width, x, y):
        super().__init__()
        self.title("Methode du Simplexe")
        self.width = my_width                                                        # width
        self.height = self.width - int(self.width / 3.46153846154)                              #height
        self.geometry(f"{self.width}x{self.height}+{x}+{y}")
        self.resizable(False, False)
        self.iconphoto(False, ImageTk.PhotoImage(Image.open('icon.png')))
        self.configure(bg = "#FFFFFF")
        self.frame2 = None

        self.canvas = Canvas(
        self,
            bg = "#D5D6DF",
            height = self.height,
            width = self.width,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )

        self.canvas.place(x = 0, y = 0)
        self.canvas.create_rectangle(
            0.0,
            self.height/341.333333333,                                                       #3.0,
            self.width,                                         #1440.0,
            self.height/2.86033519553,                                  #358.0,
            fill="#F5F5F5",
            outline="")

        self.canvas.create_text(
            self.width/120,                                          #12.0,
            self.height/85.3333333333,                                   #12.0,
            anchor="nw",
            text="Fonction objective :",
            fill="#000000",
            font=("Inter Bold", 25 * -1)
        )

        # self.entry_image_1 = PhotoImage(
        #     file= "./window_images/entry_1.png")
        self.zexpression = Entry(                                    # zexpression
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            font=("Arial,12"),
            highlightthickness=0
        )
        self.zexpression.place(
            x=self.width/4.70588235294 + 27,                                  #306.0,
            y=self.height/85.3333333333,                                     #18.0,
            width=self.width/3.68286445013 - 30,                      #391.0,
            height=self.height/20.8979591837                        #49.0
        )
        self.zexpression.insert(0, '2*x1 + 3*x2')

        self.max_min = IntVar()                                     # valeur(value) 0 pour une minimisation et valeur 1 pour une maximisation
        self.Min = Radiobutton(                                     # Modifie
            borderwidth=0,
            highlightthickness=0,
            variable=self.max_min,
            value=0,
            relief="flat"
        )
        self.Min.place(
            x=self.width/11.52,                                              #125.0,
            y=self.height/6.20606060606,                                         #165.0,
            width=self.width/90 + 7,                                                 #16.0,
            height=self.height/73.1428571429 + 7                                    #14.0
        )

        self.Max = Radiobutton(                                     # Modifie
            variable=self.max_min,
            value=1,
        )
        self.Max.place(
            x=self.width/4.69055374593 + 7,                                              #307.0,
            y=self.height/6.4                               #160.0,
        )

        self.canvas.create_text(
            self.width/29.387755102,                                         #49.0,
            self.height/6.73684210526,                                               #152.0,
            anchor="nw",
            text="Min",
            fill="#000000",
            font=("Inter ExtraBold", 25 * -1)
        )

        self.canvas.create_text(
            self.width/5.92592592593,                                #243.0,
            self.height/6.69281045752,                                           #153.0,
            anchor="nw",
            text="Max",
            fill="#000000",
            font=("Inter ExtraBold", 25 * -1)
        )

        self.canvas.create_text(
            self.width/1.8485237484,                         #779.0,
            self.height/85.3333333333 - 7,                                   #12.0,
            anchor="nw",
            text="Contraintes :",
            fill="#000000",
            font=("Inter Bold", 25 * -1)
        )

        self.frame1 = Constraint(self, self.width/4.72131147541 + 30, self.height/4.99512195122 + 37)                                             #305, 205
        self.frame1.configure(width=self.width/4.72131147541 + 50, height=self.height/4.99512195122 + 57)
        self.frame1.place(x=self.width/1.9944598338, y=self.height/22.7555555556)                                                       #x=722.0, y=45.0

        # self.entry_image_2 = PhotoImage(
        #     file= "./window_images/entry_2.png")

        def ajouter():                                               # Ajout de nouvelles contraintes
            if self.frame1.add() == 0:
                self.frame1.put_values(0, '2*x1 + 3*x2 <= 39')

        self.button_image_4 = PhotoImage(
            file= "./window_images/button_4.png")
        self.ajout = Button(
            image=self.button_image_4,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: ajouter(),
            relief="flat"
        )
        self.ajout.place(
            x=self.width/1.15292233787,                                  #1249.0,
            y=self.height/26.2564102564,                                 #39.0,
            width=self.width/8.57142857143,                                          #168.0,
            height=self.height/34.1333333333                                        #30.0
        )   

        self.button_image_5 = PhotoImage(
            file= "./window_images/button_5.png")
        self.valider = Button(
            image=self.button_image_5,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.get_frame_output(),
            relief="flat")
        self.valider.place(
            x=self.width/1.16316639742,                                                  #1238.0,
            y=self.height/3.83520599251,                                                 #267.0,
            width=self.width/8.57142857143,                                          #168.0,
            height=self.height/27.6756756757                                    #37.0
        )

    """Faire le traitements ici dans la fonction ci dessous, appels des autres fonctions pour la methode simplexe et affichage, ..."""

    def get_frame_output(self):
        contraintes = []
        if not(self.frame2 is None):
            self.frame2.destroy()
        for i in range(self.frame1.list_values_contraintes.__len__()):
            contraintes.append(self.frame1.get_values(i))
        juice = {
            'Z':self.zexpression.get(),
            'C':contraintes,
            'max_min':self.max_min.get()
        }
        #print("voici juice = ", juice)
        donnes = my_main(juice)
        #print("Voici donnes = ", donnes)
        if donnes == {}:
            messagebox.showwarning(message="Veuillez respectez la syntaxe de saisie !")
        else:
            #util = simplexe_main(donnes)
            problem = ps.Problem(liste_constraints(donnes),z_fonction(donnes['Z']),True)
            tableaux = problem.solve()
            util = ([],[],[])
            variables = tableaux[0].variables()
            variables.append('B')
            variables.append('B/Col')
            util[2].extend(variables)
            #print(len(tableaux))
            for t in tableaux:
                util[0].append(t.data())
                #print(t.base())
                util[1].append(t.base())
            flag = 1
            compteur = 0
            #print(util[1])
            for string in util[1][-1]:
                if string[0] == 'A' and round(util[0][-1][compteur]['B'], 3) != 0:
                    messagebox.showinfo(message="Problème impossible à résoudre !")
                    flag = 0
                compteur = compteur + 1
            if flag == 1:
                self.frame2 = afficher(self, self.width - 150, self.height - (self.height/2.84888888889) - 60, util)
                self.frame2.configure(width=self.width - 110, height=self.height - (self.height/2.84888888889) - 30)
                self.frame2.place(x=10, y=(self.height/2.84888888889) + 20)                             #y=225
