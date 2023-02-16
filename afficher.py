"""sortie = ([[{'x1': 1.0, 'x2': 3.0, 'x3': 2.0, 'B': 40.0, 'E1': 1, 'E2': 0, 'E3': 0}, {'x1': 3.0, 'x2': 2.0, 'x3': 1.0, 'B': 45.0, 'E2': 1, 'E1': 0, 'E3': 0}, {'x1': 1.0, 'x2': 1.0, 'x3': 4.0, 'B': 38.0, 'E3': 1, 'E1': 0, 'E2': 0}, {'x1': 10.0, 'x2': 14.0, 
'x3': 12.0, 'B': 0, 'E1': 0, 'E2': 0, 'E3': 0}], [{'x1': 0.3333333333333333, 'x2': 1.0, 'x3': 0.6666666666666666, 'B': 13.333333333333334, 'E1': 0.3333333333333333, 'E2': 0.0, 'E3': 0.0}, {'x1': 2.3333333333333335, 'x2': 0.0, 'x3': -0.33333333333333326, 'B': 18.333333333333332, 'E2': 1.0, 'E1': -0.6666666666666666, 'E3': 0.0}, {'x1': 0.6666666666666667, 'x2': 0.0, 'x3': 3.3333333333333335, 'B': 24.666666666666664, 'E3': 1.0, 'E1': -0.3333333333333333, 'E2': 0.0}, {'x1': 5.333333333333334, 'x2': 0.0, 'x3': 2.666666666666668, 'B': -186.66666666666669, 'E1': -4.666666666666666, 'E2': 0.0, 'E3': 0.0}], [{'x1': 0.0, 'x2': 1.0, 'x3': 0.7142857142857142, 'B': 10.714285714285715, 'E1': 0.42857142857142855, 'E2': -0.14285714285714285, 'E3': 0.0}, {'x1': 1.0, 'x2': 0.0, 'x3': -0.14285714285714282, 'B': 7.857142857142856, 'E2': 0.42857142857142855, 'E1': -0.2857142857142857, 'E3': 0.0}, {'x1': 0.0, 'x2': 0.0, 'x3': 3.428571428571429, 'B': 19.428571428571427, 'E3': 1.0, 'E1': -0.14285714285714282, 'E2': -0.28571428571428575}, {'x1': 0.0, 'x2': 0.0, 'x3': 3.4285714285714297, 'B': -228.57142857142858, 'E1': -3.1428571428571423, 'E2': -2.285714285714286, 'E3': 0.0}], [{'x1': 0.0, 'x2': 1.0, 'x3': 0.0, 'B': 6.666666666666669, 
'E1': 0.4583333333333333, 'E2': -0.08333333333333333, 'E3': -0.2083333333333333}, {'x1': 1.0, 'x2': 0.0, 'x3': 0.0, 'B': 8.666666666666664, 'E2': 0.41666666666666663, 'E1': -0.29166666666666663, 'E3': 0.04166666666666665}, {'x1': 0.0, 'x2': 0.0, 
'x3': 1.0, 'B': 5.666666666666666, 'E3': 0.29166666666666663, 'E1': -0.04166666666666665, 'E2': -0.08333333333333334}, {'x1': 0.0, 'x2': 0.0, 'x3': 0.0, 'B': -248.00000000000003, 'E1': -2.9999999999999996, 'E2': -2.0, 'E3': -1.0000000000000002}]],
[['E1', 'E2', 'E3'], ['x2', 'E2', 'E3'], ['x2', 'x1', 'E3'], ['x2', 'x1', 'x3']],
['x1', 'x2', 'x3', 'E1', 'E2', 'E3', 'B', 'B/Col'])"""



from tkinter import Frame, Canvas, Scrollbar, Label


class afficher(Frame):
    def __init__(self, parent, width, height, tabs):
        Frame.__init__(self, parent)
        self.configure(width=width, height=height)
        self.canvas = Canvas(self, borderwidth=0, background="#ffffff", width=width, height=height)
        self.frame = Frame(self.canvas, background="#ffffff")
        self.frame.configure(width=width, height=height)
        self.vsb = Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.vsbb = Scrollbar(self, orient="horizontal", command=self.canvas.xview)
        self.canvas.configure(yscrollcommand=self.vsb.set)
        self.canvas.configure(xscrollcommand=self.vsbb.set)
        self.vsb.pack(side="right", fill="y")
        self.vsbb.pack(side="bottom", fill="x")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((4,4), window=self.frame, anchor="nw",
                                  tags="self.frame")

        self.frame.bind("<Configure>", self.onFrameConfigure)
        self.utils = self.get_tabs_info(tabs)
        self.list_tabs = []
        self.createTabs(self.utils[0], 20 * (self.utils[1] + 1), 20 * (self.utils[2] + 1), tabs)
    
    def onFrameConfigure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def get_tabs_info(self,tabss):
        nbr_tabs = tabss[0].__len__()
        nbr_colonnes = tabss[2].__len__() - 1
        nbr_lignes = tabss[1][0].__len__() + 1

        return (nbr_tabs, nbr_colonnes, nbr_lignes)
    
    def createTabs(self, nbr, width, height, tabss):
        for i in range(nbr):
            self.list_tabs.append('frame' + str(i))
            self.list_tabs[-1] = Frame(
                self.frame,
                bd=0,
                background='#C0C0C0'
            )
            self.list_tabs[-1].configure(width=width, height=height)
            self.list_tabs[-1].grid(padx=15, pady=15, column=0)
            self.affich(i, tabss)
    
    def affich(self, i, list_tabs):
        tab = list_tabs[0][i]
        for line in range(self.utils[2]):
            for col in range(self.utils[1] + 1):
                if line == 0 and col == 0:
                    Label(self.list_tabs[-1], text="V.B",font=("Arial,12"), bd=15, bg='#C0C0C0').grid(column=col, row=(line + 1))
                elif line == 0:
                    Label(self.list_tabs[-1], text=f"{list_tabs[2][col - 1]}",font=("Arial,12"), bd=15, bg='#C0C0C0').grid(column=col, row=(line + 1))
                elif col == 0:
                    Label(self.list_tabs[-1], text=f"{list_tabs[1][i][line - 1]}",font=("Arial,12"), bd=15, bg='#C0C0C0').grid(column=col, row=(line + 1))
                else:
                    Label(self.list_tabs[-1], text=f"{round(tab[line - 1][list_tabs[2][col - 1]], 3)}",font=("Arial,12"), bd=15, bg='#C0C0C0').grid(column=col, row=(line + 1))

        Label(self.list_tabs[-1], text="Cj",font=("Arial,12"), bd=15, bg='#C0C0C0').grid(column=0, row=(self.utils[2] + 1))
        for col in range(self.utils[1]):
            Label(self.list_tabs[-1], text=f"{round(tab[-1][list_tabs[2][col]], 3)}",font=("Arial,12"), bd=15, bg='#C0C0C0').grid(column=(col + 1), row=(self.utils[2] + 1))

#if __name__ == "__main__":
#    root=Tk()
#    example = afficher(root, 500, 500, sortie)
#    example.pack(side="top", fill="both", expand=True)
#    root.mainloop()