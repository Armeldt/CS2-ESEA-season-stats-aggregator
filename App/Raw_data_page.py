import customtkinter as ctk
from CTkTable import *
import matplotlib.pyplot as plt
import pandas as pd
        

class RawDataPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        
        # Configure grid layout for the main window
        self.grid_columnconfigure(0, weight=1)  
        self.grid_rowconfigure(0, weight=1)
        
        ### BODY ###
        frame_body = ctk.CTkFrame(self,fg_color='transparent')
        frame_body.grid(row=0, column=0, sticky="nwes")
        frame_body.grid_columnconfigure((0, 1), weight=1)
        frame_body.grid_rowconfigure((0, 1, 2), weight=1)
        
        # Scoreboard
        frame_scoreboard = ctk.CTkFrame(frame_body,fg_color='#292929')
        frame_scoreboard.grid(row=0, column=0, columnspan=2, sticky="nwes", pady=(10, 5), padx=10)

        label_scoreboard = ctk.CTkLabel(frame_scoreboard, text='Aggregated scoreboard')
        label_scoreboard.pack(side='top', pady=5, padx=5)
        self.frame_scoreboard = frame_scoreboard
        self.table_scoreboard = None

        # Utility stats
        frame_utils = ctk.CTkFrame(frame_body,fg_color='#292929')
        frame_utils.grid(row=1, column=0, sticky="nwes", pady=5, padx=(10, 5))

        label_utils = ctk.CTkLabel(frame_utils, text='Raw data utility use & efficiency')
        label_utils.pack(side='top', pady=5, padx=5)
        self.frame_utils = frame_utils
        self.table_utils = None

        # Entry frags
        frame_entry = ctk.CTkFrame(frame_body,fg_color='#292929')
        frame_entry.grid(row=1, column=1, sticky="nwes", pady=5, padx=(5, 10))

        label_entry = ctk.CTkLabel(frame_entry, text='Raw data entry frags')
        label_entry.pack(side='top', pady=5, padx=5)
        self.frame_entry = frame_entry
        self.table_entry = None

        # Trades
        frame_trades = ctk.CTkFrame(frame_body,fg_color='#292929')
        frame_trades.grid(row=2, column=0, sticky="nwes", pady=(5, 10), padx=(10, 5))

        label_trades = ctk.CTkLabel(frame_trades, text='Raw data trades')
        label_trades.pack(side='top', pady=5, padx=5)
        self.frame_trades = frame_trades
        self.table_trades = None

        # Eco kills
        frame_eco = ctk.CTkFrame(frame_body,fg_color='#292929')
        frame_eco.grid(row=2, column=1, sticky="nwes", pady=(5, 10), padx=(5, 10))

        label_eco = ctk.CTkLabel(frame_eco, text='Kills according to opponent buy')
        label_eco.pack(side='top', pady=5, padx=5)
        self.frame_eco = frame_eco
        self.table_eco = None

    def create_or_update_table_scoreboard(self, frame, existing_table, values, num_rows, num_columns):
        """Helper function to create or update a CTkTable."""
        if existing_table:
            existing_table.destroy()
        table = CTkTable(master=frame, row=num_rows, column=num_columns, values=values, width=80, height=25,colors=["#1a1a1a", "#212121"])
        table.pack()
        return table
    
    def create_or_update_table(self, frame, existing_table, values, num_rows, num_columns):
        """Helper function to create or update a CTkTable."""
        if existing_table:
            existing_table.destroy()
        table = CTkTable(master=frame, row=num_rows, column=num_columns, values=values, width=100, height=30,colors=["#1a1a1a", "#212121"])
        table.pack()
        return table


    def update_data(self, analysis_results):
        # Update scoreboard
        scoreboard = analysis_results.get("scoreboard", pd.DataFrame())
        if not scoreboard.empty:
            headers_scoreboard = list(scoreboard.columns)
            values_scoreboard = [headers_scoreboard] + scoreboard.values.tolist()
        else:
            values_scoreboard = [
                ["name", "Rounds joués", "Kills", "Deaths", "Assists", "+/-", "K/D", "Damages", "ADR", "KPR", "HS", "HS %", "5K", "4K", "3K", "mvps", "KAST%", "Impact", "Rating"]
            ]
        self.table_scoreboard = self.create_or_update_table_scoreboard(
            self.frame_scoreboard,
            self.table_scoreboard,
            values_scoreboard,
            len(values_scoreboard),
            len(values_scoreboard[0])
        )

        # Update utility stats
        df_utils = analysis_results.get("util_stats", pd.DataFrame())
        if not df_utils.empty:
            headers_utils = list(df_utils.columns)
            values_utils = [headers_utils] + df_utils.values.tolist()
        else:
            values_utils = [["name", "He_dmg", "Fire_dmg", "Total_utility_dmg", "enemies_flashed_total", "Flash_assist"]]
        self.table_utils = self.create_or_update_table(
            self.frame_utils,
            self.table_utils,
            values_utils,
            len(values_utils),
            len(values_utils[0])
        )

        # Update entry frags
        df_entry = analysis_results.get("entry_stats", pd.DataFrame())
        if not df_entry.empty:
            headers_entry = list(df_entry.columns)
            values_entry = [headers_entry] + df_entry.values.tolist()
        else:
            values_entry = [["name", "Attempts", "Successes", "Ratio"]]
        self.table_entry = self.create_or_update_table(
            self.frame_entry,
            self.table_entry,
            values_entry,
            len(values_entry),
            len(values_entry[0])
        )

        # Update trades
        df_trades = analysis_results.get("trading_stats", pd.DataFrame())
        if not df_trades.empty:
            headers_trades = list(df_trades.columns)
            values_trades = [headers_trades] + df_trades.values.tolist()
        else:
            values_trades = [["name", "Trade Kills", "Traded Deaths"]]
        self.table_trades = self.create_or_update_table(
            self.frame_trades,
            self.table_trades,
            values_trades,
            len(values_trades),
            len(values_trades[0])
        )

        # Update eco kills
        df_eco = analysis_results.get("eco_kills", pd.DataFrame())
        if not df_eco.empty:
            headers_eco = list(df_eco.columns)
            values_eco = [headers_eco] + df_eco.values.tolist()
        else:
            values_eco = [["name", "Against full eco", "Against force buy", "Against full buy", "Pistol rounds"]]
        self.table_eco = self.create_or_update_table(
            self.frame_eco,
            self.table_eco,
            values_eco,
            len(values_eco),
            len(values_eco[0])
        )

if __name__ == "__main__":
    app = RawDataPage()
    app.protocol("WM_DELETE_WINDOW", app.quit)
    app.mainloop()