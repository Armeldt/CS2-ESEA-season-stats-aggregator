import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageOps, ImageDraw
from CTkTable import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from matplotlib.figure import Figure
import pandas as pd


def update_stacked_bar_chart_utils(parent, df_utils, row, column):
 # Création du stacked bar chart
        fig, ax = plt.subplots(figsize=(4, 3), facecolor='#292929')
        bars1 = ax.bar(df_utils['name'], df_utils['He_dmg'], label='He', color='#1a1a1a')
        bars2 = ax.bar(df_utils['name'], df_utils['Fire_dmg'], label='Fire', bottom=df_utils['He_dmg'], color='red')
        ax.bar_label(bars2, labels=df_utils['Total_utility_dmg'], label_type='edge',fontsize=8, fontweight='bold', color='white',padding=2)

        # Personnalisation des labels et de la légende
        ax.legend(loc="upper right", bbox_to_anchor=(1, 1.1), fontsize=8, facecolor='#212121',frameon=False)
        # ax.text(x=df_full['Total_utility_dmg'],ha='center', fontsize=10, fontweight='bold')
        ax.tick_params(axis='x', labelsize=8)
        ax.set_yticks([])
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        fig.patch.set_alpha(0)
        ax.patch.set_alpha(0)
    
        canvas1 = FigureCanvasTkAgg(fig, master=parent) 
        canvas1.draw() 
        canvas1.get_tk_widget().config(bg="#292929", highlightthickness=0) 
        canvas1.get_tk_widget().grid(row=row, column=column, sticky="nsew",pady=(0,5))

def update_bar_chart_flash(parent,df_utils, row, column):
    # Création du grouped bar chart
        fig, ax = plt.subplots(figsize=(4, 3), facecolor='#292929')
        width = 0.35  # Largeur des barres

        # Positions des barres pour chaque catégorie
        x = range(len(df_utils['name']))
        bars1 = ax.bar([pos - width / 2 for pos in x], df_utils['enemies_flashed_total'], width=width, label='Ennemy flashed', color='grey')
        bars2 = ax.bar([pos + width / 2 for pos in x], df_utils['Flash_assist'], width=width, label='Flash assist', color='orange')

        # Ajout des labels sur les barres
        ax.bar_label(bars1, labels=df_utils['enemies_flashed_total'], label_type='center', fontsize=8, fontweight='bold', color='white')
        ax.bar_label(bars2, labels=df_utils['Flash_assist'], label_type='center', fontsize=8, fontweight='bold', color='white')

        # Personnalisation des labels et de la légende
        ax.set_xticks(x)
        ax.set_xticklabels(df_utils['name'], fontsize=8)
        ax.legend(loc="upper right", bbox_to_anchor=(1, 1.1), fontsize=8, facecolor='#212121', labelcolor='white',frameon=False)
        ax.set_yticks([])
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        fig.patch.set_alpha(0)
        ax.patch.set_alpha(0)

        # Intégration dans Tkinter
        canvas2 = FigureCanvasTkAgg(fig, master=parent)
        canvas2.draw()
        canvas2.get_tk_widget().config(bg="#292929", highlightthickness=0)
        canvas2.get_tk_widget().grid(row=row, column=column, sticky="nsew",pady=(0,5))

def update_entry_chart(parent,df_entry,row,column):
        fig, ax = plt.subplots(figsize=(4, 3), facecolor='#292929')
        ax.scatter(df_entry['entry_attempts(T)'], df_entry['%_entry_success(T)'], color='#fbac18', label='Entry Success (T)')
        ax.scatter(df_entry['open_attempts(CT)'], df_entry['%_open_success(CT)'], color='#28397F', label='Open Success (CT)')
        for i, player in enumerate(df_entry['name']):
            ax.annotate(player, (df_entry['entry_attempts(T)'][i], df_entry['%_entry_success(T)'][i]), 
                        textcoords="offset points", xytext=(5,5), ha='center', color='#fbac18',fontsize=8)
            ax.annotate(player, (df_entry['open_attempts(CT)'][i], df_entry['%_open_success(CT)'][i]), 
                        textcoords="offset points", xytext=(5,5), ha='center', color='#28397F',fontsize=8)
        ax.set_ylim(0, 100)
        ax.set_xlabel('Attempts', fontsize=8)
        ax.set_ylabel('% Successes', fontsize=8)
        ax.tick_params(axis='x', labelsize=8)
        ax.tick_params(axis='y', labelsize=8)
        # ax.legend(loc="upper right", bbox_to_anchor=(1, 1.1), fontsize=8, facecolor='#212121', frameon=False)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        fig.patch.set_alpha(0)
        ax.patch.set_alpha(0)

        canvas3 = FigureCanvasTkAgg(fig, master=parent)
        canvas3.draw()
        canvas3.get_tk_widget().config(bg="#292929", highlightthickness=0)
        canvas3.get_tk_widget().grid(row=row, column=column, sticky="nsew",pady=(0,5))

class PlayerDetailPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent


        # configure grid layout for main window
        self.grid_columnconfigure(0, weight=1)  
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
      

        # ### FRAME PLAYER TILES ###
        frame_player_tiles = ctk.CTkFrame(self, fg_color='transparent')
        frame_player_tiles.grid(row=0, column=0,columnspan=5, sticky="nsew", pady=(20,10), padx=20)
        frame_player_tiles.grid_columnconfigure((0,1,2,3,4), weight=1)  
        frame_player_tiles.grid_rowconfigure(0, weight=1)

        #### RECAP JOUEUR 1 ####
        frame_joueur_1 = ctk.CTkFrame(frame_player_tiles,fg_color='#292929')
        frame_joueur_1.grid(row=0, column=0, padx=(0,10), sticky="nsew")
        frame_joueur_1.grid_columnconfigure((0,1), weight=1)
        frame_joueur_1.grid_rowconfigure((0,1,2,3,4), weight=1)

        self.label_player_name0 = ctk.CTkLabel(frame_joueur_1, text='Joueur 1', font=("Stratum2 Bd", 24), text_color='white')
        self.label_player_name0.grid(column=0,row=0,columnspan=2,sticky='')

        self.value_stats0_1 = ctk.CTkLabel(frame_joueur_1, text='', font=("Stratum2 Bd", 20), text_color='white')
        self.value_stats0_1.grid(column=0,row=1,sticky='nwe',pady=5,padx=20)

        label_stats1 = ctk.CTkLabel(frame_joueur_1, text='Rating', font=("Montserrat", 14), text_color='white')
        label_stats1.grid(column=0,row=1,sticky='swe',pady=5,padx=20)


        self.value_stats0_1_1 = ctk.CTkLabel(frame_joueur_1, text='', font=("Stratum2 Bd", 20), text_color='white')
        self.value_stats0_1_1.grid(column=1,row=1,sticky='nwe',pady=5,padx=20)

        label_stats0_1 = ctk.CTkLabel(frame_joueur_1, text='Impact', font=("Montserrat", 14), text_color='white')
        label_stats0_1.grid(column=1,row=1,sticky='swe',pady=5,padx=20)


        self.value_stats0_2 = ctk.CTkLabel(frame_joueur_1, text='', font=("Stratum2 Bd", 20), text_color='white')
        self.value_stats0_2.grid(column=0,row=2,sticky='nwe',pady=5,padx=20)

        label_stats2 = ctk.CTkLabel(frame_joueur_1, text='ADR',  font=("Montserrat", 14), text_color='white')
        label_stats2.grid(column=0,row=2,sticky='swe',pady=5,padx=20)


        self.value_stats0_2_2 = ctk.CTkLabel(frame_joueur_1, text='', font=("Stratum2 Bd", 20), text_color='white')
        self.value_stats0_2_2.grid(column=1,row=2,sticky='nwe',pady=5,padx=20)

        label_stats0_2 = ctk.CTkLabel(frame_joueur_1, text='KAST%',  font=("Montserrat", 14), text_color='white')
        label_stats0_2.grid(column=1,row=2,sticky='swe',pady=5,padx=20)
        

        self.value_stats0_3 = ctk.CTkLabel(frame_joueur_1, text='', font=("Stratum2 Bd", 20), text_color='white')
        self.value_stats0_3.grid(column=0,row=3,sticky='nwe',pady=5,padx=20)
        
        label_stats3 = ctk.CTkLabel(frame_joueur_1, text='KPR',  font=("Montserrat", 14), text_color='white')
        label_stats3.grid(column=0,row=3,sticky='swe',pady=5,padx=20)


        self.value_stats0_3_3 = ctk.CTkLabel(frame_joueur_1, text='', font=("Stratum2 Bd", 20), text_color='white')
        self.value_stats0_3_3.grid(column=1,row=3,sticky='nwe',pady=5,padx=20)

        label_stats3_3 = ctk.CTkLabel(frame_joueur_1, text='DPR',  font=("Montserrat", 14), text_color='white')
        label_stats3_3.grid(column=1,row=3,sticky='swe',pady=5,padx=20)

        #### FRAME JOUEUR 2 ####
        frame_joueur_2 = ctk.CTkFrame(frame_player_tiles,fg_color='#292929')
        frame_joueur_2.grid(row=0, column=1, padx=(10,10), sticky="nsew")
        frame_joueur_2.grid_columnconfigure((0,1), weight=1)  
        frame_joueur_2.grid_rowconfigure((0,1,2,3,4), weight=1)

        self.label_player_name1 = ctk.CTkLabel(frame_joueur_2, text='Joueur 2', font=("Stratum2 Bd", 24), text_color='white')
        self.label_player_name1.grid(column=0,row=0,columnspan=2,sticky='')

        self.value_stats1_1 = ctk.CTkLabel(frame_joueur_2, text='', font=("Stratum2 Bd", 20), text_color='white')
        self.value_stats1_1.grid(column=0,row=1,sticky='nwe',pady=5,padx=20)

        label_stats1 = ctk.CTkLabel(frame_joueur_2, text='Rating', font=("Montserrat", 14), text_color='white')
        label_stats1.grid(column=0,row=1,sticky='swe',pady=5,padx=20)


        self.value_stats1_1_1 = ctk.CTkLabel(frame_joueur_2, text='', font=("Stratum2 Bd", 20), text_color='white')
        self.value_stats1_1_1.grid(column=1,row=1,sticky='nwe',pady=5,padx=20)

        label_stats1_1 = ctk.CTkLabel(frame_joueur_2, text='Impact', font=("Montserrat", 14), text_color='white')
        label_stats1_1.grid(column=1,row=1,sticky='swe',pady=5,padx=20)


        self.value_stats1_2 = ctk.CTkLabel(frame_joueur_2, text='', font=("Stratum2 Bd", 20), text_color='white')
        self.value_stats1_2.grid(column=0,row=2,sticky='nwe',pady=5,padx=20)

        label_stats2 = ctk.CTkLabel(frame_joueur_2, text='ADR',  font=("Montserrat", 14), text_color='white')
        label_stats2.grid(column=0,row=2,sticky='swe',pady=5,padx=20)


        self.value_stats1_2_2 = ctk.CTkLabel(frame_joueur_2, text='', font=("Stratum2 Bd", 20), text_color='white')
        self.value_stats1_2_2.grid(column=1,row=2,sticky='nwe',pady=5,padx=20)

        label_stats2_2 = ctk.CTkLabel(frame_joueur_2, text='KAST%',  font=("Montserrat", 14), text_color='white')
        label_stats2_2.grid(column=1,row=2,sticky='swe',pady=5,padx=20)
        

        self.value_stats1_3 = ctk.CTkLabel(frame_joueur_2, text='', font=("Stratum2 Bd", 20), text_color='white')
        self.value_stats1_3.grid(column=0,row=3,sticky='nwe',pady=5,padx=20)
        
        label_stats3 = ctk.CTkLabel(frame_joueur_2, text='KPR',  font=("Montserrat", 14), text_color='white')
        label_stats3.grid(column=0,row=3,sticky='swe',pady=5,padx=20)


        self.value_stats1_3_3 = ctk.CTkLabel(frame_joueur_2, text='', font=("Stratum2 Bd", 20), text_color='white')
        self.value_stats1_3_3.grid(column=1,row=3,sticky='nwe',pady=5,padx=20)

        label_stats3_3 = ctk.CTkLabel(frame_joueur_2, text='DPR',  font=("Montserrat", 14), text_color='white')
        label_stats3_3.grid(column=1,row=3,sticky='swe',pady=5,padx=20)

        #### Joueur 3 ####
        frame_joueur_3 = ctk.CTkFrame(frame_player_tiles,fg_color='#292929')
        frame_joueur_3.grid(row=0, column=2, padx=(10,10), sticky="nsew")
        frame_joueur_3.grid_columnconfigure((0,1), weight=1)  
        frame_joueur_3.grid_rowconfigure((0,1,2,3,4), weight=1)

        self.label_player_name2 = ctk.CTkLabel(frame_joueur_3, text='Joueur 4', font=("Stratum2 Bd", 24), text_color='white')
        self.label_player_name2.grid(column=0,row=0,columnspan=2,sticky='')

        self.value_stats2_1 = ctk.CTkLabel(frame_joueur_3, text='', font=("Stratum2 Bd", 20), text_color='white')
        self.value_stats2_1.grid(column=0,row=1,sticky='nwe',pady=5,padx=20)

        label_stats1 = ctk.CTkLabel(frame_joueur_3, text='Rating', font=("Montserrat", 14), text_color='white')
        label_stats1.grid(column=0,row=1,sticky='swe',pady=5,padx=20)


        self.value_stats2_1_1 = ctk.CTkLabel(frame_joueur_3, text='', font=("Stratum2 Bd", 20), text_color='white')
        self.value_stats2_1_1.grid(column=1,row=1,sticky='nwe',pady=5,padx=20)

        label_stats1_1 = ctk.CTkLabel(frame_joueur_3, text='Impact', font=("Montserrat", 14), text_color='white')
        label_stats1_1.grid(column=1,row=1,sticky='swe',pady=5,padx=20)


        self.value_stats2_2 = ctk.CTkLabel(frame_joueur_3, text='', font=("Stratum2 Bd", 20), text_color='white')
        self.value_stats2_2.grid(column=0,row=2,sticky='nwe',pady=5,padx=20)

        label_stats2 = ctk.CTkLabel(frame_joueur_3, text='ADR',  font=("Montserrat", 14), text_color='white')
        label_stats2.grid(column=0,row=2,sticky='swe',pady=5,padx=20)


        self.value_stats2_2_2 = ctk.CTkLabel(frame_joueur_3, text='', font=("Stratum2 Bd", 20), text_color='white')
        self.value_stats2_2_2.grid(column=1,row=2,sticky='nwe',pady=5,padx=20)

        label_stats2_2 = ctk.CTkLabel(frame_joueur_3, text='KAST%',  font=("Montserrat", 14), text_color='white')
        label_stats2_2.grid(column=1,row=2,sticky='swe',pady=5,padx=20)
        

        self.value_stats2_3 = ctk.CTkLabel(frame_joueur_3, text='', font=("Stratum2 Bd", 20), text_color='white')
        self.value_stats2_3.grid(column=0,row=3,sticky='nwe',pady=5,padx=20)
        
        label_stats3 = ctk.CTkLabel(frame_joueur_3, text='KPR',  font=("Montserrat", 14), text_color='white')
        label_stats3.grid(column=0,row=3,sticky='swe',pady=5,padx=20)


        self.value_stats2_3_3 = ctk.CTkLabel(frame_joueur_3, text='', font=("Stratum2 Bd", 20), text_color='white')
        self.value_stats2_3_3.grid(column=1,row=3,sticky='nwe',pady=5,padx=20)

        label_stats3_3 = ctk.CTkLabel(frame_joueur_3, text='DPR',  font=("Montserrat", 14), text_color='white')
        label_stats3_3.grid(column=1,row=3,sticky='swe',pady=5,padx=20)
        

        #### Joueur 4 ####

        frame_joueur_4 = ctk.CTkFrame(frame_player_tiles,fg_color='#292929')
        frame_joueur_4.grid(row=0, column=3, padx=(10,10), sticky="nsew")
        frame_joueur_4.grid_columnconfigure((0,1), weight=1)  
        frame_joueur_4.grid_rowconfigure((0,1,2,3,4), weight=1)

        self.label_player_name3 = ctk.CTkLabel(frame_joueur_4, text='Joueur 4', font=("Stratum2 Bd", 24), text_color='white')
        self.label_player_name3.grid(column=0,row=0,columnspan=2,sticky='')

        self.value_stats3_1 = ctk.CTkLabel(frame_joueur_4, text='', font=("Stratum2 Bd", 20), text_color='white')
        self.value_stats3_1.grid(column=0,row=1,sticky='nwe',pady=5,padx=20)

        label_stats1 = ctk.CTkLabel(frame_joueur_4, text='Rating', font=("Montserrat", 14), text_color='white')
        label_stats1.grid(column=0,row=1,sticky='swe',pady=5,padx=20)


        self.value_stats3_1_1 = ctk.CTkLabel(frame_joueur_4, text='', font=("Stratum2 Bd", 20), text_color='white')
        self.value_stats3_1_1.grid(column=1,row=1,sticky='nwe',pady=5,padx=20)

        label_stats1_1 = ctk.CTkLabel(frame_joueur_4, text='Impact', font=("Montserrat", 14), text_color='white')
        label_stats1_1.grid(column=1,row=1,sticky='swe',pady=5,padx=20)


        self.value_stats3_2 = ctk.CTkLabel(frame_joueur_4, text='', font=("Stratum2 Bd", 20), text_color='white')
        self.value_stats3_2.grid(column=0,row=2,sticky='nwe',pady=5,padx=20)

        label_stats2 = ctk.CTkLabel(frame_joueur_4, text='ADR',  font=("Montserrat", 14), text_color='white')
        label_stats2.grid(column=0,row=2,sticky='swe',pady=5,padx=20)


        self.value_stats3_2_2 = ctk.CTkLabel(frame_joueur_4, text='', font=("Stratum2 Bd", 20), text_color='white')
        self.value_stats3_2_2.grid(column=1,row=2,sticky='nwe',pady=5,padx=20)

        label_stats2_2 = ctk.CTkLabel(frame_joueur_4, text='KAST%',  font=("Montserrat", 14), text_color='white')
        label_stats2_2.grid(column=1,row=2,sticky='swe',pady=5,padx=20)
        

        self.value_stats3_3 = ctk.CTkLabel(frame_joueur_4, text='', font=("Stratum2 Bd", 20), text_color='white')
        self.value_stats3_3.grid(column=0,row=3,sticky='nwe',pady=5,padx=20)
        
        label_stats3 = ctk.CTkLabel(frame_joueur_4, text='KPR',  font=("Montserrat", 14), text_color='white')
        label_stats3.grid(column=0,row=3,sticky='swe',pady=5,padx=20)


        self.value_stats3_3_3 = ctk.CTkLabel(frame_joueur_4, text='', font=("Stratum2 Bd", 20), text_color='white')
        self.value_stats3_3_3.grid(column=1,row=3,sticky='nwe',pady=5,padx=20)

        label_stats3_3 = ctk.CTkLabel(frame_joueur_4, text='DPR',  font=("Montserrat", 14), text_color='white')
        label_stats3_3.grid(column=1,row=3,sticky='swe',pady=5,padx=20)

        #### Joueur 5 ####

        frame_joueur_5 = ctk.CTkFrame(frame_player_tiles,fg_color='#292929')
        frame_joueur_5.grid(row=0, column=4, padx=(10,0), sticky="nsew")
        frame_joueur_5.grid_columnconfigure((0,1), weight=1)  
        frame_joueur_5.grid_rowconfigure((0,1,2,3,4), weight=1)

        self.label_player_name4 = ctk.CTkLabel(frame_joueur_5, text='Joueur 5', font=("Stratum2 Bd", 24), text_color='white')
        self.label_player_name4.grid(column=0,row=0,columnspan=2,sticky='')

        self.value_stats4_1 = ctk.CTkLabel(frame_joueur_5, text='', font=("Stratum2 Bd", 20), text_color='white')
        self.value_stats4_1.grid(column=0,row=1,sticky='nwe',pady=5,padx=20)

        label_stats1 = ctk.CTkLabel(frame_joueur_5, text='Rating', font=("Montserrat", 14), text_color='white')
        label_stats1.grid(column=0,row=1,sticky='swe',pady=5,padx=20)


        self.value_stats4_1_1 = ctk.CTkLabel(frame_joueur_5, text='', font=("Stratum2 Bd", 20), text_color='white')
        self.value_stats4_1_1.grid(column=1,row=1,sticky='nwe',pady=5,padx=20)

        label_stats1_1 = ctk.CTkLabel(frame_joueur_5, text='Impact', font=("Montserrat", 14), text_color='white')
        label_stats1_1.grid(column=1,row=1,sticky='swe',pady=5,padx=20)


        self.value_stats4_2 = ctk.CTkLabel(frame_joueur_5, text='', font=("Stratum2 Bd", 20), text_color='white')
        self.value_stats4_2.grid(column=0,row=2,sticky='nwe',pady=5,padx=20)

        label_stats2 = ctk.CTkLabel(frame_joueur_5, text='ADR',  font=("Montserrat", 14), text_color='white')
        label_stats2.grid(column=0,row=2,sticky='swe',pady=5,padx=20)


        self.value_stats4_2_2 = ctk.CTkLabel(frame_joueur_5, text='', font=("Stratum2 Bd", 20), text_color='white')
        self.value_stats4_2_2.grid(column=1,row=2,sticky='nwe',pady=5,padx=20)

        label_stats2_2 = ctk.CTkLabel(frame_joueur_5, text='KAST%',  font=("Montserrat", 14), text_color='white')
        label_stats2_2.grid(column=1,row=2,sticky='swe',pady=5,padx=20)
        

        self.value_stats4_3 = ctk.CTkLabel(frame_joueur_5, text='', font=("Stratum2 Bd", 20), text_color='white')
        self.value_stats4_3.grid(column=0,row=3,sticky='nwe',pady=5,padx=20)
        
        label_stats3 = ctk.CTkLabel(frame_joueur_5, text='KPR',  font=("Montserrat", 14), text_color='white')
        label_stats3.grid(column=0,row=3,sticky='swe',pady=5,padx=20)


        self.value_stats4_3_3 = ctk.CTkLabel(frame_joueur_5, text='', font=("Stratum2 Bd", 20), text_color='white')
        self.value_stats4_3_3.grid(column=1,row=3,sticky='nwe',pady=5,padx=20)

        label_stats3_3 = ctk.CTkLabel(frame_joueur_5, text='DPR',  font=("Montserrat", 14), text_color='white')
        label_stats3_3.grid(column=1,row=3,sticky='swe',pady=5,padx=20)


        ### FRAME BOTTOM ###
        frame_bottom = ctk.CTkFrame(self,corner_radius=20,fg_color='transparent')
        frame_bottom.grid(row=1, column=0, pady=(10,20),columnspan=5, padx=20, sticky="nsew")
        frame_bottom.grid_columnconfigure((0,1,2), weight=1)  
        frame_bottom.grid_rowconfigure(0, weight=1)
        
        ### FRAME utils ###
        self.frame_utils = ctk.CTkFrame(frame_bottom,fg_color="#292929")
        self.frame_utils.grid(row=0, column=0, padx=(0,10), sticky="nesw")
        self.frame_utils.grid_columnconfigure(0, weight=1)  
        self.frame_utils.grid_rowconfigure(0, weight=1)
        self.frame_utils.grid_rowconfigure(1, weight=3)
        label_utils = ctk.CTkLabel(self.frame_utils, text='Utility damage', font=("Stratum2 Bd", 20), text_color='white')
        label_utils.grid(row=0,column=0, sticky='')
      
        ### FRAME flash ###
        
        self.frame_flash = ctk.CTkFrame(frame_bottom,fg_color="#292929")
        self.frame_flash.grid(row=0, column=1, padx=(10,10), sticky="nsew")
        self.frame_flash.grid_columnconfigure(0, weight=1)  
        self.frame_flash.grid_rowconfigure(0, weight=1)
        self.frame_flash.grid_rowconfigure(1, weight=3)
        label_utils = ctk.CTkLabel(self.frame_flash, text='Flash efficiency', font=("Stratum2 Bd", 20), text_color='white')
        label_utils.grid(row=0,column=0, sticky='')

        ### FRAME entry ###
        self.frame_entry = ctk.CTkFrame(frame_bottom,fg_color="#292929")
        self.frame_entry.grid(row=0, column=2, padx=(10,0), sticky="nsew")
        self.frame_entry.grid_columnconfigure(0, weight=1)  
        self.frame_entry.grid_rowconfigure(0, weight=1)
        self.frame_entry.grid_rowconfigure(1, weight=3)
        label_utils = ctk.CTkLabel(self.frame_entry, text='Entry and Open frags', font=("Stratum2 Bd", 20), text_color='white')
        label_utils.grid(row=0,column=0, sticky='')

        
        
        
    def update_data(self, analysis_results):
        print("update_data called with analysis_results:", analysis_results)
        if analysis_results:
            #Chargement des données
            scoreboard = analysis_results.get("scoreboard", pd.DataFrame())
            df_utils = analysis_results.get("util_stats", pd.DataFrame())
            df_entry = analysis_results.get("entry_stats", pd.DataFrame())
            print("c'est le df utils",df_utils)
            #affichage des données sur la page
            self.label_player_name0.configure(text=str(scoreboard.iloc[0]['name']))
            self.value_stats0_1.configure(text=scoreboard.iloc[0]['Rating'])
            self.value_stats0_1_1.configure(text=scoreboard.iloc[0]['Impact'])
            self.value_stats0_2.configure(text=scoreboard.iloc[0]['ADR'])
            self.value_stats0_2_2.configure(text=scoreboard.iloc[0]['KAST%'])
            self.value_stats0_3.configure(text=scoreboard.iloc[0]['KPR'])
            self.value_stats0_3_3.configure(text=scoreboard.iloc[0]['DPR'])

            #affichage des données sur la page
            self.label_player_name1.configure(text=str(scoreboard.iloc[1]['name']))
            self.value_stats1_1.configure(text=scoreboard.iloc[1]['Rating'])
            self.value_stats1_1_1.configure(text=scoreboard.iloc[1]['Impact'])
            self.value_stats1_2.configure(text=scoreboard.iloc[1]['ADR'])
            self.value_stats1_2_2.configure(text=scoreboard.iloc[1]['KAST%'])
            self.value_stats1_3.configure(text=scoreboard.iloc[1]['KPR'])
            self.value_stats1_3_3.configure(text=scoreboard.iloc[1]['DPR'])

            #affichage des données sur la page
            self.label_player_name2.configure(text=str(scoreboard.iloc[2]['name']))
            self.value_stats2_1.configure(text=scoreboard.iloc[2]['Rating'])
            self.value_stats2_1_1.configure(text=scoreboard.iloc[2]['Impact'])
            self.value_stats2_2.configure(text=scoreboard.iloc[2]['ADR'])
            self.value_stats2_2_2.configure(text=scoreboard.iloc[2]['KAST%'])
            self.value_stats2_3.configure(text=scoreboard.iloc[2]['KPR'])
            self.value_stats2_3_3.configure(text=scoreboard.iloc[2]['DPR'])

            #affichage des données sur la page
            self.label_player_name3.configure(text=str(scoreboard.iloc[3]['name']))
            self.value_stats3_1.configure(text=scoreboard.iloc[3]['Rating'])
            self.value_stats3_1_1.configure(text=scoreboard.iloc[3]['Impact'])
            self.value_stats3_2.configure(text=scoreboard.iloc[3]['ADR'])
            self.value_stats3_2_2.configure(text=scoreboard.iloc[3]['KAST%'])
            self.value_stats3_3.configure(text=scoreboard.iloc[3]['KPR'])
            self.value_stats3_3_3.configure(text=scoreboard.iloc[3]['DPR'])

            #affichage des données sur la page
            self.label_player_name4.configure(text=str(scoreboard.iloc[4]['name']))
            self.value_stats4_1.configure(text=scoreboard.iloc[4]['Rating'])
            self.value_stats4_1_1.configure(text=scoreboard.iloc[4]['Impact'])
            self.value_stats4_2.configure(text=scoreboard.iloc[4]['ADR'])
            self.value_stats4_2_2.configure(text=scoreboard.iloc[4]['KAST%'])
            self.value_stats4_3.configure(text=scoreboard.iloc[4]['KPR'])
            self.value_stats4_3_3.configure(text=scoreboard.iloc[4]['DPR'])

            # Supposons que `self.frame_utils` est le frame où vous souhaitez afficher le graphique.
            update_stacked_bar_chart_utils(self.frame_utils, df_utils, 1,0)
            update_bar_chart_flash(self.frame_flash,df_utils,1,0)
            update_entry_chart(self.frame_entry,df_entry,1,0)
                
if __name__ == "__main__":
    app = PlayerDetailPage()
    app.protocol("WM_DELETE_WINDOW", app.quit)
    app.mainloop()
