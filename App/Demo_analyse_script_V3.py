import pandas as pd
import numpy as np
from demoparser2 import DemoParser
import os
from glob import glob

# 1. Fonctions utilitaires
def select_directory(file_paths="D:/Python/projet_cs_v2/demos"):
    if not os.path.isdir(file_paths):
        print("Invalid directory.")
        return None
    print(f"Directory selected: {file_paths}")
    return file_paths

def categorize_rounds(row):
    if row['total_rounds_played'] in [1, 13]:
        return 'Pistol round'
    elif row['current_equip_value'] <= 3500:
        return 'Eco round'
    elif row['current_equip_value'] <= 18000:
        return 'Force buy round'
    else:
        return 'Full buy round'

def transform_round_end(round_ends, first_round_tick):
    # Vérifie si la colonne contient des valeurs legacy qui indiquent les gagnants par un code numérique
    if 'legacy' in round_ends.columns[1].lower():
        # Remplace les valeurs numériques par les noms d'équipes ('CT' ou 'T')
        round_ends['winner'] = round_ends['winner'].replace({2: 'T', 3: 'CT'}).fillna('unknown')

        # Traduit les raisons des rounds pour plus de clarté
        reason_dict = {9: 'ct_killed', 7: 'bomb_defused', 8: 't_killed', 12: 't_saved'}
        round_ends['reason'] = round_ends['reason'].map(reason_dict).fillna('unknown')

        # Sélectionne et ordonne les colonnes
        round_ends = round_ends[['ct_team_clan_name', 't_team_clan_name', 'reason', 'tick', 'total_rounds_played', 'winner']]
        # Ajuste le décalage pour total_rounds_played
        round_ends['total_rounds_played'] += 1

    else:
        # Supprime les rounds sans raison valide après le premier round
        round_ends = round_ends[round_ends['tick'] > first_round_tick].drop(columns=['round'])

    return round_ends


# 2. Fonctions de calcul des statistiques
def calculate_match_stats(all_matches, team_name):
    match_data = []
    
    for i, match in enumerate(all_matches):
        round_info_df = match['round_info']
        team_wins, opponent_wins = calculate_match_result(round_info_df, team_name)

        game_id = f"Game_{i+1}"  # Nom du match
        map_name = match['map_info'].iloc[0]['map_name']  # Nom de la map

        # Déterminer l'équipe victorieuse
        if team_wins > opponent_wins:
            winning_team = team_name
        else:
            winning_team = round_info_df['ct_team_clan_name'].iloc[0] if opponent_wins > team_wins else round_info_df['t_team_clan_name'].iloc[0]

        # Ajouter les informations de match
        match_data.append({
            "Match id": i + 1,
            "Game Name": game_id,
            "Map": map_name,
            "Rounds Won by zobrux": team_wins,
            "Rounds Won by Opponent": opponent_wins,
            "Winning Team": winning_team
        })

    # Créer un DataFrame avec les informations de chaque match
    match_df = pd.DataFrame(match_data)

    # Calculer les statistiques globales
    own_team_wins = match_df[match_df['Winning Team'] == team_name].shape[0]
    own_team_losses = match_df[match_df['Winning Team'] != team_name].shape[0]

    # Calculer le plus long winstreak
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
    map_stats['winrate'] = (map_stats['wins_on_map'] / map_stats['times_played']) * 100

    # Retourner les statistiques sous forme de dictionnaire
    return {
        "match_results": match_df,
        "own_team_wins": own_team_wins,
        "own_team_losses": own_team_losses,
        "winstreak": winstreak,
        "map_stats": map_stats
    }

def calculate_match_result(round_info_df, team_name):
    ct_wins = round_info_df[round_info_df['winner'] == 'CT'].groupby('ct_team_clan_name').size()
    t_wins = round_info_df[round_info_df['winner'] == 'T'].groupby('t_team_clan_name').size()
    team_wins = ct_wins.get(team_name, 0) + t_wins.get(team_name, 0)
    opponent_wins = round_info_df['total_rounds_played'].max() - team_wins
    return team_wins, opponent_wins

def calculate_map_stats(match_df, team_name):
    map_stats = match_df.groupby('Map').agg(
        times_played=('Map', 'size'),
        wins_on_map=('Winning Team', lambda x: (x == team_name).sum())
    )
    map_stats['winrate'] = (map_stats['wins_on_map'] / map_stats['times_played']) * 100
    return map_stats

def calculate_wr_per_round_type(all_matches, team_name):
    all_matches_round_analysis = pd.DataFrame()
    for match_data in all_matches:
        eco_by_team = match_data['eco_info']
        round_info = match_data['round_info']  # Contient la colonne 'winner'
        
        # Associer les catégories de round à `eco_by_team`
        eco_by_team['round_category'] = eco_by_team.apply(categorize_rounds, axis=1)
        
        # Fusionner `eco_by_team` et `round_info` sur le numéro du round pour accéder à 'winner'
        df_merged = pd.merge(eco_by_team, round_info[['total_rounds_played', 'winner']], 
                             on='total_rounds_played', how='left')
        
        # Filtrer les rounds joués par l'équipe `team_name`
        rounds_team = df_merged[df_merged['team_clan_name'] == team_name]
        
        # Calculer le nombre de rounds totaux par catégorie et par side
        total_rounds_per_category_side = rounds_team.groupby(['round_category', 'side']).size()
        
        # Calculer les victoires et défaites par catégorie et par side
        wins_per_category_side = rounds_team[rounds_team['winner'] == rounds_team['side']].groupby(['round_category', 'side']).size()
        losses_per_category_side = rounds_team[rounds_team['winner'] != rounds_team['side']].groupby(['round_category', 'side']).size()
        
        # Combiner les résultats pour chaque match dans un DataFrame temporaire
        match_stats = pd.DataFrame({
            'total_rounds': total_rounds_per_category_side,
            'wins': wins_per_category_side,
            'losses': losses_per_category_side
        }).fillna(0).astype(int)
        
        # Ajouter les stats du match au DataFrame global
        all_matches_round_analysis = pd.concat([all_matches_round_analysis, match_stats])

    # Calcul du winrate et des pourcentages de défaites par type de round et par side
    wr_per_round_type = all_matches_round_analysis.groupby(['round_category', 'side']).sum()
    wr_per_round_type['win_%'] = (wr_per_round_type['wins'] / wr_per_round_type['total_rounds'] * 100).round(1)
    wr_per_round_type['loss_%'] = (wr_per_round_type['losses'] / wr_per_round_type['total_rounds'] * 100).round(1)
    
    return wr_per_round_type.reset_index()

def calculate_util_stats(joueurs, all_matches):
    all_utils_stats = pd.DataFrame()
    for match_data in all_matches:
        all_hits_regs = match_data['damage_info']
        stats_utils = match_data['agg_stats']
        player_death = match_data['player_death_info']
        
        # Calcul des flash assist kills
        flash_assist_kill = player_death[player_death['assistedflash']].groupby('assister_name').size().reset_index(name='Flash_assist')
        flash_assist_kill = flash_assist_kill.rename(columns={'assister_name':'name'})
        
        # Calcul des dégâts HE
        he_dmg = all_hits_regs[all_hits_regs["weapon"] == "hegrenade"].groupby('attacker_name')['dmg_health'].sum().reset_index().rename(columns={'attacker_name':'name', 'dmg_health': 'He_dmg'})
        
        # Calcul des dégâts molotov/incendiaire
        molotov_dmg = all_hits_regs[all_hits_regs["weapon"].isin(["molotov", "inferno"])].groupby('attacker_name')['dmg_health'].sum().reset_index().rename(columns={'attacker_name':'name', 'dmg_health': 'Fire_dmg'})
        
        # Fusion des statistiques utilitaires avec les joueurs
        utils_joueurs = joueurs.merge(he_dmg, on='name', how='left').merge(molotov_dmg, on='name', how='left').fillna(0)
        utils_joueurs['Total_utility_dmg'] = utils_joueurs['He_dmg'] + utils_joueurs['Fire_dmg']
        
        # Ajouter les flashs et autres statistiques utilitaires
        utils_joueurs = utils_joueurs.merge(stats_utils[['name', 'enemies_flashed_total']], on='name', how='left').merge(flash_assist_kill, on='name', how='left')
        
        # Remplir les valeurs manquantes et convertir uniquement les colonnes numériques en entier
        utils_joueurs.fillna(0, inplace=True)
        numeric_columns = ['Flash_assist', 'He_dmg', 'Fire_dmg', 'Total_utility_dmg', 'enemies_flashed_total']
        utils_joueurs[numeric_columns] = utils_joueurs[numeric_columns].astype(int)
        
        # Concaténer les stats pour ce match avec les autres
        all_utils_stats = pd.concat([all_utils_stats, utils_joueurs])

    return all_utils_stats.groupby('name').sum().reset_index()

def calculate_player_stats(joueurs, all_matches):
    all_players_stats = pd.DataFrame()
    for match_data in all_matches:
        stats = match_data['agg_stats']
        Stats_joueurs = joueurs.merge(stats, on='name', how='left')
        all_players_stats = pd.concat([all_players_stats, Stats_joueurs])
        
    # Agrégation des statistiques
    all_players_stats_grouped = all_players_stats.groupby('name').sum().reset_index()
    all_players_stats_grouped['ADR'] = round(all_players_stats_grouped['damage_total'] / all_players_stats_grouped["total_rounds_played"], 2)
    all_players_stats_grouped['+/-'] = all_players_stats_grouped['kills_total'] - all_players_stats_grouped["deaths_total"]
    return all_players_stats_grouped

def calculate_entry_stats(joueurs, all_matches):
    all_opening_stats = pd.DataFrame()

    for match_data in all_matches:
        player_death = match_data['player_death_info']
        first_duel = player_death.groupby('total_rounds_played').first().reset_index()
        
        opening_stats = pd.DataFrame({'name': player_death['attacker_name'].unique(), 'entry_attempts(T)': 0, 'entry_successes(T)': 0, 'open_attempts(CT)': 0, 'open_successes(CT)': 0})
        
        for _, row in first_duel.iterrows():
            attacker, user, side_user = row['attacker_name'], row['user_name'], row['side_user']
            if side_user == 'CT':
                opening_stats.loc[opening_stats['name'] == attacker, 'entry_attempts(T)'] += 1
                opening_stats.loc[opening_stats['name'] == attacker, 'entry_successes(T)'] += 1
                opening_stats.loc[opening_stats['name'] == user, 'open_attempts(CT)'] += 1
            elif side_user == 'TERRORIST':
                opening_stats.loc[opening_stats['name'] == attacker, 'open_attempts(CT)'] += 1
                opening_stats.loc[opening_stats['name'] == attacker, 'open_successes(CT)'] += 1
                opening_stats.loc[opening_stats['name'] == user, 'entry_attempts(T)'] += 1
                
        all_opening_stats = pd.concat([all_opening_stats, opening_stats])

    all_opening_stats_grouped = all_opening_stats.groupby('name').sum().reset_index()
    all_opening_stats_grouped["%_entry_success(T)"] = round((all_opening_stats_grouped["entry_successes(T)"] / all_opening_stats_grouped["entry_attempts(T)"]) * 100, 0)
    all_opening_stats_grouped["%_open_success(CT)"] = round((all_opening_stats_grouped["open_successes(CT)"] / all_opening_stats_grouped["open_attempts(CT)"]) * 100, 0)

    column_order = ['name', 'entry_attempts(T)', 'entry_successes(T)', '%_entry_success(T)', 'open_attempts(CT)', 'open_successes(CT)', '%_open_success(CT)']
    all_opening_stats_grouped = all_opening_stats_grouped[column_order]
    entry_stats = joueurs.merge(all_opening_stats_grouped, on='name', how='left')
    return entry_stats

def calculate_eco_kills(joueurs, all_matches):
    all_team_eco_kills = pd.DataFrame()

    for match_data in all_matches:
        trade_df = match_data['player_death_info']
        eco_by_team = match_data['eco_info']
        game_id = match_data['team_info']['Game_id'].iloc[0]
        trade_df['Game_id'] = game_id
        eco_by_team['Game_id'] = game_id

        df_merged_team = pd.merge(trade_df, eco_by_team, how='left', left_on=['total_rounds_played', 'team_clan_name_user', 'Game_id'], right_on=['total_rounds_played', 'team_clan_name', 'Game_id'])

        df_merged_team['kill_category'] = df_merged_team.apply(categorize_rounds, axis=1)
        team_eco_kills = df_merged_team.pivot_table(index='attacker_name', columns='kill_category', aggfunc='size', fill_value=0)
        all_team_eco_kills = pd.concat([all_team_eco_kills, team_eco_kills])
        all_team_eco_kills_grouped = all_team_eco_kills.groupby('attacker_name').sum().reset_index()
        eco_stats = pd.merge(joueurs,all_team_eco_kills_grouped,left_on='name',right_on='attacker_name',how='left')
    return eco_stats

def calculate_advanced_stats(joueurs, all_matches):
    player_stats_global = {}

    for match_data in all_matches:
        player_death = match_data['player_death_info']

        for round_number in player_death['total_rounds_played'].unique():
            round_data = player_death[player_death['total_rounds_played'] == round_number].sort_values(by='player_died_time')
            survived_players = set(player_death['user_name'].unique()) - set(round_data['user_name'].unique())

            for player in player_death['user_name'].unique():
                if player not in player_stats_global:
                    player_stats_global[player] = {'Kills': 0, 'Assists': 0, 'Deaths': 0, 'KAST_rounds': 0, 'total_rounds': 0, 'Traded_deaths': 0}

                player_stats_global[player]['total_rounds'] += 1
                kast_contributed = False

                # Calcul des kills
                kills = round_data[round_data['attacker_name'] == player]
                if len(kills) > 0:
                    player_stats_global[player]['Kills'] += len(kills)
                    player_stats_global[player]['KAST_rounds'] += 1
                    kast_contributed = True

                # Calcul des assists
                if not kast_contributed:
                    assists = round_data[round_data['assister_name'] == player]
                    if len(assists) > 0:
                        player_stats_global[player]['Assists'] += len(assists)
                        player_stats_global[player]['KAST_rounds'] += 1
                        kast_contributed = True

                # Calcul des deaths
                deaths = round_data[round_data['user_name'] == player]
                if len(deaths) > 0:
                    player_stats_global[player]['Deaths'] += len(deaths)

                # Calcul de la survie
                if not kast_contributed and player in survived_players:
                    player_stats_global[player]['KAST_rounds'] += 1
                    kast_contributed = True

                # Calcul des traded deaths
                for _, death_row in deaths.iterrows():
                    death_time = death_row['player_died_time']
                    attacker = death_row['attacker_name']
                    subsequent_rows = round_data[round_data.index > death_row.name]

                    for _, next_row in subsequent_rows.iterrows():
                        if next_row['user_name'] == attacker and next_row['player_died_time'] <= death_time + 2:
                            player_stats_global[player]['Traded_deaths'] += 1
                            if not kast_contributed:
                                player_stats_global[player]['KAST_rounds'] += 1
                                kast_contributed = True
                            break

    # Calcul des pourcentages et des indicateurs avancés
    for player, stats in player_stats_global.items():
        stats['KAST%'] = round((stats['KAST_rounds'] / stats['total_rounds']) * 100, 1)
        kills_per_round = stats['Kills'] / stats['total_rounds']
        assists_per_round = stats['Assists'] / stats['total_rounds']
        deaths_per_round = stats['Deaths'] / stats['total_rounds']
        stats["KPR"] = round(kills_per_round, 2)
        stats["APR"] = round(assists_per_round, 2)
        stats['DPR'] = round(deaths_per_round, 2)
        stats['Impact'] = round((2.13 * kills_per_round) + (0.42 * assists_per_round) - 0.41, 2)

    # Conversion en DataFrame pour intégration
    advanced_stats_df = pd.DataFrame(player_stats_global).T.reset_index().rename(columns={'index': 'name'})
    advanced_stats_df = advanced_stats_df.astype({'Kills':int,'Assists':int,'Deaths':int,'KAST_rounds':int,'total_rounds':int,'Traded_deaths':int})
    advanced_stats_df = pd.merge(joueurs,advanced_stats_df,on='name',how='left')
    return advanced_stats_df

# 3. Fonction principale
def cumulate_stats(team_name="zobrux", file_paths="D:/Python/projet_cs_v2/demos"):
    # Sélection du répertoire et initialisation des variables
    demo_directory = select_directory(file_paths)
    if not demo_directory:
        print("No directory selected.")
        return
    all_matches = []

    # Parsing des fichiers de démos
    for filename in glob(os.path.join(demo_directory, "*.dem")):
        
        demo = DemoParser(os.path.join(demo_directory, filename))
        
        max_tick = demo.parse_event("round_end")["tick"].max()
        
        first_round_tick = demo.parse_event('round_start').drop([0,1,2]).loc[3, 'tick']
        
        map = pd.DataFrame([demo.parse_header()])
        
        freezetime_end_tick = demo.parse_event("round_freeze_end")["tick"].drop([0,1]).tolist()
        
        team = demo.parse_ticks(["team_clan_name", "team_name"])
        team = team[(team['tick'] >= first_round_tick) & (team['tick'] <= max_tick)].copy()
        team.rename(columns={'team_name': 'side'}, inplace=True)
        unique_teams = team['team_clan_name'].unique()
        adversary_team = [t for t in unique_teams if t != team_name][0]
        game_id = f"VS_{adversary_team}" 
        team = team[team['team_clan_name'] == team_name]
        
        eco = demo.parse_ticks(["current_equip_value", "total_rounds_played"], ticks=freezetime_end_tick)
        eco['current_equip_value'] -= 200
        eco = eco.merge(team[['tick', 'team_clan_name', 'side']], on='tick', how='left')
        eco_by_team = eco.groupby(['total_rounds_played', 'team_clan_name', 'tick', 'side'])['current_equip_value'].sum().reset_index()
        
        # Charger le DataFrame `player_death` avec les informations sur les kills
        player_death = demo.parse_event("player_death", other=["game_time", "round_start_time", "total_rounds_played"])
        player_death['total_rounds_played'] += 1
        player_death = player_death[player_death['tick'] >= first_round_tick].copy()
        player_death["player_died_time"] = player_death["game_time"] - player_death["round_start_time"]

        # Ajouter `team_clan_name` et `side` pour `attacker_name` et `user_name` dans `player_death`
        player_death = pd.merge(player_death, team[['team_clan_name', 'side', 'name', 'tick']], 
                                left_on=["attacker_name", 'tick'], right_on=['name', 'tick'], how='left').rename(columns={'team_clan_name': 'team_clan_name_attacker', 'side': 'side_attacker'})
        player_death = pd.merge(player_death, team[['team_clan_name', 'side', 'name', 'tick']], 
                                left_on=["user_name", 'tick'], right_on=['name', 'tick'], how='left').rename(columns={'team_clan_name': 'team_clan_name_user', 'side': 'side_user'})
        player_death = player_death.drop(columns=['name_x', 'name_y'])

        all_hits_regs = demo.parse_event("player_hurt", ticks=[max_tick])
        all_hits_regs = all_hits_regs[(all_hits_regs['tick'] >= first_round_tick) & (all_hits_regs['tick'] <= max_tick)].copy()
        
        round_ends = demo.parse_event("round_end", other=["total_rounds_played", "team_clan_name"])
        round_ends = transform_round_end(round_ends, first_round_tick)
        
        

        overall_stats = ["total_rounds_played","kills_total","assists_total","deaths_total", "mvps", "headshot_kills_total", 
                         "3k_rounds_total", "4k_rounds_total", "ace_rounds_total" ,"damage_total","utility_damage_total", 
                         "enemies_flashed_total","alive_time_total"]
        agg_stats = demo.parse_ticks(overall_stats, ticks=[max_tick])

        # Ajout de `Game_id` dans les informations de match
        match_data_single = {
            'team_info': team[team['team_clan_name'] == team_name].assign(Game_id=game_id),
            'player_death_info': player_death,
            'damage_info': all_hits_regs,
            'agg_stats': agg_stats,
            'eco_info': eco_by_team.assign(Game_id=game_id),
            'round_info': round_ends.assign(Game_id=game_id),
            'map_info': map.assign(Game_id=game_id)
        }
        all_matches.append(match_data_single)

    # Calculer les statistiques de match
    match_stats = calculate_match_stats(all_matches, team_name)

    # Calcul des autres statistiques
    joueurs = pd.DataFrame({'name': team.loc[(team['team_clan_name'] == 'zobrux') & (team['tick'] == first_round_tick), 'name'].unique()})
    print(joueurs)
    util_stats = calculate_util_stats(joueurs, all_matches)
    player_stats = calculate_player_stats(joueurs, all_matches)
    entry_stats = calculate_entry_stats(joueurs, all_matches)
    eco_kills = calculate_eco_kills(joueurs, all_matches)
    advanced_stats = calculate_advanced_stats(joueurs, all_matches)
    wr_per_round_type = calculate_wr_per_round_type(all_matches, team_name)

    # Retourner tous les résultats
    results = {
        "match_results": match_stats["match_results"],
        "own_team_wins": match_stats["own_team_wins"],
        "own_team_losses": match_stats["own_team_losses"],
        "winstreak": match_stats["winstreak"],
        "map_stats": match_stats["map_stats"],
        "wr_per_round_type": wr_per_round_type,
        "util_stats": util_stats,
        "player_stats": player_stats,
        "entry_stats": entry_stats,
        "eco_kills": eco_kills,
        "advanced_stats": advanced_stats,
    }
    return results



results = cumulate_stats()
print("Map Stats:\n", results['map_stats'])
print("Win Rate per Round Type:\n", results['wr_per_round_type'])
print("Utility Stats:\n", results['util_stats'])
print("Player Stats:\n", results['player_stats'])
print("Entry Stats:\n", results['entry_stats'])
print("Eco Kills:\n", results['eco_kills'])
print("Advanced Stats:\n", results['advanced_stats'])