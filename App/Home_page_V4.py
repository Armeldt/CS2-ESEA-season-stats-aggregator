import customtkinter as ctk
from customtkinter import *
from CTkTable import *
from tkinter import filedialog
from PIL import Image
import os
import tkinter
from tkinter import filedialog
import tkinter.messagebox
from Demo_analyse_script_V4 import *


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

ctk.set_appearance_mode('dark')
ctk.set_default_color_theme("theme.json")


file_paths = ""
team_name = ""  # Définir file_paths ici pour l'utiliser globalement

instructions_text = (
                "Follow these simple steps:\n\n"
                "1. Download the demo files from all your ESEA season matches directly from Faceit's website.\n\n"
                "2. Store them in the same folder on your computer.\n\n"
                "3. Use the 'Upload your demo' button to load the demos into the tool.\n\n"
                "4. Type your team's name, ensuring proper capitalization, hyphens, etc... and press 'Enter'\n\n"
                "5. Click on the 'Analyze' button to start the analysis.\n\n"
                "6. Navigate through the pages to see how you performed individually and as a team")



class HomePage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

        #### frame subtitle + how to use ####
        frame_body = ctk.CTkFrame(self)
        frame_body.grid(row=1, column=0, sticky="nwes")
        frame_body.grid_columnconfigure(0,weight=1)
        frame_body.grid_columnconfigure(1,weight=1)
        frame_body.grid_rowconfigure((1,2,3),weight=1)

        frame_body_top = ctk.CTkFrame(frame_body)
        frame_body_top.grid(row=0, column=0, columnspan=2, sticky="nwes", pady=20,padx=20)

        label_1 = ctk.CTkLabel(frame_body_top, text="This tool analyzes the statistical results of a Counter-Strike 2 ESEA season using demo files.\n\nIt provides global team insights, individual player stats, and detailed match breakdowns.", font=('Montserrat', 18,'bold'))
        label_1.pack(pady=20)

        frame_body_left = ctk.CTkFrame(frame_body)
        frame_body_left.grid(row=1, column=0, sticky="nwes", pady=20,padx=(20,10))
    
        # how_to_use_button = ctk.CTkButton(master=frame_body_left, text="How to use", command=self.open_how_to_use_dialog)
        # how_to_use_button.pack(pady=20)

        button_1 = ctk.CTkButton(master=frame_body_left, text='Upload your demos', font=('Stratum2 Bd', 20), command=self.select_directory, height=40, width=250)
        button_1.pack(pady=(80,20))
        self.entry_1 = ctk.CTkEntry(master=frame_body_left, placeholder_text="Type the name of your team", font=('Stratum2 Bd', 20), justify='center', width=250)
        self.entry_1.bind("<Return>", self.get_team_name)
        self.entry_1.pack(pady=20)
        button_2 = ctk.CTkButton(master=frame_body_left, text='Analyze', font=('Stratum2 Bd', 30), height=80, width=300,command=self.launch_analysis)
        button_2.pack(pady=20,padx=170)

        frame_body_right = ctk.CTkFrame(frame_body)
        frame_body_right.grid(row=1, column=1, sticky="nwes", pady=20,padx=(10,20))
        label_1 = ctk.CTkLabel(frame_body_right, text="How to use", font=('Montserrat', 16,'bold'))
        label_1.pack(pady=20)
        instructions_text = (
            "Follow these simple steps:\n\n"
            "1. Download the demo files from all your ESEA season matches directly from Faceit's website.\n\n"
            "2. Store them in the same folder on your computer.\n\n"
            "3. Use the 'Upload your demo' button to load the demos into the tool.\n\n"
            "4. Type your team's name, ensuring proper capitalization, hyphens, etc.\n\n"
            "5. Click on the 'Analyze' button to start the analysis."
        )
        label_instructions = ctk.CTkLabel(frame_body_right, text=instructions_text, justify='left', font=('Montserrat', 14))
        label_instructions.pack(pady=20)

        frame_body_bottom = ctk.CTkFrame(frame_body,fg_color='transparent')
        frame_body_bottom.grid(row=3, column=0, columnspan=2, sticky="nwes", pady=20,padx=20)
        # frame_body_bottom.grid_columnconfigure((0,1),weight=1)
        label_wam = ctk.CTkLabel(frame_body_bottom, text="Proudly built by Armeldt", justify='left', font=('Montserrat', 14), padx=20)
        label_wam.pack(side='bottom')
        # label_wam.grid(row=0,column=0, pady=20,sticky="new")

        #logo = ctk.CTkImage(dark_image=Image.open('Assets/Maps/ancient.png'), size=(200,100))


    def open_how_to_use_dialog(self):
        # Create a new Toplevel window as a modal dialog for instructions
        dialog = ctk.CTkToplevel(self)
        dialog.title("How to Use")
        dialog.geometry("600x400")
        dialog.grab_set()  # Makes this window modal

        # Add a label with the instructions text
        instructions_label = ctk.CTkLabel(dialog, text=instructions_text, wraplength=450, font=("Montserrat", 14))
        instructions_label.pack(padx=20, pady=20)

        # Add a close button to dismiss the dialog
        close_button = ctk.CTkButton(dialog, text="Close", command=dialog.destroy)
        close_button.pack(pady=(10, 20))

    def get_team_name(self, event=None): 
        self.team_name = self.entry_1.get()  # Accéder au texte de l'entrée
        print(f"Team name: {self.team_name}")
        self.parent.team_name = self.team_name
        print(f"Team name set to: {team_name}")  # Debugging


    
    def launch_analysis(self):
        self.get_team_name()  # Assure-toi que `team_name` est mis à jour
        if hasattr(self, 'team_name') and self.file_paths:
            results = cumulate_stats(self.team_name, self.file_paths)
            self.master.set_analysis_results(results)
        else:
            print("Team name or file path is missing.")

    def select_directory(self):
        self.file_paths = filedialog.askdirectory(title="Select demo folder")
        if self.file_paths:  # Vérifie si un dossier a bien été sélectionné
            print(f"Directory selected: {self.file_paths}")
        else:
            print("No directory selected.")




if __name__ == "__main__":
    app = HomePage()
    app.mainloop()

