import customtkinter as ctk
from customtkinter import *
from CTkTable import *
from tkinter import filedialog
from PIL import Image
import os
import tkinter
from tkinter import filedialog, Text
import tkinter.messagebox
from Demo_analyse_script import *


########################### 
#### color palette CS2 ####s
###########################
# gris clair du site : #808080
# violet du site #3b415c
# gris foncé du site : #15171b
# jaune du logo : #fbac18
# bleu du logo : #28397f
# orange de la bannière : #e07f09
# gris clair de la bannière : #d9d9d9
# Font : Stratum2



instructions_text = (
                "Follow these simple steps:\n\n"
                "1. Download the demo files from all your ESEA season matches directly from Faceit's website.\n\n"
                "2. Store them in the same folder on your computer.\n\n"
                "3. Use the 'Upload your demo' button to load the demos from your folder into the tool.\n\n"
                "4. Type your team's name, ensuring proper capitalization, hyphens, etc...\n\n"
                "5. Click on the 'Analyze' button to start the analysis.\n\n"
                "6. Navigate through the pages to see how you performed individually and as a team")


def show_custom_popup(message):
    # Création d'une nouvelle fenêtre (Toplevel)
    popup = ctk.CTkToplevel()
    popup.geometry("300x150")
    popup.geometry(f"+{650}+{375}")  # Dimensions de la fenêtre
    popup.title("Information")  # Titre de la fenêtre
    popup.attributes("-topmost", True)

    # Texte affiché dans la fenêtre
    label = ctk.CTkLabel(popup, text=message, font=("Montserrat", 14))
    label.pack(pady=20)

    # Bouton pour fermer la fenêtre
    button = ctk.CTkButton(popup, text="OK", command=popup.destroy)
    button.pack(pady=10)


class HomePage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.file_paths = None
        self.team_name = None

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

        #### frame subtitle + how to use ####
        frame_body = ctk.CTkFrame(self, fg_color='transparent')
        frame_body.grid(row=1, column=0, sticky="nwes")
        frame_body.grid_columnconfigure(0,weight=1)
        frame_body.grid_columnconfigure(1,weight=1)
        frame_body.grid_rowconfigure((1,2,3),weight=1)

        frame_body_top = ctk.CTkFrame(frame_body,fg_color='#292929')
        frame_body_top.grid(row=0, column=0, columnspan=2, sticky="nwes", pady=(20,10),padx=20)

        label_1 = ctk.CTkLabel(frame_body_top, text="This tool aggregates data from one or multiple Counter-Strike 2 matches using demo files.\n\nIt provides comprehensive insights into team performance, individual player statistics, and a raw data tab for those who want to dive deeper into the gathered statistics.", font=('Montserrat', 18,'bold'))
        label_1.pack(pady=20)

        frame_body_left = ctk.CTkFrame(frame_body,fg_color='#292929')
        frame_body_left.grid(row=1, column=0, sticky="nwes", pady=(10,20),padx=(20,10))

        button_1 = ctk.CTkButton(master=frame_body_left, text='Upload your demos', font=('Stratum2 Bd', 20), command=self.select_directory, height=40, width=250)
        button_1.pack(pady=(80,20))
        self.entry_1 = ctk.CTkEntry(master=frame_body_left, placeholder_text="Type the name of your team", font=('Stratum2 Bd', 20), justify='center', width=250)
        self.entry_1.bind("<Return>", self.team_name)
        self.entry_1.pack(pady=20)
        button_2 = ctk.CTkButton(master=frame_body_left, text='Analyze', font=('Stratum2 Bd', 30), height=80, width=300,command=self.launch_analysis)
        button_2.pack(pady=20,padx=170)

        frame_body_right = ctk.CTkFrame(frame_body,fg_color='#292929')
        frame_body_right.grid(row=1, column=1, sticky="nwes", pady=(10,20),padx=(10,20))
        label_1 = ctk.CTkLabel(frame_body_right, text="How to use", font=('Montserrat', 16,'bold'))
        label_1.pack(pady=20)
        
        label_instructions = ctk.CTkLabel(frame_body_right, text=instructions_text, justify='left', font=('Montserrat', 14))
        label_instructions.pack(pady=20)

        documentation_button = ctk.CTkButton(master=frame_body_right, text="Documentation",font=('Stratum2 Bd', 14), command=self.open_documentation)
        documentation_button.pack(pady=20)

        frame_body_bottom = ctk.CTkFrame(frame_body,fg_color='transparent')
        frame_body_bottom.grid(row=3, column=0, columnspan=2, sticky="nwes", pady=(10,20),padx=20)
        # frame_body_bottom.grid_columnconfigure((0,1),weight=1)
        label_wam = ctk.CTkLabel(frame_body_bottom, text="Built by Armeldt thanks to LaihoE demoparser tool", justify='left', font=('Montserrat', 14), padx=20)
        label_wam.pack(side='bottom')
        
        #logo = ctk.CTkImage(dark_image=Image.open('Assets/Maps/ancient.png'), size=(200,100))


    def open_documentation(self):
        # Create a new Toplevel window as a modal dialog for instructions
        dialog = ctk.CTkToplevel(self)
        dialog.title("Documentation")
        dialog.geometry("1280x960")
        dialog.grab_set()
        dialog.grid_columnconfigure(0, weight=1)
        dialog.grid_rowconfigure(0, weight=5)
        dialog.grid_rowconfigure(1, weight=1)

        scrollable_frame = ctk.CTkScrollableFrame(dialog)
        scrollable_frame.grid(sticky='nsew')
        scrollable_frame.grid_columnconfigure(0, weight=1)
        scrollable_frame.grid_rowconfigure((0,1,2), weight=1)

        kpi_frame = ctk.CTkFrame(scrollable_frame, corner_radius=20)
        kpi_frame.grid(column=0,row=0,padx=5, pady=5,sticky='nw')

        kpi_title = ctk.CTkLabel(kpi_frame, text="Impact and Rating calculation", font=('Stratum2 Bd', 30),justify='left',anchor="w")
        kpi_title.pack(fill='x',padx=20)
       
        kpis_text = (
                        "The calculations for Impact and Rating are based on reverse engineering of HLTV's ratings, conducted by a user named Dave from the website Flashed.gg. Props to him for this work !\n\n"
                        "Here’s what he found :\n\n"
                        "- Rating 2.0 ≈ 0.0073 * KAST + 0.3591 * KPR - 0.5329 * DPR + 0.2372 * Impact + 0.0032 * ADR + 0.1587  \n\n"
                        "- Impact rating ≈ 2.13 * KPR + 0.42 * Assists per Round - 0.41 \n\n"
                        "Since these calculations were derived from a specific sample of matches, they may not be 100% accurate. However, they still provide a useful estimate of players' performance using one of the most commonly used KPIs in the CS2 community.\n\n"
                        "Source: https://flashed.gg/posts/reverse-engineering-hltv-rating/ \n\n")
        
        kpis_label = ctk.CTkLabel(kpi_frame, text=kpis_text, font=("Montserrat", 14),wraplength=900, justify='left')
        kpis_label.pack(padx=50, pady=20)
        
        trade_frame = ctk.CTkFrame(scrollable_frame, corner_radius=20)
        trade_frame.grid(column=0,row=1,padx=5, pady=5,sticky='nw')

        trade_title = ctk.CTkLabel(trade_frame, text="Trade kills", font=('Stratum2 Bd', 30),justify='left',anchor="w")
        trade_title.pack(fill='x',padx=20)
       
        trade_text = (
                        "A trade kill occurs when a player dies to an enemy, and that same enemy is killed by a teammate within a defined time frame.\n\n"
                        "The player who was traded gains a 'Traded death', meaning they contributed to the round outcome by enabling their teammate to secure a kill.\n\n"
                        "The teammate performing the trade is awarded a 'Trade kill', recognizing their contribution to the round outcome by avenging their teammate.\n\n"
                        "The time frame used in the analysis script is set to 2 seconds, starting immediately after each player’s death.\n\n")
        
        trade_label = ctk.CTkLabel(trade_frame, text=trade_text, font=("Montserrat", 14),wraplength=900, justify='left')
        trade_label.pack(padx=50, pady=20)
        
        
        eco_frame = ctk.CTkFrame(scrollable_frame, corner_radius=20)
        eco_frame.grid(column=0,row=2,padx=5, pady=5,sticky='nw')

        eco_title = ctk.CTkLabel(eco_frame, text="Economy state", font=('Stratum2 Bd', 30),justify='left',anchor="w")
        eco_title.pack(fill='x',padx=20)

        eco_text = (
                        "The economy state of a game is defined by the ability of both teams to purchase equipment.\n\n"
                        "To contextualize each round according to the economic state of each team, I defined thresholds to categorize the three most common situations: Full Eco, Force Buy, and Full Buy.\n\n"
                        "- Full Eco: Team equipment below $3500 (approximately $600 per player). The team’s purchase is limited to a few grenades and pistols.\n\n"
                        "- Force Buy: Team equipment below $18,000 (approximately $3,000 per player). The team can afford a combination of light armor with a helmet, a cheap rifle, an SMG, or some grenades.\n\n"
                        "- Full Buy: Team equipment above $18,000 (approximately $3,000+ per player). The team can buy full armor, an AK or M4, and grenades.\n\n"
                        "Note: The first and 13th rounds of each game are always labeled as 'Pistol Rounds.'\n\n")
        
        eco = ctk.CTkLabel(eco_frame, text=eco_text, font=("Montserrat", 14),wraplength=900, justify='left')
        eco.pack(padx=50, pady=20)

        # Add a close button to dismiss the dialog
        close_button = ctk.CTkButton(dialog, text="Close", command=dialog.destroy)
        close_button.grid(column=0,row=1,pady=(10, 20))


    # def get_team_name(self, event=None):
    #     self.team_name = self.entry_1.get().strip() 

    def select_directory(self):
        self.file_paths = filedialog.askdirectory(title="Select demo folder")

    def launch_analysis(self):
 
        self.team_name = self.entry_1.get().strip()
        self.master.team_name = self.team_name
        
        if not self.file_paths:
            show_custom_popup("No directory selected.")
            return

        if not self.team_name:
            show_custom_popup("Please enter a team name.")
            return
        
        # Appeler la fonction d'analyse
        results = cumulate_stats(self.team_name, self.file_paths)
        self.master.set_analysis_results(results)


if __name__ == "__main__":
    app = HomePage()
    app.protocol("WM_DELETE_WINDOW", app.quit)
    app.mainloop()

