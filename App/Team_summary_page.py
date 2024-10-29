import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageOps, ImageDraw
from CTkTable import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

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

class TeamSummaryPage(ctk.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("CS2 Stats Aggregator")
        self.geometry(f"{1600}x{900}")

        # configure grid layout for main window
        self.grid_columnconfigure(0, weight=1)  
        self.grid_columnconfigure(1, weight=10)  
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=4)
        self.grid_rowconfigure(2, weight=2)

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
        frame_left = ctk.CTkFrame(self, corner_radius=20,fg_color='#1a1a1a')
        frame_left.grid(row=1, column=0, rowspan=3, padx=(20,10), pady=(10,20), sticky="nsew")  # First large frame on left

        # Configure grid for the frame_left (columns 1 and 2 combined)
        frame_left.grid_columnconfigure((0, 1), weight=1)  # Two columns inside the frame_left
        frame_left.grid_rowconfigure(0, weight=1)
        frame_left.grid_rowconfigure((1,2,3,4), weight=3)

        # Configure grid for the frame_left (columns 1 and 2 combined)
        
        frame_record = ctk.CTkFrame(frame_left, corner_radius=20,background_corner_colors=('#1a1a1a','#1a1a1a','#1a1a1a','#1a1a1a'))
        frame_record.grid_columnconfigure((0, 1, 2), weight=1)
        frame_record.grid(row=0, column=0, columnspan=2, pady=(0,10), sticky="nsew")

        label_team_name = ctk.CTkLabel(frame_record, text="Zobrux",text_color='white', font=("Stratum2 Bd", 36))
        label_team_name.grid(row=0, column=0, sticky="nsew",padx=20, pady=20)

        label_team_record_wins = ctk.CTkLabel(frame_record, text="12 Wins",fg_color='green',text_color='white', corner_radius=20,font=("Stratum2 Bd", 24))
        label_team_record_wins.grid(row=0, column=1, sticky="nsew",padx=20, pady=20)

        label_team_record_losses= ctk.CTkLabel(frame_record, text="4 Losses",fg_color='red',text_color='white', corner_radius=20,font=("Stratum2 Bd", 24))
        label_team_record_losses.grid(row=0, column=2, sticky="nsew",padx=20, pady=20)

        #bg maps
        self.frame_bg_maps = ctk.CTkFrame(frame_left, fg_color='#8D8DB9', corner_radius=20,background_corner_colors=('#1a1a1a','#1a1a1a','#1a1a1a','#1a1a1a'))
        self.frame_bg_maps.grid(row=1, column=0, columnspan=3,rowspan=4, sticky="nsew", pady=(10,0))

        #Sous-titre (Titre de la sous-catégorie) avec fond bleu
        self.frame_subtitle = ctk.CTkFrame(frame_left, fg_color='#28397F', corner_radius=20,bg_color='transparent',background_corner_colors=('#1a1a1a','#1a1a1a','#8D8DB9','#8D8DB9'))
        self.frame_subtitle.grid(row=1, column=0, columnspan=3, sticky="nsew",pady=(10,0))
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
        self.frame_map_1.grid(row=2, column=0, padx=(10,0), pady=(30,5), sticky="n")
        self.label_map_1 = ctk.CTkLabel(self.frame_map_1, text="", image=self.ancient_img)
        self.label_map_1.pack(side="top")
        self.label_map_text_1 = ctk.CTkLabel(self.frame_map_1, text="3 wins 4 losses\nWin rate 40%", text_color='white', font=("Montserrat", 14))
        self.label_map_text_1.pack(side="top", pady=(5, 5))

        self.frame_map_2 = ctk.CTkFrame(frame_left, fg_color='#28397F', corner_radius=20, width=250, height=180,background_corner_colors=('#8D8DB9', '#8D8DB9', '#8D8DB9', '#8D8DB9'))
        self.frame_map_2.grid(row=2, column=1, padx=(0,10), pady=(30,5), sticky="n")
        self.label_map_2 = ctk.CTkLabel(self.frame_map_2, text="", image=self.mirage_img)
        self.label_map_2.pack(side="top")
        self.label_map_text_2 = ctk.CTkLabel(self.frame_map_2, text="3 wins 4 losses\nWin rate 40%", fg_color=None, text_color='white', font=("Montserrat", 14))
        self.label_map_text_2.pack(side="top", pady=(5, 5))

        self.frame_map_3 = ctk.CTkFrame(frame_left, fg_color='#28397F', corner_radius=20, width=250, height=180,background_corner_colors=('#8D8DB9', '#8D8DB9', '#8D8DB9', '#8D8DB9'))
        self.frame_map_3.grid(row=3, column=0, padx=(10,0), pady=15, sticky="n")
        self.label_map_3 = ctk.CTkLabel(self.frame_map_3, text="", image=self.nuke_img)
        self.label_map_3.pack(side="top")
        self.label_map_text_3 = ctk.CTkLabel(self.frame_map_3, text="3 wins 4 losses\nWin rate 40%", fg_color=None, text_color='white', font=("Montserrat", 14))
        self.label_map_text_3.pack(side="top", pady=(5, 5))

        self.frame_map_4 = ctk.CTkFrame(frame_left, fg_color='#28397F', corner_radius=20, width=250, height=180,background_corner_colors=('#8D8DB9', '#8D8DB9', '#8D8DB9', '#8D8DB9'))
        self.frame_map_4.grid(row=3, column=1, padx=(0,10), pady=15, sticky="n")
        self.label_map_4 = ctk.CTkLabel(self.frame_map_4, text="", image=self.dust2_img)
        self.label_map_4.pack(side="top")
        self.label_map_text_4 = ctk.CTkLabel(self.frame_map_4, text="3 wins 4 losses\nWin rate 40%", fg_color=None, text_color='white', font=("Montserrat", 14))
        self.label_map_text_4.pack(side="top", pady=(5, 5))

        self.frame_map_5 = ctk.CTkFrame(frame_left, fg_color='#28397F', corner_radius=20, width=250, height=180,background_corner_colors=('#8D8DB9', '#8D8DB9', '#8D8DB9', '#8D8DB9'))
        self.frame_map_5.grid(row=4, column=0, padx=(10,0), pady=(5,30), sticky="n")
        self.label_map_5 = ctk.CTkLabel(self.frame_map_5, text="", image=self.anubis_img)
        self.label_map_5.pack(side="top")
        self.label_map_text_5 = ctk.CTkLabel(self.frame_map_5, text="3 wins 4 losses\nWin rate 40%", fg_color=None, text_color='white', font=("Montserrat", 14))
        self.label_map_text_5.pack(side="top", pady=(5, 5))

        self.frame_map_6 = ctk.CTkFrame(frame_left, fg_color='#28397F', corner_radius=20, width=250, height=180,background_corner_colors=('#8D8DB9', '#8D8DB9', '#8D8DB9', '#8D8DB9'))
        self.frame_map_6.grid(row=4, column=1, padx=(0,10), pady=(5,30), sticky="n")
        self.label_map_6 = ctk.CTkLabel(self.frame_map_6, text="", image=self.vertigo_img)
        self.label_map_6.pack(side="top")
        self.label_map_text_6 = ctk.CTkLabel(self.frame_map_6, text="3 wins 4 losses\nWin rate 40%", fg_color=None, text_color='white', font=("Montserrat", 14))
        self.label_map_text_6.pack(side="top", pady=(5, 5))

        #### Second frame for the right side ####
        frame_right_top = ctk.CTkFrame(self, corner_radius=20)
        frame_right_top.grid(row=1, column=1, padx=(10,20), pady=(10,20), sticky="nsew")  # Second frame on right

        # Configure grid for the frame_right_top (columns 1 and 2 combined)
        frame_right_top.grid_columnconfigure((0, 1, 2), weight=1)
        frame_right_top.grid_rowconfigure(0, weight=1)
        frame_right_top.grid_rowconfigure(1, weight=10)
        frame_right_top.grid_rowconfigure(2, weight=1)

        frame_rounds_type_data_frame = ctk.CTkFrame(frame_right_top, fg_color='#8D8DB9', corner_radius=20,background_corner_colors=('#1a1a1a','#1a1a1a','#1a1a1a','#1a1a1a'))
        frame_rounds_type_data_frame.grid(row=0,column=0, columnspan=3,rowspan=3,sticky='nsew')

        frame_rounds_type_title = ctk.CTkFrame(frame_right_top, fg_color='#28397F', corner_radius=20,background_corner_colors=('#1a1a1a','#8D8DB9','#8D8DB9','#8D8DB9'))
        frame_rounds_type_title.grid(row=0,column=0,columnspan=2,sticky="nw")

        rounds_type_title = ctk.CTkLabel(frame_rounds_type_title,text="Win rate by round type", font=("Stratum2 Bd", 28), text_color='white')
        rounds_type_title.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        ### viz gun round ###
        
        frame_round_type_viz_pistol = ctk.CTkFrame(frame_right_top, corner_radius=20)
        frame_round_type_viz_pistol.grid_columnconfigure((0, 1), weight=1)
        frame_round_type_viz_pistol.grid_rowconfigure(0, weight=1)
        frame_round_type_viz_pistol.grid_rowconfigure(1, weight=3)
        frame_round_type_viz_pistol.grid(row=1,column=0, padx=(10,0),pady=(0,15), sticky="nsew")

        viz_1_title = ctk.CTkLabel(frame_round_type_viz_pistol,text="Win rate Pistol Rounds", font=("Montserrat", 18), text_color='white',fg_color='#8D8DB9',bg_color='#8D8DB9') #
        viz_1_title.grid(row=0, column=0,columnspan=2,sticky="nsew")
        

        value = 75
        title_text = "Terrorist"
        gauge_color = "#fbac18"
        min_val, max_val = 0, 100
        angle_range = -270  
        value_range = max_val - min_val
        fill_angle = angle_range * (value / 100) 
        fig, ax = plt.subplots(figsize=(1, 1), subplot_kw={'projection': 'polar'})
        ax.barh(1, np.radians(angle_range), left=np.radians(315), color="lightgray", height=0.3)
        ax.barh(1, np.radians(fill_angle), left=np.radians(315), color=gauge_color, height=0.3)
        ax.text(0, 0, f"{value:.0f}%", ha='center', va='center', fontsize=10, color="white")
        plt.title(title_text, color='white', fontsize=10, pad=15)
        ax.set_yticklabels([])
        ax.set_xticklabels([])
        ax.set_yticks([])
        ax.set_xticks([])
        ax.spines.clear()
        fig.patch.set_alpha(0)
        ax.patch.set_alpha(0)
        ax.set_theta_offset(-np.pi / 2)
        canvas1 = FigureCanvasTkAgg(fig, master=frame_round_type_viz_pistol) 
        canvas1.draw() 
        canvas1.get_tk_widget().config(bg="#8D8DB9", highlightthickness=0) 
        canvas1.get_tk_widget().grid(row=1, column=0, sticky="nsew")
        
        value = 25  
        title_text = "Counter Terrorist"
        gauge_color = "#28397f"  
        min_val, max_val = 0, 100
        angle_range = -270  
        value_range = max_val - min_val
        fill_angle = angle_range * (value / 100) 
        fig, ax = plt.subplots(figsize=(1, 1), subplot_kw={'projection': 'polar'})
        ax.barh(1, np.radians(angle_range), left=np.radians(315), color="lightgray", height=0.3)
        ax.barh(1, np.radians(fill_angle), left=np.radians(315), color=gauge_color, height=0.3)
        ax.text(0, 0, f"{value:.0f}%", ha='center', va='center', fontsize=10, color="white")
        plt.title(title_text, color='white', fontsize=10, pad=15)
        ax.set_yticklabels([])
        ax.set_xticklabels([])
        ax.set_yticks([])
        ax.set_xticks([])
        ax.spines.clear()
        fig.patch.set_alpha(0)
        ax.patch.set_alpha(0)
        ax.set_theta_offset(-np.pi / 2)

        # Affichage du graphique dans tkinter
        canvas2 = FigureCanvasTkAgg(fig, master=frame_round_type_viz_pistol) 
        canvas2.draw() 
        canvas2.get_tk_widget().config(bg="#8D8DB9", highlightthickness=0) 
        canvas2.get_tk_widget().grid(row=1, column=1, sticky="nsew")
         
        
        ### infos force buy ###

        frame_round_type_viz_forcebuy = ctk.CTkFrame(frame_right_top)
        frame_round_type_viz_forcebuy.grid_columnconfigure((0, 1), weight=1)
        frame_round_type_viz_forcebuy.grid_rowconfigure(0, weight=1)
        frame_round_type_viz_forcebuy.grid_rowconfigure(1, weight=3)
        frame_round_type_viz_forcebuy.grid(row=1,column=1,padx=(5,5),pady=(0,15), sticky="nsew")

        viz_1_title = ctk.CTkLabel(frame_round_type_viz_forcebuy,text="Win rate Force Buy Rounds", font=("Montserrat", 18), text_color='white',fg_color='#8D8DB9',bg_color='#8D8DB9')
        viz_1_title.grid(row=0, column=0,columnspan=2,sticky="nsew")
        

        #Données pour le graphique de jauge
        value = 22
        title_text = "Terrorist"
        gauge_color = "#fbac18"
        min_val, max_val = 0, 100
        angle_range = -270  
        value_range = max_val - min_val
        fill_angle = angle_range * (value / 100) 
        fig, ax = plt.subplots(figsize=(1, 1), subplot_kw={'projection': 'polar'})
        ax.barh(1, np.radians(angle_range), left=np.radians(315), color="lightgray", height=0.3)
        ax.barh(1, np.radians(fill_angle), left=np.radians(315), color=gauge_color, height=0.3)
        ax.text(0, 0, f"{value:.0f}%", ha='center', va='center', fontsize=10, color="white")
        plt.title(title_text, color='white', fontsize=10, pad=15)
        ax.set_yticklabels([])
        ax.set_xticklabels([])
        ax.set_yticks([])
        ax.set_xticks([])
        ax.spines.clear()
        fig.patch.set_alpha(0)
        ax.patch.set_alpha(0)
        ax.set_theta_offset(-np.pi / 2)
        canvas5 = FigureCanvasTkAgg(fig, master=frame_round_type_viz_forcebuy) 
        canvas5.draw() 
        canvas5.get_tk_widget().config(bg="#8D8DB9", highlightthickness=0) 
        canvas5.get_tk_widget().grid(row=1, column=0, sticky="nsew")
        

        # Exemple de données pour le graphique de jauge
        value = 34  # Exemple de pourcentage à remplir
        title_text = "Counter Terrorist"
        gauge_color = "#28397f"  # Couleur pour le remplissage de la jauge
        min_val, max_val = 0, 100
        angle_range = -270  # Plage d'angle pour la jauge (3/4 de cercle), avec un pas négatif pour aller de 315° à 44°
        value_range = max_val - min_val
        fill_angle = angle_range * (value / 100)  # Angle correspondant à la valeur de remplissage
        fig, ax = plt.subplots(figsize=(1, 1), subplot_kw={'projection': 'polar'})
        ax.barh(1, np.radians(angle_range), left=np.radians(315), color="lightgray", height=0.3)
        ax.barh(1, np.radians(fill_angle), left=np.radians(315), color=gauge_color, height=0.3)
        ax.text(0, 0, f"{value:.0f}%", ha='center', va='center', fontsize=10, color="white")
        plt.title(title_text, color='white', fontsize=10, pad=15)
        ax.set_yticklabels([])
        ax.set_xticklabels([])
        ax.set_yticks([])
        ax.set_xticks([])
        ax.spines.clear()
        fig.patch.set_alpha(0)
        ax.patch.set_alpha(0)
        ax.set_theta_offset(-np.pi / 2)

        # Affichage du graphique dans tkinter
        canvas6 = FigureCanvasTkAgg(fig, master=frame_round_type_viz_forcebuy) 
        canvas6.draw() 
        canvas6.get_tk_widget().config(bg="#8D8DB9", highlightthickness=0) 
        canvas6.get_tk_widget().grid(row=1, column=1, sticky="nsew")

        ### infos full buy rounds ###

        frame_round_type_viz_fullbuy = ctk.CTkFrame(frame_right_top)
        frame_round_type_viz_fullbuy.grid_columnconfigure((0, 1), weight=1)
        frame_round_type_viz_fullbuy.grid_rowconfigure(0, weight=1)
        frame_round_type_viz_fullbuy.grid_rowconfigure(1, weight=3)
        frame_round_type_viz_fullbuy.grid(row=1,column=2,pady=(0,15),padx=(0,10), sticky="nsew")

        viz_1_title = ctk.CTkLabel(frame_round_type_viz_fullbuy,text="Win rate Full Buy Rounds", font=("Montserrat", 18), text_color='white',fg_color='#8D8DB9',bg_color='#8D8DB9')
        viz_1_title.grid(row=0, column=0,columnspan=2,sticky="nsew")
        
        #Données pour le graphique de jauge
        value = 66
        title_text = "Terrorist"
        gauge_color = "#fbac18"
        min_val, max_val = 0, 100
        angle_range = -270  
        value_range = max_val - min_val
        fill_angle = angle_range * (value / 100) 
        fig, ax = plt.subplots(figsize=(1, 1), subplot_kw={'projection': 'polar'})
        ax.barh(1, np.radians(angle_range), left=np.radians(315), color="lightgray", height=0.3)
        ax.barh(1, np.radians(fill_angle), left=np.radians(315), color=gauge_color, height=0.3)
        ax.text(0, 0, f"{value:.0f}%", ha='center', va='center', fontsize=10, color="white")
        plt.title(title_text, color='white', fontsize=10, pad=15)
        ax.set_yticklabels([])
        ax.set_xticklabels([])
        ax.set_yticks([])
        ax.set_xticks([])
        ax.spines.clear()
        fig.patch.set_alpha(0)
        ax.patch.set_alpha(0)
        ax.set_theta_offset(-np.pi / 2)
        canvas3 = FigureCanvasTkAgg(fig, master=frame_round_type_viz_fullbuy) 
        canvas3.draw() 
        canvas3.get_tk_widget().config(bg="#8D8DB9", highlightthickness=0) 
        canvas3.get_tk_widget().grid(row=1, column=0, sticky="nsew")
        

        # Exemple de données pour le graphique de jauge
        value = 44  # Exemple de pourcentage à remplir
        title_text = "Counter Terrorist"
        gauge_color = "#28397f"  # Couleur pour le remplissage de la jauge
        min_val, max_val = 0, 100
        angle_range = -270  # Plage d'angle pour la jauge (3/4 de cercle), avec un pas négatif pour aller de 315° à 44°
        value_range = max_val - min_val
        fill_angle = angle_range * (value / 100)  # Angle correspondant à la valeur de remplissage
        fig, ax = plt.subplots(figsize=(1, 1), subplot_kw={'projection': 'polar'})
        ax.barh(1, np.radians(angle_range), left=np.radians(315), color="lightgray", height=0.3)
        ax.barh(1, np.radians(fill_angle), left=np.radians(315), color=gauge_color, height=0.3)
        ax.text(0, 0, f"{value:.0f}%", ha='center', va='center', fontsize=10, color="white")
        plt.title(title_text, color='white', fontsize=10, pad=15)
        ax.set_yticklabels([])
        ax.set_xticklabels([])
        ax.set_yticks([])
        ax.set_xticks([])
        ax.spines.clear()
        fig.patch.set_alpha(0)
        ax.patch.set_alpha(0)
        ax.set_theta_offset(-np.pi / 2)

        # Affichage du graphique dans tkinter
        canvas4 = FigureCanvasTkAgg(fig, master=frame_round_type_viz_fullbuy) 
        canvas4.draw() 
        canvas4.get_tk_widget().config(bg="#8D8DB9", highlightthickness=0) 
        canvas4.get_tk_widget().grid(row=1, column=1, sticky="nsew")
        # #affichage d'une table
        # values = [[1, 2, 3, 4],
        #   [5, 6, 7, 8],
        #   [9, 10, 11, 12],
        #   [13, 14, 15, 16]]

        # table = CTkTable(master=frame_right_top, row=6, column=17, values=values, width=50, height=30)
                # table.grid(row=2, column=0, columnspan=3,padx=20, pady=20, sticky="new")

        frame_top_3rd_row = ctk.CTkFrame(frame_right_top, corner_radius=20,fg_color='#8D8DB9',background_corner_colors=('#8D8DB9','#8D8DB9','#1a1a1a','#1a1a1a'))
        frame_top_3rd_row.grid_columnconfigure((0,1,2,3), weight=1)
        frame_top_3rd_row.grid(row=2, column=0,columnspan=4, sticky="nsew")

        frame_fb_vs_eco = ctk.CTkFrame(frame_top_3rd_row, corner_radius=20,fg_color='#28397F')
        frame_fb_vs_eco.grid_rowconfigure((0,1),weight=1)
        frame_fb_vs_eco.grid_columnconfigure(1,weight=1)
        frame_fb_vs_eco.grid(row=0,column=0,padx=(20,10), pady=5, sticky="nsew")
        label_fb_vs_eco = ctk.CTkLabel(frame_fb_vs_eco,text="Full buy VS eco losts", font=("Montserrat", 14), text_color='white')
        label_fb_vs_eco.grid(row=0,column=1,padx=10, pady=(20,5), sticky="nsew")
        value_fb_vs_eco = ctk.CTkLabel(frame_fb_vs_eco,text="1", font=("Stratum2 Bd", 28), text_color='white')
        value_fb_vs_eco.grid(row=1,column=1,padx=10, pady=(5,20), sticky="nsew")

        frame_fb_vs_force = ctk.CTkFrame(frame_top_3rd_row, corner_radius=20,fg_color='#28397F')
        frame_fb_vs_force.grid_rowconfigure((0,1),weight=1)
        frame_fb_vs_force.grid_columnconfigure(1,weight=1)
        frame_fb_vs_force.grid(row=0,column=1,padx=10, pady=5, sticky="nsew")
        label_fb_vs_force = ctk.CTkLabel(frame_fb_vs_force,text="Full buy VS force buy losts", font=("Montserrat", 14), text_color='white')
        label_fb_vs_force.grid(row=0,column=1,padx=10, pady=(20,5), sticky="nsew")
        value_fb_vs_force = ctk.CTkLabel(frame_fb_vs_force,text="4", font=("Stratum2 Bd", 28), text_color='white')
        value_fb_vs_force.grid(row=1,column=1,padx=10, pady=(5,20), sticky="nsew")

        frame_eco_vs_fb = ctk.CTkFrame(frame_top_3rd_row, corner_radius=20,fg_color='#28397F')
        frame_eco_vs_fb.grid_rowconfigure((0,1),weight=1)
        frame_eco_vs_fb.grid_columnconfigure(1,weight=1)
        frame_eco_vs_fb.grid(row=0,column=2,padx=10, pady=5, sticky="nsew")
        label_eco_vs_fb = ctk.CTkLabel(frame_eco_vs_fb,text="Eco vs Full buy won", font=("Montserrat", 14), text_color='white')
        label_eco_vs_fb.grid(row=0,column=1,padx=10, pady=(20,5), sticky="nsew")
        value_eco_vs_fb = ctk.CTkLabel(frame_eco_vs_fb,text="1", font=("Stratum2 Bd", 28), text_color='white')
        value_eco_vs_fb.grid(row=1,column=1,padx=10, pady=(5,20), sticky="nsew")
                             
        

        frame_force_vs_fb = ctk.CTkFrame(frame_top_3rd_row, corner_radius=20,fg_color='#28397F')
        frame_force_vs_fb.grid_rowconfigure((0,1),weight=1)
        frame_force_vs_fb.grid_columnconfigure(1,weight=1)
        frame_force_vs_fb.grid(row=0,column=3,padx=(10,20), pady=5, sticky="nsew")
        label_force_vs_fb = ctk.CTkLabel(frame_force_vs_fb,text="Force buy vs Full buy won", font=("Montserrat", 14), text_color='white')
        label_force_vs_fb.grid(row=0,column=1,padx=10, pady=(20,5), sticky="nsew")
        value_force_vs_fb = ctk.CTkLabel(frame_force_vs_fb,text="2", font=("Stratum2 Bd", 28), text_color='white')
        value_force_vs_fb.grid(row=1,column=1,padx=10, pady=(5,20), sticky="nsew")

        

        frame_right_bot = ctk.CTkFrame(self,fg_color="#8D8DB9",corner_radius=20,)
        frame_right_bot.grid(row=2, column=1, padx=(10,20), pady=(0,20), sticky="nsew")
        # Configure grid for the frame_right_top (columns 1 and 2 combined)
        frame_right_bot.grid_columnconfigure((0, 1, 2), weight=1)
        frame_right_bot.grid_rowconfigure((0,1), weight=1)

       
        frame_closest_win = ctk.CTkFrame(frame_right_bot, corner_radius=20,fg_color='#28397F')
        frame_closest_win.grid_columnconfigure(0,weight=1)
        frame_closest_win.grid_columnconfigure(1,weight=3)
        frame_closest_win.grid_rowconfigure(0,weight=1)
        frame_closest_win.grid(row=0,column=0,padx=(20,10), pady=(20,10), sticky="nsew")
        closest_win_label = ctk.CTkLabel(frame_closest_win,text="Closest win :", font=("Montserrat", 14), text_color='white')
        closest_win_label.grid(row=0,column=0,padx=(10,0), pady=10, sticky="nsew")
        closest_win_label = ctk.CTkLabel(frame_closest_win,text="19-17 VS Edjelsar", font=("Stratum2 Bd", 20), text_color='white')
        closest_win_label.grid(row=0,column=1,padx=(0,15), pady=10, sticky="nsew")


        frame_largest_win = ctk.CTkFrame(frame_right_bot, corner_radius=20 ,fg_color='#28397F')
        frame_largest_win.grid_columnconfigure(0,weight=1)
        frame_largest_win.grid_columnconfigure(1,weight=3)
        frame_largest_win.grid_rowconfigure(0,weight=1)
        frame_largest_win.grid(row=0,column=1,padx=(10,10), pady=(20,10), sticky="nsew")
        largest_win_label = ctk.CTkLabel(frame_largest_win,text="Largest win :", font=("Montserrat", 14), text_color='white')
        largest_win_label.grid(row=0,column=0,padx=(10,0), pady=10, sticky="nsew")
        largest_win_label = ctk.CTkLabel(frame_largest_win,text="13-1 VS MadeInPoland", font=("Stratum2 Bd", 20), text_color='white')
        largest_win_label.grid(row=0,column=1,padx=(0,15), pady=10, sticky="nsew")

    
        frame_longest_winstreak = ctk.CTkFrame(frame_right_bot, fg_color='#28397F', corner_radius=20)
        frame_longest_winstreak.grid(row=0,column=2,padx=(10,20), pady=(20,10), sticky="nsew")
        frame_longest_winstreak.grid_columnconfigure(0,weight=1)
        frame_longest_winstreak.grid_columnconfigure(1,weight=3)
        frame_longest_winstreak.grid_rowconfigure(0,weight=1)
        longest_winstreak_label = ctk.CTkLabel(frame_longest_winstreak,text="Longest winstreak :", font=("Montserrat", 14), text_color='white')
        longest_winstreak_label.grid(row=0,column=0,padx=(10,0), pady=10, sticky="nsew")
        longest_winstreak_label = ctk.CTkLabel(frame_longest_winstreak,text="6 wins", font=("Stratum2 Bd", 20), text_color='white')
        longest_winstreak_label.grid(row=0,column=1,padx=(0,15), pady=10, sticky="nsew")


        define1_frame = ctk.CTkFrame(frame_right_bot, fg_color='#28397F', corner_radius=20)
        define1_frame.grid(row=1,column=0,padx=(20,10), pady=(10,20), sticky="nsew")
        define1_frame.grid_columnconfigure(0,weight=1)
        define1_frame.grid_columnconfigure(1,weight=3)
        define1_frame.grid_rowconfigure(0,weight=1)
        define_1_label = ctk.CTkLabel(define1_frame,text="KPI a définir :", font=("Montserrat", 14), text_color='white')
        define_1_label.grid(row=0,column=0,padx=(10,0), pady=10, sticky="nsew")
        define_1_label = ctk.CTkLabel(define1_frame,text="valeur", font=("Stratum2 Bd", 20), text_color='white')
        define_1_label.grid(row=0,column=1,padx=(0,15), pady=10, sticky="nsew")

        define2_frame = ctk.CTkFrame(frame_right_bot, fg_color='#28397F', corner_radius=20)
        define2_frame.grid(row=1,column=1,padx=(10,10), pady=(10,20), sticky="nsew")
        define2_frame.grid_columnconfigure(0,weight=1)
        define2_frame.grid_columnconfigure(1,weight=3)
        define2_frame.grid_rowconfigure(0,weight=1)
        define_2_label = ctk.CTkLabel(define2_frame,text="KPI a définir :", font=("Montserrat", 14), text_color='white')
        define_2_label.grid(row=0,column=0,padx=(10,0), pady=10, sticky="nsew")
        define_2_label = ctk.CTkLabel(define2_frame,text="valeur", font=("Stratum2 Bd", 20), text_color='white')
        define_2_label.grid(row=0,column=1,padx=(0,15), pady=10, sticky="nsew")

        define3_frame = ctk.CTkFrame(frame_right_bot, fg_color='#28397F', corner_radius=20)
        define3_frame.grid(row=1,column=2,padx=(10,20), pady=(10,20), sticky="nsew")
        define3_frame.grid_columnconfigure(0,weight=1)
        define3_frame.grid_columnconfigure(1,weight=3)
        define3_frame.grid_rowconfigure(0,weight=1)
        define_3_label = ctk.CTkLabel(define3_frame,text="KPI a définir :", font=("Montserrat", 14), text_color='white')
        define_3_label.grid(row=0,column=0,padx=(10,0), pady=10, sticky="nsew")
        define_3_label = ctk.CTkLabel(define3_frame,text="valeur", font=("Stratum2 Bd", 20), text_color='white')
        define_3_label.grid(row=0,column=1,padx=(0,15), pady=10, sticky="nsew")

if __name__ == "__main__":
    app = TeamSummaryPage()
    app.protocol("WM_DELETE_WINDOW", app.quit)
    app.mainloop()
