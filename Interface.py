import customtkinter
from customtkinter import *
from tkinter import filedialog
from PIL import Image

########################### 
#### color palette CS2 ####
###########################
# gris clair du site : #808080
# gris foncé du site : #15171b
# jaune du logo : #fbac18
# bleu du logo : #28397f
# orange de la bannière : #e07f09
# gris clair de la bannière : #d9d9d9
# Font : Stratum2

customtkinter.set_appearance_mode('dark')
customtkinter.set_default_color_theme("theme.json")

app = CTk()
app.geometry("1600x900")
app.title("CS2 stats aggregator")

def analyze():
    print('tbd')
    
def get_team_name(event=None):  # Ajoute l'argument event
    team_name = entry_1.get()  # Récupère le texte tapé
    print(f"Team name: {team_name}")

def select_files():
    file_paths = filedialog.askopenfilenames(title="Select files", filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
    print(f"Files selected: {file_paths}")  # Affiche les fichiers sélectionnés
    return file_paths

frame_1 = CTkFrame(master=app)
frame_1.pack(pady=20, padx=20, fill="both", expand=True)

title = CTkLabel(master=frame_1, text=' CS2 STATS AGGREGATOR', font=("Stratum2 Bd", 60),text_color=('#fbac18'))
title.pack(pady=50)

label_1 = customtkinter.CTkLabel(master=frame_1, text="This tool analyzes the statistical results of a Counter-Strike 2 ESEA season using demo files.\n\nIt provides global team insights, individual player stats, and detailed match breakdowns.",font=('robot',18), wraplength=850)
label_1.pack(pady=20, padx=20)

label_title = customtkinter.CTkLabel(master=frame_1, text="How to use :", font=('robot', 18, 'bold'), wraplength=850)
label_title.pack(pady=10, padx=20)

instructions_text = (
    "Follow these simple steps:\n\n"
    "1. Download the demo files from all your ESEA season matches directly from Faceit's website.\n\n"
    "2. Store them in the same folder on your computer.\n\n"
    "3. Use the 'Upload your demo' button to load the demos into the tool.\n\n"
    "4. Type your team's name, ensuring proper capitalization, hyphens, etc.\n\n"
    "5. Click on the 'Analyze' button to start the analysis."
)

label_instructions = customtkinter.CTkLabel(master=frame_1, text=instructions_text,justify='left',font=('robot', 14), wraplength=850)
label_instructions.pack(pady=20, padx=20)

button_1 = customtkinter.CTkButton(master=frame_1,text='Upload your demos',font=('Stratum2 Bd', 20), command=select_files,height=40,width=250)
button_1.pack(pady=30, padx=10)

entry_1 = customtkinter.CTkEntry(master=frame_1, placeholder_text="Type the name of your team",font=('Stratum2 Bd', 20), justify='center', width=250)
entry_1.pack(pady=25, padx=10)
entry_1.bind("<Return>", get_team_name)

button_2 = customtkinter.CTkButton(master=frame_1,text='Analyze', font=('Stratum2 Bd', 30) ,command=analyze,height=80,width=300)
button_2.pack(pady=25, padx=10)

app.mainloop()
