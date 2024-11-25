import pandas as pd
import numpy as np
from demoparser2 import DemoParser
import os
from glob import glob

# 1. Fonctions utilitaires
def select_directory(file_paths=""):
    if not os.path.isdir(file_paths):
        print("Invalid directory.")
        return None
    print(f"Directory selected: {file_paths}")
    return file_paths

def categorize_rounds(row):
    if row['round'] in [1, 13]:
        return 'Pistol round'
    elif row['current_equip_value'] <= 3500:
        return 'Eco round'
    elif row['current_equip_value'] <= 18000:
        return 'Force buy round'
    else:
        return 'Full buy round'

def transform_round_end(round_winner, first_round_tick):
    # Vérifie si la colonne contient des valeurs legacy qui indiquent les gagnants par un code numérique
    if 'legacy' in round_winner.columns[1].lower():
        # Remplace les valeurs numériques par les noms d'équipes ('CT' ou 'T')
        round_winner['winner'] = round_winner['winner'].replace({2: 'T', 3: 'CT'}).fillna('unknown')

        # Traduit les raisons des rounds pour plus de clarté
        reason_dict = {9: 'ct_killed', 7: 'bomb_defused', 8: 't_killed', 12: 't_saved'}
        round_winner['reason'] = round_winner['reason'].map(reason_dict).fillna('unknown')

        # Sélectionne et ordonne les colonnes
        round_winner = round_winner[['ct_team_clan_name', 't_team_clan_name', 'reason', 'tick', 'total_rounds_played', 'winner']]
        # Ajuste le décalage pour total_rounds_played
        round_winner.loc[:, 'total_rounds_played'] += 1


    else:
        # Supprime les rounds sans raison valide après le premier round
        round_winner = round_winner[round_winner['tick'] > first_round_tick].drop(columns=['round'])

    return round_winner


# 2. Fonctions de calcul des statistiques
def calculate_match_stats(all_matches, team_name):
    match_data = []
    
    for i, match in enumerate(all_matches):
        round_info_df = match['round_info']
        team_wins, opponent_wins = calculate_match_result(round_info_df, team_name)

        game_id = f"Game_{i+1}"  # Nom du match
        game_name = match['team_info']['Game_id'].iloc[0]
        map_name = match['map_info'].iloc[0]['map_name']  # Nom de la map

        # Déterminer l'équipe victorieuse
        if team_wins > opponent_wins:
            winning_team = team_name
        else:
            winning_team = round_info_df['ct_team_clan_name'].iloc[0] if opponent_wins > team_wins else round_info_df['t_team_clan_name'].iloc[0]

        # Ajouter les informations de match
        match_data.append({
            "Game id": game_id,
            "Game Name": game_name,
            "Map": map_name,
            "Rounds Won by team": team_wins,
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
    opponent_wins = round_info_df['round'].max() - team_wins
    return team_wins, opponent_wins

def detailed_match_result(match_df, team_name):
    # Analyse des victoires et défaites
    match_df['round_diff'] = abs(match_df['Rounds Won by team'] - match_df['Rounds Won by Opponent'])

    # Filtrer les victoires et les défaites de l'équipe
    team_victories = match_df[match_df['Winning Team'] == team_name]
    team_losses = match_df[match_df['Winning Team'] != team_name]

    # Initialiser le dictionnaire des résultats
    result_summary = {
        "largest_win": None,
        "closest_win": None,
        "largest_loss": None,
        "closest_loss": None,
    }

    # Si l'équipe a gagné au moins un match, trouver la victoire la plus large et la plus serrée
    if not team_victories.empty:
        # Victoire la plus large
        largest_win = team_victories.loc[team_victories['round_diff'].idxmax()]
        result_summary["largest_win"] = {
            "game_name": largest_win['Game Name'],
            "map": largest_win['Map'],
            "team_score": largest_win['Rounds Won by team'],
            "opponent_score": largest_win['Rounds Won by Opponent'],
            "round_diff": largest_win['round_diff']
        }

        # Victoire la plus serrée
        closest_win = team_victories.loc[team_victories['round_diff'].idxmin()]
        result_summary["closest_win"] = {
            "game_name": closest_win['Game Name'],
            "map": closest_win['Map'],
            "team_score": closest_win['Rounds Won by team'],
            "opponent_score": closest_win['Rounds Won by Opponent'],
            "round_diff": closest_win['round_diff']
        }

    # Si l'équipe a perdu au moins un match, trouver la défaite la plus large et la plus serrée
    if not team_losses.empty:
        # Défaite la plus large
        largest_loss = team_losses.loc[team_losses['round_diff'].idxmax()]
        result_summary["largest_loss"] = {
            "game_name": largest_loss['Game Name'],
            "map": largest_loss['Map'],
            "team_score": largest_loss['Rounds Won by team'],
            "opponent_score": largest_loss['Rounds Won by Opponent'],
            "round_diff": largest_loss['round_diff']
        }

        # Défaite la plus serrée
        closest_loss = team_losses.loc[team_losses['round_diff'].idxmin()]
        result_summary["closest_loss"] = {
            "game_name": closest_loss['Game Name'],
            "map": closest_loss['Map'],
            "team_score": closest_loss['Rounds Won by team'],
            "opponent_score": closest_loss['Rounds Won by Opponent'],
            "round_diff": closest_loss['round_diff']
        }

    return result_summary

def calculate_map_stats(match_df, team_name):
    map_stats = match_df.groupby('Map').agg(
        times_played=('Map', 'size'),
        wins_on_map=('Winning Team', lambda x: (x == team_name).sum())
    )
    map_stats['winrate'] = (map_stats['wins_on_map'] / map_stats['times_played']) * 100
    return map_stats

def calculate_wr_per_round_type(all_matches, team_name):
    # Initialiser un DataFrame global pour stocker les rounds par catégorie et par side cumulés
    all_matches_round_analysis = pd.DataFrame()

    # Initialiser des compteurs globaux pour les cas particuliers
    total_force_against_team_lost = 0
    total_eco_against_team_lost = 0
    total_team_eco_against_full_win = 0
    total_team_force_against_full_win = 0

    # Parcourir chaque match dans 'all_matches'
    for match_data in all_matches:
        eco_by_team = match_data['eco_info']
        game_id = match_data['team_info']['Game_id'].iloc[0]
        round_info = match_data['round_info']

        eco_by_team['Game_id'] = game_id
        round_info['Game_id'] = game_id

        # Fusionner les données de rounds avec l'économie totale de l'équipe de l'attaquant
        df_merged_team = pd.merge(eco_by_team, round_info[['round', 'Game_id', 'winner']], 
                                  how='left', left_on=['round', 'Game_id'],
                                  right_on=['round', 'Game_id'])
        df_merged_team['side'] = df_merged_team['side'].replace({'TERRORIST': 'T'})

        df_merged_team['round_category'] = df_merged_team.apply(categorize_rounds, axis=1)

        # Filtrer les rounds joués par l'équipe spécifiée
        rounds_team = df_merged_team[df_merged_team['team_clan_name'] == team_name]

        # Calculer le nombre total de rounds joués dans chaque catégorie et par side
        total_rounds_per_category_side = rounds_team.groupby(['round_category', 'side']).size()

        # Calculer le nombre de victoires et de défaites par catégorie et par side
        wins_per_category_side = rounds_team[rounds_team['winner'] == rounds_team['side']].groupby(['round_category', 'side']).size()
        losses_per_category_side = rounds_team[rounds_team['winner'] != rounds_team['side']].groupby(['round_category', 'side']).size()

        # Combiner les résultats dans un DataFrame pour chaque match
        match_stats = pd.DataFrame({
            'total_rounds': total_rounds_per_category_side,
            'wins': wins_per_category_side,
            'losses': losses_per_category_side
        }).fillna(0).astype(int)

        # Cumuler les résultats dans le DataFrame global
        all_matches_round_analysis = pd.concat([all_matches_round_analysis, match_stats])

        # Calculer les cas particuliers pour ce match
        force_against_team_lost = df_merged_team[
            (df_merged_team['team_clan_name'] == team_name) &
            (df_merged_team['round_category'] == 'Full buy round') &
            (df_merged_team['winner'] != df_merged_team['side']) & 
            (df_merged_team['round_category'].shift(-1) == 'Force buy round')
        ].shape[0]

        eco_against_team_lost = df_merged_team[
            (df_merged_team['team_clan_name'] == team_name) &
            (df_merged_team['round_category'] == 'Full buy round') &
            (df_merged_team['winner'] != df_merged_team['side']) & 
            (df_merged_team['round_category'].shift(-1) == 'Eco round')
        ].shape[0]

        team_eco_against_full_win = df_merged_team[
            (df_merged_team['team_clan_name'] == team_name) &
            (df_merged_team['round_category'] == 'Eco round') &
            (df_merged_team['winner'] == df_merged_team['side']) & 
            (df_merged_team['round_category'].shift(1) == 'Full buy round')
        ].shape[0]

        team_force_against_full_win = df_merged_team[
            (df_merged_team['team_clan_name'] == team_name) &
            (df_merged_team['round_category'] == 'Force buy round') &
            (df_merged_team['winner'] == df_merged_team['side']) & 
            (df_merged_team['round_category'].shift(1) == 'Full buy round')
        ].shape[0]

        # Cumuler les résultats globaux pour les cas particuliers
        total_force_against_team_lost += force_against_team_lost
        total_eco_against_team_lost += eco_against_team_lost
        total_team_eco_against_full_win += team_eco_against_full_win
        total_team_force_against_full_win += team_force_against_full_win

    # Calcul du winrate et des pourcentages de défaites par type de round et par side
    round_type_analysis = all_matches_round_analysis.groupby(['round_category', 'side']).sum()
    round_type_analysis['win_%'] = (round_type_analysis['wins'] / round_type_analysis['total_rounds'] * 100).round(1)
    round_type_analysis['loss_%'] = (round_type_analysis['losses'] / round_type_analysis['total_rounds'] * 100).round(1)
    round_type_analysis = round_type_analysis.reset_index()

    # Préparer les cas particuliers pour un affichage dans un DataFrame
    special_cases = pd.DataFrame({
        'special_case': [
            'Full Buy lost to Force Buy',
            'Full Buy lost to Eco',
            'Eco won against Full Buy',
            'Force Buy won against Full Buy'
        ],
        'count': [
            total_force_against_team_lost,
            total_eco_against_team_lost,
            total_team_eco_against_full_win,
            total_team_force_against_full_win
        ]
    })
    return {
        "round_type_analysis": round_type_analysis,
        "special_cases": special_cases,
    }

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

def calculate_trading_stats(joueurs, all_matches):
    traded_deaths_global = []
    trade_kills_global = []
    
    for match_data in all_matches:
        player_death = match_data['player_death_info']
        
        for round_number in player_death['total_rounds_played'].unique():
            round_data = player_death[player_death['total_rounds_played'] == round_number].sort_values(by='player_died_time')

            for player in player_death['user_name'].unique():
                player_deaths = round_data[round_data['user_name'] == player]

                for _, death_row in player_deaths.iterrows():
                    death_time = death_row['player_died_time']
                    attacker = death_row['attacker_name']
                    attacker_side = death_row['side_attacker']
                    victim_side = death_row['side_user']

                    subsequent_rows = round_data[round_data.index > death_row.name]

                    for _, next_row in subsequent_rows.iterrows():
                        if next_row['user_name'] == attacker and next_row['player_died_time'] <= death_time + 2:
                            traded_deaths_global.append({
                                'player': player, 
                                'side_user': victim_side, 
                                'side_attacker': attacker_side, 
                                'round': round_number
                            })
                            trade_killer = next_row['attacker_name']
                            trade_kills_global.append({
                                'player': trade_killer, 
                                'side_user': next_row['side_user'], 
                                'side_attacker': next_row['side_attacker'], 
                                'round': round_number
                            })
                            break

    # Création des DataFrames pour les statistiques
    traded_deaths_df_global = pd.DataFrame(traded_deaths_global)
    trade_kills_df_global = pd.DataFrame(trade_kills_global)

    # Comptage des traded deaths et trade kills
    traded_deaths_count_global = traded_deaths_df_global.groupby(['player', 'side_user']).size().unstack(fill_value=0).reset_index()
    trade_kills_count_global = trade_kills_df_global.groupby(['player', 'side_user']).size().unstack(fill_value=0).reset_index()

    traded_deaths_count_global.columns = ['player','Traded_deaths(CT)','Traded_deaths(T)']
    trade_kills_count_global.columns = ['player','Trade_kills(CT)','Trade_kills(T)']

    trade_df_global = pd.merge(traded_deaths_count_global, trade_kills_count_global, on='player', how='outer').fillna(0)
    trade_df_global = trade_df_global.rename(columns={'player': 'name'})
    
    trade_stats = pd.merge(joueurs, trade_df_global, on='name', how='left').fillna(0)
    trade_stats = trade_stats.astype({'Traded_deaths(CT)':int,'Traded_deaths(T)':int,'Trade_kills(CT)':int,'Trade_kills(T)':int})
    return trade_stats

def calculate_eco_kills(joueurs, all_matches):
    all_team_eco_kills = pd.DataFrame()

    for match_data in all_matches:
        player_deaths_df = match_data['player_death_info']
        eco_by_team = match_data['eco_info']
        game_id = match_data['team_info']['Game_id'].iloc[0]
        player_deaths_df['Game_id'] = game_id
        eco_by_team['Game_id'] = game_id

        df_merged_team = pd.merge(player_deaths_df, eco_by_team, how='left', left_on=['total_rounds_played', 'team_clan_name_user', 'Game_id'], right_on=['round', 'team_clan_name', 'Game_id'])

        df_merged_team['kill_category'] = df_merged_team.apply(categorize_rounds, axis=1)
        team_eco_kills = df_merged_team.pivot_table(index='attacker_name', columns='kill_category', aggfunc='size', fill_value=0)
        all_team_eco_kills = pd.concat([all_team_eco_kills, team_eco_kills])
        all_team_eco_kills_grouped = all_team_eco_kills.groupby('attacker_name').sum().reset_index()
        eco_stats = pd.merge(joueurs,all_team_eco_kills_grouped,left_on='name',right_on='attacker_name',how='left')
        eco_stats.rename(columns={'Eco round':'Against full eco','Force buy round':'Against force buy','Full buy round':'Against full buy'},inplace=True)
        eco_stats.drop(columns={'attacker_name'},inplace=True)
    return eco_stats

def calculate_player_stats(joueurs, all_matches):
    # Calcul des statistiques avancées
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

    # Conversion en DataFrame et calcul des pourcentages et indicateurs avancés
    advanced_stats_df = pd.DataFrame.from_dict(player_stats_global, orient='index').reset_index().rename(columns={'index': 'name'})
    advanced_stats_df['KAST%'] = round((advanced_stats_df['KAST_rounds'] / advanced_stats_df['total_rounds']) * 100, 1)
    advanced_stats_df["KPR"] = round(advanced_stats_df['Kills'] / advanced_stats_df['total_rounds'], 2)
    advanced_stats_df["APR"] = round(advanced_stats_df['Assists'] / advanced_stats_df['total_rounds'], 2)
    advanced_stats_df['DPR'] = round(advanced_stats_df['Deaths'] / advanced_stats_df['total_rounds'], 2)
    advanced_stats_df['Impact'] = round((2.13 * advanced_stats_df['KPR']) + (0.42 * advanced_stats_df['APR']) - 0.41, 2)

    # Calcul des statistiques de base des joueurs
    all_players_stats = pd.DataFrame()
    for match_data in all_matches:
        stats = match_data['agg_stats']
        Stats_joueurs = joueurs.merge(stats, on='name', how='left')
        all_players_stats = pd.concat([all_players_stats, Stats_joueurs])

    # Agrégation des statistiques de base
    all_players_stats_grouped = all_players_stats.groupby('name').sum().reset_index()
    all_players_stats_grouped['ADR'] = round(all_players_stats_grouped['damage_total'] / all_players_stats_grouped["total_rounds_played"], 2)
    all_players_stats_grouped['+/-'] = all_players_stats_grouped['kills_total'] - all_players_stats_grouped["deaths_total"]
    all_players_stats_grouped['HS %'] = round((all_players_stats_grouped['headshot_kills_total'] / all_players_stats_grouped['kills_total'])*100,2)
    # Combinaison des statistiques de base et avancées
    scoreboard = all_players_stats_grouped.merge(
        advanced_stats_df[['name', 'Traded_deaths', 'KAST%', 'Impact','KPR','DPR']],
        on='name', how='left'
    )

    # Nettoyage du DataFrame final
    scoreboard.drop(columns=['steamid', 'Traded_deaths'], inplace=True, errors='ignore')
    scoreboard = scoreboard.rename(columns={"total_rounds_played":"Rounds joués","headshot_kills_total":"HS","kills_total":"Kills","assists_total":"Assists","deaths_total":"Deaths","3k_rounds_total":'3K', "4k_rounds_total":'4K', "ace_rounds_total":'5K',"damage_total":"Damages","utility_damage_total":"Utility Damages","enemies_flashed_total":"Flashed Ennemies"})
    scoreboard = scoreboard.drop(columns={"alive_time_total","Damages","HS",'Flashed Ennemies','Utility Damages'})
    scoreboard['K/D'] = round(scoreboard['Kills'] / scoreboard['Deaths'], 2)
    scoreboard['Rating'] = round((0.0073 * scoreboard['KAST%']) + \
                              (0.3591 * (scoreboard['KPR'])) + \
                              (-0.5329 * (scoreboard['DPR'])) + \
                              (0.2372 * scoreboard['Impact']) + \
                              (0.0032 * scoreboard['ADR']) + 0.1587,2)
    nouvel_ordre_colonnes = [
                'name', 'Rounds joués', 'Kills', 'Deaths', 'Assists', '+/-',
                'K/D', 'ADR', 'KPR', 'DPR','HS %', '5K', '4K', '3K', 'mvps','KAST%','Impact','Rating'
            ]
    scoreboard = scoreboard[nouvel_ordre_colonnes]

    numeric_columns = ['Rounds joués', 'Kills', 'Deaths', 'Assists', '+/-','K/D','5K', '4K', '3K', 'mvps','KAST%']
    scoreboard[numeric_columns] = scoreboard[numeric_columns].astype(int)
    
    return scoreboard.sort_values(by=['Rating'],ascending=False)






# 3. Fonction principale
def cumulate_stats(team_name="GenOne Academie", file_paths="D:/Python/projet_cs_v2/demos_G1"):
    # Sélection du répertoire et initialisation des variables
    demo_directory = select_directory(file_paths)
    if not demo_directory:
        print("No directory selected.")
        return
    all_matches = []

    # Parsing des fichiers de démos
    for filename in glob(os.path.join(demo_directory, "*.dem")):

        demo = DemoParser(os.path.join(demo_directory, filename))

        tick_round_start = demo.parse_event("round_start").drop([0,1,2])
        tick_round_start.rename(columns={'tick':'tick_start_round'},inplace=True)
        tick_freezetime_end = demo.parse_event("round_freeze_end",other=['total_rounds_played'])[["total_rounds_played",'tick']]
        tick_freezetime_end.rename(columns={'tick':'tick_freezetime_end'},inplace=True)
        round_ticks = pd.merge_asof(tick_round_start,tick_freezetime_end[['tick_freezetime_end']], left_on='tick_start_round',right_on='tick_freezetime_end', direction='forward')
        tick_round_end = demo.parse_event("round_end")[["round","tick"]]
        tick_round_end.rename(columns={'tick':'tick_end_round'},inplace=True)
        round_ticks = pd.merge_asof(round_ticks,tick_round_end[['tick_end_round']], left_on='tick_start_round',right_on='tick_end_round', direction='forward')
        round_ticks
        
        max_tick = round_ticks['tick_end_round'].max()
        
        first_round_tick = round_ticks['tick_start_round'].min()

        freezetime_end_tick = round_ticks["tick_freezetime_end"].tolist()
        
        map = pd.DataFrame([demo.parse_header()])
        
        team = demo.parse_ticks(["team_clan_name", "team_name"])
        team = team[(team['tick'] >= first_round_tick) & (team['tick'] <= max_tick)].copy()
        team.rename(columns={'team_name': 'side'}, inplace=True)

        unique_teams = team['team_clan_name'].unique()
        adversary_team = [t for t in unique_teams if t != team_name][0]
        game_id = f"VS_{adversary_team}" 
        
        eco = demo.parse_ticks(["current_equip_value", "total_rounds_played"], ticks=freezetime_end_tick)
        eco['current_equip_value'] = eco['current_equip_value']-200
        eco = pd.merge(round_ticks[['round','tick_freezetime_end']],eco[['current_equip_value','tick','name','steamid']],left_on='tick_freezetime_end',right_on='tick')
        eco_by_players = pd.merge(eco,team, on=['tick','name','steamid'])
        eco_by_team = eco_by_players.groupby(['round','team_clan_name','tick','side'])['current_equip_value'].sum().reset_index()
       
        # Charger le DataFrame `player_death` avec les informations sur les kills
        player_death = demo.parse_event("player_death", other=["game_time", "round_start_time", "total_rounds_played"])
        player_death.loc[:, 'total_rounds_played'] += 1
        # player_death = player_death[player_death['tick'] >= first_round_tick].copy()
        player_death.drop(player_death[player_death['tick'] < first_round_tick].index, inplace=True)
        player_death["player_died_time"] = player_death["game_time"] - player_death["round_start_time"]
        # Ajouter `team_clan_name` et `side` pour `attacker_name` et `user_name` dans `player_death`
        player_death = pd.merge(player_death, team[['team_clan_name', 'side', 'name', 'tick']], 
                                left_on=["attacker_name", 'tick'], right_on=['name', 'tick'], how='left').rename(columns={'team_clan_name': 'team_clan_name_attacker', 'side': 'side_attacker'})
        player_death = pd.merge(player_death, team[['team_clan_name', 'side', 'name', 'tick']], 
                                left_on=["user_name", 'tick'], right_on=['name', 'tick'], how='left').rename(columns={'team_clan_name': 'team_clan_name_user', 'side': 'side_user'})
        player_death = player_death.drop(columns=['name_x', 'name_y'])

        all_hits_regs = demo.parse_event("player_hurt")
        all_hits_regs = all_hits_regs[(all_hits_regs['tick'] >= first_round_tick) & (all_hits_regs['tick'] <= max_tick)].copy()
        
        round_winner = demo.parse_event("round_end", other=["team_clan_name"])
        round_winner = transform_round_end(round_winner, first_round_tick)
        round_winner = pd.merge(round_ticks[['round','tick_end_round']],round_winner[['ct_team_clan_name','t_team_clan_name','reason','tick','winner']],left_on='tick_end_round',right_on='tick')
        

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
            'round_info': round_winner.assign(Game_id=game_id),
            'map_info': map.assign(Game_id=game_id)
        }
        all_matches.append(match_data_single)

    # Calculer les statistiques de match
    match_stats = calculate_match_stats(all_matches, team_name)
    joueurs = pd.DataFrame({'name': team.loc[(team['team_clan_name'] == team_name) & (team['tick'] == first_round_tick), 'name'].unique()})
    util_stats = calculate_util_stats(joueurs, all_matches)
    scoreboard = calculate_player_stats(joueurs, all_matches)
    entry_stats = calculate_entry_stats(joueurs, all_matches)
    eco_kills = calculate_eco_kills(joueurs, all_matches)
    wr_per_round_type = calculate_wr_per_round_type(all_matches, team_name)
    trading_stats = calculate_trading_stats(joueurs, all_matches)
    detailed_results = detailed_match_result(match_stats["match_results"], team_name)

    # Retourner tous les résultats
    results = {
        "match_results": match_stats["match_results"],
        "own_team_wins": match_stats["own_team_wins"],
        "own_team_losses": match_stats["own_team_losses"],
        "winstreak": match_stats["winstreak"],
        "map_stats": match_stats["map_stats"],
        "wr_per_round_type": wr_per_round_type["round_type_analysis"],
        "special_round_type":wr_per_round_type["special_cases"],
        "util_stats": util_stats,
        # "player_stats": player_stats,
        "entry_stats": entry_stats,
        "eco_kills": eco_kills,
        # "advanced_stats": advanced_stats,
        "trading_stats": trading_stats,
        "detailed_match_results": detailed_results,
        "scoreboard":scoreboard
    }
    return results

results = cumulate_stats()
# print("Map Stats:\n", results['map_stats'])
# print("Win Rate per Round Type:\n", results['wr_per_round_type'])
# print("Win Rate per special Round Type:\n", results['special_round_type'])
# print("Utility Stats:\n", results['util_stats'])
# print("Entry Stats:\n", results['entry_stats'])
# print("Eco Kills:\n", results['eco_kills'])
# print("Trading Stats:\n", results['trading_stats'])
# print("Detailed Match Results:\n", results['detailed_match_results'])
#print("scoreboard:\n", results['scoreboard'])

# Utilisation de la fonction


def run_analysis(team_name, file_paths):
    # Appelle cumulate_stats avec les paramètres fournis
    results = cumulate_stats(team_name=team_name, file_paths=file_paths)
    return results
