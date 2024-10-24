import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageOps, ImageDraw
from CTkTable import *

def round_corners_top(image, radius, background_color=(141, 141, 185)):
    """Applique des coins arrondis uniquement en haut à une image et ajoute une couleur de fond."""
    width, height = image.size

    # Créer un masque avec les coins arrondis uniquement en haut
    rounded_mask = Image.new("L", (width, height), 0)
    draw = ImageDraw.Draw(rounded_mask)

    # Arrondir uniquement les coins supérieurs
    draw.pieslice([0, 0, 2 * radius, 2 * radius], 180, 270, fill=255)  # Coin supérieur gauche
    draw.pieslice([width - 2 * radius, 0, width, 2 * radius], 270, 360, fill=255)  # Coin supérieur droit
    draw.rectangle([radius, 0, width - radius, radius], fill=255)  # Ligne entre les deux coins arrondis en haut
    draw.rectangle([0, radius, width, height], fill=255)  # Le reste de l'image en bas

    # Appliquer le masque à l'image pour créer l'image arrondie
    rounded_image = ImageOps.fit(image, image.size, centering=(0.5, 0.5))
    rounded_image.putalpha(rounded_mask)

    # Créer une nouvelle image avec une couleur de fond
    background = Image.new("RGBA", (width, height), background_color)

    # Coller l'image arrondie sur l'image de fond
    background.paste(rounded_image, (0, 0), rounded_image)

    return background




ctk.set_appearance_mode('dark')
ctk.set_default_color_theme("theme.json")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("CS2 Stats Aggregator")
        self.geometry(f"{1600}x{900}")

        # configure grid layout for main window
        self.grid_columnconfigure(0, weight=1)  # Weight for the frame containing the maps
        self.grid_columnconfigure(1, weight=10)  # Weight for the empty second frame (placeholder)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=3)

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

        #### Frame for Columns 1 and 2 ####
        frame_left = ctk.CTkFrame(self, corner_radius=20)
        frame_left.grid(row=1, column=0, padx=(20,10), pady=(0,20), sticky="nsew")  # First large frame on left

        # Configure grid for the frame_left (columns 1 and 2 combined)
        frame_left.grid_columnconfigure((0, 1), weight=1)  # Two columns inside the frame_left
        frame_left.grid_rowconfigure(0, weight=1)
        frame_left.grid_rowconfigure((1,2,3,4), weight=3)

        # Configure grid for the frame_left (columns 1 and 2 combined)
        
        frame_record = ctk.CTkFrame(frame_left, corner_radius=20)
        frame_record.grid_columnconfigure((0, 1, 2), weight=1)
        frame_record.grid(row=0, column=0, columnspan=2, sticky="nsew",padx=20, pady=(20,10))

        label_team_name = ctk.CTkLabel(frame_record, text="Zobrux",text_color='white', font=("Stratum2 Bd", 36))
        label_team_name.grid(row=0, column=0, sticky="nsew",padx=20, pady=20)

        label_team_record_wins = ctk.CTkLabel(frame_record, text="12 Wins",fg_color='green',text_color='white', corner_radius=20,font=("Stratum2 Bd", 24))
        label_team_record_wins.grid(row=0, column=1, sticky="nsew",padx=20, pady=20)

        label_team_record_losses= ctk.CTkLabel(frame_record, text="4 Losses",fg_color='red',text_color='white', corner_radius=20,font=("Stratum2 Bd", 24))
        label_team_record_losses.grid(row=0, column=2, sticky="nsew",padx=20, pady=20)

        #bg maps
        self.frame_bg_maps = ctk.CTkFrame(frame_left, fg_color='#8D8DB9', corner_radius=20)
        self.frame_bg_maps.grid(row=1, column=0, columnspan=3,rowspan=4, sticky="nsew", pady=(10,20),padx=20)

        #Sous-titre (Titre de la sous-catégorie) avec fond bleu
        self.frame_subtitle = ctk.CTkFrame(frame_left, fg_color='#28397F', corner_radius=20,background_corner_colors=('#212121','#212121','#8D8DB9','#8D8DB9'))
        self.frame_subtitle.grid(row=1, column=0, columnspan=3, sticky="nsew", padx=20)
        # Label sous-titre centré avec pack
        self.label_subtitle = ctk.CTkLabel(self.frame_subtitle, text='Winrate by maps', font=("Stratum2 Bd", 28), text_color='white')
        self.label_subtitle.pack(expand=True, padx=10, pady=10)

        # chargement des images
        self.ancient_img = ctk.CTkImage(dark_image=round_corners_top(Image.open('Assets/Maps/ancient.png'), 30), size=(200,100))
        self.mirage_img = ctk.CTkImage(dark_image=round_corners_top(Image.open('Assets/Maps/mirage.png'), 30), size=(200,100))
        self.nuke_img = ctk.CTkImage(dark_image=round_corners_top(Image.open('Assets/Maps/nuke.png'), 30), size=(200,100))
        self.dust2_img = ctk.CTkImage(dark_image=round_corners_top(Image.open('Assets/Maps/dust2.jpg'), 30), size=(200,100))
        self.anubis_img = ctk.CTkImage(dark_image=round_corners_top(Image.open('Assets/Maps/anubis.png'), 30), size=(200,100))
        self.vertigo_img = ctk.CTkImage(dark_image=round_corners_top(Image.open('Assets/Maps/vertigo.png'), 30), size=(200,100))

        # Créer un frame avec un fond bleu et une largeur fixée à celle de l'image
        self.frame_map_1 = ctk.CTkFrame(frame_left, fg_color='#28397F', corner_radius=20,width=250, height=180, background_corner_colors=('#8D8DB9', '#8D8DB9', '#8D8DB9', '#8D8DB9'))
        self.frame_map_1.grid(row=2, column=0, padx=10, pady=(18,5), sticky="n")
        self.label_map_1 = ctk.CTkLabel(self.frame_map_1, text="", image=self.ancient_img)
        self.label_map_1.pack(side="top")
        self.label_map_text_1 = ctk.CTkLabel(self.frame_map_1, text="3 wins 4 losses\nWin rate 40%", text_color='white', font=("Montserrat", 14))
        self.label_map_text_1.pack(side="top", pady=(5, 5))

        self.frame_map_2 = ctk.CTkFrame(frame_left, fg_color='#28397F', corner_radius=20, width=250, height=180,background_corner_colors=('#8D8DB9', '#8D8DB9', '#8D8DB9', '#8D8DB9'))
        self.frame_map_2.grid(row=2, column=1, padx=10, pady=(18,5), sticky="n")
        self.label_map_2 = ctk.CTkLabel(self.frame_map_2, text="", image=self.mirage_img)
        self.label_map_2.pack(side="top")
        self.label_map_text_2 = ctk.CTkLabel(self.frame_map_2, text="3 wins 4 losses\nWin rate 40%", fg_color=None, text_color='white', font=("Montserrat", 14))
        self.label_map_text_2.pack(side="top", pady=(5, 5))

        self.frame_map_3 = ctk.CTkFrame(frame_left, fg_color='#28397F', corner_radius=20, width=250, height=180,background_corner_colors=('#8D8DB9', '#8D8DB9', '#8D8DB9', '#8D8DB9'))
        self.frame_map_3.grid(row=3, column=0, padx=10, pady=5, sticky="n")
        self.label_map_3 = ctk.CTkLabel(self.frame_map_3, text="", image=self.nuke_img)
        self.label_map_3.pack(side="top")
        self.label_map_text_3 = ctk.CTkLabel(self.frame_map_3, text="3 wins 4 losses\nWin rate 40%", fg_color=None, text_color='white', font=("Montserrat", 14))
        self.label_map_text_3.pack(side="top", pady=(5, 5))

        self.frame_map_4 = ctk.CTkFrame(frame_left, fg_color='#28397F', corner_radius=20, width=250, height=180,background_corner_colors=('#8D8DB9', '#8D8DB9', '#8D8DB9', '#8D8DB9'))
        self.frame_map_4.grid(row=3, column=1, padx=10, pady=5, sticky="n")
        self.label_map_4 = ctk.CTkLabel(self.frame_map_4, text="", image=self.dust2_img)
        self.label_map_4.pack(side="top")
        self.label_map_text_4 = ctk.CTkLabel(self.frame_map_4, text="3 wins 4 losses\nWin rate 40%", fg_color=None, text_color='white', font=("Montserrat", 14))
        self.label_map_text_4.pack(side="top", pady=(5, 5))

        self.frame_map_5 = ctk.CTkFrame(frame_left, fg_color='#28397F', corner_radius=20, width=250, height=180,background_corner_colors=('#8D8DB9', '#8D8DB9', '#8D8DB9', '#8D8DB9'))
        self.frame_map_5.grid(row=4, column=0, padx=10, pady=(5,15), sticky="n")
        self.label_map_5 = ctk.CTkLabel(self.frame_map_5, text="", image=self.anubis_img)
        self.label_map_5.pack(side="top")
        self.label_map_text_5 = ctk.CTkLabel(self.frame_map_5, text="3 wins 4 losses\nWin rate 40%", fg_color=None, text_color='white', font=("Montserrat", 14))
        self.label_map_text_5.pack(side="top", pady=(5, 5))

        self.frame_map_6 = ctk.CTkFrame(frame_left, fg_color='#28397F', corner_radius=20, width=250, height=180,background_corner_colors=('#8D8DB9', '#8D8DB9', '#8D8DB9', '#8D8DB9'))
        self.frame_map_6.grid(row=4, column=1, padx=10, pady=(5,15), sticky="n")
        self.label_map_6 = ctk.CTkLabel(self.frame_map_6, text="", image=self.vertigo_img)
        self.label_map_6.pack(side="top")
        self.label_map_text_6 = ctk.CTkLabel(self.frame_map_6, text="3 wins 4 losses\nWin rate 40%", fg_color=None, text_color='white', font=("Montserrat", 14))
        self.label_map_text_6.pack(side="top", pady=(5, 5))

        #### Second frame for the right side ####
        frame_right = ctk.CTkFrame(self, corner_radius=20)
        frame_right.grid(row=1, column=1, padx=(10,20), pady=(0,20), sticky="nsew")  # Second frame on right

        # Configure grid for the frame_right (columns 1 and 2 combined)
        frame_right.grid_columnconfigure((0, 1, 2 ), weight=1)  
        frame_right.grid_rowconfigure((0, 1, 2), weight=1)

        frame_rounds_type_data_frame = ctk.CTkFrame(frame_right, fg_color='#8D8DB9', corner_radius=20)
        frame_rounds_type_data_frame.grid(row=0,column=0, columnspan=3,padx=20,pady=20,sticky='nsew')
    

        frame_rounds_type_title_frame = ctk.CTkFrame(frame_right, fg_color='#28397F', corner_radius=20,background_corner_colors=('#212121','#8D8DB9','#8D8DB9','#8D8DB9'))
        frame_rounds_type_title_frame.grid_rowconfigure((0, 1), weight=1)
        frame_rounds_type_title_frame.grid(row=0,column=0,padx=20, pady=(20,0), sticky="nw")

        rounds_type_title = ctk.CTkLabel(frame_rounds_type_title_frame,text="Win rate by round type", font=("Stratum2 Bd", 28), text_color='white')
        rounds_type_title.grid(row=0, column=0, padx=20, pady=20, sticky="n")

        
        
        
        # #affichage d'une table
        # values = [[1, 2, 3, 4],
        #   [5, 6, 7, 8],
        #   [9, 10, 11, 12],
        #   [13, 14, 15, 16]]

        # table = CTkTable(master=frame_right, row=6, column=17, values=values, width=50, height=30)
        # table.grid(row=2, column=0, columnspan=3,padx=20, pady=20, sticky="new")
    

if __name__ == "__main__":
    app = App()
    app.mainloop()
