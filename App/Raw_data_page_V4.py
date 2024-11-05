import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageOps, ImageDraw
from CTkTable import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

ctk.set_appearance_mode('dark')
ctk.set_default_color_theme("theme.json")
        

class RawDataPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        # configure grid layout for main window
        self.grid_columnconfigure(0, weight=1)  
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=5)
        

        ### BODY ### 

        frame_body = ctk.CTkFrame(self)
        frame_body.grid(row=1, column=0, sticky="nwes")
        frame_body.grid_columnconfigure((0,1),weight=1)
        frame_body.grid_rowconfigure((0,1,2),weight=1)


        frame_scoreboard = ctk.CTkFrame(frame_body)
        frame_scoreboard.grid(row=0, column=0,columnspan=2, sticky="nwe")

        #affichage d'une table
        values = [
            ["name", "Rounds joués", "Kills", "Deaths", "Assists", "+/-", "K/D","Damages", "ADR", "KPR", "HS", "HS %", "5K", "4K", "3K","mvps", "KAST%", "Impact", "Rating"],
            ['-silentGG', 84, 54, 52, 22, 2, 1.04, 5618, 66.88, 0.64, 25, 46.3, 0, 0, 4, 6, 77.4, 1.01, 1.08],
            ['BELDIYA00', 84, 87, 52, 19, 35, 1.67, 9280, 110.48, 1.04, 57, 65.52, 0, 3, 3, 13, 82.1, 1.83, 1.59],
            ['OzzieOzz', 84, 55, 48, 15, 7, 1.15, 5616, 66.86, 0.65, 31, 56.36, 0, 2, 3, 9, 72.6, 1.04, 1.08],
            ['Spiritix', 84, 73, 53, 21, 20, 1.38, 7628, 90.81, 0.87, 33, 45.21, 0, 1, 6, 15, 77.4, 1.49, 1.34],
            ['godofbaldz', 84, 56, 53, 18, 3, 1.06, 6005, 71.49, 0.67, 12, 21.43, 0, 1, 3, 5, 79.8, 1.07, 1.13]
        ]

        table_scoreboard = CTkTable(master=frame_scoreboard, row=6, column=19, values=values, width=80, height=30)
        table_scoreboard.grid(row=2, column=0, columnspan=3,padx=20, pady=20, sticky="new")

        frame_utils = ctk.CTkFrame(frame_body)
        frame_utils.grid(row=1, column=0, sticky="nwes")

        label_utils = ctk.CTkLabel(frame_utils,text='Raw data utility use & efficiency')
        label_utils.pack(side='top',pady=10,padx=10)

        table_utils = CTkTable(frame_utils, row=6, column=8, values=values, width=80, height=30)
        table_utils.pack()

        frame_entry = ctk.CTkFrame(frame_body)
        frame_entry.grid(row=1, column=1, sticky="nwes")

        label_entry = ctk.CTkLabel(frame_entry,text='Raw data entry frags')
        label_entry.pack(side='top',pady=10,padx=10)

        table_entry = CTkTable(frame_entry, row=6, column=8, values=values, width=80, height=30)
        table_entry.pack()

        frame_trades = ctk.CTkFrame(frame_body)
        frame_trades.grid(row=2, column=0, sticky="nwes")

        label_trades = ctk.CTkLabel(frame_trades,text='Raw data trades')
        label_trades.pack(side='top',pady=10,padx=10)

        table_trades = CTkTable(frame_trades, row=6, column=8, values=values, width=80, height=30)
        table_trades.pack()

        frame_eco = ctk.CTkFrame(frame_body)
        frame_eco.grid(row=2, column=1, sticky="nwes")

        label_eco = ctk.CTkLabel(frame_eco,text='Raw data kills impact with economy state')
        label_eco.pack(side='top',pady=10,padx=10)

        table_eco = CTkTable(frame_eco, row=6, column=8, values=values, width=80, height=30)
        table_eco.pack(side='top',pady=10,padx=10)

    def update_data(self, analysis_results):
        # Ajoutez le code pour mettre à jour les widgets de cette page avec analysis_results
        # Exemple d'accès aux données
        raw_data = analysis_results.get("raw_data", {})
        

if __name__ == "__main__":
    app = RawDataPage()
    app.protocol("WM_DELETE_WINDOW", app.quit)
    app.mainloop()
