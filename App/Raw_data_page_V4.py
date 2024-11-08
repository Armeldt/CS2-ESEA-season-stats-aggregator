import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageOps, ImageDraw
from CTkTable import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import pandas as pd

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
        
        values_scoreboard = []
        values_utils = []
        values_trades = []
        values_eco = []
        values_entry = []
        ### BODY ### 

        frame_body = ctk.CTkFrame(self)
        frame_body.grid(row=1, column=0, sticky="nwes")
        frame_body.grid_columnconfigure((0,1),weight=1)
        frame_body.grid_rowconfigure((0,1,2),weight=1)


        frame_scoreboard = ctk.CTkFrame(frame_body)
        frame_scoreboard.grid(row=0, column=0,columnspan=2, sticky="nwe")

        self.table_scoreboard = CTkTable(master=frame_scoreboard, row=6, column=18, values=values_scoreboard, width=80, height=30)
        self.table_scoreboard.grid(row=2, column=0, columnspan=3,padx=20, pady=20, sticky="new")

        frame_utils = ctk.CTkFrame(frame_body)
        frame_utils.grid(row=1, column=0, sticky="nwes")

        label_utils = ctk.CTkLabel(frame_utils,text='Raw data utility use & efficiency')
        label_utils.pack(side='top',pady=10,padx=10)

        self.table_utils = CTkTable(frame_utils, row=6, column=6, values=values_utils, width=90, height=30)
        self.table_utils.pack()

        frame_entry = ctk.CTkFrame(frame_body)
        frame_entry.grid(row=1, column=1, sticky="nwes")

        label_entry = ctk.CTkLabel(frame_entry,text='Raw data entry frags')
        label_entry.pack(side='top',pady=10,padx=10)

        self.table_entry = CTkTable(frame_entry, row=6, column=7, values=values_entry, width=90, height=30)
        self.table_entry.pack()

        frame_trades = ctk.CTkFrame(frame_body)
        frame_trades.grid(row=2, column=0, sticky="nwes")

        label_trades = ctk.CTkLabel(frame_trades,text='Raw data trades')
        label_trades.pack(side='top',pady=10,padx=10)

        self.table_trades = CTkTable(frame_trades,row=6, column=5,  values=values_trades, width=90, height=30)
        self.table_trades.pack()

        frame_eco = ctk.CTkFrame(frame_body)
        frame_eco.grid(row=2, column=1, sticky="nwes")

        label_eco = ctk.CTkLabel(frame_eco,text='Raw data kills impact with economy state')
        label_eco.pack(side='top',pady=10,padx=10)

        self.table_eco = CTkTable(frame_eco, row=6, column=8, values=values_eco, width=80, height=30)
        self.table_eco.pack(side='top',pady=10,padx=10)

    def update_data(self, analysis_results):
        
        
        scoreboard = analysis_results.get("scoreboard", pd.DataFrame())
        
        
        if not scoreboard.empty:
            headers_scoreboard = list(scoreboard.columns)
            values_scoreboard = [headers_scoreboard] + scoreboard.values.tolist()
        else:
            values_scoreboard = [
                ["name", "Rounds joués", "Kills", "Deaths", "Assists", "+/-", "K/D", "Damages", "ADR", "KPR", "HS", "HS %", "5K", "4K", "3K", "mvps", "KAST%", "Impact", "Rating"],
                
            ]
        self.table_scoreboard.configure(values=values_scoreboard)

        df_utils = analysis_results.get("util_stats", pd.DataFrame())
        
        if not df_utils.empty:
            headers_utils = list(df_utils.columns)
            values_utils = [headers_utils] + df_utils.values.tolist()
        else:
            values_utils = [
                ["name", "He_dmg", "Fire_dmg", "Total_utility_dmg", "enemies_flashed_total", "Flash_assist"],
                
            ]
        self.table_utils.configure(values=values_utils)

        df_entry = analysis_results.get("entry_stats", pd.DataFrame())

        if not df_entry.empty:
            headers_entry = list(df_entry.columns)
            values_entry = [headers_entry] + df_entry.values.tolist()
        else:
            values_entry = [
                ["name", "He_dmg", "Fire_dmg", "Total_utility_dmg", "enemies_flashed_total", "Flash_assist"],
                
            ]
        self.table_entry.configure(values=values_entry)

        df_trades = analysis_results.get("trading_stats", pd.DataFrame())

        if not df_trades.empty:
            headers_trades = list(df_trades.columns)
            values_trades = [headers_trades] + df_trades.values.tolist()
        else:
            values_trades = [
                ["name", "He_dmg", "Fire_dmg", "Total_utility_dmg", "enemies_flashed_total", "Flash_assist"],
                
            ]
        self.table_trades.configure(values=values_trades)

        # df_eco = analysis_results.get("trading_stats", pd.DataFrame())

        # if not df_eco.empty:
        #     headers = list(df_eco.columns)
        #     values_eco = [headers] + scoreboard.values.tolist()
        # else:
        #     values_eco = [
        #         ["name", "He_dmg", "Fire_dmg", "Total_utility_dmg", "enemies_flashed_total", "Flash_assist"],
                
        #     ]
        # self.table_eco.configure(values=values_eco)

if __name__ == "__main__":
    app = RawDataPage()
    app.protocol("WM_DELETE_WINDOW", app.quit)
    app.mainloop()
