import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageOps, ImageDraw
from CTkTable import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from matplotlib.figure import Figure
import pandas as pd


ctk.set_appearance_mode('dark')
ctk.set_default_color_theme("theme.json")

class PlayerDetailPage(ctk.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("CS2 Stats Aggregator")
        self.geometry(f"{1600}x{900}")

        # configure grid layout for main window
        self.grid_columnconfigure(0, weight=1)  
        self.grid_columnconfigure((1,2,3,4), weight=1)  
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=10)
        

        #### Header ####
        frame_header = ctk.CTkFrame(self)
        frame_header.grid(row=0, column=0,columnspan=5, sticky="nwe")

        # Configurer les colonnes du frame_header
        frame_header.grid_columnconfigure(0, weight=1)
        frame_header.grid_columnconfigure(1, weight=1)

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

        ### FRAME PLAYER TILES ###
        frame_player_tiles = ctk.CTkFrame(self, corner_radius=20,fg_color="transparent")
        frame_player_tiles.grid(row=1, column=0,columnspan=5, sticky="nsew")
        frame_player_tiles.grid_columnconfigure((0,1,2,3,4), weight=1)  
        frame_player_tiles.grid_rowconfigure(0, weight=1)

        #### RECAP JOUEUR 1 ####
        frame_joueur_1 = ctk.CTkFrame(frame_player_tiles, corner_radius=20,fg_color="#8D8DB9")
        frame_joueur_1.grid(row=0, column=0, padx=(20,10), pady=(10,10), sticky="nsew")
        frame_joueur_1.grid_columnconfigure((0,1), weight=1)  
        frame_joueur_1.grid_rowconfigure((0,1,2,3,4), weight=1)

        frame_player_name = ctk.CTkFrame(frame_joueur_1,corner_radius=20,fg_color='#28397F',background_corner_colors=('#1a1a1a','#1a1a1a','#8D8DB9','#8D8DB9'))
        frame_player_name.grid(row=0,column=0,columnspan=2,sticky='nwe')

        label_player_name = ctk.CTkLabel(frame_player_name, text='Joueur 1', font=("Stratum2 Bd", 25), text_color='white')
        label_player_name.pack(pady=5,padx=10)

        frame_player_stats1 = ctk.CTkFrame(frame_joueur_1,corner_radius=20,fg_color='#28397F',background_corner_colors=('#8D8DB9','#8D8DB9','#8D8DB9','#8D8DB9'))
        frame_player_stats1.grid(row=1,column=0,padx=(10,5),pady=5,sticky='nwe')

        label_stats1 = ctk.CTkLabel(frame_player_stats1, text='Rating', font=("Stratum2 Bd", 16), text_color='white')
        label_stats1.pack(pady=1,padx=10)

        value_stats1 = ctk.CTkLabel(frame_player_stats1, text='1,04', font=("Montserrat", 14), text_color='white')
        value_stats1.pack(pady=1,padx=10)

        frame_player_stats1_1 = ctk.CTkFrame(frame_joueur_1,corner_radius=20,fg_color='#28397F',background_corner_colors=('#8D8DB9','#8D8DB9','#8D8DB9','#8D8DB9'))
        frame_player_stats1_1.grid(row=1,column=1,padx=(5,10),pady=5,sticky='nwe')

        label_stats1_1 = ctk.CTkLabel(frame_player_stats1_1, text='Impact', font=("Stratum2 Bd", 16), text_color='white')
        label_stats1_1.pack(pady=1,padx=10)

        value_stats1_1 = ctk.CTkLabel(frame_player_stats1_1, text='0,98', font=("Montserrat", 14), text_color='white')
        value_stats1_1.pack(pady=1,padx=10)

        frame_player_stats2 = ctk.CTkFrame(frame_joueur_1,corner_radius=20,fg_color='#28397F',background_corner_colors=('#8D8DB9','#8D8DB9','#8D8DB9','#8D8DB9'))
        frame_player_stats2.grid(row=2,column=0,padx=(10,5),pady=5,sticky='nwe')

        label_stats2 = ctk.CTkLabel(frame_player_stats2, text='ADR', font=("Stratum2 Bd", 16), text_color='white')
        label_stats2.pack(pady=1,padx=10)

        value_stats2 = ctk.CTkLabel(frame_player_stats2, text='102', font=("Montserrat", 14), text_color='white')
        value_stats2.pack(pady=1,padx=10)

        frame_player_stats2_2 = ctk.CTkFrame(frame_joueur_1,corner_radius=20,fg_color='#28397F',background_corner_colors=('#8D8DB9','#8D8DB9','#8D8DB9','#8D8DB9'))
        frame_player_stats2_2.grid(row=2,column=1,padx=(5,10),pady=5,sticky='nwe')

        label_stats2_2 = ctk.CTkLabel(frame_player_stats2_2, text='KAST%', font=("Stratum2 Bd", 16), text_color='white')
        label_stats2_2.pack(pady=1,padx=10)

        value_stats2_2 = ctk.CTkLabel(frame_player_stats2_2, text='72%', font=("Montserrat", 14), text_color='white')
        value_stats2_2.pack(pady=1,padx=10)

        frame_player_stats3 = ctk.CTkFrame(frame_joueur_1,corner_radius=20,fg_color='#28397F',background_corner_colors=('#8D8DB9','#8D8DB9','#8D8DB9','#8D8DB9'))
        frame_player_stats3.grid(row=3,column=0,padx=(10,5),pady=(5,10),sticky='nwe')

        label_stats3 = ctk.CTkLabel(frame_player_stats3, text='KPR', font=("Stratum2 Bd", 16), text_color='white')
        label_stats3.pack(pady=1,padx=10)

        value_stats3 = ctk.CTkLabel(frame_player_stats3, text='1,00', font=("Montserrat", 14), text_color='white')
        value_stats3.pack(pady=1,padx=10)
        
        frame_player_stats3_3 = ctk.CTkFrame(frame_joueur_1,corner_radius=20,fg_color='#28397F',background_corner_colors=('#8D8DB9','#8D8DB9','#8D8DB9','#8D8DB9'))
        frame_player_stats3_3.grid(row=3,column=1,padx=(5,10),pady=(5,10),sticky='nwe')

        label_stats3_3 = ctk.CTkLabel(frame_player_stats3_3, text='DPR', font=("Stratum2 Bd", 16), text_color='white')
        label_stats3_3.pack(pady=1,padx=10)

        value_stats3_3 = ctk.CTkLabel(frame_player_stats3_3, text='0,66', font=("Montserrat", 14), text_color='white')
        value_stats3_3.pack(pady=1,padx=10)
        

        #### FRAME JOUEUR 2 ####
        frame_joueur_2 = ctk.CTkFrame(frame_player_tiles, corner_radius=20,fg_color="#8D8DB9")
        frame_joueur_2.grid(row=0, column=1, padx=(10,10), pady=(10,10), sticky="nsew")
        frame_joueur_2.grid_columnconfigure((0,1), weight=1)  
        frame_joueur_2.grid_rowconfigure((0,1,2,3,4), weight=1)

        frame_player_name = ctk.CTkFrame(frame_joueur_2,corner_radius=20,fg_color='#28397F',background_corner_colors=('#1a1a1a','#1a1a1a','#8D8DB9','#8D8DB9'))
        frame_player_name.grid(row=0,column=0,columnspan=2,sticky='nwe')

        label_player_name = ctk.CTkLabel(frame_player_name, text='Joueur 2', font=("Stratum2 Bd", 25), text_color='white')
        label_player_name.pack(pady=5,padx=10)

        frame_player_stats1 = ctk.CTkFrame(frame_joueur_2,corner_radius=20,fg_color='#28397F',background_corner_colors=('#8D8DB9','#8D8DB9','#8D8DB9','#8D8DB9'))
        frame_player_stats1.grid(row=1,column=0,padx=(10,5),pady=5,sticky='nwe')

        label_stats1 = ctk.CTkLabel(frame_player_stats1, text='Rating', font=("Stratum2 Bd", 16), text_color='white')
        label_stats1.pack(pady=1,padx=10)

        value_stats1 = ctk.CTkLabel(frame_player_stats1, text='1,04', font=("Montserrat", 14), text_color='white')
        value_stats1.pack(pady=1,padx=10)

        frame_player_stats1_1 = ctk.CTkFrame(frame_joueur_2,corner_radius=20,fg_color='#28397F',background_corner_colors=('#8D8DB9','#8D8DB9','#8D8DB9','#8D8DB9'))
        frame_player_stats1_1.grid(row=1,column=1,padx=(5,10),pady=5,sticky='nwe')

        label_stats1_1 = ctk.CTkLabel(frame_player_stats1_1, text='Impact', font=("Stratum2 Bd", 16), text_color='white')
        label_stats1_1.pack(pady=1,padx=10)

        value_stats1_1 = ctk.CTkLabel(frame_player_stats1_1, text='0,98', font=("Montserrat", 14), text_color='white')
        value_stats1_1.pack(pady=1,padx=10)

        frame_player_stats2 = ctk.CTkFrame(frame_joueur_2,corner_radius=20,fg_color='#28397F',background_corner_colors=('#8D8DB9','#8D8DB9','#8D8DB9','#8D8DB9'))
        frame_player_stats2.grid(row=2,column=0,padx=(10,5),pady=5,sticky='nwe')

        label_stats2 = ctk.CTkLabel(frame_player_stats2, text='ADR', font=("Stratum2 Bd", 16), text_color='white')
        label_stats2.pack(pady=1,padx=10)

        value_stats2 = ctk.CTkLabel(frame_player_stats2, text='102', font=("Montserrat", 14), text_color='white')
        value_stats2.pack(pady=1,padx=10)

        frame_player_stats2_2 = ctk.CTkFrame(frame_joueur_2,corner_radius=20,fg_color='#28397F',background_corner_colors=('#8D8DB9','#8D8DB9','#8D8DB9','#8D8DB9'))
        frame_player_stats2_2.grid(row=2,column=1,padx=(5,10),pady=5,sticky='nwe')

        label_stats2_2 = ctk.CTkLabel(frame_player_stats2_2, text='KAST%', font=("Stratum2 Bd", 16), text_color='white')
        label_stats2_2.pack(pady=1,padx=10)

        value_stats2_2 = ctk.CTkLabel(frame_player_stats2_2, text='72%', font=("Montserrat", 14), text_color='white')
        value_stats2_2.pack(pady=1,padx=10)

        frame_player_stats3 = ctk.CTkFrame(frame_joueur_2,corner_radius=20,fg_color='#28397F',background_corner_colors=('#8D8DB9','#8D8DB9','#8D8DB9','#8D8DB9'))
        frame_player_stats3.grid(row=3,column=0,padx=(10,5),pady=(5,10),sticky='nwe')

        label_stats3 = ctk.CTkLabel(frame_player_stats3, text='KPR', font=("Stratum2 Bd", 16), text_color='white')
        label_stats3.pack(pady=1,padx=10)

        value_stats3 = ctk.CTkLabel(frame_player_stats3, text='1,00', font=("Montserrat", 14), text_color='white')
        value_stats3.pack(pady=1,padx=10)
        
        frame_player_stats3_3 = ctk.CTkFrame(frame_joueur_2,corner_radius=20,fg_color='#28397F',background_corner_colors=('#8D8DB9','#8D8DB9','#8D8DB9','#8D8DB9'))
        frame_player_stats3_3.grid(row=3,column=1,padx=(5,10),pady=(5,10),sticky='nwe')

        label_stats3_3 = ctk.CTkLabel(frame_player_stats3_3, text='DPR', font=("Stratum2 Bd", 16), text_color='white')
        label_stats3_3.pack(pady=1,padx=10)

        value_stats3_3 = ctk.CTkLabel(frame_player_stats3_3, text='0,66', font=("Montserrat", 14), text_color='white')
        value_stats3_3.pack(pady=1,padx=10)

        #### Joueur 3 ####
        frame_joueur_3 = ctk.CTkFrame(frame_player_tiles, corner_radius=20,fg_color="#8D8DB9")
        frame_joueur_3.grid(row=0, column=2, padx=(10,10), pady=(10,10), sticky="nsew")
        frame_joueur_3.grid_columnconfigure((0,1), weight=1)  
        frame_joueur_3.grid_rowconfigure((0,1,2,3,4), weight=1)

        frame_player_name = ctk.CTkFrame(frame_joueur_3,corner_radius=20,fg_color='#28397F',background_corner_colors=('#1a1a1a','#1a1a1a','#8D8DB9','#8D8DB9'))
        frame_player_name.grid(row=0,column=0,columnspan=2,sticky='nwe')

        label_player_name = ctk.CTkLabel(frame_player_name, text='Joueur 3', font=("Stratum2 Bd", 25), text_color='white')
        label_player_name.pack(pady=5,padx=10)

        frame_player_stats1 = ctk.CTkFrame(frame_joueur_3,corner_radius=20,fg_color='#28397F',background_corner_colors=('#8D8DB9','#8D8DB9','#8D8DB9','#8D8DB9'))
        frame_player_stats1.grid(row=1,column=0,padx=(10,5),pady=5,sticky='nwe')

        label_stats1 = ctk.CTkLabel(frame_player_stats1, text='Rating', font=("Stratum2 Bd", 16), text_color='white')
        label_stats1.pack(pady=1,padx=10)

        value_stats1 = ctk.CTkLabel(frame_player_stats1, text='1,04', font=("Montserrat", 14), text_color='white')
        value_stats1.pack(pady=1,padx=10)

        frame_player_stats1_1 = ctk.CTkFrame(frame_joueur_3,corner_radius=20,fg_color='#28397F',background_corner_colors=('#8D8DB9','#8D8DB9','#8D8DB9','#8D8DB9'))
        frame_player_stats1_1.grid(row=1,column=1,padx=(5,10),pady=5,sticky='nwe')

        label_stats1_1 = ctk.CTkLabel(frame_player_stats1_1, text='Impact', font=("Stratum2 Bd", 16), text_color='white')
        label_stats1_1.pack(pady=1,padx=10)

        value_stats1_1 = ctk.CTkLabel(frame_player_stats1_1, text='0,98', font=("Montserrat", 14), text_color='white')
        value_stats1_1.pack(pady=1,padx=10)

        frame_player_stats2 = ctk.CTkFrame(frame_joueur_3,corner_radius=20,fg_color='#28397F',background_corner_colors=('#8D8DB9','#8D8DB9','#8D8DB9','#8D8DB9'))
        frame_player_stats2.grid(row=2,column=0,padx=(10,5),pady=5,sticky='nwe')

        label_stats2 = ctk.CTkLabel(frame_player_stats2, text='ADR', font=("Stratum2 Bd", 16), text_color='white')
        label_stats2.pack(pady=1,padx=10)

        value_stats2 = ctk.CTkLabel(frame_player_stats2, text='102', font=("Montserrat", 14), text_color='white')
        value_stats2.pack(pady=1,padx=10)

        frame_player_stats2_2 = ctk.CTkFrame(frame_joueur_3,corner_radius=20,fg_color='#28397F',background_corner_colors=('#8D8DB9','#8D8DB9','#8D8DB9','#8D8DB9'))
        frame_player_stats2_2.grid(row=2,column=1,padx=(5,10),pady=5,sticky='nwe')

        label_stats2_2 = ctk.CTkLabel(frame_player_stats2_2, text='KAST%', font=("Stratum2 Bd", 16), text_color='white')
        label_stats2_2.pack(pady=1,padx=10)

        value_stats2_2 = ctk.CTkLabel(frame_player_stats2_2, text='72%', font=("Montserrat", 14), text_color='white')
        value_stats2_2.pack(pady=1,padx=10)

        frame_player_stats3 = ctk.CTkFrame(frame_joueur_3,corner_radius=20,fg_color='#28397F',background_corner_colors=('#8D8DB9','#8D8DB9','#8D8DB9','#8D8DB9'))
        frame_player_stats3.grid(row=3,column=0,padx=(10,5),pady=(5,10),sticky='nwe')

        label_stats3 = ctk.CTkLabel(frame_player_stats3, text='KPR', font=("Stratum2 Bd", 16), text_color='white')
        label_stats3.pack(pady=1,padx=10)

        value_stats3 = ctk.CTkLabel(frame_player_stats3, text='1,00', font=("Montserrat", 14), text_color='white')
        value_stats3.pack(pady=1,padx=10)
        
        frame_player_stats3_3 = ctk.CTkFrame(frame_joueur_3,corner_radius=20,fg_color='#28397F',background_corner_colors=('#8D8DB9','#8D8DB9','#8D8DB9','#8D8DB9'))
        frame_player_stats3_3.grid(row=3,column=1,padx=(5,10),pady=(5,10),sticky='nwe')

        label_stats3_3 = ctk.CTkLabel(frame_player_stats3_3, text='DPR', font=("Stratum2 Bd", 16), text_color='white')
        label_stats3_3.pack(pady=1,padx=10)

        value_stats3_3 = ctk.CTkLabel(frame_player_stats3_3, text='0,66', font=("Montserrat", 14), text_color='white')
        value_stats3_3.pack(pady=1,padx=10)

        #### Joueur 4 ####
        frame_joueur_4 = ctk.CTkFrame(frame_player_tiles, corner_radius=20,fg_color="#8D8DB9")
        frame_joueur_4.grid(row=0, column=3, padx=(10,10), pady=(10,10), sticky="nsew")
        frame_joueur_4.grid_columnconfigure((0,1), weight=1)  
        frame_joueur_4.grid_rowconfigure((0,1,2,3,4), weight=1)

        frame_player_name = ctk.CTkFrame(frame_joueur_4,corner_radius=20,fg_color='#28397F',background_corner_colors=('#1a1a1a','#1a1a1a','#8D8DB9','#8D8DB9'))
        frame_player_name.grid(row=0,column=0,columnspan=2,sticky='nwe')

        label_player_name = ctk.CTkLabel(frame_player_name, text='Joueur 4', font=("Stratum2 Bd", 25), text_color='white')
        label_player_name.pack(pady=5,padx=10)

        frame_player_stats1 = ctk.CTkFrame(frame_joueur_4,corner_radius=20,fg_color='#28397F',background_corner_colors=('#8D8DB9','#8D8DB9','#8D8DB9','#8D8DB9'))
        frame_player_stats1.grid(row=1,column=0,padx=(10,5),pady=5,sticky='nwe')

        label_stats1 = ctk.CTkLabel(frame_player_stats1, text='Rating', font=("Stratum2 Bd", 16), text_color='white')
        label_stats1.pack(pady=1,padx=10)

        value_stats1 = ctk.CTkLabel(frame_player_stats1, text='1,04', font=("Montserrat", 14), text_color='white')
        value_stats1.pack(pady=1,padx=10)

        frame_player_stats1_1 = ctk.CTkFrame(frame_joueur_4,corner_radius=20,fg_color='#28397F',background_corner_colors=('#8D8DB9','#8D8DB9','#8D8DB9','#8D8DB9'))
        frame_player_stats1_1.grid(row=1,column=1,padx=(5,10),pady=5,sticky='nwe')

        label_stats1_1 = ctk.CTkLabel(frame_player_stats1_1, text='Impact', font=("Stratum2 Bd", 16), text_color='white')
        label_stats1_1.pack(pady=1,padx=10)

        value_stats1_1 = ctk.CTkLabel(frame_player_stats1_1, text='0,98', font=("Montserrat", 14), text_color='white')
        value_stats1_1.pack(pady=1,padx=10)

        frame_player_stats2 = ctk.CTkFrame(frame_joueur_4,corner_radius=20,fg_color='#28397F',background_corner_colors=('#8D8DB9','#8D8DB9','#8D8DB9','#8D8DB9'))
        frame_player_stats2.grid(row=2,column=0,padx=(10,5),pady=5,sticky='nwe')

        label_stats2 = ctk.CTkLabel(frame_player_stats2, text='ADR', font=("Stratum2 Bd", 16), text_color='white')
        label_stats2.pack(pady=1,padx=10)

        value_stats2 = ctk.CTkLabel(frame_player_stats2, text='102', font=("Montserrat", 14), text_color='white')
        value_stats2.pack(pady=1,padx=10)

        frame_player_stats2_2 = ctk.CTkFrame(frame_joueur_4,corner_radius=20,fg_color='#28397F',background_corner_colors=('#8D8DB9','#8D8DB9','#8D8DB9','#8D8DB9'))
        frame_player_stats2_2.grid(row=2,column=1,padx=(5,10),pady=5,sticky='nwe')

        label_stats2_2 = ctk.CTkLabel(frame_player_stats2_2, text='KAST%', font=("Stratum2 Bd", 16), text_color='white')
        label_stats2_2.pack(pady=1,padx=10)

        value_stats2_2 = ctk.CTkLabel(frame_player_stats2_2, text='72%', font=("Montserrat", 14), text_color='white')
        value_stats2_2.pack(pady=1,padx=10)

        frame_player_stats3 = ctk.CTkFrame(frame_joueur_4,corner_radius=20,fg_color='#28397F',background_corner_colors=('#8D8DB9','#8D8DB9','#8D8DB9','#8D8DB9'))
        frame_player_stats3.grid(row=3,column=0,padx=(10,5),pady=(5,10),sticky='nwe')

        label_stats3 = ctk.CTkLabel(frame_player_stats3, text='KPR', font=("Stratum2 Bd", 16), text_color='white')
        label_stats3.pack(pady=1,padx=10)

        value_stats3 = ctk.CTkLabel(frame_player_stats3, text='1,00', font=("Montserrat", 14), text_color='white')
        value_stats3.pack(pady=1,padx=10)
        
        frame_player_stats3_3 = ctk.CTkFrame(frame_joueur_4,corner_radius=20,fg_color='#28397F',background_corner_colors=('#8D8DB9','#8D8DB9','#8D8DB9','#8D8DB9'))
        frame_player_stats3_3.grid(row=3,column=1,padx=(5,10),pady=(5,10),sticky='nwe')

        label_stats3_3 = ctk.CTkLabel(frame_player_stats3_3, text='DPR', font=("Stratum2 Bd", 16), text_color='white')
        label_stats3_3.pack(pady=1,padx=10)

        value_stats3_3 = ctk.CTkLabel(frame_player_stats3_3, text='0,66', font=("Montserrat", 14), text_color='white')
        value_stats3_3.pack(pady=1,padx=10)

        #### Frame for Columns 1 and 2 ####
        frame_joueur_5 = ctk.CTkFrame(frame_player_tiles, corner_radius=20,fg_color="#8D8DB9")
        frame_joueur_5.grid(row=0, column=4, padx=(10,20), pady=(10,10), sticky="nsew")
        frame_joueur_5.grid_columnconfigure((0,1), weight=1)  
        frame_joueur_5.grid_rowconfigure((0,1,2,3,4), weight=1)

        frame_player_name = ctk.CTkFrame(frame_joueur_5,corner_radius=20,fg_color='#28397F',background_corner_colors=('#1a1a1a','#1a1a1a','#8D8DB9','#8D8DB9'))
        frame_player_name.grid(row=0,column=0,columnspan=2,sticky='nwe')

        label_player_name = ctk.CTkLabel(frame_player_name, text='Joueur 5', font=("Stratum2 Bd", 25), text_color='white')
        label_player_name.pack(pady=5,padx=10)

        frame_player_stats1 = ctk.CTkFrame(frame_joueur_5,corner_radius=20,fg_color='#28397F',background_corner_colors=('#8D8DB9','#8D8DB9','#8D8DB9','#8D8DB9'))
        frame_player_stats1.grid(row=1,column=0,padx=(10,5),pady=5,sticky='nwe')

        label_stats1 = ctk.CTkLabel(frame_player_stats1, text='Rating', font=("Stratum2 Bd", 16), text_color='white')
        label_stats1.pack(pady=1,padx=10)

        value_stats1 = ctk.CTkLabel(frame_player_stats1, text='1,04', font=("Montserrat", 14), text_color='white')
        value_stats1.pack(pady=1,padx=10)

        frame_player_stats1_1 = ctk.CTkFrame(frame_joueur_5,corner_radius=20,fg_color='#28397F',background_corner_colors=('#8D8DB9','#8D8DB9','#8D8DB9','#8D8DB9'))
        frame_player_stats1_1.grid(row=1,column=1,padx=(5,10),pady=5,sticky='nwe')

        label_stats1_1 = ctk.CTkLabel(frame_player_stats1_1, text='Impact', font=("Stratum2 Bd", 16), text_color='white')
        label_stats1_1.pack(pady=1,padx=10)

        value_stats1_1 = ctk.CTkLabel(frame_player_stats1_1, text='0,98', font=("Montserrat", 14), text_color='white')
        value_stats1_1.pack(pady=1,padx=10)

        frame_player_stats2 = ctk.CTkFrame(frame_joueur_5,corner_radius=20,fg_color='#28397F',background_corner_colors=('#8D8DB9','#8D8DB9','#8D8DB9','#8D8DB9'))
        frame_player_stats2.grid(row=2,column=0,padx=(10,5),pady=5,sticky='nwe')

        label_stats2 = ctk.CTkLabel(frame_player_stats2, text='ADR', font=("Stratum2 Bd", 16), text_color='white')
        label_stats2.pack(pady=1,padx=10)

        value_stats2 = ctk.CTkLabel(frame_player_stats2, text='102', font=("Montserrat", 14), text_color='white')
        value_stats2.pack(pady=1,padx=10)

        frame_player_stats2_2 = ctk.CTkFrame(frame_joueur_5,corner_radius=20,fg_color='#28397F',background_corner_colors=('#8D8DB9','#8D8DB9','#8D8DB9','#8D8DB9'))
        frame_player_stats2_2.grid(row=2,column=1,padx=(5,10),pady=5,sticky='nwe')

        label_stats2_2 = ctk.CTkLabel(frame_player_stats2_2, text='KAST%', font=("Stratum2 Bd", 16), text_color='white')
        label_stats2_2.pack(pady=1,padx=10)

        value_stats2_2 = ctk.CTkLabel(frame_player_stats2_2, text='72%', font=("Montserrat", 14), text_color='white')
        value_stats2_2.pack(pady=1,padx=10)

        frame_player_stats3 = ctk.CTkFrame(frame_joueur_5,corner_radius=20,fg_color='#28397F',background_corner_colors=('#8D8DB9','#8D8DB9','#8D8DB9','#8D8DB9'))
        frame_player_stats3.grid(row=3,column=0,padx=(10,5),pady=(5,10),sticky='nwe')

        label_stats3 = ctk.CTkLabel(frame_player_stats3, text='KPR', font=("Stratum2 Bd", 16), text_color='white')
        label_stats3.pack(pady=1,padx=10)

        value_stats3 = ctk.CTkLabel(frame_player_stats3, text='1,00', font=("Montserrat", 14), text_color='white')
        value_stats3.pack(pady=1,padx=10)
        
        frame_player_stats3_3 = ctk.CTkFrame(frame_joueur_5,corner_radius=20,fg_color='#28397F',background_corner_colors=('#8D8DB9','#8D8DB9','#8D8DB9','#8D8DB9'))
        frame_player_stats3_3.grid(row=3,column=1,padx=(5,10),pady=(5,10),sticky='nwe')

        label_stats3_3 = ctk.CTkLabel(frame_player_stats3_3, text='DPR', font=("Stratum2 Bd", 16), text_color='white')
        label_stats3_3.pack(pady=1,padx=10)

        value_stats3_3 = ctk.CTkLabel(frame_player_stats3_3, text='0,66', font=("Montserrat", 14), text_color='white')
        value_stats3_3.pack(pady=1,padx=10)
        

        ### FRAME BOTTOM ###
        frame_bottom = ctk.CTkFrame(self,corner_radius=20,fg_color='transparent')#fg_color="#8D8DB9"
        frame_bottom.grid(row=2, column=0, padx=20,columnspan=5, pady=(10,20), sticky="nsew")
        frame_bottom.grid_columnconfigure((0,1,2), weight=1)  
        frame_bottom.grid_rowconfigure((0,1), weight=1)
        
        ### FRAME utils ###
        frame_utils = ctk.CTkFrame(frame_bottom, corner_radius=20,fg_color="#8D8DB9",background_corner_colors=('#1a1a1a','#1a1a1a','#1a1a1a','#1a1a1a'))
        frame_utils.grid(row=0, column=0, padx=20, pady=(10,10), sticky="nesw")
        frame_utils.grid_columnconfigure(0, weight=1)  
        frame_utils.grid_rowconfigure((0,1), weight=1)

        ### stacked bar chart dmg utils ###
        
        data_util = {
        'name': ['-silentGG', 'BELDIYA00', 'OzzieOzz', 'Spiritix', 'godofbaldz'],
        'He_dmg': [186, 495, 286, 253, 340],
        'Fire_dmg': [264, 189, 52, 120, 89],
        'Total_utility_dmg':[450,684,338,373,429]
        }
        df_util = pd.DataFrame(data_util)
        
        # Création du stacked bar chart
        fig, ax = plt.subplots(figsize=(4, 3), facecolor='#8D8DB9')
        bars1 = ax.bar(df_util['name'], df_util['He_dmg'], label='He', color='#1a1a1a')
        bars2 = ax.bar(df_util['name'], df_util['Fire_dmg'], label='Fire', bottom=df_util['He_dmg'], color='red')
        ax.bar_label(bars2, labels=df_util['Total_utility_dmg'], label_type='edge',fontsize=8, fontweight='bold', color='white',padding=2)

        # Personnalisation des labels et de la légende
        ax.legend(loc="upper right", bbox_to_anchor=(1, 1.1), fontsize=8, facecolor='#8D8DB9',frameon=False)
        # ax.text(x=df_full['Total_utility_dmg'],ha='center', fontsize=10, fontweight='bold')
        ax.tick_params(axis='x', labelsize=8)
        ax.set_yticks([])
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        fig.patch.set_alpha(0)
        ax.patch.set_alpha(0)
    
        canvas1 = FigureCanvasTkAgg(fig, master=frame_utils) 
        canvas1.draw() 
        canvas1.get_tk_widget().config(bg="#8D8DB9", highlightthickness=0) 
        canvas1.get_tk_widget().grid(row=0, column=0, sticky="nsew")

        ### FRAME utils ###
        frame_flash = ctk.CTkFrame(frame_bottom, corner_radius=20,fg_color="#8D8DB9",background_corner_colors=('#1a1a1a','#1a1a1a','#1a1a1a','#1a1a1a'))
        frame_flash.grid(row=0, column=1, padx=20, pady=(10,10), sticky="nsew")
        frame_flash.grid_columnconfigure(0, weight=1)  
        frame_flash.grid_rowconfigure((0,1), weight=1)

        data_util_2 = {
        'name': ['-silentGG', 'BELDIYA00', 'OzzieOzz', 'Spiritix', 'godofbaldz'],
        'Ennemy_flashed': [65, 32, 43, 16, 53],
        'flash_assist': [12, 3, 22, 1, 14],
        }
        df_util_2 = pd.DataFrame(data_util_2)

        # Création du grouped bar chart
        fig, ax = plt.subplots(figsize=(4, 3), facecolor='#8D8DB9')
        width = 0.35  # Largeur des barres

        # Positions des barres pour chaque catégorie
        x = range(len(df_util_2['name']))
        bars1 = ax.bar([pos - width / 2 for pos in x], df_util_2['Ennemy_flashed'], width=width, label='Ennemy flashed', color='grey')
        bars2 = ax.bar([pos + width / 2 for pos in x], df_util_2['flash_assist'], width=width, label='Flash assist', color='orange')

        # Ajout des labels sur les barres
        ax.bar_label(bars1, labels=df_util_2['Ennemy_flashed'], label_type='center', fontsize=8, fontweight='bold', color='white')
        ax.bar_label(bars2, labels=df_util_2['flash_assist'], label_type='center', fontsize=8, fontweight='bold', color='white')

        # Personnalisation des labels et de la légende
        ax.set_xticks(x)
        ax.set_xticklabels(df_util_2['name'], fontsize=8)
        ax.legend(loc="upper right", bbox_to_anchor=(1, 1.1), fontsize=8, facecolor='#8D8DB9', frameon=False)
        ax.set_yticks([])
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        fig.patch.set_alpha(0)
        ax.patch.set_alpha(0)

        # Intégration dans Tkinter
        canvas2 = FigureCanvasTkAgg(fig, master=frame_flash)
        canvas2.draw()
        canvas2.get_tk_widget().config(bg="#8D8DB9", highlightthickness=0)
        canvas2.get_tk_widget().grid(row=0, column=0, sticky="nsew")

        ### FRAME utils ###
        frame_entry = ctk.CTkFrame(frame_bottom, corner_radius=20,fg_color="#8D8DB9",bg_color="#8D8DB9",background_corner_colors=('#1a1a1a','#1a1a1a','#1a1a1a','#1a1a1a'))
        frame_entry.grid(row=0, column=2, padx=20, pady=(10,10), sticky="nsew")
        frame_entry.grid_columnconfigure(0, weight=1)  
        frame_entry.grid_rowconfigure((0,1), weight=1)

        data_entry = {
            "name": ["Spiritix", "OzzieOzz", "-silentGG", "godofbaldz", "BELDIYA00"],
            "entry_attempts(T)": [8, 5, 6, 11, 9],
            "entry_successes(T)": [6, 2, 3, 8, 7],
            "%_entry_success(T)": [75.0, 40.0, 50.0, 73.0, 78.0],
            "open_attempts(CT)": [17, 6, 7, 10, 5],
            "open_successes(CT)": [12, 1, 5, 5, 4],
            "%_open_success(CT)": [71.0, 17.0, 71.0, 50.0, 80.0]
        }
        df_entry = pd.DataFrame(data_entry)

        fig, ax = plt.subplots(figsize=(4, 3), facecolor='#8D8DB9')
        ax.scatter(df_entry['entry_attempts(T)'], df_entry['%_open_success(CT)'], color='#fbac18', label='Entry Success (T)')
        ax.scatter(df_entry['open_attempts(CT)'], df_entry['%_open_success(CT)'], color='#28397F', label='Open Success (CT)')
        for i, player in enumerate(df_entry['name']):
            ax.annotate(player, (df_entry['entry_attempts(T)'][i], df_entry['%_open_success(CT)'][i]), 
                        textcoords="offset points", xytext=(5,5), ha='center', color='#fbac18',fontsize=8)
            ax.annotate(player, (df_entry['open_attempts(CT)'][i], df_entry['%_open_success(CT)'][i]), 
                        textcoords="offset points", xytext=(5,5), ha='center', color='#28397F',fontsize=8)
        ax.set_xlabel('Attempts', fontsize=8)
        ax.set_ylabel('% Successes', fontsize=8)
        ax.tick_params(axis='x', labelsize=8)
        ax.tick_params(axis='y', labelsize=8)
        ax.legend(fontsize=8, facecolor='#8D8DB9',frameon=False)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        fig.patch.set_alpha(0)
        ax.patch.set_alpha(0)

        canvas3 = FigureCanvasTkAgg(fig, master=frame_entry)
        canvas3.draw()
        canvas3.get_tk_widget().config(bg="#8D8DB9", highlightthickness=0)
        canvas3.get_tk_widget().grid(row=0, column=0, sticky="nsew")
        
        ### FRAME utils ###
        frame_eco = ctk.CTkFrame(frame_bottom, corner_radius=20,fg_color="#8D8DB9",background_corner_colors=('#1a1a1a','#1a1a1a','#1a1a1a','#1a1a1a'))
        frame_eco.grid(row=1, column=0, columnspan=3,padx=20, pady=(10,10), sticky="nw")
        frame_eco.grid_columnconfigure(0, weight=1)  
        frame_eco.grid_rowconfigure((0,1), weight=1)


        data_eco={
            "name": ["Spiritix", "OzzieOzz", "-silentGG", "godofbaldz", "BELDIYA00"],
            "Anti eco kill": [8, 5, 6, 11, 9],
            "Anti force buy kill": [6, 2, 3, 8, 7],
            "Full buy kill": [75, 40, 50, 73, 78],
            "Pistol round": [17, 6, 7, 10, 5]
        }
        df_eco = pd.DataFrame(data_eco)
        
        fig, axes = plt.subplots(1, len(df_eco), figsize=(6, 2), facecolor='#8D8DB9')
        labels = ['Anti eco kill', 'Anti force buy kill', 'Full buy kill']
        colors = ['#FF9999', '#66B2FF', '#99FF99']
        for i, ax in enumerate(axes):
            player_data = df_eco.iloc[i, 1:-1]  # On exclut la dernière colonne (Pistol round)
            ax.pie(player_data, autopct='%1.1f%%',pctdistance=1.5, startangle=90, colors=colors,textprops={'fontsize': 8})
            ax.set_title(df_eco['name'][i],fontsize=8,pad=15)
        fig.legend(labels=labels, loc='lower center', ncol=3,fontsize=8, facecolor='#8D8DB9',frameon=False)
        plt.tight_layout(rect=[0, 0.2, 1, 1])

        canvas4 = FigureCanvasTkAgg(fig, master=frame_eco)
        canvas4.draw()
        canvas4.get_tk_widget().config(bg="#8D8DB9", highlightthickness=0)
        canvas4.get_tk_widget().grid(row=1, column=0, sticky="nsew")

        # #affichage d'une table
        # values = [[1, 2, 3, 4],
        #   [5, 6, 7, 8],
        #   [9, 10, 11, 12],
        #   [13, 14, 15, 16]]

        # table = CTkTable(master=frame_right_top, row=6, column=17, values=values, width=50, height=30)
                # table.grid(row=2, column=0, columnspan=3,padx=20, pady=20, sticky="new")

       
        # frame_bot = ctk.CTkFrame(self,fg_color="#8D8DB9",corner_radius=20,)
        # frame_bot.grid(row=2, column=1, padx=(10,20), pady=(0,20), sticky="nsew")

        
if __name__ == "__main__":
    app = PlayerDetailPage()
    app.protocol("WM_DELETE_WINDOW", app.quit)
    app.mainloop()
