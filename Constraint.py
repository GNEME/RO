from tkinter import Frame, Entry, Scrollbar, Canvas, PhotoImage, Button

class Constraint(Frame):
    def __init__(self, parent, width, height):

        Frame.__init__(self, parent)
        self.parent = parent
        self.configure(width=width, height=height)#width=parent.wi/4.72131147541, height=self.parent/4.99512195122
        self.canvas = Canvas(self, borderwidth=0, background="#ffffff", width=width, height=height)
        self.frame = Frame(self.canvas, background="#ffffff")
        self.frame.configure(width=width, height=height)
        self.vsb = Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((4,4), window=self.frame, anchor="nw",
                                  tags="self.frame")

        self.frame.bind("<Configure>", self.onFrameConfigure)
        self.button_image3 = PhotoImage(
            file= "./window_images/button_3.png")
        self.list_values_contraintes = []
        self.list_button = []
        self.j = []

    def add(self):
        self.parent.update_idletasks()
        i = self.list_values_contraintes.__len__()
        self.list_values_contraintes.append('c' + str(i))
        self.list_button.append("button_im" + str(i))
        self.list_values_contraintes[i] = Entry(                                        # contrainte n0
            self.frame,
            bd=0,
            bg="#C0C0C0",
            fg="#000716",
            font=("Arial,12"),
            highlightthickness=0)
        self.list_values_contraintes[i].grid(padx=5, pady=5, column=1)

        self.list_button[i] = Button(                                     # deleteci pour supprimer une contrainte i
            self.frame,
            image=self.button_image3,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.delete(i),
            relief="flat"
        )
        self.list_button[i].grid(padx=5, row=i, column=2)

        return i
    
    def delete(self, i):
        if i == self.list_values_contraintes.__len__() - 1:
            self.list_values_contraintes[i].destroy()
            self.list_button[i].destroy()
            del(self.list_values_contraintes[i])
            del(self.list_button[i])
        else:
            self.j.append(i)
            indice = i
            for k in range(self.j.__len__() - 1):
                if i > self.j[k]:
                    indice = indice - 1
            self.list_values_contraintes[indice].destroy()
            self.list_button[indice].destroy()
            del(self.list_values_contraintes[indice])
            del(self.list_button[indice])
        self.update()
        self.parent.update()
        if self.list_values_contraintes.__len__() == 0:
            self.j = []

    def onFrameConfigure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def get_values(self, i):
        return self.list_values_contraintes[i].get()
    
    def put_values(self, i, string):
        self.list_values_contraintes[i].insert(0,string)

#if __name__ == "__main__":
#    root=Tk()
#    example = Constraint(root, 100, 100)
#    example.pack(side="top", fill="both", expand=True)
#    root.mainloop()