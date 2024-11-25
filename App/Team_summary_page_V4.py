import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageOps, ImageDraw
from CTkTable import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import pandas as pd
       
    

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


def update_gauge_chart(parent, value, title_text, gauge_color, row, column):
    min_val, max_val = 0, 100
    angle_range = -270
    fill_angle = angle_range * (value / 100)

    fig, ax = plt.subplots(figsize=(1, 1), subplot_kw={'projection': 'polar'})
    ax.barh(1, np.radians(angle_range), left=np.radians(315), color="lightgray", height=0.3)
    ax.barh(1, np.radians(fill_angle), left=np.radians(315), color=gauge_color, height=0.3)
    ax.text(0, 0, f"{value:.0f}%", ha='center', va='center', fontsize=12, color="white")
    plt.title(title_text, color='white', fontsize=10, pad=20)
    
    # Clear axis details for a cleaner look
    ax.set_yticklabels([])
    ax.set_xticklabels([])
    ax.set_yticks([])
    ax.set_xticks([])
    ax.spines.clear()
    fig.patch.set_alpha(0)
    ax.patch.set_alpha(0)
    ax.set_theta_offset(-np.pi / 2)

    # Attach the figure to Tkinter canvas and place it in the grid
    canvas = FigureCanvasTkAgg(fig, master=parent)
    canvas.draw()
    canvas.get_tk_widget().config(bg="#8D8DB9", highlightthickness=0)
    canvas.get_tk_widget().grid(row=row, column=column, sticky="nsew")


ctk.set_appearance_mode('dark')
ctk.set_default_color_theme("theme.json")

class TeamSummaryPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        # configure grid layout for main window
        self.grid_columnconfigure(0, weight=1)  
        self.grid_columnconfigure(1, weight=3)  
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=4)
        self.grid_rowconfigure(2, weight=2)


        #### Frame for Columns 1 and 2 ####
        frame_left = ctk.CTkFrame(self, corner_radius=20,fg_color='transparent')
        frame_left.grid(row=1, column=0, rowspan=3, padx=(20,10), pady=(10,20), sticky="nsew")  # First large frame on left

        # Configure grid for the frame_left (columns 1 and 2 combined)
        frame_left.grid_columnconfigure((0, 1), weight=1)  # Two columns inside the frame_left
        frame_left.grid_rowconfigure(0, weight=1)
        frame_left.grid_rowconfigure((1,2,3,4,5), weight=3)

        # Configure grid for the frame_left (columns 1 and 2 combined)
        
        frame_record = ctk.CTkFrame(frame_left, corner_radius=20,fg_color='#1a1a1a')#background_corner_colors=('#1a1a1a','#1a1a1a','#1a1a1a','#1a1a1a'))
        frame_record.grid_columnconfigure((0, 1, 2), weight=1)
        frame_record.grid(row=0, column=0, columnspan=2, pady=(10,10), sticky="nsew")

        self.label_team_name = ctk.CTkLabel(frame_record, text="",text_color='white', font=("Stratum2 Bd", 36))
        self.label_team_name.grid(row=0, column=0, sticky="nsew",padx=20, pady=20)

        self.label_team_record_wins = ctk.CTkLabel(frame_record, text="",fg_color='green',text_color='white', corner_radius=20,font=("Stratum2 Bd", 24))
        self.label_team_record_wins.grid(row=0, column=1, sticky="nsew",padx=20, pady=20)

        self.label_team_record_losses= ctk.CTkLabel(frame_record, text="",fg_color='red',text_color='white', corner_radius=20,font=("Stratum2 Bd", 24))
        self.label_team_record_losses.grid(row=0, column=2, sticky="nsew",padx=20, pady=20)

        #bg maps
        self.frame_bg_maps = ctk.CTkFrame(frame_left, fg_color='#8D8DB9', corner_radius=20)#,background_corner_colors=('#1a1a1a','#1a1a1a','#1a1a1a','#1a1a1a'))
        self.frame_bg_maps.grid(row=1, column=0, columnspan=3,rowspan=5, sticky="nsew", pady=(10,0))

        #Sous-titre (Titre de la sous-catégorie) avec fond bleu
        self.frame_subtitle = ctk.CTkFrame(frame_left, fg_color='#28397F', corner_radius=20,bg_color='transparent',background_corner_colors=('','','#8D8DB9','#8D8DB9'))
        self.frame_subtitle.grid(row=1, column=0, columnspan=3, sticky="nsew",pady=(10,0))
        # Label sous-titre centré avec pack
        self.label_subtitle = ctk.CTkLabel(self.frame_subtitle, text='Winrate by maps', font=("Stratum2 Bd", 28), text_color='white')
        self.label_subtitle.pack(expand=True, padx=10, pady=10)

        # chargement des images
        target_size = (200, 100)  # Dimensions finales
        self.ancient_img = ctk.CTkImage(dark_image=round_corners_top(Image.open('Assets/Maps/ancient.png'), 30), size=target_size)
        self.mirage_img = ctk.CTkImage(dark_image=round_corners_top(Image.open('Assets/Maps/mirage.png'), 30), size=target_size)
        self.nuke_img = ctk.CTkImage(dark_image=round_corners_top(Image.open('Assets/Maps/nuke.png'), 30), size=target_size)
        self.dust2_img = ctk.CTkImage(dark_image=round_corners_top(Image.open('Assets/Maps/dust2.jpg'), 30), size=target_size)
        self.anubis_img = ctk.CTkImage(dark_image=round_corners_top(Image.open('Assets/Maps/anubis.png'), 30), size=target_size)
        self.vertigo_img = ctk.CTkImage(dark_image=round_corners_top(Image.open('Assets/Maps/vertigo.png'), 30), size=target_size)
        self.inferno_img = ctk.CTkImage(dark_image=round_corners_top(Image.open('Assets/Maps/inferno.png'), 30), size=target_size)
        
        # Créer un frame avec un fond bleu et une largeur fixée à celle de l'image
        self.frame_map_1 = ctk.CTkFrame(frame_left, fg_color='#28397F', corner_radius=20,width=250, height=180, background_corner_colors=('#8D8DB9', '#8D8DB9', '#8D8DB9', '#8D8DB9'))
        self.frame_map_1.grid(row=2, column=0, padx=(10,0), pady=(10,5), sticky="n")
        self.label_map_1 = ctk.CTkLabel(self.frame_map_1, text="", image=self.ancient_img)
        self.label_map_1.pack(side="top")
        self.label_map_text_1 = ctk.CTkLabel(self.frame_map_1, text="", text_color='white', font=("Montserrat", 12))
        self.label_map_text_1.pack(side="top", pady=(3, 3))

        self.frame_map_2 = ctk.CTkFrame(frame_left, fg_color='#28397F', corner_radius=20, width=250, height=180,background_corner_colors=('#8D8DB9', '#8D8DB9', '#8D8DB9', '#8D8DB9'))
        self.frame_map_2.grid(row=2, column=1, padx=(0,10), pady=(10,5), sticky="n")
        self.label_map_2 = ctk.CTkLabel(self.frame_map_2, text="", image=self.mirage_img)
        self.label_map_2.pack(side="top")
        self.label_map_text_2 = ctk.CTkLabel(self.frame_map_2, text="", fg_color=None, text_color='white', font=("Montserrat", 12))
        self.label_map_text_2.pack(side="top", pady=(3, 3))

        self.frame_map_3 = ctk.CTkFrame(frame_left, fg_color='#28397F', corner_radius=20, width=250, height=180,background_corner_colors=('#8D8DB9', '#8D8DB9', '#8D8DB9', '#8D8DB9'))
        self.frame_map_3.grid(row=3, column=0, padx=(10,0), pady=5, sticky="n")
        self.label_map_3 = ctk.CTkLabel(self.frame_map_3, text="", image=self.nuke_img)
        self.label_map_3.pack(side="top")
        self.label_map_text_3 = ctk.CTkLabel(self.frame_map_3, text="", fg_color=None, text_color='white', font=("Montserrat", 12))
        self.label_map_text_3.pack(side="top", pady=(3, 3))

        self.frame_map_4 = ctk.CTkFrame(frame_left, fg_color='#28397F', corner_radius=20, width=250, height=180,background_corner_colors=('#8D8DB9', '#8D8DB9', '#8D8DB9', '#8D8DB9'))
        self.frame_map_4.grid(row=3, column=1, padx=(0,10), pady=5, sticky="n")
        self.label_map_4 = ctk.CTkLabel(self.frame_map_4, text="", image=self.dust2_img)
        self.label_map_4.pack(side="top")
        self.label_map_text_4 = ctk.CTkLabel(self.frame_map_4, text="", fg_color=None, text_color='white', font=("Montserrat", 12))
        self.label_map_text_4.pack(side="top", pady=(3, 3))

        self.frame_map_5 = ctk.CTkFrame(frame_left, fg_color='#28397F', corner_radius=20, width=250, height=180,background_corner_colors=('#8D8DB9', '#8D8DB9', '#8D8DB9', '#8D8DB9'))
        self.frame_map_5.grid(row=4, column=0, padx=(10,0), pady=5, sticky="n")
        self.label_map_5 = ctk.CTkLabel(self.frame_map_5, text="", image=self.anubis_img)
        self.label_map_5.pack(side="top")
        self.label_map_text_5 = ctk.CTkLabel(self.frame_map_5, text="", fg_color=None, text_color='white', font=("Montserrat", 12))
        self.label_map_text_5.pack(side="top", pady=(3, 3))

        self.frame_map_6 = ctk.CTkFrame(frame_left, fg_color='#28397F', corner_radius=20, width=250, height=180,background_corner_colors=('#8D8DB9', '#8D8DB9', '#8D8DB9', '#8D8DB9'))
        self.frame_map_6.grid(row=4, column=1, padx=(0,10), pady=5, sticky="n")
        self.label_map_6 = ctk.CTkLabel(self.frame_map_6, text="", image=self.vertigo_img)
        self.label_map_6.pack(side="top")
        self.label_map_text_6 = ctk.CTkLabel(self.frame_map_6, text="", fg_color=None, text_color='white', font=("Montserrat", 12))
        self.label_map_text_6.pack(side="top", pady=(3, 3))

        self.frame_map_7 = ctk.CTkFrame(frame_left, fg_color='#28397F', corner_radius=20, width=250, height=180,background_corner_colors=('#8D8DB9', '#8D8DB9', '#8D8DB9', '#8D8DB9'))
        self.frame_map_7.grid(row=5, column=0, columnspan=2, padx=(0,10), pady=(5,15), sticky="n")
        self.label_map_7 = ctk.CTkLabel(self.frame_map_7, text="", image=self.inferno_img)
        self.label_map_7.pack(side="top")
        self.label_map_text_7 = ctk.CTkLabel(self.frame_map_7, text="", fg_color=None, text_color='white', font=("Montserrat", 12))
        self.label_map_text_7.pack(side="top", pady=(3, 3))

        #### Second frame for the right side ####
        frame_right_top = ctk.CTkFrame(self, corner_radius=20,fg_color='transparent')
        frame_right_top.grid(row=1, column=1, padx=(10,20), pady=(20,20), sticky="nsew")  # Second frame on right

        # Configure grid for the frame_right_top (columns 1 and 2 combined)
        frame_right_top.grid_columnconfigure((0, 1, 2), weight=1)
        frame_right_top.grid_rowconfigure(0, weight=1)
        frame_right_top.grid_rowconfigure(1, weight=10)
        frame_right_top.grid_rowconfigure(2, weight=1)

        frame_rounds_type_data_frame = ctk.CTkFrame(frame_right_top, fg_color='#8D8DB9', corner_radius=20)
        frame_rounds_type_data_frame.grid(row=0,column=0, columnspan=3,rowspan=3,sticky='nsew')

        frame_rounds_type_title = ctk.CTkFrame(frame_right_top, fg_color='#28397F', corner_radius=20,background_corner_colors=('','#8D8DB9','#8D8DB9','#8D8DB9'))
        frame_rounds_type_title.grid(row=0,column=0,columnspan=2,sticky="nw")

        rounds_type_title = ctk.CTkLabel(frame_rounds_type_title,text="Win rate by round type", font=("Stratum2 Bd", 28), text_color='white')
        rounds_type_title.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        ### viz gun round ###
        
        self.frame_round_type_viz_pistol = ctk.CTkFrame(frame_right_top, corner_radius=20)
        self.frame_round_type_viz_pistol.grid_columnconfigure((0, 1), weight=1)
        self.frame_round_type_viz_pistol.grid_rowconfigure(0, weight=1)
        self.frame_round_type_viz_pistol.grid_rowconfigure(1, weight=3)
        self.frame_round_type_viz_pistol.grid(row=1,column=0, padx=(10,0),pady=(0,15), sticky="nsew")

        viz_1_title = ctk.CTkLabel(self.frame_round_type_viz_pistol,text="Pistol rounds", font=("Montserrat", 18), text_color='white',fg_color='#8D8DB9',bg_color='#8D8DB9') #
        viz_1_title.grid(row=0, column=0,columnspan=2,sticky="nsew")
        
        
        ### infos force buy ###

        self.frame_round_type_viz_forcebuy = ctk.CTkFrame(frame_right_top)
        self.frame_round_type_viz_forcebuy.grid_columnconfigure((0, 1), weight=1)
        self.frame_round_type_viz_forcebuy.grid_rowconfigure(0, weight=1)
        self.frame_round_type_viz_forcebuy.grid_rowconfigure(1, weight=3)
        self.frame_round_type_viz_forcebuy.grid(row=1,column=1,padx=(5,5),pady=(0,15), sticky="nsew")

        viz_1_title = ctk.CTkLabel(self.frame_round_type_viz_forcebuy,text="Force Buy rounds", font=("Montserrat", 18), text_color='white',fg_color='#8D8DB9',bg_color='#8D8DB9')
        viz_1_title.grid(row=0, column=0,columnspan=2,sticky="nsew")
        

        ### infos full buy rounds ###

        self.frame_round_type_viz_fullbuy = ctk.CTkFrame(frame_right_top)
        self.frame_round_type_viz_fullbuy.grid_columnconfigure((0, 1), weight=1)
        self.frame_round_type_viz_fullbuy.grid_rowconfigure(0, weight=1)
        self.frame_round_type_viz_fullbuy.grid_rowconfigure(1, weight=3)
        self.frame_round_type_viz_fullbuy.grid(row=1,column=2,pady=(0,15),padx=(0,10), sticky="nsew")

        viz_1_title = ctk.CTkLabel(self.frame_round_type_viz_fullbuy,text="Full Buy rounds", font=("Montserrat", 18), text_color='white',fg_color='#8D8DB9',bg_color='#8D8DB9')
        viz_1_title.grid(row=0, column=0,columnspan=2,sticky="nsew")
        
        ###frame top###
        frame_top_3rd_row = ctk.CTkFrame(frame_right_top, corner_radius=20,fg_color='#8D8DB9',background_corner_colors=('#8D8DB9','#8D8DB9','',''))
        frame_top_3rd_row.grid_columnconfigure((0,1,2,3), weight=1)
        frame_top_3rd_row.grid(row=2, column=0,columnspan=4, sticky="nsew")

        frame_fb_vs_eco = ctk.CTkFrame(frame_top_3rd_row, corner_radius=20,fg_color='#28397F')
        frame_fb_vs_eco.grid_rowconfigure((0,1),weight=1)
        frame_fb_vs_eco.grid_columnconfigure(1,weight=1)
        frame_fb_vs_eco.grid(row=0,column=0,padx=(20,10), pady=5, sticky="nsew")
        label_fb_vs_eco = ctk.CTkLabel(frame_fb_vs_eco,text="Full buy losts against eco", font=("Montserrat", 14), text_color='white')
        label_fb_vs_eco.grid(row=0,column=1,padx=10, pady=(20,5), sticky="nsew")
        self.value_fb_vs_eco = ctk.CTkLabel(frame_fb_vs_eco,text="", font=("Stratum2 Bd", 28), text_color='white')
        self.value_fb_vs_eco.grid(row=1,column=1,padx=10, pady=(5,20), sticky="nsew")

        frame_fb_vs_force = ctk.CTkFrame(frame_top_3rd_row, corner_radius=20,fg_color='#28397F')
        frame_fb_vs_force.grid_rowconfigure((0,1),weight=1)
        frame_fb_vs_force.grid_columnconfigure(1,weight=1)
        frame_fb_vs_force.grid(row=0,column=1,padx=10, pady=5, sticky="nsew")
        label_fb_vs_force = ctk.CTkLabel(frame_fb_vs_force,text="Full buy losts against force buy ", font=("Montserrat", 14), text_color='white')
        label_fb_vs_force.grid(row=0,column=1,padx=10, pady=(20,5), sticky="nsew")
        self.value_fb_vs_force = ctk.CTkLabel(frame_fb_vs_force,text="", font=("Stratum2 Bd", 28), text_color='white')
        self.value_fb_vs_force.grid(row=1,column=1,padx=10, pady=(5,20), sticky="nsew")

        frame_eco_vs_fb = ctk.CTkFrame(frame_top_3rd_row, corner_radius=20,fg_color='#28397F')
        frame_eco_vs_fb.grid_rowconfigure((0,1),weight=1)
        frame_eco_vs_fb.grid_columnconfigure(1,weight=1)
        frame_eco_vs_fb.grid(row=0,column=2,padx=10, pady=5, sticky="nsew")
        label_eco_vs_fb = ctk.CTkLabel(frame_eco_vs_fb,text="Eco won against full buy", font=("Montserrat", 14), text_color='white')
        label_eco_vs_fb.grid(row=0,column=1,padx=10, pady=(20,5), sticky="nsew")
        self.value_eco_vs_fb = ctk.CTkLabel(frame_eco_vs_fb,text="", font=("Stratum2 Bd", 28), text_color='white')
        self.value_eco_vs_fb.grid(row=1,column=1,padx=10, pady=(5,20), sticky="nsew")
                             
        

        frame_force_vs_fb = ctk.CTkFrame(frame_top_3rd_row, corner_radius=20,fg_color='#28397F')
        frame_force_vs_fb.grid_rowconfigure((0,1),weight=1)
        frame_force_vs_fb.grid_columnconfigure(1,weight=1)
        frame_force_vs_fb.grid(row=0,column=3,padx=(10,20), pady=5, sticky="nsew")
        label_force_vs_fb = ctk.CTkLabel(frame_force_vs_fb,text="Force buy won against full buy", font=("Montserrat", 14), text_color='white')
        label_force_vs_fb.grid(row=0,column=1,padx=10, pady=(20,5), sticky="nsew")
        self.value_force_vs_fb = ctk.CTkLabel(frame_force_vs_fb,text="", font=("Stratum2 Bd", 28), text_color='white')
        self.value_force_vs_fb.grid(row=1,column=1,padx=10, pady=(5,20), sticky="nsew")

        

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
        self.closest_win_value = ctk.CTkLabel(frame_closest_win,text="", font=("Stratum2 Bd", 20), text_color='white')
        self.closest_win_value.grid(row=0,column=1,padx=(0,15), pady=10, sticky="nsew")


        frame_largest_win = ctk.CTkFrame(frame_right_bot, corner_radius=20 ,fg_color='#28397F')
        frame_largest_win.grid_columnconfigure(0,weight=1)
        frame_largest_win.grid_columnconfigure(1,weight=3)
        frame_largest_win.grid_rowconfigure(0,weight=1)
        frame_largest_win.grid(row=0,column=1,padx=(10,10), pady=(20,10), sticky="nsew")
        largest_win_label = ctk.CTkLabel(frame_largest_win,text="Largest win :", font=("Montserrat", 14), text_color='white')
        largest_win_label.grid(row=0,column=0,padx=(10,0), pady=10, sticky="nsew")
        self.largest_win_value = ctk.CTkLabel(frame_largest_win,text="", font=("Stratum2 Bd", 20), text_color='white')
        self.largest_win_value.grid(row=0,column=1,padx=(0,15), pady=10, sticky="nsew")

    
        frame_longest_winstreak = ctk.CTkFrame(frame_right_bot, fg_color='#28397F', corner_radius=20)
        frame_longest_winstreak.grid(row=0,column=2,padx=(10,20), pady=(20,10), sticky="nsew")
        frame_longest_winstreak.grid_columnconfigure(0,weight=1)
        frame_longest_winstreak.grid_columnconfigure(1,weight=3)
        frame_longest_winstreak.grid_rowconfigure(0,weight=1)
        longest_winstreak_label = ctk.CTkLabel(frame_longest_winstreak,text="Longest winstreak :", font=("Montserrat", 14), text_color='white')
        longest_winstreak_label.grid(row=0,column=0,padx=(10,0), pady=10, sticky="nsew")
        self.longest_winstreak_value = ctk.CTkLabel(frame_longest_winstreak,text="", font=("Stratum2 Bd", 20), text_color='white')
        self.longest_winstreak_value.grid(row=0,column=1,padx=(0,15), pady=10, sticky="nsew")


        total_rounds_played_frame = ctk.CTkFrame(frame_right_bot, fg_color='#28397F', corner_radius=20)
        total_rounds_played_frame.grid(row=1,column=0,padx=(20,10), pady=(10,20), sticky="nsew")
        total_rounds_played_frame.grid_columnconfigure(0,weight=1)
        total_rounds_played_frame.grid_columnconfigure(1,weight=3)
        total_rounds_played_frame.grid_rowconfigure(0,weight=1)
        total_rounds_played_label = ctk.CTkLabel(total_rounds_played_frame,text="Total rounds played :", font=("Montserrat", 14), text_color='white')
        total_rounds_played_label.grid(row=0,column=0,padx=(10,0), pady=10, sticky="nsew")
        self.total_rounds_played_value = ctk.CTkLabel(total_rounds_played_frame,text="", font=("Stratum2 Bd", 20), text_color='white')
        self.total_rounds_played_value.grid(row=0,column=1,padx=(0,15), pady=10, sticky="nsew")

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
    
    def update_data(self, analysis_results):
        # Vérifiez que les résultats d'analyse contiennent les données nécessaires
        if analysis_results:
            # Chargement des données depuis le script d'analyse
            team_name = self.master.team_name if hasattr(self.master, 'team_name') else "Unknown Team"
            own_team_wins = analysis_results.get("own_team_wins", 0)
            own_team_losses = analysis_results.get("own_team_losses", 0)
            special_round_type = analysis_results.get("special_round_type")
            map_stats = analysis_results.get("map_stats")
            round_stats = analysis_results.get("wr_per_round_type",pd.DataFrame())
            detailed_match_results = analysis_results.get("detailed_match_results")
            winstreak = analysis_results.get("winstreak")

            # mise a jour des widgets
            self.label_team_name.configure(text=team_name)
            self.label_team_record_wins.configure(text=f"{own_team_wins} Wins")
            self.label_team_record_losses.configure(text=f"{own_team_losses} Losses")

            self.value_fb_vs_eco.configure(text=special_round_type['count'][1])
            self.value_fb_vs_force.configure(text=special_round_type['count'][0])
            self.value_eco_vs_fb.configure(text=special_round_type['count'][2])
            self.value_force_vs_fb.configure(text=special_round_type['count'][3])

            # Victoire la plus large
            if detailed_match_results["largest_win"]:
                self.largest_win_value.configure(
                    text=f"{detailed_match_results['largest_win']['game_name']} {detailed_match_results['largest_win']['team_score']} - {detailed_match_results['largest_win']['opponent_score']}"
                )
            else:
                self.largest_win_value.configure(text="Aucune victoire enregistrée.")

            # Victoire la plus serrée
            if detailed_match_results["closest_win"]:
                self.closest_win_value.configure(
                    text=f"{detailed_match_results['closest_win']['game_name']} {detailed_match_results['closest_win']['team_score']} - {detailed_match_results['closest_win']['opponent_score']}"
                )
            else:
                self.closest_win_value.configure(text="Aucune victoire enregistrée.")

            self.longest_winstreak_value.configure(text=winstreak)

            self.total_rounds_played_value.configure(text=round_stats['total_rounds'].sum())
        
            if not map_stats.empty:
                # Exemple pour afficher les stats de de_anubis
                if "de_ancient" in map_stats.index:
                    ancient_stats = map_stats.loc["de_ancient"]
                    self.label_map_text_1.configure(text=f"Won : {ancient_stats['wins_on_map']} | Lost : {ancient_stats['times_played'] - ancient_stats['wins_on_map']} | WR : {ancient_stats['winrate']}%")
                else:
                    self.label_map_text_1.configure(text="Map not played")

                if "de_mirage" in map_stats.index:
                    mirage_stats = map_stats.loc["de_mirage"]
                    self.label_map_text_2.configure(text=f"Won : {int(mirage_stats['wins_on_map'])} | Lost : {int(mirage_stats['times_played'] - mirage_stats['wins_on_map'])} | WR : {int(mirage_stats['winrate'])}%")
                else:
                    self.label_map_text_2.configure(text="Map not played")

                if "de_nuke" in map_stats.index:
                    nuke_stats = map_stats.loc["de_nuke"]
                    self.label_map_text_3.configure(text=f"Won : {int(nuke_stats['wins_on_map'])} | Lost : {int(nuke_stats['times_played'] - nuke_stats['wins_on_map'])} | WR : {int(nuke_stats['winrate'])}%")
                else:
                    self.label_map_text_3.configure(text="Map not played")

                if "de_dust2" in map_stats.index:
                    dust2_stats = map_stats.loc["de_dust2"]
                    self.label_map_text_4.configure(text=f"Won : {int(dust2_stats['wins_on_map'])} | Lost : {int(dust2_stats['times_played'] - dust2_stats['wins_on_map'])} | WR : {int(dust2_stats['winrate'])}%")
                else:
                    self.label_map_text_4.configure(text="Map not played")

                if "de_anubis" in map_stats.index:
                    anubis_stats = map_stats.loc["de_anubis"]
                    self.label_map_text_5.configure(text=f"Won : {int(anubis_stats['wins_on_map'])} | Lost : {int(anubis_stats['times_played'] - anubis_stats['wins_on_map'])} | WR : {int(anubis_stats['winrate'])}%")
                else:
                    self.label_map_text_5.configure(text="Map not played")
                    
                if "de_vertigo" in map_stats.index:
                    vertigo_stats = map_stats.loc["de_vertigo"]
                    self.label_map_text_6.configure(text=f"Won : {int(vertigo_stats['wins_on_map'])} | Lost : {int(vertigo_stats['times_played'] - vertigo_stats['wins_on_map'])} | WR : {int(vertigo_stats['winrate'])}%")
                else:
                    self.label_map_text_6.configure(text="Map not played")

                if "de_inferno" in map_stats.index:
                    inferno_stats = map_stats.loc["de_inferno"]
                    self.label_map_text_7.configure(text=f"Won : {int(inferno_stats['wins_on_map'])} | Lost : {int(inferno_stats['times_played'] - inferno_stats['wins_on_map'])} | WR : {int(inferno_stats['winrate'])}%")
                else:
                    self.label_map_text_7.configure(text="Map not played")

            
            if not round_stats.empty:
                # Pistol Round CT
                pistol_ct = round_stats[(round_stats['round_category'] == 'Pistol round') & (round_stats['side'] == 'CT')]
                winrate_pistol_ct = int(pistol_ct['win_%'].values[0]) if not pistol_ct.empty else 0
                update_gauge_chart(self.frame_round_type_viz_pistol, winrate_pistol_ct, "CT", "#28397f", row=1, column=0)

                # Pistol Round Terrorist
                pistol_terrorist = round_stats[(round_stats['round_category'] == 'Pistol round') & (round_stats['side'] == 'T')]
                winrate_pistol_terrorist = int(pistol_terrorist['win_%'].values[0]) if not pistol_terrorist.empty else 0
                update_gauge_chart(self.frame_round_type_viz_pistol, winrate_pistol_terrorist, "T", "#fbac18", row=1, column=1)

                # Full Buy Round CT
                fullbuy_ct = round_stats[(round_stats['round_category'] == 'Full buy round') & (round_stats['side'] == 'CT')]
                winrate_fullbuy_ct = int(fullbuy_ct['win_%'].values[0]) if not fullbuy_ct.empty else 0
                update_gauge_chart(self.frame_round_type_viz_fullbuy, winrate_fullbuy_ct, "CT", "#28397f",row=1, column=0)

                # Full Buy Round Terrorist
                fullbuy_terrorist = round_stats[(round_stats['round_category'] == 'Full buy round') & (round_stats['side'] == 'T')]
                winrate_fullbuy_terrorist = int(fullbuy_terrorist['win_%'].values[0]) if not fullbuy_terrorist.empty else 0
                update_gauge_chart(self.frame_round_type_viz_fullbuy, winrate_fullbuy_terrorist, "T", "#fbac18", row=1, column=1)

                # Force Buy Round CT
                forcebuy_ct = round_stats[(round_stats['round_category'] == 'Force buy round') & (round_stats['side'] == 'CT')]
                winrate_forcebuy_ct = int(forcebuy_ct['win_%'].values[0]) if not forcebuy_ct.empty else 0
                update_gauge_chart(self.frame_round_type_viz_forcebuy, winrate_forcebuy_ct, "CT", "#28397f",row=1, column=0)

                # Force Buy Round Terrorist
                forcebuy_terrorist = round_stats[(round_stats['round_category'] == 'Force buy round') & (round_stats['side'] == 'T')]
                winrate_forcebuy_terrorist = int(forcebuy_terrorist['win_%'].values[0]) if not forcebuy_terrorist.empty else 0
                update_gauge_chart(self.frame_round_type_viz_forcebuy, winrate_forcebuy_terrorist, "T", "#fbac18", row=1, column=1)

            
        
            
if __name__ == "__main__":
    app = TeamSummaryPage()
    app.protocol("WM_DELETE_WINDOW", app.quit)
    app.mainloop()
