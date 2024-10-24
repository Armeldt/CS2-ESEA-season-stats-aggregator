import customtkinter
from customtkinter import *
from CTkTable import *
from tkinter import filedialog
from PIL import Image
import pandas as pd
import numpy as np
from demoparser2 import DemoParser
import matplotlib.pyplot as plt
import seaborn as sns
import os

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

customtkinter.set_appearance_mode('dark')
customtkinter.set_default_color_theme("theme.json")

app = CTk()
app.geometry("1600x900")
app.title("CS2 stats aggregator")

file_paths = ""  # Définir file_paths ici pour l'utiliser globalement

all_players_stats_grouped = None
own_team_wins = None
own_team_losses = None
winstreak = None
map_stats = None
largest_win = None
closest_win = None
largest_loss = None
closest_loss = None  

def get_team_name(event=None): 
    global team_name 
    team_name = home_page.entry_1.get()  # Accéder à l'entrée pour obtenir le texte
    print(f"Team name: {team_name}")
    return team_name

def select_directory():
    global file_paths  # Rendre file_paths global pour l'utiliser dans d'autres fonctions
    file_paths = filedialog.askdirectory(title="Select demo folder")
    if file_paths:  # Vérifie si un dossier a bien été sélectionné
        print(f"Directory selected: {file_paths}")
    else:
        print("No directory selected.")
    return file_paths

def analyze():
    global all_players_stats_grouped 
    global own_team_wins
    global own_team_losses
    global winstreak
    global map_stats
    global largest_win
    global closest_win
    global largest_loss
    global closest_loss

    team = get_team_name()  # Appelle la fonction pour obtenir le nom de l'équipe
    demo_directory = file_paths  # Utiliser le dossier sélectionné
    if not demo_directory:
        print("No directory selected.")
        return

    print(f"Analyzing for team: {team} with demo files in directory: {demo_directory}")
    
    # Vérifier si le dossier contient des fichiers `.dem`
    files_in_directory = os.listdir(demo_directory)
    print(f"Files in directory: {files_in_directory}")  # Affiche tous les fichiers dans le répertoire

    # Créer une liste pour stocker les DataFrames concaténés pour chaque fichier
    all_matches = []

    # Parcours des fichiers dans le répertoire
    for filename in os.listdir(demo_directory):
        if filename.endswith(".dem"): 
            # Chargement de la démo
            demo = DemoParser(os.path.join(demo_directory, filename))

            # Extraction du tick max de la partie
            max_tick = demo.parse_event("round_end")["tick"].max()

            # Extraction du premier tick de la partie
            first_round_tick = demo.parse_event('round_start').drop([0,1,2]).loc[3, 'tick'] # on drop le knife round, le warmup round et le RR

            # Extraction de la carte 
            map = pd.DataFrame([demo.parse_header()])

            #tick fin période d'achat
            freezetime_end_tick = demo.parse_event("round_freeze_end")["tick"].drop([0,1]).tolist()# on drop le knife round et le warmup, pas de freezetime au RR

            # Extraction des noms des joueurs et des équipes 
            team_V3 = demo.parse_ticks(["team_clan_name","team_name"])
            team_V3.drop(team_V3[team_V3['tick'] < first_round_tick].index, inplace=True)
            team_V3.drop(team_V3[team_V3['tick'] > max_tick].index, inplace=True)
            team_V3.rename(columns={'team_name':'side'}, inplace=True)
            name_to_team = dict(zip(team_V3['name'], team_V3['team_clan_name']))

            #eco 
            eco = demo.parse_ticks(["current_equip_value", "total_rounds_played"], ticks=freezetime_end_tick)
            if eco['total_rounds_played'].min() == 0:
                eco['total_rounds_played'] = eco['total_rounds_played'] + 1
            eco['current_equip_value'] = eco['current_equip_value'] - 200
            #eco par équipe
            eco_by_players = pd.merge(eco,team_V3, on=['tick','name','steamid'])
            eco_by_team = eco_by_players.groupby(['total_rounds_played','team_clan_name','tick','side'])['current_equip_value'].sum().reset_index()

            # Kills DataFrame
            trade = demo.parse_event("player_death", other=["game_time", "round_start_time",'total_rounds_played'])
            trade['total_rounds_played'] = trade['total_rounds_played'] + 1
            trade.drop(trade[trade['tick'] < first_round_tick].index, inplace=True)
            trade["player_died_time"] = trade["game_time"] - trade["round_start_time"]
            trade = pd.merge(trade, team_V3[['team_clan_name','side','name','tick']], left_on=["attacker_name",'tick'], right_on=['name','tick'])
            trade = trade.rename(columns={'team_clan_name':'team_clan_name_attacker', 'side':'side_attacker'})
            trade = pd.merge(trade, team_V3[['team_clan_name','side','name','tick']], left_on=["user_name",'tick'], right_on=['name','tick'])
            trade = trade.rename(columns={'team_clan_name':'team_clan_name_user','side':'side_user'})

            # Damage DataFrame
            all_hits_regs = demo.parse_event("player_hurt", ticks=[max_tick])
            all_hits_regs.drop(all_hits_regs[all_hits_regs['tick'] < first_round_tick].index, inplace=True)
            all_hits_regs.drop(all_hits_regs[all_hits_regs['tick'] > max_tick].index, inplace=True)
            all_hits_regs['attacker_team'] = all_hits_regs['attacker_name'].map(name_to_team)
            all_hits_regs['user_team'] = all_hits_regs['user_name'].map(name_to_team)
            all_hits_regs = all_hits_regs[all_hits_regs['attacker_team'] != all_hits_regs['user_team']]

            # Stats DataFrame
            overall_stats = ["total_rounds_played","kills_total","assists_total","deaths_total", "mvps", "headshot_kills_total", 
                            "3k_rounds_total", "4k_rounds_total", "ace_rounds_total" ,"damage_total","utility_damage_total", 
                            "enemies_flashed_total","alive_time_total"]
            agg_stats = demo.parse_ticks(overall_stats, ticks=[max_tick])

            # round_winner
            round_ends = demo.parse_event("round_end", other=["total_rounds_played","team_clan_name"])
            
            def transform_round_end(round_ends, first_round_tick):
                # Vérifier si la première colonne est 'legacy'
                if round_ends.columns[1].lower() == 'legacy':
                    round_ends['winner'] = round_ends['winner'].apply(lambda x: 'T' if x == 2 else 'CT' if x == 3 else 'unknown')
                    def reason_mapping(x):
                        if x == 9:
                            return 'ct_killed'
                        elif x == 7:
                            return 'bomb_defused'
                        elif x == 8:
                            return 't_killed'
                        elif x == 12:
                            return 't_saved'
                        else:
                            return 'unknown'

                    round_ends['reason'] = round_ends['reason'].apply(reason_mapping)
                    round_ends.drop(round_ends[round_ends['tick'] <= first_round_tick].index, inplace=True)
                    round_ends = round_ends[['ct_team_clan_name','t_team_clan_name','reason', 'tick', 'total_rounds_played', 'winner']]
                    round_ends['total_rounds_played'] = round_ends['total_rounds_played'] + 1
                
                else:
                    round_ends.drop(round_ends[round_ends['tick'] <= first_round_tick].index, inplace=True)
                    round_ends.drop(columns=['round'], inplace=True)
                
                return round_ends

            round_ends = transform_round_end(round_ends, first_round_tick)


            # Identification de l'équipe adverse
            unique_teams = team_V3['team_clan_name'].unique()
            adversary_team = [t for t in unique_teams if t != team][0]  # Trouver l'équipe adverse

            # Sélection des joueurs spécifiés dans zobrux
            df_team = team_V3.loc[team_V3['team_clan_name'] == team, :]

            # Ajouter une colonne avec l'équipe adverse comme Game_id
            df_team['Game_id'] = "VS_"+adversary_team

            # Stocker chaque DataFrame dans un dictionnaire pour ce fichier, y compris eco_info
            match_data = {
                'team_info': df_team,
                'trade_info': trade,
                'damage_info': all_hits_regs,
                'agg_stats': agg_stats,
                'eco_info': eco_by_team,
                'round_info': round_ends,
                'map_info' : map
            }

            # Ajout du dictionnaire à la liste
            all_matches.append(match_data)

            #### calculs des indicateurs equipe ###

            # Liste pour stocker les informations des matchs
            match_data = []

            # Fonction pour calculer le score d'une partie et déterminer le gagnant
            def calculate_match_result(round_info_df, team_name):
                team_wins = 0
                opponent_wins = 0

                # Initialiser la première équipe CT
                current_ct_team = round_info_df['ct_team_clan_name'].iloc[0]
                
                for index, row in round_info_df.iterrows():
                    # Si l'équipe CT change, cela signifie un changement de côté
                    if row['ct_team_clan_name'] != current_ct_team:
                        current_ct_team = row['ct_team_clan_name']
                    
                    # Calculer les victoires en fonction du gagnant du round (CT ou T)
                    if row['winner'] == 'CT':
                        if row['ct_team_clan_name'] == team_name:
                            team_wins += 1
                        else:
                            opponent_wins += 1
                    elif row['winner'] == 'T':
                        if row['t_team_clan_name'] == team_name:
                            team_wins += 1
                        else:
                            opponent_wins += 1

                return team_wins, opponent_wins

            # Parcourir toutes les parties stockées dans la liste all_matches
            for i, match in enumerate(all_matches):  # match est un dictionnaire contenant 'round_info', 'map_info' et 'team_info'
                round_info_df = match['round_info']
                
                # Calculer le résultat du match
                team_wins, opponent_wins = calculate_match_result(round_info_df, team_name)

                # Obtenir le nom du match (Game_id) et la map jouée
                game_id = match['team_info']['Game_id'].iloc[0]
                map_name = match['map_info']['map_name'].iloc[0]

                # Déterminer l'équipe victorieuse
                if team_wins > opponent_wins:
                    winning_team = team_name
                else:
                    winning_team = round_info_df['ct_team_clan_name'].iloc[0] if opponent_wins > team_wins else round_info_df['t_team_clan_name'].iloc[0]

                # Ajouter les informations du match dans la liste
                match_data.append({
                    "Match id": i + 1,
                    "Game Name": game_id,
                    "Map": map_name,
                    "Rounds Won by zobrux": team_wins,
                    "Rounds Won by Opponent": opponent_wins,
                    "Winning Team": winning_team
                })

            # Créer un DataFrame à partir des données de match
            match_df = pd.DataFrame(match_data)

            # Nombre de victoires de zobrux
            own_team_wins = match_df[match_df['Winning Team'] == team_name].shape[0]

            # Nombre de défaites de zobrux
            own_team_losses = match_df[match_df['Winning Team'] != team_name].shape[0]

            # Calcul du plus long winstreak
            winstreak = 0
            current_streak = 0

            for winning_team in match_df['Winning Team']:
                if winning_team == team_name:
                    current_streak += 1
                    winstreak = max(winstreak, current_streak)
                else:
                    current_streak = 0

            # Nombre de fois où chaque carte a été jouée et le taux de victoire
            map_stats = match_df.groupby('Map').agg(
                times_played=('Map', 'size'),
                wins_on_map=('Winning Team', lambda x: (x == team_name).sum())
            )

            # Calcul du pourcentage de victoire par carte
            map_stats['winrate'] = (map_stats['wins_on_map'] / map_stats['times_played']) * 100

            # analyse des victoires et defaites
            match_df['round_diff'] = abs(match_df['Rounds Won by zobrux'] - match_df['Rounds Won by Opponent'])

            # Filtrer les victoires et les défaites de zobrux
            zobrux_victories = match_df[match_df['Winning Team'] == team_name]
            zobrux_losses = match_df[match_df['Winning Team'] != team_name]

            # Si zobrux a gagné au moins un match, trouver la victoire la plus large et la plus serrée
            if not zobrux_victories.empty:
                # Victoire la plus large
                largest_win = zobrux_victories.loc[zobrux_victories['round_diff'].idxmax()]

                # Victoire la plus serrée
                closest_win = zobrux_victories.loc[zobrux_victories['round_diff'].idxmin()]

                print(f"Victoire la plus large : {largest_win['Game Name']} sur {largest_win['Map']} avec {largest_win['Rounds Won by zobrux']} - {largest_win['Rounds Won by Opponent']}")
                print(f"Victoire la plus serrée : {closest_win['Game Name']} sur {closest_win['Map']} avec {closest_win['Rounds Won by zobrux']} - {closest_win['Rounds Won by Opponent']}")
            else:
                print(f"{team_name} n'a pas encore gagné de match.")

            # Si zobrux a perdu au moins un match, trouver la défaite la plus large et la plus serrée
            if not zobrux_losses.empty:
                # Défaite la plus large
                largest_loss = zobrux_losses.loc[zobrux_losses['round_diff'].idxmax()]

                # Défaite la plus serrée
                closest_loss = zobrux_losses.loc[zobrux_losses['round_diff'].idxmin()]

                print(f"Défaite la plus large : {largest_loss['Game Name']} sur {largest_loss['Map']} avec {largest_loss['Rounds Won by zobrux']} - {largest_loss['Rounds Won by Opponent']}")
                print(f"Défaite la plus serrée : {closest_loss['Game Name']} sur {closest_loss['Map']} avec {closest_loss['Rounds Won by zobrux']} - {closest_loss['Rounds Won by Opponent']}")
            else:
                print(f"{team_name} n'a pas encore perdu de match.")

            ### calculs des indicateurs joueurs ###

            #### Definition des joueurs
            joueurs = pd.DataFrame()
            joueurs['name']  = team_V3.loc[(team_V3['team_clan_name'] == 'zobrux') & (team_V3['tick'] == first_round_tick), 'name']
            joueurs = joueurs.reset_index().drop(columns={'index'})

            #### calcul scoreborad
            all_players_stats = pd.DataFrame()
            for match_data in all_matches:
                # Récupérer les statistiques du match
                stats = match_data['agg_stats']
                
                # Joindre les stats des joueurs
                Stats_joueurs = joueurs.merge(stats, on='name', how='left')
                
                # Ajouter les stats agrégées des joueurs à la liste générale
                all_players_stats = pd.concat([all_players_stats, Stats_joueurs])

            # Faire la somme des stats par joueur
            all_players_stats_grouped = all_players_stats.groupby('name').sum().reset_index()
            all_players_stats_grouped['ADR'] = round(all_players_stats_grouped['damage_total'] / all_players_stats_grouped["total_rounds_played"],2)
            all_players_stats_grouped['+/-'] = round(all_players_stats_grouped['kills_total'] - all_players_stats_grouped["deaths_total"],2)
            all_players_stats_grouped['HS %'] = round((all_players_stats_grouped['headshot_kills_total'] / all_players_stats_grouped['kills_total'])*100,2)
            all_players_stats_grouped['KPR'] = round((all_players_stats_grouped['kills_total'] / all_players_stats_grouped['total_rounds_played']), 2)
            all_players_stats_grouped['K/D'] = round((all_players_stats_grouped['kills_total'] / all_players_stats_grouped['deaths_total']),2)
            all_players_stats_grouped = all_players_stats_grouped.rename(columns={"total_rounds_played":"Rounds joués","headshot_kills_total":"HS","kills_total":"Kills","assists_total":"Assists","deaths_total":"Deaths","3k_rounds_total":'3K', "4k_rounds_total":'4K', "ace_rounds_total":'5K',"damage_total":"Damages","utility_damage_total":"Utility Damages","enemies_flashed_total":"Flashed Ennemies"})
            all_players_stats_grouped = all_players_stats_grouped.drop(columns={"tick"})
            nouvel_ordre_colonnes = [
                'name', 'steamid', 'Rounds joués', 'Kills', 'Deaths','+/-', 'Assists', 
                'K/D', 'Damages', 'ADR', 'KPR', 'HS', 'HS %', '5K', '4K', '3K', 'mvps'
            ]
            all_players_stats_grouped = all_players_stats_grouped[nouvel_ordre_colonnes]


#### Pages architecture #### 

def hide_all():
    """ Hides all the pages """
    home_page.hide()
    page_team_summary.hide()
    page_team_details.hide()
    page_match_analysis.hide()

def show_home_page():
    home_page.show()

def show_team_summary():
    page_team_summary.show()

def show_team_details():
    page_team_details.show()

def show_match_analysis():
    page_match_analysis.show()

#### Classe des différentes pages ####

class HomePage:
    def __init__(self):
        self.frame = CTkFrame(master=app)
        self.label_1 = customtkinter.CTkLabel(master=self.frame, text="This tool analyzes the statistical results of a Counter-Strike 2 ESEA season using demo files.\n\nIt provides global team insights, individual player stats, and detailed match breakdowns.", font=('robot', 18), wraplength=850)
        self.label_title = customtkinter.CTkLabel(master=self.frame, text="How to use :", font=('robot', 18, 'bold'), wraplength=850)
        self.instructions_text = (
            "Follow these simple steps:\n\n"
            "1. Download the demo files from all your ESEA season matches directly from Faceit's website.\n\n"
            "2. Store them in the same folder on your computer.\n\n"
            "3. Use the 'Upload your demo' button to load the demos into the tool.\n\n"
            "4. Type your team's name, ensuring proper capitalization, hyphens, etc.\n\n"
            "5. Click on the 'Analyze' button to start the analysis."
        )
        self.label_instructions = customtkinter.CTkLabel(master=self.frame, text=self.instructions_text, justify='left', font=('robot', 14), wraplength=850)
        self.button_1 = customtkinter.CTkButton(master=self.frame, text='Upload your demos', font=('Stratum2 Bd', 20), command=select_directory, height=40, width=250)
        self.entry_1 = customtkinter.CTkEntry(master=self.frame, placeholder_text="Type the name of your team", font=('Stratum2 Bd', 20), justify='center', width=250)
        self.entry_1.bind("<Return>", get_team_name)
        self.button_2 = customtkinter.CTkButton(master=self.frame, text='Analyze', font=('Stratum2 Bd', 30), command=analyze, height=80, width=300)

    def show(self):
        hide_all()
        self.frame.pack(pady=(10, 20), padx=20, fill="both", expand=True)
        self.label_1.pack(pady=20, padx=20)
        self.label_title.pack(pady=10, padx=20)
        self.label_instructions.pack(pady=20, padx=20)
        self.button_1.pack(pady=30, padx=10)
        self.entry_1.pack(pady=25, padx=10)
        self.button_2.pack(pady=25, padx=10)

    def hide(self):
        self.frame.pack_forget()

class TeamSummaryPage:
    def __init__(self):
        self.frame = CTkFrame(master=app)
        self.label = CTkLabel(master=self.frame, text="Team Season Summary", font=('Stratum2 Bd', 20))

    def show(self):
        hide_all()
        self.frame.pack(pady=20, padx=20, fill="both", expand=True)
        self.label.pack(pady=50)

        # Afficher des données fictives en attendant les vraies données
        if all_players_stats_grouped is not None:
            summary_label = CTkLabel(master=self.frame, text="Team Summary Data", font=('Stratum2 Bd', 14))
            summary_label.pack(pady=10)
        else:
            error_label = CTkLabel(master=self.frame, text="No data available. Please run the analysis first.", font=('Stratum2 Bd', 16))
            error_label.pack(pady=10)

    def hide(self):
        self.frame.pack_forget()

class TeamDetailsPage:
    def __init__(self):
        self.frame = CTkFrame(master=app)
        self.label = CTkLabel(master=self.frame, text="Team Detailed Performances", font=('Stratum2 Bd', 20))

    def show(self):
        hide_all()
        self.frame.pack(pady=20, padx=20, fill="both", expand=True)
        self.label.pack(pady=50)

        if all_players_stats_grouped is not None:
            table_frame = CTkFrame(self.frame)
            table_frame.pack(fill="both", expand=True)
            # Affichage de la table
            table = CTkTable(master=table_frame, row=6, column=17, values=([all_players_stats_grouped.columns.tolist()])+(all_players_stats_grouped.values.tolist()))
            table.pack(expand=True, padx=20, pady=20)
            # table_label = CTkLabel(master=table_frame, text=str(all_players_stats_grouped.head()), font=('Stratum2 Bd', 14))
            # table_label.pack(pady=10)
        else:
            error_label = CTkLabel(master=self.frame, text="No data available. Please run the analysis first.", font=('Stratum2 Bd', 16))
            error_label.pack(pady=10)

    def hide(self):
        self.frame.pack_forget()

class MatchAnalysisPage:
    def __init__(self):
        self.frame = CTkFrame(master=app)
        self.label = CTkLabel(master=self.frame, text="Specific Match Analysis", font=('Stratum2 Bd', 20))

    def show(self):
        hide_all()
        self.frame.pack(pady=20, padx=20, fill="both", expand=True)
        self.label.pack(pady=50)

    def hide(self):
        self.frame.pack_forget()

#### Création des pages ####
home_page = HomePage()
page_team_summary = TeamSummaryPage()
page_team_details = TeamDetailsPage()
page_match_analysis = MatchAnalysisPage()

#### Header ####
frame_header = CTkFrame(master=app)
frame_header.pack(pady=(20, 10), padx=20, fill="both", expand=True)

title = CTkLabel(master=frame_header, text='CS2 STATS AGGREGATOR', font=("Stratum2 Bd", 60), text_color=('#fbac18'))
title.pack(pady=10)

button_frame = CTkFrame(master=frame_header, fg_color='transparent')
button_frame.pack(pady=10)

### Boutons de navigation ###
button_home = CTkButton(master=button_frame, text='Home', font=('Stratum2 Bd', 20), command=show_home_page)
button_home.grid(row=0, column=0, padx=20)

button_team_summary = CTkButton(master=button_frame, text='Team Season Summary', font=('Stratum2 Bd', 20), command=show_team_summary)
button_team_summary.grid(row=0, column=1, padx=20)

button_team_details = CTkButton(master=button_frame, text='Team Detailed Performances', font=('Stratum2 Bd', 20), command=show_team_details)
button_team_details.grid(row=0, column=2, padx=20)

button_match_analysis = CTkButton(master=button_frame, text='Specific Match Analysis', font=('Stratum2 Bd', 20), command=show_match_analysis)
button_match_analysis.grid(row=0, column=3, padx=20)

#### Affichage initial de la page d'accueil ####
home_page.show()

app.mainloop()
