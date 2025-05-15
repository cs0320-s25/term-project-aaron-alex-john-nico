import pandas as pd
from dotenv import load_dotenv
import os
load_dotenv()
league_swid = os.getenv("SWID")
league_s2 = os.getenv("ESPN_S2")

#install: pip install python-dotenv
#pip install espn_api

from espn_api.football import League  

# league = League(league_id=4572608, year=2024, espn_s2=league_s2, swid=league_swid)  # Replace with your league ID

league2025 = League(league_id=1246266673, year = 2025, espn_s2=league_s2, swid=league_swid)


# #data = league.get_team_data()
# data = league.teams
# print(data)

# team = league.teams[1]

# print(team)

# player = team.roster[0]
# print(player)
# print(player.playerId)
# print(player.name)
# print(player.position)
# print(player.proTeam)
# print(player.projected_avg_points)
# print(player.posRank)
# print(player.injuryStatus)
# print(player.total_points)

#This is probably the most efficient way to obtain the data required for the algorithim. 
#With this, we can get stats of players, position + position rank, projected avg points, all of which will be useful. 
#If everyone is ok with this method, we can create a function to go through each player on our roster plus top free agents. It is
#unrealistic to get every single player but we 

#Create player dataclass: Contains name, position, rank, projected points

# free_agents = league.free_agents(size=5)  # get all available free agents and important stats

# for player in free_agents:
#     print(f"{player.name} - {player.position} - PosRank: {player.posRank} - ProjPts: {player.projected_avg_points}")

# free_agents_2025 = league2025.free_agents(size=5)

# for player in free_agents_2025:
#     print(f"{player.name} - {player.position} - PosRank: {player.posRank} - ProjPts: {player.projected_avg_points}")

player_population = league2025.free_agents(size= 400)

#With this, we can get the top n free agents based on their projected points and position rank. I'm thinking we create a player dataclass
#that has all of this information? Then we can take it and sort based on pos rank, make groups of each position, etc. 






