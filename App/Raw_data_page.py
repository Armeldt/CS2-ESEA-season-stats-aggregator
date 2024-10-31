import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageOps, ImageDraw
from CTkTable import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

ctk.set_appearance_mode('dark')
ctk.set_default_color_theme("theme.json")

class RawDataPage(ctk.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("CS2 Stats Aggregator")
        self.geometry(f"{1600}x{900}")

        # configure grid layout for main window
        self.grid_columnconfigure(0, weight=1)  
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=5)
        

        #### Header ####
        frame_header = ctk.CTkFrame(self)
        frame_header.grid(row=0, column=0,columnspan=2, sticky="nwe")

        # Configurer les colonnes du frame_header
        frame_header.grid_columnconfigure(0, weight=1)  # Colonne pour le titre (gauche)
        frame_header.grid_columnconfigure(1, weight=1)  # Colonne pour les boutons (droite)

        # Titre aligné à gauche
        title = ctk.CTkLabel(master=frame_header, text='CS2 STATS AGGREGATOR', font=("Stratum2 Bd", 50), text_color=('#fbac18'))
        title.grid(row=0, column=0, sticky="w", padx=20, pady=15)

        # Frame des boutons aligné à droite
        button_frame = ctk.CTkFrame(master=frame_header, fg_color="transparent")
        button_frame.grid(row=0, column=1, sticky="e", padx=20,pady=15)

        ### Boutons de navigation dans button_frame ###
        button_home = ctk.CTkButton(master=button_frame, text='Home', font=('Stratum2 Bd', 20))
        button_home.grid(row=0, column=0, padx=20)

        button_team_summary = ctk.CTkButton(master=button_frame, text='Team Season Summary', font=('Stratum2 Bd', 20))
        button_team_summary.grid(row=0, column=1, padx=20)

        button_player_details = ctk.CTkButton(master=button_frame, text='Players Detailed Performances', font=('Stratum2 Bd', 20))
        button_player_details.grid(row=0, column=2, padx=20)

        button_match_analysis = ctk.CTkButton(master=button_frame, text='Specific Match Analysis', font=('Stratum2 Bd', 20))
        button_match_analysis.grid(row=0, column=3, padx=20)

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


        

if __name__ == "__main__":
    app = RawDataPage()
    app.protocol("WM_DELETE_WINDOW", app.quit)
    app.mainloop()
