import pandas as pd
import csv
import nfl_data_py as nfl

years = list(range(2012, 2025))
#weeklybruh = nfl.import_weekly_data(years)

#Note: you must install nfl_data_py, and if you wanna use it you 
#will probably need to switch to python 3.11 because it works with the nfl package

#We make a weekly dataframe to get stats like name and position
df = nfl.import_weekly_data([2023])
print(df.columns.tolist())

#seaosnal dataframe
dfseason = nfl.import_seasonal_data(years, 'REG')
print('seasons')
print(dfseason.columns.tolist())

weekly = nfl.import_weekly_data(years)
player_positions = weekly[['player_id', 'position']].drop_duplicates()

refined_seasonal = dfseason[[
    'player_id', 'season', 'games', 'targets', 'receptions',
    'passing_yards', 'passing_tds', 'attempts',
    'rushing_yards', 'rushing_tds', 'carries',
    'receiving_yards', 'receiving_tds',
    'fantasy_points_ppr', 'interceptions', 'sack_fumbles', 'rushing_fumbles', 'receiving_fumbles' 
]]

#if youre accounting for fumbles I can just add the columns 

player_info = weekly[['player_id', 'player_display_name', 'position']].drop_duplicates()

refined_df = refined_seasonal.merge(player_info, on='player_id', how='left')

refined_df.to_csv("2015-24_seasonal_data.csv", index=False)

#Seasonal data fields

#['player_id', 'season', 'season_type', 'completions', 'attempts', 'passing_yards', 'passing_tds', 'interceptions', 'sacks', 'sack_yards', 
# 'sack_fumbles', 'sack_fumbles_lost', 'passing_air_yards', 'passing_yards_after_catch', 'passing_first_downs', 'passing_epa', 
# 'passing_2pt_conversions', 'pacr', 'dakota', 'carries', 'rushing_yards', 'rushing_tds', 'rushing_fumbles', 'rushing_fumbles_lost', 
# 'rushing_first_downs', 'rushing_epa', 'rushing_2pt_conversions', 'receptions', 'targets', 'receiving_yards', 'receiving_tds', 
# 'receiving_fumbles', 'receiving_fumbles_lost', 'receiving_air_yards', 'receiving_yards_after_catch', 'receiving_first_downs', 
# 'receiving_epa', 'receiving_2pt_conversions', 'racr', 'target_share', 'air_yards_share', 'wopr_x', 'special_teams_tds', 
# 'fantasy_points', 'fantasy_points_ppr', 'games', 'tgt_sh', 'ay_sh', 'yac_sh', 'wopr_y', 'ry_sh', 'rtd_sh', 'rfd_sh', 'rtdfd_sh', 'dom', 'w8dom', 'yptmpa', 'ppr_sh']

#Most useful fields: Pos, games, targets, receptions, passing yds, passing tds, passing atts
#, rushing yds, rushing tds, rushing att, receiving yds, receiving tds, fantasy points, int, fumbles, fumbles lost, year

'''
So, seasonal has: Year, games, targets, receptions, passing yards, passing tds, passing attempts (attempts), rushing yards, rushing tds, rushing attempts (carries),
receiving yds, receiving tds, fantasy points, int, fumbles. To match the format you had, we just need player name and position, which we can get from id
'''

# Weekly data: 

# ['player_id', 'player_name', 'player_display_name', 'position', 'position_group', 'headshot_url', 'recent_team', 
#  'season', 'week', 'season_type', 'opponent_team', 'completions', 'attempts', 'passing_yards', 'passing_tds', 'interceptions', 
#  'sacks', 'sack_yards', 'sack_fumbles', 'sack_fumbles_lost', 'passing_air_yards', 'passing_yards_after_catch', 'passing_first_downs', 
#  'passing_epa', 'passing_2pt_conversions', 'pacr', 'dakota', 'carries', 'rushing_yards', 'rushing_tds', 'rushing_fumbles', 
#  'rushing_fumbles_lost', 'rushing_first_downs', 'rushing_epa', 'rushing_2pt_conversions', 'receptions', 'targets', 'receiving_yards', 
#  'receiving_tds', 'receiving_fumbles', 'receiving_fumbles_lost', 'receiving_air_yards', 'receiving_yards_after_catch', 'receiving_first_downs', 
#  'receiving_epa', 'receiving_2pt_conversions', 'racr', 'target_share', 'air_yards_share', 'wopr', 'special_teams_tds', 'fantasy_points', 
#  'fantasy_points_ppr']