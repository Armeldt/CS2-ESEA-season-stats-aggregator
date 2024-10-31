import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from demoparser2 import DemoParser  # Assurez-vous d'avoir importé DemoParser correctement

def analyze():
    global all_players_stats_grouped, own_team_wins, own_team_losses
    global winstreak, map_stats, largest_win, closest_win, largest_loss
    global closest_loss, cumulative_stats

    team = 'zobrux'  # Nom de l'équipe
    demo_directory = "D:/Python/projet_cs_v2/demos"
    if not demo_directory:
        print("No directory selected.")
        return

    print(f"Analyzing for team: {team} with demo files in directory: {demo_directory}")

    # Extraction des informations pour chaque fichier .dem dans le répertoire
    all_matches = []
    for filename in os.listdir(demo_directory):
        if filename.endswith(".dem"):
            demo = DemoParser(os.path.join(demo_directory, filename))
            max_tick = demo.parse_event("round_end")["tick"].max()
            first_round_tick = demo.parse_event('round_start').drop([0,1,2]).loc[3, 'tick']
            map_info = pd.DataFrame([demo.parse_header()])

            # Tick fin période d'achat
            freezetime_end_tick = demo.parse_event("round_freeze_end")["tick"].drop([0,1]).tolist()
            team_V3 = demo.parse_ticks(["team_clan_name","team_name"])
            team_V3.drop(team_V3[team_V3['tick'] < first_round_tick].index, inplace=True)
            team_V3.drop(team_V3[team_V3['tick'] > max_tick].index, inplace=True)
            team_V3.rename(columns={'team_name':'side'}, inplace=True)
            name_to_team = dict(zip(team_V3['name'], team_V3['team_clan_name']))

            # Économie par équipe
            eco = demo.parse_ticks(["current_equip_value", "total_rounds_played"], ticks=freezetime_end_tick)
            eco['total_rounds_played'] = eco['total_rounds_played'].apply(lambda x: x+1 if x == 0 else x)
            eco['current_equip_value'] -= 200
            eco_by_players = pd.merge(eco, team_V3, on=['tick','name','steamid'])
            eco_by_team = eco_by_players.groupby(['total_rounds_played','team_clan_name','tick','side'])['current_equip_value'].sum().reset_index()

            # Kills et Damages
            trade = prepare_trade_data(demo, team_V3, name_to_team, first_round_tick)
            all_hits_regs = prepare_damage_data(demo, name_to_team, first_round_tick, max_tick)
            agg_stats = demo.parse_ticks(["total_rounds_played","kills_total","assists_total","deaths_total", "mvps", "headshot_kills_total", "3k_rounds_total", "4k_rounds_total", "ace_rounds_total" ,"damage_total","utility_damage_total", "enemies_flashed_total","alive_time_total"], ticks=[max_tick])
            round_ends = transform_round_end(demo.parse_event("round_end", other=["total_rounds_played","team_clan_name"]), first_round_tick)

            adversary_team = [t for t in team_V3['team_clan_name'].unique() if t != team][0]
            df_team = team_V3.loc[team_V3['team_clan_name'] == team, :].assign(Game_id="VS_" + adversary_team)

            match_data = {
                'team_info': df_team,
                'trade_info': trade,
                'damage_info': all_hits_regs,
                'agg_stats': agg_stats,
                'eco_info': eco_by_team,
                'round_info': round_ends,
                'map_info' : map_info
            }
            all_matches.append(match_data)

    # Calcul des résultats globaux
    process_team_indicators(team, all_matches)
    cumulative_stats = process_round_categories(team, all_matches)

    # Affichage des statistiques par joueur
    process_player_stats(all_matches, team_V3, first_round_tick)


def prepare_trade_data(demo, team_V3, name_to_team, first_round_tick):
    trade = demo.parse_event("player_death", other=["game_time", "round_start_time",'total_rounds_played'])
    trade['total_rounds_played'] += 1
    trade.drop(trade[trade['tick'] < first_round_tick].index, inplace=True)
    trade["player_died_time"] = trade["game_time"] - trade["round_start_time"]
    trade = pd.merge(trade, team_V3[['team_clan_name','side','name','tick']], left_on=["attacker_name",'tick'], right_on=['name','tick'])
    trade = trade.rename(columns={'team_clan_name':'team_clan_name_attacker', 'side':'side_attacker'})
    trade = pd.merge(trade, team_V3[['team_clan_name','side','name','tick']], left_on=["user_name",'tick'], right_on=['name','tick'])
    trade = trade.rename(columns={'team_clan_name':'team_clan_name_user','side':'side_user'})
    return trade


def prepare_damage_data(demo, name_to_team, first_round_tick, max_tick):
    all_hits_regs = demo.parse_event("player_hurt", ticks=[max_tick])
    all_hits_regs = all_hits_regs[(all_hits_regs['tick'] >= first_round_tick) & (all_hits_regs['tick'] <= max_tick)]
    all_hits_regs['attacker_team'] = all_hits_regs['attacker_name'].map(name_to_team)
    all_hits_regs['user_team'] = all_hits_regs['user_name'].map(name_to_team)
    return all_hits_regs[all_hits_regs['attacker_team'] != all_hits_regs['user_team']]


def transform_round_end(round_ends, first_round_tick):
    if round_ends.columns[1].lower() == 'legacy':
        round_ends['winner'] = round_ends['winner'].apply(lambda x: 'T' if x == 2 else 'CT' if x == 3 else 'unknown')
        round_ends['reason'] = round_ends['reason'].map({9: 'ct_killed', 7: 'bomb_defused', 8: 't_killed', 12: 't_saved', 11: 'time_end'}).fillna('unknown')
    round_ends.drop(round_ends[round_ends['tick'] <= first_round_tick].index, inplace=True)
    return round_ends


def process_team_indicators(team, all_matches):
    match_data = []
    for i, match in enumerate(all_matches):
        round_info_df = match['round_info']
        team_wins, opponent_wins = calculate_match_result(round_info_df, team)
        game_id = match['team_info']['Game_id'].iloc[0]
        map_name = match['map_info']['map_name'].iloc[0]

        winning_team = team if team_wins > opponent_wins else round_info_df['ct_team_clan_name'].iloc[0]
        match_data.append({
            "Match id": i + 1,
            "Game Name": game_id,
            "Map": map_name,
            "Rounds Won by zobrux": team_wins,
            "Rounds Won by Opponent": opponent_wins,
            "Winning Team": winning_team
        })

    match_df = pd.DataFrame(match_data)
    global own_team_wins, own_team_losses, winstreak, map_stats, largest_win, closest_win, largest_loss, closest_loss
    own_team_wins = match_df[match_df['Winning Team'] == team].shape[0]
    own_team_losses = match_df[match_df['Winning Team'] != team].shape[0]
    winstreak = calculate_winstreak(match_df, team)

    map_stats = match_df.groupby('Map').agg(times_played=('Map', 'size'), wins_on_map=('Winning Team', lambda x: (x == team).sum()))
    map_stats['winrate'] = (map_stats['wins_on_map'] / map_stats['times_played']) * 100

    zobrux_victories = match_df[match_df['Winning Team'] == team]
    zobrux_losses = match_df[match_df['Winning Team'] != team]

    if not zobrux_victories.empty:
        largest_win = zobrux_victories.loc[zobrux_victories['round_diff'].idxmax()]
        closest_win = zobrux_victories.loc[zobrux_victories['round_diff'].idxmin()]

    if not zobrux_losses.empty:
        largest_loss = zobrux_losses.loc[zobrux_losses['round_diff'].idxmax()]
        closest_loss = zobrux_losses.loc[zobrux_losses['round_diff'].idxmin()]


def process_player_stats(all_matches, team_V3, first_round_tick):
    joueurs = pd.DataFrame(team_V3.loc[(team_V3['team_clan_name'] == 'zobrux') & (team_V3['tick'] == first_round_tick), 'name']).reset_index(drop=True)
    all_players_stats = pd.concat([joueurs.merge(match['agg_stats'], on='name', how='left') for match in all_matches])
    
    global all_players_stats_grouped
    all_players_stats_grouped = all_players_stats.groupby('name').sum().reset_index()
    all_players_stats_grouped['ADR'] = round(all_players_stats_grouped['damage_total'] / all_players_stats_grouped["total_rounds_played"],2)
    all_players_stats_grouped['+/-'] = all_players_stats_grouped['kills_total'] - all_players_stats_grouped["deaths_total"]
    all_players_stats_grouped['HS %'] = (all_players_stats_grouped['headshot_kills_total'] / all_players_stats_grouped['kills_total']) * 100
    all_players_stats_grouped['KPR'] = all_players_stats_grouped['kills_total'] / all_players_stats_grouped['total_rounds_played']
    all_players_stats_grouped['K/D'] = all_players_stats_grouped['kills_total'] / all_players_stats_grouped['deaths_total']

    nouvel_ordre_colonnes = ['name', 'steamid', 'Rounds joués', 'Kills', 'Deaths', '+/-', 'Assists', 'K/D', 'Damages', 'ADR', 'KPR', 'HS', 'HS %', '5K', '4K', '3K', 'mvps']
    all_players_stats_grouped = all_players_stats_grouped[nouvel_ordre_colonnes]
