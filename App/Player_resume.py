import customtkinter as ctk
from CTkTable import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from PIL import Image, ImageDraw, ImageOps
import os
import sys
import random

def round_corners_top(image, radius, background_color=(41, 41, 41)):
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

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        # Mode exécutable : PyInstaller extrait les fichiers dans _MEIPASS
        return os.path.join(sys._MEIPASS, relative_path)
    # Mode script Python
    return os.path.join(os.path.abspath("."), relative_path)

agent1 = resource_path('Assets/ava.png')
agent2= resource_path('Assets/shahmat.png')
agent3 = resource_path('Assets/osiris.png')
agent4 = resource_path('Assets/syfers.png')
agent5 = resource_path('Assets/blackwolf.png')
agent6 = resource_path('Assets/slingshot.png')
agent7 = resource_path('Assets/daco.png')
agent8 = resource_path('Assets/noidea.png')
agent_set = {agent1, agent2, agent3, agent4, agent5,agent6,agent7,agent8}

ancient_img = resource_path('Assets/ancient.png')
mirage_img = resource_path('Assets/mirage.png')
inferno_img = resource_path('Assets/inferno.png')
nuke_img = resource_path('Assets/nuke.png')
dust2_img = resource_path('Assets/dust2.jpg')
vertigo_img = resource_path('Assets/vertigo.png')
anubis_img = resource_path('Assets/anubis.png')


# def update_stacked_bar_chart_utils(parent, df_utils, row, column):
#  # Création du stacked bar chart
#         fig, ax = plt.subplots(figsize=(4, 3), facecolor='#292929')
#         bars1 = ax.bar(df_utils['name'], df_utils['He_dmg'], label='He', color='#1a1a1a')
#         bars2 = ax.bar(df_utils['name'], df_utils['Fire_dmg'], label='Fire', bottom=df_utils['He_dmg'], color='red')
#         ax.bar_label(bars2, labels=df_utils['Total_utility_dmg'], label_type='edge',fontsize=8, fontweight='bold', color='white',padding=2)

#         # Personnalisation des labels et de la légende
#         ax.legend(loc="upper right", bbox_to_anchor=(1, 1.1), fontsize=8, facecolor='#212121',frameon=False)
#         # ax.text(x=df_full['Total_utility_dmg'],ha='center', fontsize=10, fontweight='bold')
#         ax.tick_params(axis='x', labelsize=8)
#         ax.set_yticks([])
#         ax.spines['top'].set_visible(False)
#         ax.spines['right'].set_visible(False)
#         ax.spines['left'].set_visible(False)
#         fig.patch.set_alpha(0)
#         ax.patch.set_alpha(0)
    
#         canvas1 = FigureCanvasTkAgg(fig, master=parent) 
#         canvas1.draw() 
#         canvas1.get_tk_widget().config(bg="#292929", highlightthickness=0) 
#         canvas1.get_tk_widget().grid(row=row, column=column, sticky="nsew",pady=(0,5))

# def update_bar_chart_flash(parent,df_utils, row, column):
#     # Création du grouped bar chart
#         fig, ax = plt.subplots(figsize=(4, 3), facecolor='#292929')
#         width = 0.35  # Largeur des barres

#         # Positions des barres pour chaque catégorie
#         x = range(len(df_utils['name']))
#         bars1 = ax.bar([pos - width / 2 for pos in x], df_utils['enemies_flashed_total'], width=width, label='Ennemy flashed', color='grey')
#         bars2 = ax.bar([pos + width / 2 for pos in x], df_utils['Flash_assist'], width=width, label='Flash assist', color='orange')

#         # Ajout des labels sur les barres
#         ax.bar_label(bars1, labels=df_utils['enemies_flashed_total'], label_type='center', fontsize=8, fontweight='bold', color='white')
#         ax.bar_label(bars2, labels=df_utils['Flash_assist'], label_type='center', fontsize=8, fontweight='bold', color='white')

#         # Personnalisation des labels et de la légende
#         ax.set_xticks(x)
#         ax.set_xticklabels(df_utils['name'], fontsize=8)
#         ax.legend(loc="upper right", bbox_to_anchor=(1, 1.1), fontsize=8, facecolor='#212121', labelcolor='white',frameon=False)
#         ax.set_yticks([])
#         ax.spines['top'].set_visible(False)
#         ax.spines['right'].set_visible(False)
#         ax.spines['left'].set_visible(False)
#         fig.patch.set_alpha(0)
#         ax.patch.set_alpha(0)

#         # Intégration dans Tkinter
#         canvas2 = FigureCanvasTkAgg(fig, master=parent)
#         canvas2.draw()
#         canvas2.get_tk_widget().config(bg="#292929", highlightthickness=0)
#         canvas2.get_tk_widget().grid(row=row, column=column, sticky="nsew",pady=(0,5))

# def update_entry_chart(parent,df_entry,row,column):
#         fig, ax = plt.subplots(figsize=(4, 3), facecolor='#292929')
#         ax.scatter(df_entry['entry_attempts(T)'], df_entry['%_entry_success(T)'], color='#fbac18', label='Entry Success (T)')
#         ax.scatter(df_entry['open_attempts(CT)'], df_entry['%_open_success(CT)'], color='#28397F', label='Open Success (CT)')
#         for i, player in enumerate(df_entry['name']):
#             ax.annotate(player, (df_entry['entry_attempts(T)'][i], df_entry['%_entry_success(T)'][i]), 
#                         textcoords="offset points", xytext=(5,5), ha='center', color='#fbac18',fontsize=8)
#             ax.annotate(player, (df_entry['open_attempts(CT)'][i], df_entry['%_open_success(CT)'][i]), 
#                         textcoords="offset points", xytext=(5,5), ha='center', color='#28397F',fontsize=8)
#         ax.set_ylim(0, 100)
#         ax.set_xlabel('Attempts', fontsize=8)
#         ax.set_ylabel('% Successes', fontsize=8)
#         ax.tick_params(axis='x', labelsize=8)
#         ax.tick_params(axis='y', labelsize=8)
#         # ax.legend(loc="upper right", bbox_to_anchor=(1, 1.1), fontsize=8, facecolor='#212121', frameon=False)
#         ax.spines['top'].set_visible(False)
#         ax.spines['right'].set_visible(False)
#         fig.patch.set_alpha(0)
#         ax.patch.set_alpha(0)

#         canvas3 = FigureCanvasTkAgg(fig, master=parent)
#         canvas3.draw()
#         canvas3.get_tk_widget().config(bg="#292929", highlightthickness=0)
#         canvas3.get_tk_widget().grid(row=row, column=column, sticky="nsew",pady=(0,5))

class PlayerResumePage(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("1600x900")
        # configure grid layout for main window
        self.grid_columnconfigure((0,1,2), weight=1)  
        self.grid_rowconfigure((0,1,2,3,4,5), weight=1)

        self.label_player_name = ctk.CTkLabel(self, text='Joueur 1', font=("Stratum2 Bd", 50), text_color='white')
        self.label_player_name.grid(column=1,row=0,sticky='nsew')

        target_size = (300, 531)  # Dimensions finales
        self.visuel = ctk.CTkImage(dark_image=Image.open(random.choice(tuple(agent_set))), size=target_size)
    
        self.label_agent = ctk.CTkLabel(self, text="", image=self.visuel)
        self.label_agent.grid(column=1,row=1, rowspan=4,sticky='new')

        self.frame_rating = ctk.CTkFrame(self)
        self.frame_rating.grid(column=0,row=1,sticky='nwe',pady=5,padx=20)

        self.value_rating = ctk.CTkLabel(self.frame_rating, text='1.15', font=("Stratum2 Bd", 20), text_color='white')
        self.value_rating.pack(side='top')

        self.label_rating = ctk.CTkLabel(self.frame_rating, text='Rating', font=("Montserrat", 14), text_color='white')
        self.label_rating.pack(side='bottom')

        self.frame_impact = ctk.CTkFrame(self)
        self.frame_impact.grid(column=2,row=1,sticky='nwe',pady=5,padx=20)

        self.value_impact = ctk.CTkLabel(self.frame_impact, text='1.20', font=("Stratum2 Bd", 20), text_color='white')
        self.value_impact.pack(side='top')

        label_impact = ctk.CTkLabel(self.frame_impact, text='Impact', font=("Montserrat", 14), text_color='white')
        label_impact.pack(side='bottom')

        self.frame_ADR = ctk.CTkFrame(self)
        self.frame_ADR.grid(column=0,row=2,sticky='nwe',pady=5,padx=20)

        self.value_ADR = ctk.CTkLabel(self.frame_ADR, text='105', font=("Stratum2 Bd", 20), text_color='white')
        self.value_ADR.pack(side='top')

        self.label_ADR = ctk.CTkLabel(self.frame_ADR, text='ADR',  font=("Montserrat", 14), text_color='white')
        self.label_ADR.pack(side='bottom')

        self.frame_KAST= ctk.CTkFrame(self)
        self.frame_KAST.grid(column=2,row=2,sticky='nwe',pady=5,padx=20)

        self.value_KAST = ctk.CTkLabel(self.frame_KAST, text='83%', font=("Stratum2 Bd", 20), text_color='white')
        self.value_KAST.pack(side='top')

        label_KAST = ctk.CTkLabel(self.frame_KAST, text='KAST%',  font=("Montserrat", 14), text_color='white')
        label_KAST.pack(side='bottom')
        
        self.frame_KPR= ctk.CTkFrame(self)
        self.frame_KPR.grid(column=0,row=3,sticky='nwe',pady=5,padx=20)

        self.value_KPR = ctk.CTkLabel(self.frame_KPR, text='1.1', font=("Stratum2 Bd", 20), text_color='white')
        self.value_KPR.pack(side='top')
        
        label_KPR = ctk.CTkLabel(self.frame_KPR, text='KPR',  font=("Montserrat", 14), text_color='white')
        label_KPR.pack(side='bottom')

        self.frame_DPR= ctk.CTkFrame(self)
        self.frame_DPR.grid(column=2,row=3,sticky='nwe',pady=5,padx=20)

        self.value_DPR = ctk.CTkLabel(self.frame_DPR, text='0.68', font=("Stratum2 Bd", 20), text_color='white')
        self.value_DPR.pack(side='top')

        label_DPR = ctk.CTkLabel(self.frame_DPR, text='DPR',  font=("Montserrat", 14), text_color='white')
        label_DPR.pack(side='bottom')

        self.frame_entry= ctk.CTkFrame(self)
        self.frame_entry.grid(column=0,row=4,sticky='nwe',pady=5,padx=20)

        label_entry = ctk.CTkLabel(self.frame_entry, text='Playstyle',  font=("Stratum2 Bd", 20), text_color='white')
        label_entry.pack(side='top')

        self.value_entry = ctk.CTkLabel(self.frame_entry, text='Agressive', font=("Stratum2 Bd", 16), text_color='white')
        self.value_entry.pack()

        self.value_entry = ctk.CTkLabel(self.frame_entry, text="Took 50% of opening duels within the team", font=("Montserrat", 14), text_color='white')
        self.value_entry.pack(side='bottom')

        self.frame_weapons= ctk.CTkFrame(self)
        self.frame_weapons.grid(column=2,row=4,sticky='nwe',pady=5,padx=20)

        self.value_weapons = ctk.CTkLabel(self.frame_weapons, text='Most used weapon', font=("Stratum2 Bd", 20), text_color='white')
        self.value_weapons.pack(side='top')

        label_weapons = ctk.CTkLabel(self.frame_weapons, text='AK47 : 580 frags / 1.13 K/D \n M4A1S : 512 frags / 1.08 K/D',  font=("Montserrat", 14), text_color='white')
        label_weapons.pack(side='bottom')

        self.frame_Bestmaps= ctk.CTkFrame(self)
        self.frame_Bestmaps.grid(column=0, columnspan=3,row=5,sticky='sew',pady=5,padx=20)
        self.frame_Bestmaps.grid_columnconfigure((0,1,2), weight=1)
        self.frame_Bestmaps.grid_rowconfigure((0,1),weight=1)

        self.frame_title= ctk.CTkLabel(self.frame_Bestmaps, text=' Best Maps',font=("Stratum2 Bd", 20),text_color='white')
        self.frame_title.grid(column=0, columnspan=3,row=0,sticky='nsew',pady=5,padx=20)

        target_size_map = (300, 150)  # Dimensions finales
        self.ancient_img = ctk.CTkImage(dark_image=round_corners_top(Image.open(ancient_img),15), size=target_size_map)
        self.mirage_img = ctk.CTkImage(dark_image=round_corners_top(Image.open(mirage_img),15), size=target_size_map)
        self.nuke_img = ctk.CTkImage(dark_image=round_corners_top(Image.open(nuke_img),15), size=target_size_map)
        self.dust2_img = ctk.CTkImage(dark_image=round_corners_top(Image.open(dust2_img),15), size=target_size_map)
        self.anubis_img = ctk.CTkImage(dark_image=round_corners_top(Image.open(anubis_img),15), size=target_size_map)
        self.vertigo_img = ctk.CTkImage(dark_image=round_corners_top(Image.open(vertigo_img),15), size=target_size_map)
        self.inferno_img = ctk.CTkImage(dark_image=round_corners_top(Image.open(inferno_img),15), size=target_size_map)

        self.frame_Map1_img= ctk.CTkLabel(self.frame_Bestmaps,text='ADR : 112', justify='left',anchor='s',font=("Stratum2 Bd", 20),text_color='white',image=self.ancient_img)
        self.frame_Map1_img.grid(column=0,row=1,sticky='nsew',pady=5,padx=20)

        self.frame_Map2= ctk.CTkLabel(self.frame_Bestmaps, text='ADR : 108',font=("Stratum2 Bd", 20),text_color='white',image=self.mirage_img)
        self.frame_Map2.grid(column=1,row=1,sticky='nsew',pady=5,padx=20)

        self.frame_Map3= ctk.CTkLabel(self.frame_Bestmaps, text='ADR : 102',font=("Stratum2 Bd", 20),text_color='white',image=self.dust2_img)
        self.frame_Map3.grid(column=2,row=1,sticky='nsew',pady=5,padx=20)

        
    # def update_data(self, analysis_results):
    #     print("update_data called with analysis_results:", analysis_results)
    #     if analysis_results:
    #         #Chargement des données
    #         scoreboard = analysis_results.get("scoreboard", pd.DataFrame())
    #         df_utils = analysis_results.get("util_stats", pd.DataFrame())
    #         df_entry = analysis_results.get("entry_stats", pd.DataFrame())
    #         print("c'est le df utils",df_utils)
    #         #affichage des données sur la page
    #         self.label_player_name0.configure(text=str(scoreboard.iloc[0]['name']))
    #         self.value_stats0_1.configure(text=scoreboard.iloc[0]['Rating'])
    #         self.value_stats0_1_1.configure(text=scoreboard.iloc[0]['Impact'])
    #         self.value_stats0_2.configure(text=scoreboard.iloc[0]['ADR'])
    #         self.value_stats0_2_2.configure(text=scoreboard.iloc[0]['KAST%'])
    #         self.value_stats0_3.configure(text=scoreboard.iloc[0]['KPR'])
    #         self.value_stats0_3_3.configure(text=scoreboard.iloc[0]['DPR'])

    #         #affichage des données sur la page
    #         self.label_player_name1.configure(text=str(scoreboard.iloc[1]['name']))
    #         self.value_stats1_1.configure(text=scoreboard.iloc[1]['Rating'])
    #         self.value_stats1_1_1.configure(text=scoreboard.iloc[1]['Impact'])
    #         self.value_stats1_2.configure(text=scoreboard.iloc[1]['ADR'])
    #         self.value_stats1_2_2.configure(text=scoreboard.iloc[1]['KAST%'])
    #         self.value_stats1_3.configure(text=scoreboard.iloc[1]['KPR'])
    #         self.value_stats1_3_3.configure(text=scoreboard.iloc[1]['DPR'])

    #         #affichage des données sur la page
    #         self.label_player_name2.configure(text=str(scoreboard.iloc[2]['name']))
    #         self.value_stats2_1.configure(text=scoreboard.iloc[2]['Rating'])
    #         self.value_stats2_1_1.configure(text=scoreboard.iloc[2]['Impact'])
    #         self.value_stats2_2.configure(text=scoreboard.iloc[2]['ADR'])
    #         self.value_stats2_2_2.configure(text=scoreboard.iloc[2]['KAST%'])
    #         self.value_stats2_3.configure(text=scoreboard.iloc[2]['KPR'])
    #         self.value_stats2_3_3.configure(text=scoreboard.iloc[2]['DPR'])

    #         #affichage des données sur la page
    #         self.label_player_name3.configure(text=str(scoreboard.iloc[3]['name']))
    #         self.value_stats3_1.configure(text=scoreboard.iloc[3]['Rating'])
    #         self.value_stats3_1_1.configure(text=scoreboard.iloc[3]['Impact'])
    #         self.value_stats3_2.configure(text=scoreboard.iloc[3]['ADR'])
    #         self.value_stats3_2_2.configure(text=scoreboard.iloc[3]['KAST%'])
    #         self.value_stats3_3.configure(text=scoreboard.iloc[3]['KPR'])
    #         self.value_stats3_3_3.configure(text=scoreboard.iloc[3]['DPR'])

    #         #affichage des données sur la page
    #         self.label_player_name4.configure(text=str(scoreboard.iloc[4]['name']))
    #         self.value_stats4_1.configure(text=scoreboard.iloc[4]['Rating'])
    #         self.value_stats4_1_1.configure(text=scoreboard.iloc[4]['Impact'])
    #         self.value_stats4_2.configure(text=scoreboard.iloc[4]['ADR'])
    #         self.value_stats4_2_2.configure(text=scoreboard.iloc[4]['KAST%'])
    #         self.value_stats4_3.configure(text=scoreboard.iloc[4]['KPR'])
    #         self.value_stats4_3_3.configure(text=scoreboard.iloc[4]['DPR'])

    #         # Supposons que `self.frame_utils` est le frame où vous souhaitez afficher le graphique.
    #         update_stacked_bar_chart_utils(self.frame_utils, df_utils, 1,0)
    #         update_bar_chart_flash(self.frame_flash,df_utils,1,0)
    #         update_entry_chart(self.frame_entry,df_entry,1,0)
                
if __name__ == "__main__":
    app = PlayerResumePage()
    app.protocol("WM_DELETE_WINDOW", app.quit)
    app.mainloop()
